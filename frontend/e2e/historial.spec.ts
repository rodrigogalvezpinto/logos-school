import { test, expect } from '@playwright/test';

test.describe('Historial y notas por materia (Fase 1.2)', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('rendir una prueba de unidad la deja ver en Mis Notas', async ({ page }) => {
    await page.goto('/alumno/evaluaciones');
    await page.waitForSelector('.fila');
    // Índice distinto al usado por casos-borde.spec.ts (0,1,2) para no reanudar un
    // intento ya entregado por esos tests — ver la nota sobre idempotencia en ese archivo.
    await page.getByRole('link', { name: 'Rendir' }).nth(3).click();
    await expect(page).toHaveURL(/alumno\/prueba\/\d+/);
    await page.getByRole('button', { name: 'Comenzar' }).click();
    await page.waitForSelector('.runner__nav');

    const siguiente = page.getByRole('button', { name: 'Siguiente' });
    while (await siguiente.isVisible().catch(() => false)) {
      await siguiente.click();
      await page.waitForTimeout(50);
    }
    await page.getByRole('button', { name: 'Entregar' }).click();
    // El aviso de "preguntas sin responder" siempre aparece acá (no se respondió
    // ninguna) — esperarlo evita la carrera con el render de Angular.
    await expect(page.locator('.modal')).toBeVisible();
    await page.getByRole('button', { name: 'Enviar de todas formas' }).click();
    await expect(page.locator('.resultado')).toBeVisible();

    await page.goto('/alumno/notas');
    await expect(page.locator('h1')).toContainText('Mis Notas');
    await expect(page.locator('.fila-historial').first()).toBeVisible();
    await expect(page.locator('.nota-card').first()).toBeVisible();
  });

  test('estudiar una guía la marca como revisada en el historial', async ({ page }) => {
    await page.goto('/alumno/asignaturas');
    await page.waitForSelector('.asignatura-card');
    await page.locator('.asignatura-card').first().click();
    await page.waitForSelector('.oa-card');
    await page.getByRole('link', { name: 'Estudiar guía' }).first().click();
    await expect(page).toHaveURL(/alumno\/estudiar\/\d+/);

    await page.goto('/alumno/notas');
    await expect(page.locator('.fila-historial', { hasText: 'Guía revisada' }).first()).toBeVisible();
  });

  test('el panel del apoderado permite entrar al progreso de un alumno', async ({ page }) => {
    await page.goto('/apoderado/progreso');
    await expect(page.locator('h1')).toContainText('Progreso por Alumno');
    await page.getByRole('link', { name: /Sofía/ }).first().click();
    await expect(page).toHaveURL(/apoderado\/progreso\/\d+/);
    await expect(page.locator('h1')).toContainText('Mis Notas');
  });
});
