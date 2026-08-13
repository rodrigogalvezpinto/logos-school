import { Page, expect } from '@playwright/test';

/** Captura errores de consola del navegador — la "lectura de logs" del loop de pruebas. */
export function capturarErroresConsola(page: Page): string[] {
  const errores: string[] = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') errores.push(msg.text());
  });
  page.on('pageerror', (err) => errores.push(err.message));
  return errores;
}

/** Cuenta de prueba real (ver backend/scripts/datos_de_prueba.py) — apoderado con dos
 * alumnos (Sofía en 4° básico, Mateo en 6° básico) y plan activo. */
export const CREDENCIALES_PRUEBA = {
  email: 'apoderado.prueba@logos.cl',
  password: 'Logos2026!',
};

export async function loginYEntrarComoSofia(page: Page) {
  await page.goto('/login');
  await page.fill('input[type=email]', CREDENCIALES_PRUEBA.email);
  await page.fill('input[type=password]', CREDENCIALES_PRUEBA.password);
  await page.click('button[type=submit]');
  await page.waitForURL('**/selector-perfil');
  await page.getByText('Sofía').click();
  await expect(page).toHaveURL(/alumno\/inicio/);
}
