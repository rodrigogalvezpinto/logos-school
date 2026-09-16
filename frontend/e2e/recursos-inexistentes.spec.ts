import { test, expect } from '@playwright/test';
import { capturarErroresConsola } from './helpers';

/** Qué ve el alumno cuando navega a un OA/asignatura/nivel que no existe — hasta ahora solo
 * se verificaba el código HTTP en el backend, nunca la experiencia en pantalla (P2 del plan
 * de pruebas exhaustivo, planificacion/28-plan-de-pruebas-exhaustivo.md).
 *
 * Verificado en el código backend (`app/routers/contenido.py`, `app/routers/evaluaciones.py`)
 * antes de escribir estos casos: `GET /objetivos/{oa_id}` y `GET /autoevaluacion/{oa_id}` dan
 * 404 real si no existe (esperado — un "Failed to load resource: 404" queda en la consola
 * por ese request deliberadamente inválido, se filtra de la aserción de errores); en cambio
 * `listar_asignaturas`/`listar_objetivos` (para un nivel/asignatura inexistente) devuelven
 * 200 con lista vacía — no hay un "nivel no encontrado" a nivel HTTP.
 *
 * Bug real encontrado escribiendo este archivo: `estudiar-oa.ts` llamaba
 * `marcarGuiaRevisada(perfil.id, oaId)` sin condicionar a que la guía hubiese cargado — con
 * un `oa_id` inexistente, el INSERT violaba la FK de `progreso_oa.oa_id` en Postgres,
 * produciendo un 500 sin manejar que el navegador reportaba como error de CORS (enmascarado,
 * porque el `.subscribe()` no tenía manejador de error). Corregido moviendo esas llamadas
 * dentro del callback de éxito de `obtenerObjetivo`. */

function esRuidoEsperado(mensaje: string): boolean {
  return mensaje.includes('404') && (mensaje.includes('999999') || mensaje.includes('Not Found'));
}

test.describe('Recursos de contenido inexistentes', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('un OA inexistente muestra un mensaje de error claro, no una pantalla rota', async ({ page }) => {
    const errores = capturarErroresConsola(page);
    await page.goto('/alumno/estudiar/999999');
    await expect(page.locator('.error-carga')).toBeVisible();
    await expect(page.locator('.error-carga')).toContainText('No se pudo cargar la guía');
    expect(errores.filter((e) => !esRuidoEsperado(e))).toEqual([]);
  });

  test('una autoevaluación de un OA inexistente muestra un mensaje de error claro', async ({ page }) => {
    const errores = capturarErroresConsola(page);
    await page.goto('/alumno/autoevaluacion/999999');
    await expect(page.locator('.error-carga')).toBeVisible();
    await expect(page.locator('.error-carga')).toContainText('No se pudo cargar la práctica');
    expect(errores.filter((e) => !esRuidoEsperado(e))).toEqual([]);
  });

  test('una asignatura inexistente muestra "0 OA" en vez de reventar', async ({ page }) => {
    const errores = capturarErroresConsola(page);
    await page.goto('/alumno/asignaturas/999999');
    await expect(page.locator('h1')).toBeVisible();
    await expect(page.locator('p').filter({ hasText: '0 OA en esta asignatura' })).toBeVisible();
    expect(errores).toEqual([]); // acá el backend no da 404 — no debería haber ningún ruido
  });
});

// Nota: no existe una ruta de frontend parametrizada por `nivel_id` que el alumno pueda
// navegar directamente (el nivel se fija al registrarse, no aparece en la URL) — el caso
// "nivel inexistente" del plan de pruebas ya queda cubierto por el comportamiento verificado
// arriba de `listar_asignaturas`/`listar_objetivos` (200 + lista vacía, mismo repositorio
// que usa `GET /niveles/{nivel_id}/asignaturas`), no amerita un caso de Playwright aparte.
