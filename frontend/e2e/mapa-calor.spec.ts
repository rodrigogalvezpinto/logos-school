import { test, expect } from '@playwright/test';

/** Mapa de calor por eje temático — idea propia (no un hallazgo de la competencia, ver
 * planificacion/27-plan-incorporacion-hallazgos-brincus.md).
 *
 * No se puede probar con la cuenta compartida "Sofía": sus intentos ya entregados resultaron
 * ser, por azar, todos de preguntas sin oa_id vinculado (hallazgo real al verificar este test
 * — las preguntas de "prueba_unidad" tienen un vínculo "best effort" a un OA que en la
 * práctica falla para buena parte del banco; las de "examen_simulacro" sí tienen buena
 * cobertura). Por eso este test crea una cuenta propia y rinde directamente, por API, un
 * examen simulacro real (conjunto 1987, "Examen Ciencias Naturales Forma B", nivel 6) que sí
 * tiene preguntas de alternativas con oa_id + eje_temático poblado — mismo patrón de
 * verificación con datos reales ya usado en alerta-ritmo.spec.ts. */

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

const NIVEL_ID = 6;
const CONJUNTO_EXAMEN_ID = 90; // "Examen Ciencias Naturales Forma B" (6° básico) — contenido real y estable del dev DB

// Respuestas correctas reales del conjunto 90 (solo preguntas "alternativas", que sí tienen
// oa_id + eje_temático poblado) — no se pueden obtener por API con una cuenta sin privilegios
// (GET /evaluaciones/conjuntos/{id} oculta `respuesta_correcta` a propósito), así que se
// registran acá igual que Sofía es una cuenta de datos reales fijos en el resto de la suite.
const RESPUESTAS_CORRECTAS: Record<number, string> = {
  2316: 'Las algas y las cianobacterias',
  2317: 'Azúcar (glucosa)',
  2319: 'Alimentarse de los restos de otros organismos y liberar nutrientes al suelo',
  2320: 'Consumidor de tercer orden',
  2322: 'El estirón de crecimiento',
  2323: 'La edad de inicio de la pubertad varía de una persona a otra, y esa variación es normal',
  2325: 'Fortalece el sistema cardiovascular y ayuda a mantener un peso corporal saludable',
  2326: 'Lavarse el rostro diariamente',
  2328: 'Tanto los objetos como los seres vivos necesitan energía para que ocurra cualquier tipo de cambio',
  2329: 'Energía calórica',
  2331: 'Energía geotérmica',
  2332: 'Sus numerosos ríos y caudales abundantes',
  2334: 'Condensación',
  2335: 'La evaporación ocurre lentamente en la superficie del líquido a cualquier temperatura, mientras que la ebullición ocurre rápidamente en todo el volumen del líquido a una temperatura específica',
  2337: 'Atmósfera',
  2339: 'El viento',
};

test('el mapa de calor agrupa por asignatura y eje temático tras rendir un examen real', async ({ page, request }) => {
  const sufijo = `${Date.now()}${Math.floor(Math.random() * 1000)}`;
  const email = `qa.mapacalor.${sufijo}@logos.cl`;
  const rut = rutValido(40_000_000 + (Number(sufijo) % 9_000_000));

  await page.goto('/registro');
  await page.fill('input[name=nombre]', 'QA Mapa Calor');
  await page.fill('input[name=email]', email);
  await page.fill('input[name=password]', 'Prueba2026!');
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/agregar-alumno/);

  await page.fill('input[name=nombre]', 'Alumno Mapa Calor');
  await page.fill('input[name=apellidos]', 'Prueba Test');
  await page.fill('input[name=fechaNacimiento]', '2013-03-10');
  await page.fill('input[name=rut]', rut);
  await page.selectOption('select[name=nivelId]', String(NIVEL_ID));
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/seleccion-plan/);
  await expect(page.locator('.plan')).toHaveCount(3);
  await page.click('button:has-text("Comenzar mis 5 días gratis")');
  await expect(page).toHaveURL(/selector-perfil/, { timeout: 15000 });

  await page.getByText('Alumno Mapa Calor').click();
  await expect(page).toHaveURL(/alumno\/inicio/);

  const token = await page.evaluate(() => localStorage.getItem('logos_token'));
  const perfilCrudo = await page.evaluate(() => localStorage.getItem('logos_perfil_activo'));
  const perfil = JSON.parse(perfilCrudo!);
  const headers = { Authorization: `Bearer ${token}` };

  const intento = await (
    await request.post('http://localhost:8000/evaluaciones/intentos', {
      headers,
      data: { perfil_alumno_id: perfil.id, conjunto_evaluacion_id: CONJUNTO_EXAMEN_ID },
    })
  ).json();

  for (const [preguntaId, respuesta] of Object.entries(RESPUESTAS_CORRECTAS)) {
    await request.patch(`http://localhost:8000/evaluaciones/intentos/${intento.id}/responder`, {
      headers,
      data: { pregunta_id: Number(preguntaId), respuesta },
    });
  }
  await request.post(`http://localhost:8000/evaluaciones/intentos/${intento.id}/entregar`, { headers });

  await page.goto('/alumno/notas');
  await page.waitForSelector('.prediccion');

  const celdas = page.locator('.mapa-calor__celda');
  await expect(celdas.first()).toBeVisible();
  expect(await celdas.count()).toBeGreaterThan(0);

  const primerPct = await celdas.first().locator('.mapa-calor__eje-pct').textContent();
  const valor = Number(primerPct!.replace('%', ''));
  expect(valor).toBeGreaterThanOrEqual(0);
  expect(valor).toBeLessThanOrEqual(100);

  await expect(page.locator('.mapa-calor__asignatura').first()).toBeVisible();
  await expect(page.locator('.mapa-calor__asignatura h3').first()).toContainText('Ciencias Naturales');
});
