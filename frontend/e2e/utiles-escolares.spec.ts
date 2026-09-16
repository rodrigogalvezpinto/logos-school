import { test, expect } from '@playwright/test';

/** Útiles Escolares (hallazgo comparando en vivo contra Brincus, sección "Informaciones" —
 * ver planificacion/25-analisis-competencia-brincus.md, Paso 12), piloto en 4° básico. */
test.describe('Útiles Escolares', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('muestra la lista agrupada por asignatura, con materiales generales primero', async ({ page }) => {
    await page.goto('/alumno/utiles-escolares');
    await page.waitForSelector('.grupo');
    const grupos = page.locator('.grupo');
    await expect(grupos.first()).toContainText('Materiales generales');
    await expect(grupos).not.toHaveCount(0);
    await expect(page.locator('.lista-items li').first()).toContainText('×');
  });

  test('el sidebar tiene un link a Útiles Escolares', async ({ page }) => {
    await page.goto('/alumno/inicio');
    await page.getByRole('link', { name: 'Útiles Escolares' }).click();
    await expect(page).toHaveURL(/alumno\/utiles-escolares/);
  });
});
