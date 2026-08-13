import { test, expect } from '@playwright/test';
import { AxeBuilder } from '@axe-core/playwright';
import { CREDENCIALES_PRUEBA } from './helpers';

/** Auditoría automatizada de accesibilidad (axe-core) sobre las páginas públicas y el panel
 * del Alumno — ver planificacion/22-analisis-de-brechas.md. Solo falla ante violaciones
 * "serias"/"críticas" nuevas; no persigue cada regla "moderada" hasta el final (ver nota de
 * `.fila-historial--bloqueada` en notas.ts: WCAG exime a componentes de UI inactivos del
 * contraste mínimo, y esa tarjeta representa una evaluación aún bloqueada). */
async function sinViolacionesGraves(page: import('@playwright/test').Page) {
  const resultados = await new AxeBuilder({ page }).analyze();
  const graves = resultados.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical');
  expect(graves, JSON.stringify(graves, null, 2)).toEqual([]);
}

test.describe('Accesibilidad (axe-core)', () => {
  test('landing sin violaciones graves', async ({ page }) => {
    await page.goto('/');
    await sinViolacionesGraves(page);
  });

  test('login sin violaciones graves', async ({ page }) => {
    await page.goto('/login');
    await sinViolacionesGraves(page);
  });

  test('registro sin violaciones graves', async ({ page }) => {
    await page.goto('/registro');
    await sinViolacionesGraves(page);
  });

  test('panel del Alumno sin violaciones graves', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type=email]', CREDENCIALES_PRUEBA.email);
    await page.fill('input[type=password]', CREDENCIALES_PRUEBA.password);
    await page.click('button[type=submit]');
    await page.waitForURL('**/selector-perfil');
    await page.getByText('Sofía').click();
    await expect(page).toHaveURL(/alumno\/inicio/);
    await sinViolacionesGraves(page);
  });
});
