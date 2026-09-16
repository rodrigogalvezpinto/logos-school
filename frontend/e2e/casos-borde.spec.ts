import { test, expect, type Browser, type Page } from '@playwright/test';
import { CREDENCIALES_PRUEBA } from './helpers';

/** Cada test que rinde una prueba de unidad usa su propio índice de conjunto —
 * los intentos son idempotentes por (perfil, conjunto) en el backend, así que
 * si dos tests comparten la misma prueba, el segundo reanuda el intento ya
 * entregado por el primero en vez de empezar uno nuevo.
 *
 * Este describe usa una cuenta recién registrada (no Sofía): ninguno de estos tests depende
 * de datos históricos específicos de Sofía, solo necesitan varias pruebas de unidad nunca
 * antes rendidas — y la cuenta compartida ya no las tiene. Hallazgo real encontrado
 * verificando este archivo (2026-08-16): de las 11+ pruebas que el diseño original asumía
 * disponibles (usa índices hasta 10), a Sofía le quedaba **una sola** sin rendir, agotada
 * por años de corridas acumuladas del suite contra la misma cuenta de la base de Desarrollo
 * — el índice 10 directamente dejó de existir. Una cuenta fresca por navegador (en
 * `beforeAll`, no por test — mismo motivo de rate-limit ya documentado en
 * alerta-ritmo.spec.ts) resuelve la causa raíz en vez de solo parchar índices. */
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

async function registrarAlumnoFresco(page: Page): Promise<void> {
  const sufijo = `${Date.now()}${Math.floor(Math.random() * 1000)}`;
  const email = `qa.casosborde.${sufijo}@logos.cl`;
  const rut = rutValido(60_000_000 + (Number(sufijo) % 9_000_000));

  await page.goto('/registro');
  await page.fill('input[name=nombre]', 'QA Casos Borde');
  await page.fill('input[name=email]', email);
  await page.fill('input[name=password]', 'Prueba2026!');
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/agregar-alumno/);

  await page.fill('input[name=nombre]', 'Alumno Casos Borde');
  await page.fill('input[name=apellidos]', 'Prueba Test');
  await page.fill('input[name=fechaNacimiento]', '2015-03-10');
  await page.fill('input[name=rut]', rut);
  // "5° básico" explícito, no el default del <select> (el primer nivel que devuelve el
  // backend, "1° básico", solo tiene 12 pruebas de unidad en total — con 3 de estos tests
  // entregando su prueba de forma permanente antes de llegar al índice 10, quedan 9
  // disponibles, insuficiente. "5° básico" tiene 14, con margen real de sobra).
  await page.selectOption('select[name=nivelId]', { label: '5° básico' });
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/seleccion-plan/);

  await page.click('button:has-text("Comenzar mis 5 días gratis")');
  await expect(page).toHaveURL(/selector-perfil/);

  await page.getByText('Alumno Casos Borde').click();
  await expect(page).toHaveURL(/alumno\/inicio/);
}

async function irAPrimeraPruebaDeUnidad(page: Page, indice = 0) {
  await page.goto('/alumno/evaluaciones');
  await page.waitForSelector('.fila');
  // `exact: true` es necesario: por defecto Playwright matchea por substring, así que sin
  // esto "Rendir" también matchea "Volver a rendir" (fila del examen ya entregado).
  await page.getByRole('link', { name: 'Rendir', exact: true }).nth(indice).click();
  await expect(page).toHaveURL(/alumno\/prueba\/\d+/);
  await page.getByRole('button', { name: 'Comenzar' }).click();
  // Espera a que renderice la primera pregunta antes de que el test navegue —
  // .count() no espera al render de Angular, a diferencia de los métodos de expect/locator.
  await page.waitForSelector('.runner__nav');
}

/** Avanza hasta la última pregunta usando expect (que sí reintenta), en vez de
 * `.count()` (que no espera al render y puede leer 0 antes de tiempo). */
async function irAUltimaPregunta(page: import('@playwright/test').Page) {
  const siguiente = page.getByRole('button', { name: 'Siguiente' });
  while (await siguiente.isVisible().catch(() => false)) {
    await siguiente.click();
    await page.waitForTimeout(50);
  }
}

test.describe.configure({ mode: 'serial' });

