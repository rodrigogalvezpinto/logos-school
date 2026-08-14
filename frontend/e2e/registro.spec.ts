import { test, expect } from '@playwright/test';
import { capturarErroresConsola } from './helpers';

// Cuenta y RUT únicos por corrida — la base de Desarrollo no se resetea entre corridas
// (y el RUT ahora es único a nivel de negocio, ver fix de "RUT duplicado" 2026-08-14).
function rutValidoUnico(): string {
  const cuerpo = String(10000000 + (Date.now() % 89999999));
  let suma = 0;
  let multiplicador = 2;
  for (let i = cuerpo.length - 1; i >= 0; i--) {
    suma += Number(cuerpo[i]) * multiplicador;
    multiplicador = multiplicador < 7 ? multiplicador + 1 : 2;
  }
  const resto = 11 - (suma % 11);
  const dv = resto === 11 ? '0' : resto === 10 ? 'K' : String(resto);
  return `${cuerpo}-${dv}`;
}

const sufijo = Date.now();
const email = `qa.registro.${sufijo}@logos.cl`;
const rut = rutValidoUnico();

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
  await page.fill('input[name=rut]', rut);
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/seleccion-plan/);

  // El nombre del alumno recién creado debe reflejarse, no un valor hardcodeado.
  await expect(page.locator('h1')).toContainText('Alumno QA');

  await page.click('button:has-text("Comenzar mis 7 días gratis")');
  await expect(page).toHaveURL(/selector-perfil/);
  await expect(page.getByText('Alumno QA')).toBeVisible();

  await page.getByText('Alumno QA').click();
  await expect(page).toHaveURL(/alumno\/inicio/);
  await expect(page.locator('h1')).toContainText('Alumno QA');

  expect(errores, `Errores de consola: ${errores.join(', ')}`).toEqual([]);
});
