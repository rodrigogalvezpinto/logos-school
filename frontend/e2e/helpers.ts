import { execFileSync } from 'node:child_process';
import { randomInt, randomUUID } from 'node:crypto';
import { Page, expect } from '@playwright/test';

export const API_URL = process.env['LOGOS_E2E_API_URL'] ?? 'http://localhost:8000';

export function ejecutarSqlPrueba(sql: string): void {
  const raw = process.env['LOGOS_E2E_DATABASE_URL'];
  if (!raw) throw new Error('Las fixtures SQL requieren LOGOS_E2E_DATABASE_URL explícito.');
  const url = new URL(raw);
  if (!['postgres:', 'postgresql:'].includes(url.protocol)
    || !['localhost', '127.0.0.1', '[::1]'].includes(url.hostname)
    || url.pathname !== '/logos_auditoria_test') {
    throw new Error('Las fixtures SQL solo pueden modificar la base local de auditoría autorizada.');
  }
  execFileSync('psql', [
    '--host', url.hostname.replace(/^\[|\]$/g, ''), '--port', url.port || '5432',
    '--username', decodeURIComponent(url.username), '--dbname', 'logos_auditoria_test',
    '--set', 'ON_ERROR_STOP=1', '--command', sql,
  ], { env: { ...process.env, PGPASSWORD: decodeURIComponent(url.password) }, stdio: 'pipe' });
}

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

type PerfilPrueba = { id: number; nivel_id: number; nombre: string; apellidos: string };

export async function obtenerSesionAlumno(page: Page) {
  await page.goto('/alumno/inicio');
  const sesion = await page.evaluate(() => ({
    token: localStorage.getItem('logos_token'),
    perfil: JSON.parse(localStorage.getItem('logos_perfil_activo') || 'null') as PerfilPrueba | null,
  }));
  if (!sesion.token || !sesion.perfil) throw new Error('La fixture requiere una sesión de alumno activa.');
  const headers = { Authorization: `Bearer ${sesion.token}` };
  const respuesta = await page.request.get(`${API_URL}/auth/alumnos`, { headers });
  expect(respuesta.status(), 'Consultar perfiles de la sesión').toBe(200);
  const perfiles: PerfilPrueba[] = await respuesta.json();
  const perfil = perfiles.find((p) => p.id === sesion.perfil!.id);
  if (!perfil) throw new Error('El perfil activo no pertenece a la sesión.');
  return { perfil, headers };
}

export async function prepararIntentoReprobado(page: Page) {
  const { perfil, headers } = await obtenerSesionAlumno(page);
  const asignaturasRespuesta = await page.request.get(`${API_URL}/contenido/niveles/${perfil.nivel_id}/asignaturas`);
  expect(asignaturasRespuesta.status()).toBe(200);
  const asignaturas: { id: number }[] = await asignaturasRespuesta.json();
  let conjuntoId: number | undefined;
  for (const asignatura of asignaturas) {
    const respuesta = await page.request.get(`${API_URL}/evaluaciones/conjuntos/asignatura/${asignatura.id}`, { headers });
    expect(respuesta.status()).toBe(200);
    const conjuntos: { id: number; tipo: string; num_preguntas: number }[] = await respuesta.json();
    conjuntoId = conjuntos.find((c) => c.tipo === 'prueba_unidad' && c.num_preguntas > 0)?.id;
    if (conjuntoId) break;
  }
  if (!conjuntoId) throw new Error('El nivel no tiene pruebas de unidad disponibles para la fixture.');
  const inicio = await page.request.post(`${API_URL}/evaluaciones/intentos`, {
    headers, data: { perfil_alumno_id: perfil.id, conjunto_evaluacion_id: conjuntoId },
  });
  expect(inicio.status()).toBe(201);
  const intento: { id: number; respuestas: Record<string, string> } = await inicio.json();
  expect(intento.respuestas, 'La fixture requiere un intento nuevo sin respuestas previas').toEqual({});
  const entrega = await page.request.post(`${API_URL}/evaluaciones/intentos/${intento.id}/entregar`, { headers });
  expect(entrega.status()).toBe(200);
  const resultado = await entrega.json();
  expect(resultado.nota, 'La precondición debe ser un intento reprobado controlado').toBe(1);
  expect(resultado.fecha_termino).toBeTruthy();
  return perfil;
}

export async function prepararAlumnoAislado(page: Page) {
  const { perfil: origen } = await obtenerSesionAlumno(page);
  const registro = await page.request.post(`${API_URL}/auth/registro`, {
    data: { nombre: 'Apoderado QA Plan', email: `qa.plan.${randomUUID()}@logos.cl`, password: randomUUID() },
  });
  expect(registro.status(), 'Crear cuenta aislada para el plan').toBe(201);
  const { access_token: token } = await registro.json();
  const headers = { Authorization: `Bearer ${token}` };
  const cuerpo = String(randomInt(40000000, 99000000));
  const suma = [...cuerpo].reverse().reduce((total, digito, i) => total + Number(digito) * (2 + i % 6), 0);
  const resto = 11 - suma % 11;
  const rut = `${cuerpo}-${resto === 11 ? '0' : resto === 10 ? 'K' : resto}`;
  const alumno = await page.request.post(`${API_URL}/auth/alumnos`, {
    headers, data: { nombre: 'Alumno QA Plan', apellidos: 'Sintético', fecha_nacimiento: '2016-03-15', rut, nivel_id: origen.nivel_id },
  });
  expect(alumno.status(), 'Crear alumno aislado para el plan').toBe(201);
  const perfil: PerfilPrueba = await alumno.json();
  const planes = await page.request.get(`${API_URL}/auth/planes`, { headers });
  expect(planes.status()).toBe(200);
  const catalogo: { id: number }[] = await planes.json();
  expect(catalogo.length).toBeGreaterThan(0);
  const suscripcion = await page.request.post(`${API_URL}/auth/alumnos/${perfil.id}/prueba-gratis`, {
    headers, data: { plan_id: catalogo[0].id },
  });
  expect(suscripcion.status()).toBe(200);
  await page.evaluate(({ token, perfil }) => {
    localStorage.setItem('logos_token', token);
    localStorage.setItem('logos_perfil_activo', JSON.stringify(perfil));
    localStorage.setItem('logos_nombre_apoderado', 'Apoderado QA Plan');
  }, { token, perfil });
  return { perfil, headers };
}

export async function prepararPlanAislado(page: Page) {
  const { perfil, headers } = await prepararAlumnoAislado(page);
  const plan = await page.request.post(`${API_URL}/plan-estudio/${perfil.id}`, {
    headers, data: { dias_por_semana: 3, dias_elegidos: ['lunes', 'miercoles', 'viernes'] },
  });
  expect(plan.status()).toBe(201);
  expect((await plan.json()).sesiones.length).toBeGreaterThan(0);
}

export async function loginYEntrarComoSofia(page: Page) {
  await page.goto('/login');
  await page.fill('input[type=email]', CREDENCIALES_PRUEBA.email);
  await page.fill('input[type=password]', CREDENCIALES_PRUEBA.password);
  await page.click('button[type=submit]');
  await page.waitForURL('**/selector-perfil');
  await page.getByText('Sofía').click();
  await expect(page).toHaveURL(/alumno\/inicio/);
}
