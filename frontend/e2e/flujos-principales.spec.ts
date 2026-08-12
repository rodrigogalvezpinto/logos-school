import { test, expect } from '@playwright/test';
import { capturarErroresConsola } from './helpers';

test.describe('Landing y páginas institucionales', () => {
  test('la landing carga sin errores de consola y navega a Cómo funciona', async ({ page }) => {
    const errores = capturarErroresConsola(page);
    await page.goto('/');
    await expect(page.locator('h1')).toContainText('Examen Libre');

    await page.getByRole('link', { name: 'Cómo funciona' }).click();
    await expect(page).toHaveURL(/como-funciona/);
    await expect(page.locator('h1')).toContainText('Examen Libre');

    expect(errores, `Errores de consola: ${errores.join(', ')}`).toEqual([]);
  });

  test('navega a Preguntas frecuentes y despliega una respuesta', async ({ page }) => {
    await page.goto('/preguntas-frecuentes');
    await expect(page.locator('h1')).toContainText('Preguntas frecuentes');

    // La primera pregunta viene abierta por defecto (buen UX: no llega vacío).
    await expect(page.locator('.item__respuesta').first()).toBeVisible();

    // La segunda, al hacer clic, debe abrirse (y la primera se cierra — acordeón).
    const segundaPregunta = page.locator('.item__pregunta').nth(1);
    await segundaPregunta.click();
    await expect(page.locator('.item--abierto .item__respuesta')).toHaveCount(1);
  });
});

test.describe('Flujo de registro y onboarding', () => {
  test('registro → agregar alumno → plan → selector de perfil → panel alumno', async ({ page }) => {
    const errores = capturarErroresConsola(page);

    await page.goto('/registro');
    await expect(page.locator('h1')).toContainText('Crea tu cuenta');
    await page.getByRole('button', { name: /Crear cuenta/i }).click();

    await expect(page).toHaveURL(/agregar-alumno/);
    await page.getByRole('button', { name: 'Continuar' }).click();

    await expect(page).toHaveURL(/seleccion-plan/);
    await page.getByRole('button', { name: /Continuar al pago/i }).click();

    await expect(page).toHaveURL(/selector-perfil/);
    await expect(page.locator('h1')).toContainText('Quién va a estudiar');

    await page.getByText('Sofía').click();
    await expect(page).toHaveURL(/alumno\/inicio/);
    await expect(page.locator('h1')).toContainText('Sofía');

    expect(errores, `Errores de consola: ${errores.join(', ')}`).toEqual([]);
  });
});

test.describe('Panel del Alumno', () => {
  test('navega Home → Asignatura → Estudiar → Autoevaluación', async ({ page }) => {
    await page.goto('/alumno/inicio');
    await page.getByRole('link', { name: /Matemática/ }).first().click();
    await expect(page).toHaveURL(/asignaturas\/matematica/);

    await page.getByRole('link', { name: 'Estudiar guía' }).first().click();
    await expect(page).toHaveURL(/estudiar/);
    await expect(page.locator('h1')).toContainText('10.000');

    await page.getByRole('link', { name: 'Practicar este tema' }).click();
    await expect(page).toHaveURL(/autoevaluacion/);
    await page.getByRole('button', { name: 'Comenzar' }).click();
    await expect(page.locator('.pregunta__enunciado')).toBeVisible();
  });

  test('el panel Apoderado se ve y no rompe', async ({ page }) => {
    const errores = capturarErroresConsola(page);
    await page.goto('/apoderado/inicio');
    await expect(page.locator('h1')).toContainText('Rodrigo');
    expect(errores, `Errores de consola: ${errores.join(', ')}`).toEqual([]);
  });
});
