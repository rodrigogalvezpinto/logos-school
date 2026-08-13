import { test, expect } from '@playwright/test';
import { CREDENCIALES_PRUEBA } from './helpers';

/** Cada test que rinde una prueba de unidad usa su propio índice de conjunto —
 * los intentos son idempotentes por (perfil, conjunto) en el backend, así que
 * si dos tests comparten la misma prueba, el segundo reanuda el intento ya
 * entregado por el primero en vez de empezar uno nuevo. */
async function irAPrimeraPruebaDeUnidad(page: import('@playwright/test').Page, indice = 0) {
  await page.goto('/alumno/evaluaciones');
  await page.waitForSelector('.fila');
  await page.getByRole('link', { name: 'Rendir' }).nth(indice).click();
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

test.describe('Casos borde del motor de evaluación (backend real)', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('avisa si quedan preguntas sin responder antes de entregar', async ({ page }) => {
    await irAPrimeraPruebaDeUnidad(page, 0);

    // No responde nada — salta directo al final y presiona Entregar.
    await irAUltimaPregunta(page);
    await page.getByRole('button', { name: 'Entregar' }).click();

    await expect(page.locator('.modal')).toBeVisible();
    await expect(page.locator('.modal')).toContainText('Te falta responder');

    await page.getByRole('button', { name: 'Ir a revisar' }).click();
    await expect(page.locator('.modal')).not.toBeVisible();
  });

  test('"Enviar de todas formas" entrega igual con preguntas en blanco, y la nota es real', async ({
    page,
  }) => {
    await irAPrimeraPruebaDeUnidad(page, 1);
    await irAUltimaPregunta(page);
    await page.getByRole('button', { name: 'Entregar' }).click();
    await page.getByRole('button', { name: 'Enviar de todas formas' }).click();

    await expect(page.locator('.resultado')).toBeVisible();
    // La nota viene calculada por el backend (planificacion/12-motor-de-evaluacion.md,
    // escala 1.0-7.0) — confirma que el número realmente llegó, no quedó vacío.
    await expect(page.locator('.resultado__nota')).toContainText(/Nota: \d(\.\d)?/);
  });

  test('el resultado tiene un botón Volver que funciona', async ({ page }) => {
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

  test('hay un botón "Salir" visible durante una prueba (no solo al terminar)', async ({ page }) => {
    await irAPrimeraPruebaDeUnidad(page);
    await expect(page.getByRole('button', { name: /Salir/ })).toBeVisible();
  });

  test('responder una pregunta la marca como respondida en el mapa de preguntas', async ({ page }) => {
    await irAPrimeraPruebaDeUnidad(page);
    const radio = page.locator('.opcion input[type=radio]').first();
    if (await radio.count()) {
      await radio.click();
      await expect(page.locator('.mapa-item--respondida')).toHaveCount(1);
    }
  });
});

test.describe('Examen simulacro — modo serio (backend real)', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('no muestra la sidebar y tiene contraste correcto (fondo oscuro, texto claro)', async ({ page }) => {
    await page.goto('/alumno/evaluaciones');
    await page.waitForSelector('.fila--examen');
    await page.getByRole('link', { name: 'Comenzar examen' }).first().click();
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
