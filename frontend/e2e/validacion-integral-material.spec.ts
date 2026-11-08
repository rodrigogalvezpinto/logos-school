import { test, expect, Page, APIRequestContext } from '@playwright/test';
import { existsSync, readFileSync } from 'node:fs';
import { API_URL } from './helpers';

/**
 * Validación integral del material en el navegador (auditoría 2026-11-06).
 *
 * Recorre TODOS los cursos, TODAS las asignaturas, TODAS las guías (estudio +
 * autoevaluación) y TODAS las pruebas de unidad y simulacros, pregunta por pregunta:
 *  - el enunciado se muestra sin restos de Markdown ni de la pauta;
 *  - el control corresponde al tipo (radio para alternativas y V/F, casillas para
 *    «varias correctas») y muestra exactamente las opciones de la base;
 *  - marcando la clave de la base, la autoevaluación dice «¡Correcto!» y la
 *    prueba/simulacro entregada obtiene N de N correctas y nota 7.0.
 * Así se comprueba de punta a punta que cada clave, cada opción y la corrección
 * (frontend + backend) son coherentes.
 *
 * Requiere la fixture con claves exportada desde la MISMA base que usa la API:
 *   DATABASE_URL=... python backend/scripts/exportar_fixture_validacion_e2e.py \
 *     frontend/e2e/fixtures/material-validacion.json
 * Ejecutar: LOGOS_E2E_WEB_URL=... LOGOS_E2E_API_URL=... npx playwright test \
 *   validacion-integral-material --project=chromium
 * Filtrar curso: LOGOS_VALIDAR_NIVEL="4° medio".
 */

type Clave = { tipo: string; correcta: string; opciones: string[] | null };
type Conjunto = { id: number; tipo: string; nombre: string; preguntas: number };
type Asignatura = { id: number; nombre: string; oas: { id: number; codigo: string; preguntas: number }[]; conjuntos: Conjunto[] };
type Nivel = { id: number; nombre: string; asignaturas: Asignatura[]; integrados: Conjunto[] };
type PreguntaApi = { id: number; tipo: string; enunciado: string; opciones: string[] | null };

const RUTA_FIXTURE = 'e2e/fixtures/material-validacion.json';
const fixture: { niveles: Nivel[]; claves: Record<string, Clave> } | null = existsSync(RUTA_FIXTURE)
  ? JSON.parse(readFileSync(RUTA_FIXTURE, 'utf-8'))
  : null;
const FILTRO_NIVEL = process.env['LOGOS_VALIDAR_NIVEL'];

