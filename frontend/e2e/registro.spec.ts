import { test, expect } from '@playwright/test';
import { capturarErroresConsola } from './helpers';

// Cuenta única por corrida — la base de Desarrollo no se resetea entre corridas.
const sufijo = Date.now();
const email = `qa.registro.${sufijo}@logos.cl`;

test('flujo completo de registro: crear cuenta → agregar alumno → plan → panel del alumno', async ({ page }) => {
  const errores = capturarErroresConsola(page);

  await page.goto('/registro');
  await page.fill('input[name=nombre]', 'QA Apoderado');
  await page.fill('input[name=email]', email);
  await page.fill('input[name=password]', 'Prueba2026!');
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/agregar-alumno/);

  await page.fill('input[name=nombre]', 'Alumno QA');
  await page.fill('input[name=apellidos]', 'Prueba Test');
  await page.fill('input[name=fechaNacimiento]', '2015-03-10');
  await page.fill('input[name=rut]', '11.111.111-1');
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/seleccion-plan/);

  // El nombre del alumno recién creado debe reflejarse, no un valor hardcodeado.
  await expect(page.locator('h1')).toContainText('Alumno QA');

  await page.click('button:has-text("Continuar al pago")');
  await expect(page).toHaveURL(/selector-perfil/);
  await expect(page.getByText('Alumno QA')).toBeVisible();

  await page.getByText('Alumno QA').click();
  await expect(page).toHaveURL(/alumno\/inicio/);
  await expect(page.locator('h1')).toContainText('Alumno QA');

  expect(errores, `Errores de consola: ${errores.join(', ')}`).toEqual([]);
});
