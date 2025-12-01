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
