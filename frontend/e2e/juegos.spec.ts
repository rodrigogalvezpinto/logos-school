import { test, expect } from '@playwright/test';

/** Juegos de práctica (tarea 13, rama feature/juegos-practica): elegir modo y asignatura, responder y ver la retroalimentación. */
test.describe('Juegos de práctica', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('el alumno juega Racha: responde y recibe retroalimentación inmediata', async ({ page }) => {
    await page.goto('/alumno/juegos');
    await expect(page.getByRole('heading', { name: 'Juegos' })).toBeVisible();
    await page.getByRole('button', { name: /Racha/ }).click();
    await page.locator('.asignatura').first().click();
    await expect(page.locator('.pregunta__enunciado')).not.toBeEmpty();
    const opcion = page.locator('.opcion').first();
    await opcion.click();
    if (await page.getByRole('button', { name: 'Responder' }).isVisible()) await page.getByRole('button', { name: 'Responder' }).click();
    await expect(page.locator('.retro')).toBeVisible();
    await expect(page.getByRole('button', { name: /Siguiente|Ver resultado/ })).toBeVisible();
  });
});
