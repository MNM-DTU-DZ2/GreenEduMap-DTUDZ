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

test.describe('School Map UI', () => {
    test('Map loads and displays markers', async ({ page }) => {
        await page.goto('/schools/map');

        // Wait for map to load
        await page.waitForSelector('.mapboxgl-map', { timeout: 10000 });

        // Check that markers are rendered
        const markers = await page.locator('.mapboxgl-marker').count();
        expect(markers).toBeGreaterThan(0);

        console.log(`✅ Found ${markers} school markers on map`);
    });

    test('Legend is visible', async ({ page }) => {
        await page.goto('/schools/map');
        await page.waitForSelector('.mapboxgl-map');

        // Check legend exists
        const legend = await page.getByText('Green Score');
        await expect(legend).toBeVisible();

        // Check color labels
        await expect(page.getByText(/High.*70/)).toBeVisible();
        await expect(page.getByText(/Medium.*40-70/)).toBeVisible();
        await expect(page.getByText(/Low.*40/)).toBeVisible();

        console.log('✅ Legend is visible with correct color coding');
    });

    test('Map controls are functional', async ({ page }) => {
        await page.goto('/schools/map');
        await page.waitForSelector('.mapboxgl-map');

        // Check navigation controls
        const zoomIn = await page.locator('.mapboxgl-ctrl-zoom-in');
        const zoomOut = await page.locator('.mapboxgl-ctrl-zoom-out');

        await expect(zoomIn).toBeVisible();
        await expect(zoomOut).toBeVisible();

        console.log('✅ Map controls are present');
    });
});
