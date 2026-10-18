import { test, expect, type APIRequestContext, type Browser, type Page } from '@playwright/test';

/** Alerta temprana de ritmo de estudio — idea propia (no un hallazgo de la competencia, ver
 * planificacion/27-plan-incorporacion-hallazgos-brincus.md). Necesita una fecha objetivo en
 * el Plan de Estudio — se crea vía API directa (mismo patrón que
 * faltantes-simulacro-parcial.spec.ts) para no depender de la fragilidad de un formulario
 * multi-paso.
 *
 * Los 3 casos comparten UNA sola cuenta recién registrada en beforeAll (no la cuenta
 * compartida "Sofía", y no una cuenta nueva por caso): /auth/registro está limitado a
 * 5/minuto por IP (app/routers/auth.py) — con 3 navegadores × 1 cuenta por caso ya son 9
 * registros en menos de un minuto, lo que dispara 429 y hace fallar el registro mismo (bug
 * real encontrado así). Con una cuenta por navegador alcanza: cada plan-estudio creado
 * reemplaza al anterior, así que los casos "con alerta" y "sin fecha objetivo" no dejan
 * estado permanente entre sí. El caso "revisar todas las guías" sí deja progreso
 * irreversible (/progreso/.../revisada) — por eso corre último, en modo serial. */

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

async function registrarAlumnoFresco(page: Page): Promise<{ token: string; perfilId: number }> {
  const sufijo = `${Date.now()}${Math.floor(Math.random() * 1000)}`;
  const email = `qa.ritmo.${sufijo}@logos.cl`;
  const rut = rutValido(20_000_000 + (Number(sufijo) % 9_000_000));

  await page.goto('/registro');
  await page.fill('input[name=nombre]', 'QA Ritmo');
  await page.fill('input[name=email]', email);
  await page.fill('input[name=password]', 'Prueba2026!');
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/agregar-alumno/);

  await page.fill('input[name=nombre]', 'Alumno Ritmo');
  await page.fill('input[name=apellidos]', 'Prueba Test');
  await page.fill('input[name=fechaNacimiento]', '2015-03-10');
  await page.fill('input[name=rut]', rut);
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/seleccion-plan/);

  await page.click('button:has-text("Comenzar mis 5 días gratis")');
  await expect(page).toHaveURL(/selector-perfil/);

  await page.getByText('Alumno Ritmo').click();
  await expect(page).toHaveURL(/alumno\/inicio/);

  const token = await page.evaluate(() => localStorage.getItem('logos_token'));
  const perfilCrudo = await page.evaluate(() => localStorage.getItem('logos_perfil_activo'));
  const perfil = JSON.parse(perfilCrudo!);
  return { token: token!, perfilId: perfil.id };
}

test.describe.configure({ mode: 'serial' });

test.describe('Alerta de ritmo de estudio', () => {
  let page: Page;
  let request: APIRequestContext;
  let token: string;
  let perfilId: number;

  test.beforeAll(async ({ browser }: { browser: Browser }) => {
    const context = await browser.newContext();
    page = await context.newPage();
    request = context.request;
    ({ token, perfilId } = await registrarAlumnoFresco(page));
  });

  test.afterAll(async () => {
    await page.close();
  });

  test('un plan con fecha objetivo cercana y sin avance muestra la alerta en Mis Notas', async () => {
    const headers = { Authorization: `Bearer ${token}` };
    const fechaCercana = new Date();
    fechaCercana.setDate(fechaCercana.getDate() + 3);
    await request.post(`http://localhost:8000/plan-estudio/${perfilId}`, {
      headers,
      data: {
        dias_por_semana: 3,
        dias_elegidos: ['lunes', 'miercoles', 'viernes'],
        fecha_objetivo: fechaCercana.toISOString().slice(0, 10),
      },
    });

    await page.goto('/alumno/notas');
    await page.waitForSelector('.alerta-ritmo');
    await expect(page.locator('.alerta-ritmo')).not.toHaveClass(/alerta-ritmo--ok/);
    await expect(page.locator('.alerta-ritmo__mensaje')).toContainText('días');
  });

  test('un plan sin fecha objetivo no muestra ninguna alerta', async () => {
    const headers = { Authorization: `Bearer ${token}` };
    await request.post(`http://localhost:8000/plan-estudio/${perfilId}`, {
      headers,
      data: { dias_por_semana: 3, dias_elegidos: ['lunes', 'miercoles', 'viernes'] },
    });

    await page.goto('/alumno/notas');
    await page.waitForSelector('.prediccion'); // otra sección de la misma página sí carga
    await expect(page.locator('.alerta-ritmo')).toHaveCount(0);
  });

  test('revisar todas las guías del plan cambia la alerta a "vas muy bien"', async () => {
    const headers = { Authorization: `Bearer ${token}` };
    const fechaCercana = new Date();
    fechaCercana.setDate(fechaCercana.getDate() + 10);
    const plan = await (
      await request.post(`http://localhost:8000/plan-estudio/${perfilId}`, {
        headers,
        data: {
          dias_por_semana: 3, dias_elegidos: ['lunes', 'miercoles', 'viernes'],
          fecha_objetivo: fechaCercana.toISOString().slice(0, 10),
        },
      })
    ).json();

    const oaIds = new Set<number>();
    for (const sesion of plan.sesiones) for (const oaId of sesion.oa_ids) oaIds.add(oaId);
    for (const oaId of oaIds) {
      await request.post(`http://localhost:8000/progreso/${perfilId}/guias/${oaId}/revisada`, { headers });
    }

    await page.goto('/alumno/notas');
    await page.waitForSelector('.alerta-ritmo');
    await expect(page.locator('.alerta-ritmo')).toHaveClass(/alerta-ritmo--ok/);
    await expect(page.locator('.alerta-ritmo__mensaje')).toContainText('vas muy bien');
  });
});
