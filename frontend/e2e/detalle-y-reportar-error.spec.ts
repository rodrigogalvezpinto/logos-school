import { test, expect } from '@playwright/test';

/** Fase 1, ítem 2.1 del plan de incorporación de hallazgos de Brincus — resumen final
 * con detalle por pregunta y "Reportar error" a nivel de pregunta individual. Ver
 * planificacion/27-plan-incorporacion-hallazgos-brincus.md. Usa índices de "Rendir"
 * distintos a casos-borde.spec.ts (0,1,2) e historial.spec.ts (3) para no reanudar un
 * intento ya entregado por esos tests. */

async function irAPruebaDeUnidad(page: import('@playwright/test').Page, indice: number) {
  await page.goto('/alumno/evaluaciones');
  await page.waitForSelector('.fila');
  await page.getByRole('link', { name: 'Rendir' }).nth(indice).click();
  await expect(page).toHaveURL(/alumno\/prueba\/\d+/);
  await page.getByRole('button', { name: 'Comenzar' }).click();
  await page.waitForSelector('.runner__nav');
}

async function irAUltimaPregunta(page: import('@playwright/test').Page) {
  const siguiente = page.getByRole('button', { name: 'Siguiente' });
  while (await siguiente.isVisible().catch(() => false)) {
    await siguiente.click();
    await page.waitForTimeout(50);
  }
}

test.describe('Resumen final con detalle por pregunta (Fase 1, ítem 2.1)', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('el "Finalizar intento" persistente funciona desde cualquier pregunta, no solo la última', async ({
    page,
  }) => {
    await irAPruebaDeUnidad(page, 4);
    // Está en la primera pregunta, no en la última — el botón persistente debe estar visible igual.
    await expect(page.getByRole('button', { name: 'Finalizar intento' })).toBeVisible();
    await page.getByRole('button', { name: 'Finalizar intento' }).click();
    // Sin responder nada, debe salir el mismo aviso de preguntas faltantes.
    await expect(page.locator('.modal')).toBeVisible();
    await page.getByRole('button', { name: 'Enviar de todas formas' }).click();
    await expect(page.locator('.resultado')).toBeVisible();
  });

  test('el resultado muestra una fila por pregunta con Resultado y opción de Revisión', async ({ page }) => {
    await irAPruebaDeUnidad(page, 5);

    // Responde la primera pregunta si es de alternativas, para tener al menos un dato real.
    const radio = page.locator('.opcion input[type=radio]').first();
    if (await radio.count()) await radio.click();

    await irAUltimaPregunta(page);
    await page.getByRole('button', { name: 'Entregar' }).click();
    // Puede aparecer el aviso de preguntas incompletas o entregar directo — espera a
    // que suceda cualquiera de las dos cosas en vez de un chequeo inmediato sin esperar
    // (mismo patrón de carrera con el render de Angular que documenta casos-borde.spec.ts).
    await expect(page.locator('.modal, .resultado')).toBeVisible();
    if (await page.locator('.modal').isVisible().catch(() => false)) {
      await page.getByRole('button', { name: 'Enviar de todas formas' }).click();
    }

    await expect(page.locator('.resultado')).toBeVisible();
    await expect(page.locator('.resultado__detalle')).toBeVisible();
    const filas = page.locator('.resultado__detalle tbody tr').filter({ hasText: /Revisar/ });
    expect(await filas.count()).toBeGreaterThan(0);

    // Abre la revisión de la primera pregunta — debe mostrar el enunciado y la respuesta correcta.
    await page.getByRole('button', { name: 'Revisar' }).first().click();
    await expect(page.locator('.resultado__enunciado').first()).toBeVisible();
  });
});

test.describe('Reportar error de una pregunta (Fase 1, ítems 2.1 y 2.6)', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('reportar un error en la pregunta actual muestra confirmación', async ({ page }) => {
    await irAPruebaDeUnidad(page, 6);

    await page.getByRole('button', { name: /Reportar error en esta pregunta/ }).click();
    await page.fill('textarea[placeholder*="pregunta"]', 'Esta pregunta tiene un error de tipeo.');
    await page.getByRole('button', { name: 'Enviar reporte' }).click();

    await expect(page.getByText('Gracias, revisaremos esta pregunta')).toBeVisible();
  });

  test('se puede reportar sin escribir comentario (reporte de un clic)', async ({ page }) => {
    await irAPruebaDeUnidad(page, 7);

    await page.getByRole('button', { name: /Reportar error en esta pregunta/ }).click();
    await page.getByRole('button', { name: 'Enviar reporte' }).click();

    await expect(page.getByText('Gracias, revisaremos esta pregunta')).toBeVisible();
  });

  test('cancelar el formulario de reporte no envía nada', async ({ page }) => {
    await irAPruebaDeUnidad(page, 8);

    await page.getByRole('button', { name: /Reportar error en esta pregunta/ }).click();
    await page.getByRole('button', { name: 'Cancelar' }).click();

    await expect(page.getByRole('button', { name: /Reportar error en esta pregunta/ })).toBeVisible();
    await expect(page.getByText('Gracias, revisaremos esta pregunta')).not.toBeVisible();
  });
});
