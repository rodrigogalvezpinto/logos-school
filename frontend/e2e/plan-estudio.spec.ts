import { test, expect } from '@playwright/test';

test.describe('Plan de estudio (Fase 1.3)', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('crear un plan de estudio muestra las próximas sesiones', async ({ page }) => {
    await page.goto('/alumno/plan-estudio');
    await expect(page.locator('h1')).toContainText('Plan de Estudio');

    // Si ya existe un plan de una corrida anterior, la página lo muestra directo sin
    // formulario — el formulario ya trae lunes/miércoles/viernes preseleccionados
    // (3 días, el mínimo), así que alcanza con enviar.
    const formulario = page.locator('.form-crear');
    if (await formulario.isVisible().catch(() => false)) {
      await page.click('button:has-text("Crear mi plan de estudio")');
    }

    await expect(page.locator('.lista-sesiones')).toBeVisible();
  });

  test('el sidebar ya no muestra "pronto" en Plan de Estudio', async ({ page }) => {
    await page.goto('/alumno/inicio');
    const item = page.locator('.sidebar__item', { hasText: 'Plan de Estudio' });
    await expect(item.locator('.sidebar__badge')).toHaveCount(0);
  });
});
