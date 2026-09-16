import { test, expect } from '@playwright/test';

/** Marcadores de roadmap en el sidebar (Profesor IA, Juegos, Videos) — explícitamente
 * fuera de alcance de esta etapa (ver planificacion/27-plan-incorporacion-hallazgos-brincus.md),
 * pero visibles con badge "pronto" en vez de estar ocultos o rotos sin avisar. Mismo patrón
 * ya usado antes para Plan de Estudio mientras no estaba construido. */

test.describe('Marcadores "próximamente" en el sidebar', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('Profesor IA, Juegos y Videos aparecen con el badge "pronto" y no navegan', async ({ page }) => {
    await page.goto('/alumno/inicio');
    for (const etiqueta of ['Profesor IA', 'Juegos', 'Videos']) {
      const item = page.locator('.sidebar__item', { hasText: etiqueta });
      await expect(item.locator('.sidebar__badge')).toContainText('pronto');
      await item.click();
      await expect(page).toHaveURL(/alumno\/inicio/); // no navega a ningún lado
    }
  });
});
