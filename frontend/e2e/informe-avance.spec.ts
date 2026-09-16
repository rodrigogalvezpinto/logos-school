import { test, expect } from '@playwright/test';

/** Fase 1 del plan de incorporación de hallazgos de Brincus — informe de avance
 * descargable en PDF para el Apoderado. Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md.
 * Mismo patrón que certificado-alumno-regular.spec.ts: se verifica la respuesta HTTP real
 * del click en vez de perseguir la pestaña `blob:` que abre `window.open`. */

test.describe('Informe de avance en PDF', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('el botón "Descargar informe en PDF" en Mis Notas pide un PDF real y autenticado', async ({ page }) => {
    await page.goto('/alumno/notas');

    const [respuesta] = await Promise.all([
      page.waitForResponse((r) => r.url().includes('/informe-avance.pdf')),
      page.getByRole('button', { name: /Descargar informe en PDF/ }).click(),
    ]);

    expect(respuesta.status()).toBe(200);
    expect(respuesta.headers()['content-type']).toBe('application/pdf');
    const cuerpo = await respuesta.body();
    expect(cuerpo.subarray(0, 5).toString()).toBe('%PDF-');
  });
});
