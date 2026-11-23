import { test, expect } from '@playwright/test';

/** Desde 2026-11-22 el menú no muestra marcadores «pronto»: Juegos ya existe, el Profesor IA vive bajo cada guía y
 * Videos no está en el alcance. El menú solo ofrece lo que la app hace. */
test.describe('Menú del alumno sin marcadores «pronto»', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('no hay ítems «pronto» y Juegos navega', async ({ page }) => {
    await page.goto('/alumno/inicio');
    await expect(page.locator('.sidebar__badge')).toHaveCount(0);
    await expect(page.locator('.sidebar__item', { hasText: 'Videos' })).toHaveCount(0);
    await page.locator('.sidebar__item', { hasText: 'Juegos' }).click();
    await expect(page).toHaveURL(/alumno\/juegos/);
  });
});
