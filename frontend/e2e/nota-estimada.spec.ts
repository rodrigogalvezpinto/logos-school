import { test, expect } from '@playwright/test';

/** Nota estimada del Examen Libre — idea propia (no un hallazgo de la competencia, ver
 * planificacion/27-plan-incorporacion-hallazgos-brincus.md). Sofía (cuenta de prueba) ya
 * tiene evaluaciones entregadas de sesiones previas, así que la tarjeta debe mostrar una
 * nota real, no el estado "sin datos". */

test.describe('Nota estimada del Examen Libre', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('muestra una nota general con nivel de confianza y desglose por asignatura', async ({ page }) => {
    await page.goto('/alumno/notas');
    await page.waitForSelector('.prediccion');

    const numero = page.locator('.prediccion__numero');
    await expect(numero).toBeVisible();
    const texto = await numero.textContent();
    expect(Number(texto)).toBeGreaterThanOrEqual(1);
    expect(Number(texto)).toBeLessThanOrEqual(7);

    await expect(page.locator('.prediccion__confianza')).toBeVisible();
    expect(await page.locator('.prediccion__fila').count()).toBeGreaterThan(0);
  });
});
