import { test, expect } from '@playwright/test';

/** Plan Lector (hallazgo comparando en vivo contra Brincus — ver
 * planificacion/25-analisis-competencia-brincus.md), piloto en 4° básico. */
test.describe('Plan Lector', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('muestra la lista curada de libros con autor y editorial', async ({ page }) => {
    await page.goto('/alumno/plan-lector');
    await page.waitForSelector('.libro-card');
    await expect(page.locator('.libro-card')).not.toHaveCount(0);
    await expect(page.locator('.libro-card').first()).toContainText('Papelucho');
  });

  test('el sidebar tiene un link a Plan Lector', async ({ page }) => {
    await page.goto('/alumno/inicio');
    await page.getByRole('link', { name: 'Plan Lector' }).click();
    await expect(page).toHaveURL(/alumno\/plan-lector/);
  });
});
