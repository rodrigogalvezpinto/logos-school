import { test, expect } from '@playwright/test';

/** Fase 1 del plan de incorporación de hallazgos de Brincus — búsqueda global de
 * contenido, visible en la topbar de cualquier página del Alumno (a diferencia del
 * buscador de asignatura-detalle.spec.ts, que solo filtra dentro de una asignatura ya
 * abierta). Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md. */

test.describe('Búsqueda global de contenido', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('busca un objetivo por palabra clave y navega a su página de estudio', async ({ page }) => {
    await page.goto('/alumno/inicio');
    const input = page.locator('input[type="search"]');
    await expect(input).toBeVisible();

    await input.fill('fracc');
    await expect(page.locator('.busqueda-global__item').first()).toBeVisible();
    const primerResultado = page.locator('.busqueda-global__item').first();
    await expect(primerResultado).toContainText('Matemática');

    await primerResultado.click();
    await expect(page).toHaveURL(/\/alumno\/estudiar\/\d+/);
  });

  test('no aparece la búsqueda global en la topbar del Apoderado', async ({ page }) => {
    await page.goto('/apoderado/inicio');
    await expect(page.locator('input[type="search"]')).toHaveCount(0);
  });
});
