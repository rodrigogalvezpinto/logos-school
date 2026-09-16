import { test, expect } from '@playwright/test';

/** "Racha de la casa" / jardín semanal — idea 3 del boceto de innovación (2026-08-17),
 * variante recomendada (jardín acumulado, nunca se marchita) tras evaluar los límites de la
 * idea original en el propio boceto. Solo lectura (GET) — puede usar la cuenta compartida
 * "Sofía" sin riesgo, igual que mapa-calor.spec.ts. Sofía ya tiene actividad real en más de
 * una semana, así que debe haber variedad de etapas, no solo "semilla". */

test.describe('Jardín semanal (Mis Logros)', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('muestra la planta actual grande y las 8 semanas en miniatura, con más de una etapa', async ({ page }) => {
    await page.goto('/alumno/logros');
    await page.waitForSelector('.jardin');

    await expect(page.locator('h2', { hasText: 'Tu jardín' })).toBeVisible();

    const plantas = page.locator('.jardin app-planta-jardin svg');
    await expect(plantas.first()).toBeVisible();
    expect(await plantas.count()).toBe(9); // 1 grande (semana actual) + 8 del historial

    const miniaturas = page.locator('.jardin__historial app-planta-jardin');
    expect(await miniaturas.count()).toBe(8);

    // Confirma que no todas las semanas son "semilla" — hay variedad real de estados.
    const etiquetas = await page.locator('.jardin__historial app-planta-jardin svg').evaluateAll(
      (svgs) => svgs.map((svg) => svg.getAttribute('aria-label')),
    );
    const distintas = new Set(etiquetas);
    expect(distintas.size).toBeGreaterThan(1);
  });
});
