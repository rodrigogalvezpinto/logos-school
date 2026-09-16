import { test, expect } from '@playwright/test';

/** Fase 1, ítem 2.5 del plan de incorporación de hallazgos de Brincus — descarga de guía
 * en PDF. Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md. */

test.describe('Descargar guía en PDF (Fase 1, ítem 2.5)', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('el link "Descargar guía en PDF" apunta a un PDF real', async ({ page, request }) => {
    await page.goto('/alumno/asignaturas');
    await page.waitForSelector('a[href*="/alumno/asignaturas/"]');
    await page.locator('a[href*="/alumno/asignaturas/"]').first().click();
    await page.waitForSelector('a[href*="/alumno/estudiar/"]');
    await page.locator('a[href*="/alumno/estudiar/"]').first().click();
    await page.waitForURL(/alumno\/estudiar\/\d+/);

    const link = page.locator('a.descargar-pdf');
    await expect(link).toBeVisible();
    const href = await link.getAttribute('href');
    expect(href).toMatch(/\/contenido\/objetivos\/\d+\/guia\.pdf$/);
    expect(await link.getAttribute('target')).toBe('_blank');

    const respuesta = await request.get(href!);
    expect(respuesta.status()).toBe(200);
    expect(respuesta.headers()['content-type']).toBe('application/pdf');
    const cuerpo = await respuesta.body();
    expect(cuerpo.subarray(0, 5).toString()).toBe('%PDF-');
  });
});
