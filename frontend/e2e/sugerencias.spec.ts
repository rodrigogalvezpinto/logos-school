import { test, expect } from '@playwright/test';

/** Buzón de sugerencias (Fase 1 — ver planificacion/27-plan-incorporacion-hallazgos-brincus.md,
 * Paso 13, hallazgo comparando en vivo contra Brincus: "¿Cómo doy ideas para mejorar la
 * plataforma?"). */

test.describe('Ideas para mejorar Logos School', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('enviar una sugerencia muestra la confirmación', async ({ page }) => {
    await page.goto('/alumno/configuracion');
    await page.fill('textarea[name="sugerencia"]', 'Sería genial tener modo oscuro.');
    await page.click('button:has-text("Enviar sugerencia")');
    await expect(page.locator('.confirmacion')).toBeVisible();
    await expect(page.locator('textarea[name="sugerencia"]')).toHaveValue('');
  });

  test('el botón queda deshabilitado con el campo vacío', async ({ page }) => {
    await page.goto('/alumno/configuracion');
    await expect(page.locator('button:has-text("Enviar sugerencia")')).toBeDisabled();
  });
});
