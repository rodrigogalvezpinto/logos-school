// Ensayo de producción local (2026-11-21): sin globalSetup (no hay usuarios de prueba en una base de producción).
import { defineConfig, devices } from '@playwright/test';
export default defineConfig({
  testDir: './e2e', workers: 1, reporter: [['line']], outputDir: '/tmp/logos-pw-prod',
  use: { baseURL: process.env['LOGOS_E2E_WEB_URL'] ?? 'http://localhost:4410', trace: 'retain-on-failure', screenshot: 'only-on-failure' },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
});
