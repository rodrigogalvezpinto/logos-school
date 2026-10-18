import { test, expect } from '@playwright/test';

/** Fase 1, ítem 2.10 del plan de incorporación de hallazgos de Brincus — vista
 * semanal/mensual del plan de estudio (agrupación de UI sobre datos que ya existen). Ver
 * planificacion/27-plan-incorporacion-hallazgos-brincus.md. */

test.describe('Plan de estudio — vista semanal/mensual (Fase 1, ítem 2.10)', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('el selector Lista/Semanal/Mensual existe y cambia la agrupación', async ({ page }) => {
    await page.goto('/alumno/plan-estudio');
    await page.waitForSelector('.selector-vista');

    await expect(page.locator('.lista-sesiones').first()).toBeVisible();

    await page.getByRole('button', { name: 'Semanal' }).click();
    await expect(page.locator('.grupo-semana__titulo').first()).toContainText('Semana del');

    await page.getByRole('button', { name: 'Mensual' }).click();
    await expect(page.locator('.grupo-semana__titulo').first()).toBeVisible();

    await page.getByRole('button', { name: 'Lista' }).click();
    await expect(page.locator('.grupo-semana')).toHaveCount(0);
  });
});
