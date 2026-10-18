import { test, expect } from '@playwright/test';

/** Fase 1 del plan de incorporación de hallazgos de Brincus — "Avance de contenido"
 * separado de las notas (hallazgo Paso 12: Brincus separa "Progreso"/Ruta de aprendizaje
 * de "Calificaciones"). Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md.
 * Reutiliza el dato de cobertura que ya calculaba /progreso/{id}/faltantes. */

test.describe('Avance de contenido (Mis Notas)', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('muestra una tarjeta con % de avance por asignatura, antes de las notas', async ({ page }) => {
    await page.goto('/alumno/notas');
    await page.waitForSelector('.avance-card');

    const avance = page.locator('.avance-card').first();
    await expect(avance).toBeVisible();
    await expect(avance.locator('.avance-card__pct')).toContainText('%');

    // El encabezado "Avance de contenido" debe aparecer antes que "Notas por asignatura".
    const titulos = await page.locator('h2').allTextContents();
    const indiceAvance = titulos.indexOf('Avance de contenido');
    const indiceNotas = titulos.indexOf('Notas por asignatura');
    expect(indiceAvance).toBeGreaterThanOrEqual(0);
    expect(indiceAvance).toBeLessThan(indiceNotas);
  });
});
