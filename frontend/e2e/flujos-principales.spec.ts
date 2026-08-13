import { test, expect } from '@playwright/test';
import { capturarErroresConsola, loginYEntrarComoSofia, CREDENCIALES_PRUEBA } from './helpers';

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
    await expect(page.locator('.item__respuesta').first()).toBeVisible();

    const segundaPregunta = page.locator('.item__pregunta').nth(1);
    await segundaPregunta.click();
    await expect(page.locator('.item--abierto .item__respuesta')).toHaveCount(1);
  });

  test('privacidad y términos son accesibles desde el registro', async ({ page }) => {
    await page.goto('/registro');
    await expect(page.getByRole('link', { name: 'Política de Privacidad' })).toBeVisible();
    await page.getByRole('link', { name: 'Términos y Condiciones' }).click();
    await expect(page).toHaveURL(/terminos/);
    await expect(page.locator('h1')).toContainText('Términos y Condiciones');
  });
});

test.describe('Login real contra el backend', () => {
  test('login con credenciales incorrectas muestra error, no navega', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type=email]', CREDENCIALES_PRUEBA.email);
    await page.fill('input[type=password]', 'clave-incorrecta');
    await page.click('button[type=submit]');
    await expect(page.locator('.error')).toBeVisible();
    await expect(page).toHaveURL(/login/);
  });

  test('login correcto → selector de perfil con los alumnos reales → panel del alumno', async ({ page }) => {
    const errores = capturarErroresConsola(page);
    await loginYEntrarComoSofia(page);
    await expect(page.locator('h1')).toContainText('Sofía');
    expect(errores, `Errores de consola: ${errores.join(', ')}`).toEqual([]);
  });

  test('recargar la página no pierde la sesión ni el perfil elegido', async ({ page }) => {
    await loginYEntrarComoSofia(page);
    await page.reload();
    await expect(page).toHaveURL(/alumno\/inicio/);
    await expect(page.locator('h1')).toContainText('Sofía');
  });

  test('sin sesión, /alumno/inicio redirige a login', async ({ page }) => {
    await page.goto('/alumno/inicio');
    await expect(page).toHaveURL(/login/);
  });
});

test.describe('Panel del Alumno — contenido real', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('navega Home → Asignatura → Estudiar → Autoevaluación con datos reales', async ({ page }) => {
    await page.goto('/alumno/inicio');
    await expect(page.locator('h1')).toContainText('Sofía');

    await page.getByRole('link', { name: 'Matemática' }).click();
    await expect(page).toHaveURL(/asignaturas\/\d+/);

    await page.getByRole('link', { name: 'Estudiar guía' }).first().click();
    await expect(page).toHaveURL(/estudiar\/\d+/);
    await expect(page.locator('.contenido-guia')).not.toBeEmpty();

    await page.getByRole('link', { name: 'Practicar este tema' }).click();
    await expect(page).toHaveURL(/autoevaluacion\/\d+/);
    await page.getByRole('button', { name: 'Comenzar' }).click();
    await expect(page.locator('.pregunta__enunciado')).not.toBeEmpty();
  });

  test('el panel Apoderado se ve y no rompe', async ({ page }) => {
    const errores = capturarErroresConsola(page);
    await page.goto('/apoderado/inicio');
    await expect(page.locator('.alumno-card')).toHaveCount(2); // Sofía y Mateo
    expect(errores, `Errores de consola: ${errores.join(', ')}`).toEqual([]);
  });
});
