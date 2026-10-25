import { test, expect } from '@playwright/test';

/** Fase 1, ítem 2.2 del plan de incorporación de hallazgos de Brincus — gamificación
 * (XP, nivel, avatar). Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md. */

test.describe('Mis Logros — gamificación (Fase 1, ítem 2.2)', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('la página muestra nivel, XP y la grilla de avatares', async ({ page }) => {
    await page.goto('/alumno/logros');
    await expect(page.locator('.resumen__nivel')).toContainText(/Nivel \d+/);
    await expect(page.locator('.resumen__xp')).toContainText(/\d+ XP total/);
    expect(await page.locator('.avatar-opcion').count()).toBeGreaterThanOrEqual(5);
  });

  test('muestra "¿Sabías que…?" con estadísticas de uso reales', async ({ page }) => {
    // Hallazgo comparando en vivo contra Brincus (ver
    // planificacion/27-plan-incorporacion-hallazgos-brincus.md) — datos que ya existían en
    // el dominio de gamificación, mostrados como dato curioso al alumno.
    await page.goto('/alumno/logros');
    await page.waitForSelector('.datos-curiosos');
    const items = page.locator('.datos-curiosos li');
    await expect(items).toHaveCount(4);
    await expect(items.nth(0)).toContainText('racha más larga');
    await expect(items.nth(1)).toContainText('dedicado');
    await expect(items.nth(2)).toContainText('entregado');
    await expect(items.nth(3)).toContainText('revisado');
  });

  test('el sidebar tiene un link a Mis Logros', async ({ page }) => {
    await page.goto('/alumno/inicio');
    await page.getByRole('link', { name: 'Mis Logros' }).click();
    await expect(page).toHaveURL(/alumno\/logros/);
  });

  test('elegir un avatar distinto lo marca como elegido', async ({ page }) => {
    await page.goto('/alumno/logros');
    await page.waitForSelector('.avatar-opcion');
    const opciones = page.locator('.avatar-opcion');
    const total = await opciones.count();
    // Elige la última opción (probablemente distinta a la ya elegida por defecto).
    await opciones.nth(total - 1).click();
    await expect(opciones.nth(total - 1)).toHaveClass(/avatar-opcion--elegido/);
  });

  test('entregar una prueba de unidad suma XP visible en Mis Logros', async ({ page }) => {
    await page.goto('/alumno/logros');
    await page.waitForSelector('.resumen__xp');
    const xpTexto = await page.locator('.resumen__xp').textContent();
    const xpAntes = parseInt(xpTexto!.match(/\d+/)![0], 10);

    await page.goto('/alumno/evaluaciones');
    await page.waitForSelector('.fila');
    // Índice alto para no chocar con los intentos ya entregados por otros specs.
    await page.getByRole('link', { name: 'Rendir' }).nth(9).click();
    await expect(page).toHaveURL(/alumno\/prueba\/\d+/);
    await page.getByRole('button', { name: 'Comenzar' }).click();
    await page.waitForSelector('.runner__nav');
    await page.getByRole('button', { name: 'Finalizar intento' }).click();
    const avisoOResultado = page.locator('.modal, .resultado');
    await expect(avisoOResultado).toBeVisible();
    if (await page.locator('.modal').isVisible().catch(() => false)) {
      await page.getByRole('button', { name: 'Enviar de todas formas' }).click();
    }
    await expect(page.locator('.resultado')).toBeVisible();

    await page.goto('/alumno/logros');
    await page.waitForSelector('.resumen__xp');
    const xpDespuesTexto = await page.locator('.resumen__xp').textContent();
    const xpDespues = parseInt(xpDespuesTexto!.match(/\d+/)![0], 10);
    expect(xpDespues).toBeGreaterThan(xpAntes);

    // Entregar una evaluación registra actividad del día — la racha debe quedar en al
    // menos 1 día (profundización de gamificación, 2026-08-15, ver
    // planificacion/25-analisis-competencia-brincus.md).
    await expect(page.locator('.resumen__racha')).toBeVisible();
    await expect(page.locator('.resumen__racha-num')).toContainText('🔥');
  });

  test('la grilla de insignias muestra las 15, con insignias desbloqueadas y bloqueadas', async ({ page }) => {
    await page.goto('/alumno/logros');
    await page.waitForSelector('.logro-card');
    await expect(page.locator('.logro-card')).toHaveCount(15);
    // Sofía entregó al menos una evaluación en el test anterior — "Primer intento" debe
    // estar desbloqueado (sin el candado ni el estilo bloqueado).
    const primerIntento = page.locator('.logro-card', { hasText: 'Primer intento' });
    await expect(primerIntento).not.toHaveClass(/logro-card--bloqueado/);
    // Logros avanzados que aún no alcanza (Nivel 20) deben mostrarse bloqueados.
    const nivel20 = page.locator('.logro-card', { hasText: 'Nivel 20' });
    await expect(nivel20).toHaveClass(/logro-card--bloqueado/);
  });
});
