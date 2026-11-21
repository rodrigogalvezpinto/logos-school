import { test, expect } from '@playwright/test';

/** Profesor IA (tarea 14): desactivado no aparece; activado (respuestas simuladas) muestra la conversación. */
test.describe('Profesor IA', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  async function abrirGuia(page: import('@playwright/test').Page) {
    await page.goto('/alumno/asignaturas');
    await page.locator('a[href*="/alumno/asignaturas/"]').first().click();
    await page.locator('a[href*="/alumno/estudiar/"]').first().click();
    await expect(page.locator('.contenido-guia')).toBeVisible();
  }

  test('sin activar, el panel no aparece', async ({ page }) => {
    await abrirGuia(page);
    await expect(page.locator('.tutor')).toHaveCount(0);
  });

  test('activado, el alumno pregunta y ve la respuesta', async ({ page }) => {
    await page.route('**/tutor-ia/estado', (r) => r.fulfill({ json: { habilitado: true } }));
    await page.route('**/tutor-ia/*/oa/*', (r) => r.fulfill({ json: { texto: 'Pista: mira el ejemplo 1.', derivacion: false } }));
    await abrirGuia(page);
    await page.fill('#pregunta-tutor', '¿Me das una pista?');
    await page.getByRole('button', { name: 'Preguntar' }).click();
    await expect(page.locator('.burbuja').last()).toContainText('Pista: mira el ejemplo 1.');
  });
});
