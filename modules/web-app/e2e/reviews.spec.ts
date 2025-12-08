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

test.describe('School Reviews', () => {
    test('Review form is visible on school details page', async ({ page }) => {
        const apiResponse = await page.request.get('http://localhost:8000/api/v1/schools?limit=1');
        const schools = await apiResponse.json();

        await page.goto(`/schools/${schools[0].id}`);

        const reviewForm = page.getByText('Viết đánh giá của bạn');
        await reviewForm.scrollIntoViewIfNeeded();

        await expect(reviewForm).toBeVisible();

        console.log('✅ Review form is visible');
    });

    test('Can submit a review', async ({ page }) => {
        const apiResponse = await page.request.get('http://localhost:8000/api/v1/schools?limit=1');
        const schools = await apiResponse.json();

        await page.goto(`/schools/${schools[0].id}`);
        await page.waitForLoadState('networkidle');
        await page.waitForTimeout(1000);

        await page.getByText('Viết đánh giá của bạn').scrollIntoViewIfNeeded();
        await page.waitForTimeout(500);

        const nameInput = page.getByPlaceholder(/nhập tên/i);
        await nameInput.waitFor({ state: 'visible', timeout: 10000 });
        await nameInput.fill('E2E Test User');

        const formSection = page.locator('form').filter({ hasText: 'Viết đánh giá' });
        const starButtons = formSection.locator('button').filter({ has: page.locator('svg[class*="lucide"]') });
        await starButtons.nth(4).click();
        await page.waitForTimeout(500);

        const commentInput = page.getByPlaceholder(/chia sẻ trải nghiệm/i);
        await commentInput.fill('This is an automated E2E test review!');
        await page.waitForTimeout(300);

        const submitButton = page.getByRole('button', { name: /Gửi đánh giá/i });
        await submitButton.click();

        // Wait much longer for API response and state update
        await page.waitForTimeout(5000);

        await expect(page.getByText('E2E Test User')).toBeVisible({ timeout: 10000 });
        await expect(page.getByText('This is an automated E2E test review!')).toBeVisible({ timeout: 5000 });

        console.log('✅ Review submitted successfully and appears in list');
    });

    test('Rating stars are interactive', async ({ page }) => {
        const apiResponse = await page.request.get('http://localhost:8000/api/v1/schools?limit=1');
        const schools = await apiResponse.json();

        await page.goto(`/schools/${schools[0].id}`);

        await page.getByText('Viết đánh giá của bạn').scrollIntoViewIfNeeded();

        const formSection = page.locator('form').filter({ hasText: 'Viết đánh giá' });
        const stars = formSection.locator('button').filter({ has: page.locator('svg') });

        await stars.nth(2).click();
        await page.waitForTimeout(300);

        await stars.nth(4).click();
        await page.waitForTimeout(300);

        console.log('✅ Rating stars are interactive');
    });

    test('Average rating displays in header', async ({ page }) => {
        const apiResponse = await page.request.get('http://localhost:8000/api/v1/schools?limit=1');
        const schools = await apiResponse.json();

        await page.goto(`/schools/${schools[0].id}`);
        await page.waitForLoadState('networkidle');

        const ratingText = page.getByText(/\d+\.\d+.*đánh giá/i).or(page.getByText(/0\.0.*đánh giá/i));
        await expect(ratingText).toBeVisible({ timeout: 5000 });

        console.log('✅ Average rating is displayed');
    });

    test('Review list displays existing reviews', async ({ page }) => {
        const apiResponse = await page.request.get('http://localhost:8000/api/v1/schools?limit=1');
        const schools = await apiResponse.json();

        await page.goto(`/schools/${schools[0].id}`);
        await page.waitForLoadState('networkidle');

        const reviewHeading = page.getByText(/Đánh giá từ cộng đồng.*\(/i);
        await reviewHeading.scrollIntoViewIfNeeded();
        await page.waitForTimeout(500);

        await expect(reviewHeading).toBeVisible({ timeout: 5000 });

        console.log('✅ Review list section is visible');
    });
});
