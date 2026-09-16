import { test, expect } from '@playwright/test';

/** Auto-envío del examen simulacro al agotarse el tiempo — hasta ahora sin cobertura (P2 del
 * plan de pruebas exhaustivo, planificacion/28-plan-de-pruebas-exhaustivo.md): el cronómetro
 * de `evaluacion-runner.ts` llama `confirmarEnvio()` en cuanto `tiempoRestanteSeg() === 0`
 * (sin excepción de "quedan preguntas sin responder", a diferencia del envío manual). Se usa
 * `page.clock` para saltar la duración completa del examen sin esperar minutos reales.
 *
 * Reutiliza la cuenta compartida "Sofía": entregar un intento es idempotente por
 * (perfil, conjunto_evaluacion) — un segundo "entregar" sobre el mismo intento ya entregado
 * no recalcula ni sobreescribe nada (ver `IntentoEvaluacion.entregar`), así que correr este
 * test varias veces contra el mismo examen de Sofía no contamina otros tests (mismo patrón ya
 * usado en casos-borde.spec.ts para el modo examen). */

test.describe('Auto-envío del examen al agotarse el tiempo', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('el examen se entrega solo cuando el cronómetro llega a 00:00, sin que el alumno haga nada', async ({ page }) => {
    await page.clock.install();

    await page.goto('/alumno/evaluaciones');
    await page.waitForSelector('.fila--examen');
    // "Comenzar examen" la primera vez, "Volver a rendir" si Sofía ya entregó ese examen en
    // una corrida anterior de este mismo test — ambos inician un intento nuevo por igual
    // (`buscar_activo` en el backend solo reutiliza intentos NO entregados). Se busca el
    // link DENTRO de `.fila--examen`: "Volver a rendir" también es el texto de una prueba de
    // unidad ya entregada, así que un `getByRole` sin acotar podía matchear la fila
    // equivocada (bug real de test encontrado así — terminó navegando a /alumno/prueba/...).
    await page.locator('.fila--examen').getByRole('link', { name: /Comenzar examen|Volver a rendir/ }).first().click();
    await expect(page).toHaveURL(/examen\/\d+/);

    await page.getByRole('button', { name: 'Comenzar' }).click();
    await expect(page.locator('.runner__cronometro')).toBeVisible();

    // No se responde ninguna pregunta a propósito — el auto-envío debe ocurrir igual, sin
    // el aviso de "quedan preguntas sin responder" que sí aparece en el envío manual.
    await page.clock.fastForward('02:00:00'); // cubre cualquier duración real (máx. 90 min)

    await expect(page.locator('.resultado')).toBeVisible({ timeout: 10_000 });
    await expect(page.locator('.resultado__nota')).toBeVisible();
    // El auto-envío por tiempo agotado llama confirmarEnvio() directo (línea 371 de
    // evaluacion-runner.ts), no intentarEnviar() — nunca debería pasar por el modal de
    // "quedan preguntas sin responder" que sí existe para el botón "Entregar" manual.
    await expect(page.locator('.modal-fondo')).toHaveCount(0);
  });
});
