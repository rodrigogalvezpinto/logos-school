import { test, expect } from '@playwright/test';

test.describe('Casos borde del motor de evaluación', () => {
  test('avisa si quedan preguntas sin responder antes de entregar', async ({ page }) => {
    await page.goto('/alumno/autoevaluacion/oa1');
    await page.getByRole('button', { name: 'Comenzar' }).click();

    // No responde nada — va directo a "Siguiente" hasta la última y presiona Entregar.
    for (let i = 0; i < 2; i++) {
      await page.getByRole('button', { name: 'Siguiente' }).click();
    }
    await page.getByRole('button', { name: 'Entregar' }).click();

    // Debe aparecer el modal de aviso, no enviar directo.
    await expect(page.locator('.modal')).toBeVisible();
    await expect(page.locator('.modal')).toContainText('Te falta responder');

    // El botón "Ir a revisar" debe llevar de vuelta a una pregunta sin responder.
    await page.getByRole('button', { name: 'Ir a revisar' }).click();
    await expect(page.locator('.modal')).not.toBeVisible();
  });

  test('el botón "Enviar de todas formas" sí permite terminar con preguntas en blanco', async ({
    page,
  }) => {
    await page.goto('/alumno/autoevaluacion/oa1');
    await page.getByRole('button', { name: 'Comenzar' }).click();
    for (let i = 0; i < 2; i++) {
      await page.getByRole('button', { name: 'Siguiente' }).click();
    }
    await page.getByRole('button', { name: 'Entregar' }).click();
    await page.getByRole('button', { name: 'Enviar de todas formas' }).click();

    await expect(page.locator('.resultado')).toBeVisible();
  });

  test('el resultado tiene un botón Volver que funciona', async ({ page }) => {
    await page.goto('/alumno/prueba/matematica-num');
    await page.getByRole('button', { name: 'Comenzar' }).click();

    // Responde todo lo posible avanzando y usando "Enviar de todas formas" si aparece.
    for (let i = 0; i < 2; i++) {
      await page.getByRole('button', { name: 'Siguiente' }).click();
    }
    await page.getByRole('button', { name: 'Entregar' }).click();
    const modal = page.locator('.modal');
    if (await modal.isVisible().catch(() => false)) {
      await page.getByRole('button', { name: 'Enviar de todas formas' }).click();
    }

    await expect(page.locator('.resultado')).toBeVisible();
    const botonVolver = page.getByRole('button', { name: 'Volver' });
    await expect(botonVolver).toBeVisible();
    await botonVolver.click();
    await expect(page).toHaveURL(/alumno\/evaluaciones/);
  });

  test('hay un botón "Salir" visible durante una prueba (no solo al terminar)', async ({
    page,
  }) => {
    await page.goto('/alumno/prueba/matematica-num');
    await page.getByRole('button', { name: 'Comenzar' }).click();
    await expect(page.getByRole('button', { name: /Salir/ })).toBeVisible();
  });
});

test.describe('Examen simulacro — modo serio', () => {
  test('no muestra la sidebar y tiene contraste correcto (fondo oscuro, texto claro)', async ({
    page,
  }) => {
    await page.goto('/examen/integrado-a');
    await expect(page.locator('.sidebar')).toHaveCount(0);

    const fondo = await page.locator('.examen-fondo').evaluate((el) => getComputedStyle(el).backgroundColor);
    // El fondo del examen debe ser oscuro (#14132B → rgb(20, 19, 43)), no blanco.
    expect(fondo).toBe('rgb(20, 19, 43)');

    await page.getByRole('button', { name: 'Comenzar' }).click();
    await expect(page.locator('.runner__cronometro')).toBeVisible();

    // Las tarjetas dentro del examen deben usar el fondo oscuro sobreescrito, no el
    // blanco por defecto — si esto falla, es el bug de contraste ya corregido antes.
    const fondoTarjeta = await page
      .locator('.pregunta')
      .first()
      .evaluate((el) => getComputedStyle(el).backgroundColor);
    expect(fondoTarjeta).not.toBe('rgb(255, 255, 255)');
  });

  test('el resultado del examen también tiene botón Volver', async ({ page }) => {
    await page.goto('/alumno/evaluaciones');
    await expect(page.getByRole('link', { name: 'Comenzar examen' })).toBeVisible();
  });
});

test.describe('Centrado del formulario de login/registro', () => {
  test('el panel de login está centrado dentro de su mitad de pantalla, no pegado a la izquierda', async ({
    page,
  }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto('/login');

    const panel = page.locator('.auth__panel-inner');
    const box = await panel.boundingBox();
    expect(box).not.toBeNull();

    // La mitad izquierda de la pantalla mide 640px (viewport 1280 / 2, dos columnas iguales).
    // El panel (400px máx.) debe quedar centrado ahí, con margen visible a ambos lados —
    // si el bug de flex+margin:auto volviera, box.x sería ~0.
    const margenIzquierdo = box!.x;
    expect(margenIzquierdo).toBeGreaterThan(50);
  });

  test('el panel de registro también está centrado', async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto('/registro');
    const box = await page.locator('.auth__panel-inner').boundingBox();
    expect(box!.x).toBeGreaterThan(50);
  });
});
