import { execSync } from 'node:child_process';
import { test, expect, type APIRequestContext, type Browser, type Page } from '@playwright/test';

/** Chip "Atrasada" del Plan de Estudio y su reflejo en la campana de notificaciones, ambos
 * con datos reales — hasta ahora solo tenían cobertura de backend (`test_plan_estudio.py`,
 * `test_notificaciones.py`), nunca se habían verificado en pantalla (P1 del plan de pruebas
 * exhaustivo, planificacion/28-plan-de-pruebas-exhaustivo.md).
 *
 * No hay forma de crear una sesión con `fecha_programada` en el pasado a través de la API
 * (`CrearPlanDeEstudio` siempre usa `reloj.ahora().date()` como fecha de inicio, sin
 * parámetro para forzar otra) — el mismo motivo por el que el test de backend manipula la
 * fila ORM directamente en vez de pasar por la API. Acá se hace el equivalente con `psql`
 * directo contra la base de Desarrollo.
 *
 * Una sola cuenta por navegador en `beforeAll` (no una por caso): igual que en
 * alerta-ritmo.spec.ts, `/auth/registro` está limitado a 5/minuto por IP — 2 casos × 3
 * navegadores ya son 6 registros en la misma corrida y dispara 429 (bug real encontrado así
 * en el primer intento de este archivo). Ambos casos leen la misma sesión atrasada ya
 * sembrada, así que no hay conflicto por compartir la cuenta dentro del archivo. */

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

async function registrarConSesionAtrasada(page: Page): Promise<void> {
  const sufijo = `${Date.now()}${Math.floor(Math.random() * 1000)}`;
  const email = `qa.atrasada.${sufijo}@logos.cl`;
  const rut = rutValido(50_000_000 + (Number(sufijo) % 9_000_000));

  await page.goto('/registro');
  await page.fill('input[name=nombre]', 'QA Atrasada');
  await page.fill('input[name=email]', email);
  await page.fill('input[name=password]', 'Prueba2026!');
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/agregar-alumno/);

  await page.fill('input[name=nombre]', 'Alumno Atrasada');
  await page.fill('input[name=apellidos]', 'Prueba Test');
  await page.fill('input[name=fechaNacimiento]', '2015-03-10');
  await page.fill('input[name=rut]', rut);
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/seleccion-plan/);

  await page.click('button:has-text("Comenzar mis 5 días gratis")');
  await expect(page).toHaveURL(/selector-perfil/);

  await page.getByText('Alumno Atrasada').click();
  await expect(page).toHaveURL(/alumno\/inicio/);
}

async function sembrarSesionAtrasada(page: Page, request: APIRequestContext): Promise<void> {
  const token = await page.evaluate(() => localStorage.getItem('logos_token'));
  const perfilCrudo = await page.evaluate(() => localStorage.getItem('logos_perfil_activo'));
  const perfil = JSON.parse(perfilCrudo!);
  const headers = { Authorization: `Bearer ${token}` };

  const plan = await (
    await request.post(`http://localhost:8000/plan-estudio/${perfil.id}`, {
      headers,
      data: { dias_por_semana: 3, dias_elegidos: ['lunes', 'miercoles', 'viernes'] },
    })
  ).json();
  const primeraSesionId = plan.sesiones[0].id;

  execSync(
    `psql "postgresql://logos_dev:logos_dev_local@localhost:5432/logos_dev" -c "UPDATE sesion_estudio SET fecha_programada = current_date - interval '1 day' WHERE id = ${primeraSesionId}"`,
  );
}

test.describe.configure({ mode: 'serial' });

test.describe('Sesión atrasada del Plan de Estudio — reflejo en pantalla', () => {
  let page: Page;
  let request: APIRequestContext;

  test.beforeAll(async ({ browser }: { browser: Browser }) => {
    const context = await browser.newContext();
    page = await context.newPage();
    request = context.request;
    await registrarConSesionAtrasada(page);
    await sembrarSesionAtrasada(page, request);
  });

  test.afterAll(async () => {
    await page.close();
  });

  test('una sesión con fecha pasada y no cumplida muestra el chip "Atrasada" en pantalla', async () => {
    await page.goto('/alumno/plan-estudio');
    await page.waitForSelector('.chip');

    const chipAtrasado = page.locator('.chip--atrasada').first();
    await expect(chipAtrasado).toBeVisible();
    await expect(chipAtrasado).toContainText('Atrasada');
  });

  test('la misma sesión atrasada aparece como notificación real en la campana', async () => {
    // Mismo hallazgo de fondo que alerta-ritmo/nota-estimada: `test_notificaciones.py`
    // (backend) ya cubre a fondo las 3 fuentes, pero el widget nunca se había verificado en
    // pantalla con datos reales — solo que abre vacío.
    await page.goto('/alumno/inicio');
    // El check-in emocional diario ya se contestó implícitamente si el test anterior
    // navegó por /alumno/inicio antes — por si no, se descarta si aparece.
    const checkin = page.locator('.checkin__opcion').first();
    if (await checkin.isVisible().catch(() => false)) {
      await checkin.click();
    }
    await page.locator('.campana__boton').click();
    await expect(page.locator('.campana__badge')).toHaveText('1');

    const item = page.locator('.campana__lista li').first();
    await expect(item).toBeVisible();
    await expect(item.locator('.campana__titulo')).toContainText('atrasada');
  });
});
