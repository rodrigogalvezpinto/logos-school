import { test, expect } from '@playwright/test';

/** Idea 1 del boceto de innovación (2026-08-17): "Estadísticas" como vista propia del
 * Apoderado, agregando a todos sus alumnos de una vez — solo tiene sentido con 2+ alumnos,
 * por eso el sidebar la oculta con uno solo. Cuenta fresca (no Sofía) para controlar
 * exactamente cuántos alumnos tiene la cuenta. */

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

test('con un solo alumno no aparece "Estadísticas"; al agregar un segundo, sí — y muestra a ambos', async ({ page }) => {
  const sufijo = `${Date.now()}${Math.floor(Math.random() * 1000)}`;
  const email = `qa.estadisticas.${sufijo}@logos.cl`;

  await page.goto('/registro');
  await page.fill('input[name=nombre]', 'QA Estadisticas');
  await page.fill('input[name=email]', email);
  await page.fill('input[name=password]', 'Prueba2026!');
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/agregar-alumno/);

  await page.fill('input[name=nombre]', 'Primer Hijo');
  await page.fill('input[name=apellidos]', 'Prueba Test');
  await page.fill('input[name=fechaNacimiento]', '2015-03-10');
  await page.fill('input[name=rut]', rutValido(80_000_000 + (Number(sufijo) % 9_000_000)));
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/seleccion-plan/);

  await page.click('button:has-text("Comenzar mis 5 días gratis")');
  await expect(page).toHaveURL(/selector-perfil/);

  await page.goto('/apoderado/inicio');
  await expect(page.locator('.sidebar__item', { hasText: 'Estadísticas' })).toHaveCount(0);

  await page.getByRole('button', { name: 'Agregar otro alumno' }).click();
  await page.fill('input[name=nombre]', 'Segundo Hijo');
  await page.fill('input[name=apellidos]', 'Prueba Test');
  await page.fill('input[name=fechaNacimiento]', '2013-05-20');
  await page.fill('input[name=rut]', rutValido(81_000_000 + (Number(sufijo) % 9_000_000)));
  await page.getByRole('button', { name: 'Agregar alumno' }).click();
  await expect(page.locator('.formulario-inline')).not.toBeVisible();

  await page.goto('/apoderado/inicio');
  const itemEstadisticas = page.locator('.sidebar__item', { hasText: 'Estadísticas' });
  await expect(itemEstadisticas).toBeVisible();
  await itemEstadisticas.click();
  await expect(page).toHaveURL(/apoderado\/estadisticas/);

  await expect(page.locator('.estadistica-card', { hasText: 'Primer Hijo' })).toBeVisible();
  await expect(page.locator('.estadistica-card', { hasText: 'Segundo Hijo' })).toBeVisible();
  await expect(page.locator('.estadistica-card').first()).toContainText('% del temario cubierto');
});
