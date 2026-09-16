import { test, expect } from '@playwright/test';

/** Calificación con estrellas por guía (Fase 1 — ver
 * planificacion/27-plan-incorporacion-hallazgos-brincus.md, cuarta pasada, hallazgo
 * comparando en vivo contra Brincus: tab "Evaluar Sección" con estrellas). */

test.describe('Calificar guía con estrellas', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('calificar con estrellas muestra el mensaje de agradecimiento y persiste al recargar', async ({ page }) => {
    await page.goto('/alumno/asignaturas');
    await page.waitForSelector('a[href*="/alumno/asignaturas/"]');
    await page.locator('a[href*="/alumno/asignaturas/"]').first().click();
    await page.waitForSelector('a[href*="/alumno/estudiar/"]');
    await page.locator('a[href*="/alumno/estudiar/"]').first().click();
    await page.waitForURL(/alumno\/estudiar\/\d+/);

    await page.waitForSelector('.calificar-guia__estrella');
    const estrellas = page.locator('.calificar-guia__estrella');
    await estrellas.nth(3).click(); // 4ª estrella

    await expect(page.locator('.calificar-guia__gracias')).toBeVisible();
    await expect(page.locator('.calificar-guia__estrella--llena')).toHaveCount(4);

    await page.reload();
    await page.waitForSelector('.calificar-guia__estrella');
    await expect(page.locator('.calificar-guia__estrella--llena')).toHaveCount(4);
  });
});
