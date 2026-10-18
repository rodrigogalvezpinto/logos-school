import { test, expect } from '@playwright/test';

/** Fase 1, ítem 2.8 del plan de incorporación de hallazgos de Brincus — historial de
 * pagos para el Apoderado. Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md. */

test.describe('Plan y Pagos — historial de pagos del Apoderado (Fase 1, ítem 2.8)', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('muestra una fila por alumno con su plan/estado, y la nota de comprobante pendiente', async ({ page }) => {
    await page.goto('/apoderado/plan');
    await expect(page.locator('h1')).toContainText('Plan y Pagos');
    await expect(page.locator('.fila-pago').first()).toBeVisible();
    await expect(page.locator('.nota')).toContainText('pasarela de pago');
  });
});
