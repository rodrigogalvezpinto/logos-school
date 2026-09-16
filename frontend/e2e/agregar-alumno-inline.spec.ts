import { test, expect } from '@playwright/test';

/** Fase 1, ítem 2.9 del plan de incorporación de hallazgos de Brincus — agregar alumno
 * inline en el panel del Apoderado. Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md. */

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

test.describe('Agregar alumno inline en el panel del Apoderado (Fase 1, ítem 2.9)', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('el botón "Agregar otro alumno" muestra el formulario sin salir de /apoderado/inicio', async ({ page }) => {
    await page.goto('/apoderado/inicio');
    await page.getByRole('button', { name: 'Agregar otro alumno' }).click();
    await expect(page.locator('.formulario-inline')).toBeVisible();
    await expect(page).toHaveURL(/apoderado\/inicio/);
  });

  test('cancelar oculta el formulario sin agregar nada', async ({ page }) => {
    await page.goto('/apoderado/inicio');
    await page.getByRole('button', { name: 'Agregar otro alumno' }).click();
    await page.getByRole('button', { name: 'Cancelar' }).click();
    await expect(page.locator('.formulario-inline')).not.toBeVisible();
    await expect(page.getByRole('button', { name: 'Agregar otro alumno' })).toBeVisible();
  });

  test('RUT inválido muestra error sin salir del formulario', async ({ page }) => {
    await page.goto('/apoderado/inicio');
    await page.getByRole('button', { name: 'Agregar otro alumno' }).click();

    await page.fill('input[name=nombre]', 'Test');
    await page.fill('input[name=apellidos]', 'Apellido');
    await page.fill('input[name=fechaNacimiento]', '2016-01-01');
    await page.fill('input[name=rut]', '11.111.111-2'); // dígito verificador incorrecto
    await page.getByRole('button', { name: 'Agregar alumno' }).click();

    await expect(page.locator('.error')).toContainText('RUT');
    await expect(page.locator('.formulario-inline')).toBeVisible();
  });
});

test.describe('Agregar alumno inline — flujo completo con datos reales', () => {
  // Sin storageState de Sofía a propósito: agregar un alumno de verdad quedaría pegado
  // permanentemente en la cuenta demo compartida por el resto del suite y rompería tests
  // que cuentan cuántos alumnos tiene (ver flujos-principales.spec.ts, "el panel
  // Apoderado se ve y no rompe") — usa una cuenta nueva, igual que registro.spec.ts.
  test('agregar un alumno lo deja ver en la lista sin navegar a otra ruta', async ({ page }) => {
    const email = `agregar.inline.${Date.now()}.${Math.floor(Math.random() * 100000)}@logos.cl`;
    await page.goto('/registro');
    await page.fill('input[name=nombre]', 'Apoderado Inline QA');
    await page.fill('input[name=email]', email);
    await page.fill('input[name=password]', 'Prueba2026!');
    await page.click('button[type=submit]');
    await expect(page).toHaveURL(/agregar-alumno/);
    await page.fill('input[name=nombre]', 'Primer Alumno');
    await page.fill('input[name=apellidos]', 'Prueba Test');
    await page.fill('input[name=fechaNacimiento]', '2015-03-10');
    await page.fill('input[name=rut]', rutValidoUnico());
    await page.click('button[type=submit]');
    await expect(page).toHaveURL(/seleccion-plan/);
    await page.click('button:has-text("Comenzar mis 5 días gratis")');
    await expect(page).toHaveURL(/selector-perfil/);
    await page.goto('/apoderado/inicio');

    await page.getByRole('button', { name: 'Agregar otro alumno' }).click();
    await page.fill('input[name=nombre]', 'Hermano QA');
    await page.fill('input[name=apellidos]', 'Prueba Test');
    await page.fill('input[name=fechaNacimiento]', '2017-05-05');
    await page.fill('input[name=rut]', rutValidoUnico());
    await page.getByRole('button', { name: 'Agregar alumno' }).click();

    await expect(page.locator('.alumno-card', { hasText: 'Hermano QA' })).toBeVisible();
    await expect(page.locator('.formulario-inline')).not.toBeVisible();
    await expect(page).toHaveURL(/apoderado\/inicio/);
  });
});
