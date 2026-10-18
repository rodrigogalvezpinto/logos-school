import { test, expect } from '@playwright/test';

/** Fase 1 del plan de incorporación de hallazgos de Brincus — botón de ayuda contextual
 * (sin IA todavía). Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md. */

test.describe('Ayuda contextual', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('el botón flotante muestra un tip distinto según la página y un link a preguntas frecuentes', async ({ page }) => {
    await page.goto('/alumno/evaluaciones');
    await page.click('.ayuda-contextual__boton');
    await expect(page.locator('.ayuda-contextual__panel')).toContainText('Examen simulacro');
    await expect(page.getByRole('link', { name: /preguntas frecuentes/i })).toHaveAttribute('href', '/preguntas-frecuentes');

    await page.click('.ayuda-contextual__cerrar');
    await expect(page.locator('.ayuda-contextual__panel')).toHaveCount(0);

    await page.goto('/alumno/plan-estudio');
    await page.click('.ayuda-contextual__boton');
    await expect(page.locator('.ayuda-contextual__panel')).toContainText('plan reparte el contenido');
  });

  test('el botón de ayuda también existe en el panel del Apoderado', async ({ page }) => {
    await page.goto('/apoderado/inicio');
    await expect(page.locator('.ayuda-contextual__boton')).toBeVisible();
  });
});
