import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './e2e',
  // Los tests comparten una única cuenta demo real (backend/scripts/datos_de_prueba.py)
  // contra la base de Desarrollo — correrlos en paralelo puede hacer que dos tests
  // reanuden el mismo intento de evaluación a la vez. Se corren en serie por ahora;
  // una app con datos de prueba aislados por test podría paralelizar de nuevo.
  workers: 1,
  reporter: [['list']],
  globalSetup: './e2e/global-setup.ts',
  use: {
    baseURL: 'http://localhost:4300',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
  },
  projects: [{ name: 'chromium', use: { ...devices['Desktop Chrome'] } }],
});
