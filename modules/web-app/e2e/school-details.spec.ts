/*
 * GreenEduMap-DTUDZ - Open Data Platform for Green Urban Development
 * Copyright (C) 2025 DTU-DZ2 Team
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program. If not, see <https://www.gnu.org/licenses/>.
 */

import { test, expect } from '@playwright/test';

test.describe('School Details Page', () => {
    test('Can navigate to school details', async ({ page }) => {
        const apiResponse = await page.request.get('http://localhost:8000/api/v1/schools?limit=1');
        const schools = await apiResponse.json();

        expect(schools).toHaveLength(1);
        const schoolId = schools[0].id;

        await page.goto(`/schools/${schoolId}`);

        await expect(page.locator('h1')).toBeVisible();

        console.log('✅ School details page loaded');
    });

    test('School details displays correct information', async ({ page }) => {
        const apiResponse = await page.request.get('http://localhost:8000/api/v1/schools?limit=1');
        const schools = await apiResponse.json();
        const school = schools[0];

        await page.goto(`/schools/${school.id}`);

        await expect(page.getByRole('heading', { name: school.name })).toBeVisible();
        await expect(page.getByText(school.address)).toBeVisible();
        await expect(page.getByText('Green Score')).toBeVisible();

        console.log('✅ School details shows correct information');
    });

    test('Back to map button works', async ({ page }) => {
        const apiResponse = await page.request.get('http://localhost:8000/api/v1/schools?limit=1');
        const schools = await apiResponse.json();

        await page.goto(`/schools/${schools[0].id}`);

        const backButton = page.getByRole('link', { name: /Quay lại/i });
        await expect(backButton).toBeVisible();
        await backButton.click();

        await expect(page).toHaveURL('/schools/map');

        console.log('✅ Back button navigates to map');
    });

    test('Facilities section displays', async ({ page }) => {
        const apiResponse = await page.request.get('http://localhost:8000/api/v1/schools?limit=1');
        const schools = await apiResponse.json();

        await page.goto(`/schools/${schools[0].id}`);
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(500);

        const facilitiesHeading = page.getByRole('heading').filter({ hasText: /cơ sở vật chất/i });
        await expect(facilitiesHeading).toBeVisible({ timeout: 10000 });

        console.log('✅ Facilities section is visible');
    });

    test('Green courses section displays', async ({ page }) => {
        const apiResponse = await page.request.get('http://localhost:8000/api/v1/schools?limit=1');
        const schools = await apiResponse.json();

        await page.goto(`/schools/${schools[0].id}`);
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(500);

        const coursesHeading = page.getByRole('heading').filter({ hasText: /khóa học/i });
        await expect(coursesHeading).toBeVisible({ timeout: 10000 });

        console.log('✅ Green courses section is visible');
    });
});
