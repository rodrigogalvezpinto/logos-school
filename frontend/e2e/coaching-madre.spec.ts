import { test, expect } from '@playwright/test';

/** Coaching a la madre según el momento — idea propia (no un hallazgo de Brincus). Antes de
 * que el apoderado vea las notas de un hijo, si hay al menos una nota reprobada, un tip
 * breve sobre cómo reaccionar sin generar presión, con un botón para revelar las notas.
 * Sofía (cuenta de prueba) ya tiene notas de práctica reprobadas (1.0) en las 4 asignaturas
 * de sesiones previas, así que el tip debe aparecer. */

test.describe('Coaching a la madre antes de ver una nota baja', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('el apoderado ve el tip antes de las notas, y "Ver la nota" las revela', async ({ page }) => {
    await page.goto('/apoderado/progreso/1');
    await expect(page.locator('h1')).toContainText('Mis Notas');

    const coaching = page.locator('.coaching-madre');
    await expect(coaching).toBeVisible();
    await expect(coaching).toContainText('Antes de ver la nota');
    await expect(page.locator('.grid-notas')).toHaveCount(0);

    await coaching.getByRole('button', { name: 'Ver la nota' }).click();
    await expect(coaching).toHaveCount(0);
    await expect(page.locator('.grid-notas')).toBeVisible();
  });

  test('el propio alumno viendo sus notas no ve el coaching (es solo para el apoderado)', async ({ page }) => {
    await page.goto('/alumno/notas');
    await expect(page.locator('.coaching-madre')).toHaveCount(0);
    await expect(page.locator('.grid-notas')).toBeVisible();
  });
});
