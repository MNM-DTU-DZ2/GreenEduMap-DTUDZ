import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
    testDir: './e2e',
    timeout: 30000,
    fullyParallel: false,
    retries: 0,
    workers: 1,

    reporter: [
        ['html'],
        ['list']
    ],

    use: {
        baseURL: 'http://localhost:3000',
        headless: false, // Show browser
        screenshot: 'only-on-failure',
        video: 'retain-on-failure',
        trace: 'on-first-retry',
    },

    projects: [
        {
            name: 'chromium',
            use: { ...devices['Desktop Chrome'] },
        },
    ],
});
