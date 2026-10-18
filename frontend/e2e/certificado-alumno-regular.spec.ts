import { test, expect } from '@playwright/test';

/** Fase 1, ítem 2.7 del plan de incorporación de hallazgos de Brincus — certificado de
 * alumno regular en PDF. Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md.
 * El endpoint exige sesión (a diferencia de la guía, que es pública) — se descarga como
 * blob autenticado desde Angular, no un <a href> directo. Se verifica interceptando la
 * respuesta HTTP real del click, en vez de perseguir la pestaña `blob:` que abre
 * `window.open` (flaky de temporizar en Chromium headless). */

test.describe('Certificado de alumno regular (Fase 1, ítem 2.7)', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('el botón "Descargar certificado en PDF" pide un PDF real y autenticado', async ({ page }) => {
    await page.goto('/alumno/configuracion');

    const [respuesta] = await Promise.all([
      page.waitForResponse((r) => r.url().includes('/certificado.pdf')),
      page.getByRole('button', { name: /Descargar certificado en PDF/ }).click(),
    ]);

    expect(respuesta.status()).toBe(200);
    expect(respuesta.headers()['content-type']).toBe('application/pdf');
    const cuerpo = await respuesta.body();
    expect(cuerpo.subarray(0, 5).toString()).toBe('%PDF-');
  });
});
