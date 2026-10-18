import { test, expect } from '@playwright/test';

/** Auditoría de seguridad (2026-08-17): no existía forma de que un apoderado pidiera
 * borrar los datos de un hijo. Cuenta fresca — la eliminación es irreversible. */

function rutValido(cuerpo: number): string {
  const cuerpoStr = String(cuerpo);
  let suma = 0;
  let multiplicador = 2;
  for (let i = cuerpoStr.length - 1; i >= 0; i--) {
    suma += Number(cuerpoStr[i]) * multiplicador;
    multiplicador = multiplicador < 7 ? multiplicador + 1 : 2;
  }
  const resto = 11 - (suma % 11);
  const dv = resto === 11 ? '0' : resto === 10 ? 'K' : String(resto);
  return `${cuerpoStr}-${dv}`;
}

test('eliminar un alumno pide confirmación y lo quita de la lista', async ({ page }) => {
  const sufijo = `${Date.now()}${Math.floor(Math.random() * 1000)}`;
  const email = `qa.eliminar.${sufijo}@logos.cl`;

  await page.goto('/registro');
  await page.fill('input[name=nombre]', 'QA Eliminar');
  await page.fill('input[name=email]', email);
  await page.fill('input[name=password]', 'Prueba2026!');
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/agregar-alumno/);

  await page.fill('input[name=nombre]', 'Alumno Eliminar');
  await page.fill('input[name=apellidos]', 'Prueba Test');
  await page.fill('input[name=fechaNacimiento]', '2015-03-10');
  await page.fill('input[name=rut]', rutValido(96_000_000 + (Number(sufijo) % 9_000_000)));
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/seleccion-plan/);

  await page.click('button:has-text("Comenzar mis 5 días gratis")');
  await expect(page).toHaveURL(/selector-perfil/);

  await page.goto('/apoderado/inicio');
  const tarjeta = page.locator('.alumno-card', { hasText: 'Alumno Eliminar' });
  await expect(tarjeta).toBeVisible();

  // Cancelar no borra nada.
  await tarjeta.locator('.alumno-card__eliminar').click();
  await expect(tarjeta.locator('.alumno-card__confirmar')).toBeVisible();
  await tarjeta.getByRole('button', { name: 'Cancelar' }).click();
  await expect(page.locator('.alumno-card', { hasText: 'Alumno Eliminar' })).toBeVisible();

  // Confirmar sí borra.
  await tarjeta.locator('.alumno-card__eliminar').click();
  await tarjeta.getByRole('button', { name: 'Sí, eliminar' }).click();
  await expect(page.locator('.alumno-card', { hasText: 'Alumno Eliminar' })).toHaveCount(0);

  // Persiste al recargar — de verdad se borró en el servidor, no solo en la UI.
  await page.reload();
  await expect(page.locator('.alumno-card', { hasText: 'Alumno Eliminar' })).toHaveCount(0);
});