const normalizar = (s: string) => s.replace(/\s+/g, ' ').trim();
const RESTOS_PROHIBIDOS = [/::(contar|dibujo|emoji|fraccion|posicion|fila|largo|regla|balanza|barras|linea|circular|caja|mapa)::/, /\*\*Respuesta/i, /Respuesta correcta:/i, /^#{1,6}\s/m, /\bundefined\b/, /\[object Object\]/];

function rutValido(semilla: number): string {
  const cuerpo = String(15000000 + (semilla % 9000000));
  let suma = 0;
  let m = 2;
  for (let i = cuerpo.length - 1; i >= 0; i--) {
    suma += Number(cuerpo[i]) * m;
    m = m < 7 ? m + 1 : 2;
  }
  const r = 11 - (suma % 11);
  return `${cuerpo}-${r === 11 ? '0' : r === 10 ? 'K' : String(r)}`;
}

/** Crea por API una cuenta apoderado + alumno del nivel, con prueba gratis activa. */
async function crearAlumno(api: APIRequestContext, nivel: Nivel) {
  const sello = Date.now() + nivel.id * 7919 + Math.floor(Math.random() * 1000);
  const email = `validacion.${nivel.id}.${sello}@logos.cl`;
  const reg = await api.post(`${API_URL}/auth/registro`, { data: { email, password: 'Validacion2026!', nombre: 'Validación Integral' } });
  expect(reg.status(), 'registro').toBe(201);
  const token = (await reg.json()).access_token as string;
  const headers = { Authorization: `Bearer ${token}` };
  const alta = await api.post(`${API_URL}/auth/alumnos`, {
    headers,
    data: { nombre: 'Valida', apellidos: `Nivel ${nivel.id}`, fecha_nacimiento: '2010-03-15', rut: rutValido(sello), nivel_id: nivel.id },
  });
  expect(alta.status(), 'alta alumno').toBe(201);
  const perfil = await alta.json();
  const planes = await (await api.get(`${API_URL}/auth/planes`, { headers })).json();
  const gratis = await api.post(`${API_URL}/auth/alumnos/${perfil.id}/prueba-gratis`, { headers, data: { plan_id: planes[0].id } });
  expect(gratis.status(), 'prueba gratis').toBe(200);
  return { token, perfil };
}

async function abrirSesion(page: Page, sesion: { token: string; perfil: unknown }) {
  await page.addInitScript((s) => {
    localStorage.setItem('logos_token', s.token);
    localStorage.setItem('logos_perfil_activo', JSON.stringify(s.perfil));
    localStorage.setItem('logos_nombre_apoderado', 'Validación Integral');
  }, sesion);
}

async function cerrarCheckin(page: Page) {
  const checkin = page.locator('.checkin__opcion', { hasText: 'Tranquilo' });
  if (await checkin.isVisible().catch(() => false)) await checkin.click();
}

/** Marca la clave de la pregunta visible y verifica control y opciones. */
async function responderCorrecto(page: Page, p: PreguntaApi, clave: Clave, ref: string) {
  const enunciado = page.locator('.pregunta__enunciado');
  await expect(enunciado, `${ref}: enunciado`).not.toBeEmpty();
  const texto = await enunciado.innerText();
  for (const patron of RESTOS_PROHIBIDOS) expect(texto, `${ref}: resto prohibido ${patron}`).not.toMatch(patron);
  expect(p.tipo, `${ref}: tipo API = tipo base`).toBe(clave.tipo);

  const etiquetas = page.locator('.pregunta .opciones .opcion');
  const textos = (await etiquetas.allInnerTexts()).map(normalizar);

  if (clave.tipo === 'verdadero_falso') {
    expect(textos, `${ref}: opciones V/F`).toEqual(['Verdadero', 'Falso']);
    await etiquetas.nth(clave.correcta === 'Verdadero' ? 0 : 1).locator('input[type=radio]').check();
    await expect(page.locator('.pregunta .opcion--elegida'), `${ref}: V/F registrada`).toHaveText(clave.correcta);
    return;
  }
  const opciones = (clave.opciones ?? []).map(normalizar);
  // Opciones con marcador visual (::contar::🍎::9::) se dibujan: se compara el texto solo en las demás.
  const visual = (o: string) => /::(contar|emoji|dibujo|fraccion|posicion|fila|largo|regla|balanza|barras|linea|circular|caja|mapa)::/.test(o);
  expect(textos.length, `${ref}: cantidad de opciones`).toBe(opciones.length);
  opciones.forEach((o, j) => {
    if (visual(o)) expect(textos[j], `${ref}: opción visual dibujada, sin marcador crudo`).not.toContain('::');
    else expect(textos[j], `${ref}: opción ${j + 1} = base`).toBe(o);
  });
  if (clave.tipo === 'alternativas') {
    await expect(etiquetas.locator('input[type=radio]'), `${ref}: radios`).toHaveCount(opciones.length);
    const i = opciones.indexOf(normalizar(clave.correcta));
    expect(i, `${ref}: la clave está entre las opciones`).toBeGreaterThanOrEqual(0);
    await etiquetas.nth(i).locator('input').check();
    await expect(page.locator('.pregunta .opcion--elegida'), `${ref}: alternativa registrada`).toHaveCount(1);
  } else if (clave.tipo === 'varias_correctas') {
    await expect(etiquetas.locator('input[type=checkbox]'), `${ref}: casillas`).toHaveCount(opciones.length);
    await expect(page.locator('.opciones__instruccion'), `${ref}: instrucción varias`).toBeVisible();
    const correctas: string[] = JSON.parse(clave.correcta);
    expect(correctas.length, `${ref}: varias con ≥2 claves`).toBeGreaterThanOrEqual(2);
    for (const c of correctas) {
      const i = opciones.indexOf(normalizar(c));
      expect(i, `${ref}: clave «${c}» entre las opciones`).toBeGreaterThanOrEqual(0);
      await etiquetas.nth(i).locator('input').check();
    }
    await expect(page.locator('.pregunta .opcion--elegida'), `${ref}: casillas registradas`).toHaveCount(correctas.length);
  } else {
    throw new Error(`${ref}: tipo no cerrado «${clave.tipo}»`);
  }
}

async function validarConjunto(page: Page, nivel: Nivel, conjunto: Conjunto, sesion: { token: string; perfil: { id: number } }) {
  const ruta = conjunto.tipo === 'prueba_unidad' ? `/alumno/prueba/${conjunto.id}` : `/examen/${conjunto.id}`;
  const respuesta = page.waitForResponse((r) => r.url().includes(`/evaluaciones/conjuntos/${conjunto.id}`) && r.request().method() === 'GET');
  await page.goto(ruta);
  const detalle = await (await respuesta).json();
  const preguntas: PreguntaApi[] = detalle.preguntas;
  expect(preguntas.length, `${conjunto.nombre}: n.º de preguntas`).toBe(conjunto.preguntas);
  await cerrarCheckin(page);
  await page.getByRole('button', { name: 'Comenzar' }).click();

  for (let i = 0; i < preguntas.length; i++) {
    const ref = `${nivel.nombre} · ${conjunto.nombre} · P${i + 1} (id ${preguntas[i].id})`;
    await expect(page.locator('.runner__progreso')).toHaveText(`Pregunta ${i + 1} de ${preguntas.length}`);
    await responderCorrecto(page, preguntas[i], fixture!.claves[String(preguntas[i].id)], ref);
    if (i < preguntas.length - 1) await page.locator('.runner__nav').getByRole('button', { name: 'Siguiente' }).click();
  }
  await page.locator('.runner__nav').getByRole('button', { name: 'Entregar' }).click();
  // Con todas respondidas no debe aparecer el aviso de faltantes: si aparece, se perdió una respuesta.
  await expect(page.locator('.resultado__puntaje'), `${conjunto.nombre}: puntaje`).toContainText(
    `${preguntas.length} de ${preguntas.length} correctas`,
  );
  await expect(page.locator('.resultado__nota'), `${conjunto.nombre}: nota`).toContainText('7');
  await expect(page.locator('.resultado__nota')).not.toHaveClass(/reprobada/);
  void sesion;
}

async function validarGuias(page: Page, nivel: Nivel, asig: Asignatura) {
  for (const oa of asig.oas) {
    const ref = `${nivel.nombre} · ${asig.nombre} · ${oa.codigo} (oa ${oa.id})`;
    await page.goto(`/alumno/estudiar/${oa.id}`);
    await cerrarCheckin(page);
    const contenido = page.locator('.contenido-guia');
    await expect(contenido, `${ref}: guía`).not.toBeEmpty();
    const textoGuia = await contenido.innerText();
    expect(textoGuia, `${ref}: guía sin encabezados crudos`).not.toMatch(/^#{1,6}\s/m);
    expect(textoGuia, `${ref}: guía sin undefined`).not.toMatch(/\bundefined\b|\[object Object\]/);

    if (oa.preguntas === 0) continue;
    const respuesta = page.waitForResponse((r) => r.url().includes(`/evaluaciones/autoevaluacion/${oa.id}`));
    await page.goto(`/alumno/autoevaluacion/${oa.id}`);
    const preguntas: PreguntaApi[] = await (await respuesta).json();
    expect(preguntas.length, `${ref}: preguntas de autoevaluación`).toBe(oa.preguntas);
    await cerrarCheckin(page);
    // La guía (textos, tablas, gráficos) debe poder consultarse sin salir de la práctica.
    const panelGuia = page.locator('details.guia-consulta');
    await expect(panelGuia, `${ref}: panel «Ver la guía»`).toBeVisible();
    await panelGuia.locator('summary').click();
    await expect(panelGuia.locator('.guia-consulta__contenido'), `${ref}: guía en el panel`).not.toBeEmpty();
    expect(await panelGuia.innerText(), `${ref}: el panel no muestra claves`).not.toMatch(/(✅|\*\*)\s*Respuesta correcta|Respuesta correcta\s*:/i);
    await panelGuia.locator('summary').click();
    await page.getByRole('button', { name: 'Comenzar' }).click();
    for (let i = 0; i < preguntas.length; i++) {
      const refP = `${ref} · P${i + 1} (id ${preguntas[i].id})`;
      await expect(page.locator('.runner__progreso')).toHaveText(`Pregunta ${i + 1} de ${preguntas.length}`);
      await responderCorrecto(page, preguntas[i], fixture!.claves[String(preguntas[i].id)], refP);
      await page.locator('.btn-ayuda-practica').click();
      await expect(page.locator('.feedback__tag-ok'), `${refP}: la app marca «¡Correcto!» con la clave`).toBeVisible();
      if (i < preguntas.length - 1) await page.locator('.runner__nav').getByRole('button', { name: 'Siguiente' }).click();
    }
  }
}

test.describe('Validación integral del material (todos los cursos y ramos)', () => {
  test.skip(!fixture, `Falta ${RUTA_FIXTURE}: exportarla con backend/scripts/exportar_fixture_validacion_e2e.py`);
  if (!fixture) return;

  for (const nivel of fixture.niveles.filter((n) => !FILTRO_NIVEL || n.nombre === FILTRO_NIVEL)) {
    test.describe(nivel.nombre, () => {
      let sesion: { token: string; perfil: { id: number } };
      test.beforeAll(async ({ playwright }) => {
        const api = await playwright.request.newContext();
        sesion = await crearAlumno(api, nivel);
        await api.dispose();
      });
      test.beforeEach(async ({ page }) => abrirSesion(page, sesion));

      for (const asig of nivel.asignaturas) {
        test(`${nivel.nombre} · ${asig.nombre} · guías y autoevaluación (${asig.oas.length} OA)`, async ({ page }) => {
          test.setTimeout(30 * 60_000);
          await validarGuias(page, nivel, asig);
        });
        for (const c of asig.conjuntos) {
          test(`${nivel.nombre} · ${asig.nombre} · ${c.nombre}`, async ({ page }) => {
            test.setTimeout(10 * 60_000);
            await validarConjunto(page, nivel, c, sesion);
          });
        }
      }
      for (const c of nivel.integrados) {
        test(`${nivel.nombre} · integrado · ${c.nombre}`, async ({ page }) => {
          test.setTimeout(10 * 60_000);
          await validarConjunto(page, nivel, c, sesion);
        });
      }
    });
  }
});