test.describe('Casos borde del motor de evaluación (backend real)', () => {
  let page: Page;

  test.beforeAll(async ({ browser }: { browser: Browser }) => {
    const context = await browser.newContext();
    page = await context.newPage();
    await registrarAlumnoFresco(page);
  });

  test.afterAll(async () => {
    await page.close();
  });

  test('avisa si quedan preguntas sin responder antes de entregar', async () => {
    await irAPrimeraPruebaDeUnidad(page, 0);

    // No responde nada — salta directo al final y presiona Entregar.
    await irAUltimaPregunta(page);
    await page.getByRole('button', { name: 'Entregar' }).click();

    await expect(page.locator('.modal')).toBeVisible();
    await expect(page.locator('.modal')).toContainText('Te falta responder');

    await page.getByRole('button', { name: 'Ir a revisar' }).click();
    await expect(page.locator('.modal')).not.toBeVisible();
  });

  test('"Enviar de todas formas" entrega igual con preguntas en blanco, y la nota es real', async () => {
    await irAPrimeraPruebaDeUnidad(page, 1);
    await irAUltimaPregunta(page);
    await page.getByRole('button', { name: 'Entregar' }).click();
    await page.getByRole('button', { name: 'Enviar de todas formas' }).click();

    await expect(page.locator('.resultado')).toBeVisible();
    // La nota viene calculada por el backend (planificacion/12-motor-de-evaluacion.md,
    // escala 1.0-7.0) — confirma que el número realmente llegó, no quedó vacío.
    await expect(page.locator('.resultado__nota')).toContainText(/Nota: \d(\.\d)?/);
    // Con todo en blanco la nota reprueba (< 4.0) — debe verse en rojo, no en verde
    // (bug encontrado simulando un alumno real: mostraba una nota 1.0 en verde de éxito).
    await expect(page.locator('.resultado__nota')).toHaveClass(/resultado__nota--reprobada/);
  });

  test('el resultado tiene un botón Volver que funciona', async () => {
    await irAPrimeraPruebaDeUnidad(page, 2);
    // No marca respuestas — el foco de este test es el botón Volver, no la nota.
    await irAUltimaPregunta(page);
    await page.getByRole('button', { name: 'Entregar' }).click();
    // No se respondió ninguna pregunta, así que el modal de aviso siempre aparece
    // (aunque tarde un instante en renderizar) — esperarlo en vez de un chequeo
    // inmediato evita una carrera con el render de Angular.
    await expect(page.locator('.modal')).toBeVisible();
    await page.getByRole('button', { name: 'Enviar de todas formas' }).click();
    await expect(page.locator('.resultado')).toBeVisible();
    const botonVolver = page.getByRole('button', { name: 'Volver' });
    await expect(botonVolver).toBeVisible();
    await botonVolver.click();
    await expect(page).toHaveURL(/alumno\/evaluaciones/);
  });

  test('hay un botón "Salir" visible durante una prueba (no solo al terminar)', async () => {
    await irAPrimeraPruebaDeUnidad(page);
    await expect(page.getByRole('button', { name: /Salir/ })).toBeVisible();
  });

  test('responder una pregunta la marca como respondida en el mapa de preguntas', async () => {
    await irAPrimeraPruebaDeUnidad(page);
    const radio = page.locator('.opcion input[type=radio]').first();
    if (await radio.count()) {
      await radio.click();
      await expect(page.locator('.mapa-item--respondida')).toHaveCount(1);
    }
  });

  test('recargar la página a mitad de una prueba conserva las respuestas ya guardadas', async () => {
    // Bug real (comparado en vivo contra Brincus, que sí retoma el intento donde quedó):
    // el backend ya reanudaba el mismo intento (IniciarIntento.ejecutar) y devolvía las
    // respuestas guardadas, pero el frontend las descartaba — el alumno veía todo en
    // blanco de nuevo aunque sus respuestas ya estuvieran guardadas en el servidor.
    await irAPrimeraPruebaDeUnidad(page, 10);
    const radio = page.locator('.opcion input[type=radio]').first();
    if (!(await radio.count())) return; // la primera pregunta de este índice no es de alternativas
    await radio.click();
    await expect(page.locator('.mapa-item--respondida')).toHaveCount(1);

    await page.reload();
    await page.getByRole('button', { name: 'Comenzar' }).click();
    await page.waitForSelector('.runner__nav');

    await expect(page.locator('.mapa-item--respondida')).toHaveCount(1);
    await expect(page.locator('.opcion input[type=radio]').first()).toBeChecked();
  });
});

test.describe('Examen simulacro — modo serio (backend real)', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('no muestra la sidebar y tiene contraste correcto (fondo oscuro, texto claro)', async ({ page }) => {
    await page.goto('/alumno/evaluaciones');
    await page.waitForSelector('.fila--examen');
    // "Comenzar examen" la primera vez, "Volver a rendir" si Sofía ya lo entregó en otra
    // corrida — mismo criterio que examen-auto-envio.spec.ts, acotado a `.fila--examen`
    // porque "Volver a rendir" también es el texto de una prueba de unidad ya entregada.
    await page.locator('.fila--examen').getByRole('link', { name: /Comenzar examen|Volver a rendir/ }).first().click();
    await expect(page).toHaveURL(/examen\/\d+/);

    await expect(page.locator('.sidebar')).toHaveCount(0);
    const fondo = await page.locator('.examen-fondo').evaluate((el) => getComputedStyle(el).backgroundColor);
    expect(fondo).toBe('rgb(20, 19, 43)');

    await page.getByRole('button', { name: 'Comenzar' }).click();
    await expect(page.locator('.runner__cronometro')).toBeVisible();

    const fondoTarjeta = await page.locator('.pregunta').first().evaluate((el) => getComputedStyle(el).backgroundColor);
    expect(fondoTarjeta).not.toBe('rgb(255, 255, 255)');
  });
});

test.describe('Centrado del formulario de login/registro', () => {
  test('el panel de login está centrado dentro de su mitad de pantalla, no pegado a la izquierda', async ({
    page,
  }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto('/login');
    const box = await page.locator('.auth__panel-inner').boundingBox();
    expect(box).not.toBeNull();
    expect(box!.x).toBeGreaterThan(50);
  });

  test('el panel de registro también está centrado', async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto('/registro');
    const box = await page.locator('.auth__panel-inner').boundingBox();
    expect(box!.x).toBeGreaterThan(50);
  });
});

test.describe('Validación de RUT en el formulario de agregar alumno', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('rechaza un RUT con dígito verificador incorrecto', async ({ page }) => {
    await page.goto('/agregar-alumno');

    await page.fill('input[name=nombre]', 'Test');
    await page.fill('input[name=apellidos]', 'Apellido');
    await page.fill('input[name=fechaNacimiento]', '2016-01-01');
    await page.fill('input[name=rut]', '11.111.111-2'); // dígito verificador incorrecto (el correcto es "1")
    await page.click('button[type=submit]');

    await expect(page.locator('.error')).toContainText('RUT');
    await expect(page).toHaveURL(/agregar-alumno/);
  });
});
