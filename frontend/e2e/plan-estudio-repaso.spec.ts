import { test, expect } from '@playwright/test';

/** Fase 1 del plan de incorporación de hallazgos de Brincus — repaso de contenido de años
 * anteriores dentro del Plan de Estudio (Sofía cursa 4° básico, así que 1°-3° básico deben
 * aparecer como cursos anteriores). Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md. */

test.describe('Plan de estudio — repaso de años anteriores', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('el formulario de repaso ofrece cursos anteriores y agrega una sesión al final del plan', async ({ page }) => {
    await page.goto('/alumno/plan-estudio');
    await page.waitForSelector('.lista-sesiones');

    await page.getByRole('button', { name: 'Repasar contenido de años anteriores' }).click();
    const selectNivel = page.locator('.form-repaso select').first();
    await expect(selectNivel).toBeVisible();

    const opciones = await selectNivel.locator('option').allTextContents();
    expect(opciones).toContain('3° básico');
    expect(opciones).not.toContain('4° básico');
    expect(opciones).not.toContain('5° básico');

    await selectNivel.selectOption({ label: '3° básico' });
    const selectAsignatura = page.locator('.form-repaso select').nth(1);
    await expect(selectAsignatura).toBeVisible();
    await selectAsignatura.selectOption({ index: 1 });

    const primeraOa = page.locator('.oa-repaso-opcion input[type="checkbox"]').first();
    await expect(primeraOa).toBeVisible();
    await primeraOa.check();

    const chipsAntes = await page.locator('.chip-repaso').count();
    await page.getByRole('button', { name: 'Agregar al plan' }).click();

    await expect(page.locator('.chip-repaso')).toHaveCount(chipsAntes + 1);
    await expect(page.locator('.form-repaso')).toHaveCount(0);
  });
});
