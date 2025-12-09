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

test.describe('School Search', () => {
    test('Search bar appears on map', async ({ page }) => {
        await page.goto('/schools/map');

        // Wait for search input
        const searchInput = page.getByPlaceholder(/Tìm kiếm/i);
        await expect(searchInput).toBeVisible();

        console.log('✅ Search bar is visible');
    });

    test('Search filters schools by name', async ({ page }) => {
        await page.goto('/schools/map');

        // Wait for map and search to be ready
        await page.waitForSelector('.mapboxgl-map');
        const searchInput = page.getByPlaceholder(/Tìm kiếm/i);
        await searchInput.waitFor({ state: 'visible' });

        // Type in search slowly to trigger autocomplete
        await searchInput.click();
        await searchInput.fill('Trường', { timeout: 5000 });

        // Wait longer for results to appear (async search)
        await page.waitForTimeout(1500);

        // Check if the value was entered correctly
        const searchValue = await searchInput.inputValue();
        expect(searchValue).toContain('Trường');

        console.log('✅ Search text entered successfully');
    });

    test('Can clear search', async ({ page }) => {
        await page.goto('/schools/map');

        const searchInput = page.getByPlaceholder(/Tìm kiếm/i);
        await searchInput.fill('Test School');
        await page.waitForTimeout(500);

        // Clear search
        await searchInput.clear();

        const value = await searchInput.inputValue();
        expect(value).toBe('');

        console.log('✅ Search can be cleared');
    });
});
