import { test, expect } from '@playwright/test';

/** Fase 1, ítem 2.4 del plan de incorporación de hallazgos de Brincus — check-in
 * emocional diario. Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md.
 * Usa una cuenta nueva (no Sofía) para garantizar que el check-in de hoy nunca se haya
 * registrado antes, sin depender del orden de ejecución de otros specs. */

function rutValidoUnico(): string {
  const cuerpo = String(10000000 + (Date.now() % 89999999) + Math.floor(Math.random() * 900));
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

async function registrarYEntrar(page: import('@playwright/test').Page) {
  const email = `checkin.${Date.now()}.${Math.floor(Math.random() * 100000)}@logos.cl`;
  await page.goto('/registro');
  await page.fill('input[name=nombre]', 'Apoderado Checkin');
  await page.fill('input[name=email]', email);
  await page.fill('input[name=password]', 'Prueba2026!');
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/agregar-alumno/);

  await page.fill('input[name=nombre]', 'Alumno QA');
  await page.fill('input[name=apellidos]', 'Prueba Test');
  await page.fill('input[name=fechaNacimiento]', '2016-01-01');
  await page.fill('input[name=rut]', rutValidoUnico());
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/seleccion-plan/);
  await page.click('button:has-text("Comenzar mis 5 días gratis")');
  await expect(page).toHaveURL(/selector-perfil/);
  await page.getByText('Alumno QA').click();
  await expect(page).toHaveURL(/alumno\/inicio/);
}

test.describe('Check-in emocional diario (Fase 1, ítem 2.4)', () => {
  test('aparece el modal "¿Cómo te sientes hoy?" la primera vez del día, con 7 opciones', async ({ page }) => {
    await registrarYEntrar(page);
    await expect(page.locator('.checkin')).toBeVisible();
    expect(await page.locator('.checkin__opcion').count()).toBe(7);
  });

  test('elegir un estado cierra el modal y no vuelve a aparecer al recargar', async ({ page }) => {
    await registrarYEntrar(page);
    await expect(page.locator('.checkin')).toBeVisible();
    await page.locator('.checkin__opcion', { hasText: 'Feliz' }).click();
    await expect(page.locator('.checkin')).not.toBeVisible();

    await page.reload();
    await expect(page.locator('.checkin')).not.toBeVisible();
  });
});
