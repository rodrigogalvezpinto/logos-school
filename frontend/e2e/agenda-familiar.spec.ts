import { test, expect } from '@playwright/test';

/** Idea 7 del boceto de innovación (2026-08-17): agenda familiar del domingo — 3 preguntas
 * (o menos, según qué datos reales existan) para que la mamá no tenga que inventar de qué
 * hablar, con un botón para marcar "ya conversamos" que la oculta hasta la próxima semana.
 * Cuenta fresca (no Sofía): marcar "conversada" es progreso permanente para esa semana —
 * reusar la cuenta compartida podría dejarla oculta para corridas futuras de este mismo
 * archivo dentro de la misma semana calendario. */

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

test('la agenda familiar muestra preguntas reales y "Ya conversamos" la oculta', async ({ page }) => {
  const sufijo = `${Date.now()}${Math.floor(Math.random() * 1000)}`;
  const email = `qa.agenda.${sufijo}@logos.cl`;
  const rut = rutValido(95_000_000 + (Number(sufijo) % 9_000_000));

  await page.goto('/registro');
  await page.fill('input[name=nombre]', 'QA Agenda');
  await page.fill('input[name=email]', email);
  await page.fill('input[name=password]', 'Prueba2026!');
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/agregar-alumno/);

  await page.fill('input[name=nombre]', 'Alumno Agenda');
  await page.fill('input[name=apellidos]', 'Prueba Test');
  await page.fill('input[name=fechaNacimiento]', '2015-03-10');
  await page.fill('input[name=rut]', rut);
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/seleccion-plan/);

  await page.click('button:has-text("Comenzar mis 5 días gratis")');
  await expect(page).toHaveURL(/selector-perfil/);

  await page.getByText('Alumno Agenda').click();
  await expect(page).toHaveURL(/alumno\/inicio/);

  const perfilCrudo = await page.evaluate(() => localStorage.getItem('logos_perfil_activo'));
  const perfil = JSON.parse(perfilCrudo!);

  await page.goto(`/apoderado/progreso/${perfil.id}`);
  await expect(page.locator('h1')).toContainText('Mis Notas');

  const agenda = page.locator('.agenda-familiar');
  await expect(agenda).toBeVisible();
  await expect(agenda.locator('li')).toHaveCount(1); // sin datos previos, solo la pregunta genérica

  await agenda.getByRole('button', { name: 'Ya conversamos ✓' }).click();
  await expect(agenda).toHaveCount(0);

  // Persiste al recargar — no reaparece dentro de la misma semana.
  await page.reload();
  await expect(page.locator('.agenda-familiar')).toHaveCount(0);
});
