import { test, expect } from '@playwright/test';

/** Fase 1 del plan de incorporación de hallazgos de Brincus — centro de notificaciones
 * (Paso 12: campana con Notificaciones / Errores reportados). Ver
 * planificacion/27-plan-incorporacion-hallazgos-brincus.md. Las 3 fuentes (comunicados,
 * sesiones atrasadas, reportes resueltos) ya están cubiertas a fondo en
 * backend/tests/test_notificaciones.py — acá solo se verifica que el widget existe, abre
 * su panel y no aparece en la topbar del Apoderado. */

test.describe('Centro de notificaciones', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('la campana abre un panel de notificaciones', async ({ page }) => {
    await page.goto('/alumno/inicio');
    const boton = page.locator('.campana__boton');
    await expect(boton).toBeVisible();

    await boton.click();
    await expect(page.locator('.campana__panel')).toBeVisible();
    await expect(page.locator('.campana__panel h3')).toContainText('Notificaciones');
  });

  test('no aparece la campana en la topbar del Apoderado', async ({ page }) => {
    await page.goto('/apoderado/inicio');
    await expect(page.locator('.campana__boton')).toHaveCount(0);
  });
});
