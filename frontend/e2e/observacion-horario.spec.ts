import { execSync } from 'node:child_process';
import { test, expect } from '@playwright/test';

/** Cruce sueño / horario de estudio — idea propia (no un hallazgo de Brincus, ver
 * planificacion/27-plan-incorporacion-hallazgos-brincus.md). Solo visible para el
 * Apoderado, nunca para el alumno. No hay forma de forzar la hora de un intento por API
 * (siempre usa `reloj.ahora()`) — se backdatea directo en Postgres, mismo patrón ya usado
 * en plan-estudio-atrasada.spec.ts. Cuenta fresca con nivel explícito ("5° básico", con
 * varios conjuntos de prueba de unidad disponibles) para no tocar la cuenta compartida
 * Sofía ni depender de cuántas pruebas le queden sin rendir. */

const NIVEL_ID = 6; // "5° básico"

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

test('el apoderado ve una observación cuando el alumno estudia tarde en la noche varias veces', async ({ page, request }) => {
  const sufijo = `${Date.now()}${Math.floor(Math.random() * 1000)}`;
  const email = `qa.horario.${sufijo}@logos.cl`;
  const rut = rutValido(70_000_000 + (Number(sufijo) % 9_000_000));

  await page.goto('/registro');
  await page.fill('input[name=nombre]', 'QA Horario');
  await page.fill('input[name=email]', email);
  await page.fill('input[name=password]', 'Prueba2026!');
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/agregar-alumno/);

  await page.fill('input[name=nombre]', 'Alumno Horario');
  await page.fill('input[name=apellidos]', 'Prueba Test');
  await page.fill('input[name=fechaNacimiento]', '2014-03-10');
  await page.fill('input[name=rut]', rut);
  await page.selectOption('select[name=nivelId]', { label: '5° básico' });
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/seleccion-plan/);

  await page.click('button:has-text("Comenzar mis 5 días gratis")');
  await expect(page).toHaveURL(/selector-perfil/);

  await page.getByText('Alumno Horario').click();
  await expect(page).toHaveURL(/alumno\/inicio/);

  const token = await page.evaluate(() => localStorage.getItem('logos_token'));
  const perfilCrudo = await page.evaluate(() => localStorage.getItem('logos_perfil_activo'));
  const perfil = JSON.parse(perfilCrudo!);
  const headers = { Authorization: `Bearer ${token}` };

  // Régimen B (5° básico en adelante): las pruebas de unidad son por asignatura, no
  // integradas por nivel (esa es otra ruta, /conjuntos/nivel/{id}, solo para Régimen A) —
  // hay que recorrer las asignaturas del nivel hasta juntar suficientes.
  const asignaturas = await (
    await request.get(`http://localhost:8000/contenido/niveles/${NIVEL_ID}/asignaturas`, { headers })
  ).json();
  const pruebas: { id: number }[] = [];
  for (const asignatura of asignaturas) {
    if (pruebas.length >= 3) break;
    const conjuntos = await (
      await request.get(`http://localhost:8000/evaluaciones/conjuntos/asignatura/${asignatura.id}`, { headers })
    ).json();
    pruebas.push(...conjuntos.filter((c: { tipo: string }) => c.tipo === 'prueba_unidad'));
  }
  expect(pruebas.length).toBeGreaterThanOrEqual(3);

  const idsIntentos: number[] = [];
  for (const prueba of pruebas.slice(0, 3)) {
    const intento = await (
      await request.post('http://localhost:8000/evaluaciones/intentos', {
        headers,
        data: { perfil_alumno_id: perfil.id, conjunto_evaluacion_id: prueba.id },
      })
    ).json();
    await request.post(`http://localhost:8000/evaluaciones/intentos/${intento.id}/entregar`, { headers });
    idsIntentos.push(intento.id);
  }

  // 23:00 hora de Chile = 02:00 UTC del día siguiente (offset fijo -3 que usa el backend).
  for (const id of idsIntentos) {
    execSync(
      `psql "postgresql://logos_dev:logos_dev_local@localhost:5432/logos_dev" -c "UPDATE intento_evaluacion SET fecha_termino = '2026-08-10 02:00:00' WHERE id = ${id}"`,
    );
  }

  await page.goto(`/apoderado/progreso/${perfil.id}`);
  await expect(page.locator('h1')).toContainText('Mis Notas');

  const observacion = page.locator('.observacion-horario');
  await expect(observacion).toBeVisible();
  await expect(observacion).toContainText('21:00');

  // Nunca visible para el propio alumno — es información para que decida un adulto.
  await page.goto('/alumno/notas');
  await expect(page.locator('.observacion-horario')).toHaveCount(0);
});
