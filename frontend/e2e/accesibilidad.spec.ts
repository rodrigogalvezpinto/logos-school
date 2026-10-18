import { test, expect } from '@playwright/test';
import { AxeBuilder } from '@axe-core/playwright';
import { CREDENCIALES_PRUEBA } from './helpers';

const CREDENCIALES_ADMIN = {
  email: 'admin.prueba@logos.cl',
  password: 'AdminLogos2026!',
};

/** Auditoría automatizada de accesibilidad (axe-core) sobre las páginas públicas y el panel
 * del Alumno — ver planificacion/22-analisis-de-brechas.md. Solo falla ante violaciones
 * "serias"/"críticas" nuevas; no persigue cada regla "moderada" hasta el final (ver nota de
 * `.fila-historial--bloqueada` en notas.ts: WCAG exime a componentes de UI inactivos del
 * contraste mínimo, y esa tarjeta representa una evaluación aún bloqueada). */
async function sinViolacionesGraves(page: import('@playwright/test').Page) {
  const resultados = await new AxeBuilder({ page })
    // Ver nota de archivo: tarjeta de evaluación bloqueada, exenta a propósito. Mismo
    // criterio para una insignia de logro todavía no conseguida (logros.ts).
    .exclude('.fila-historial--bloqueada')
    .exclude('.logro-card--bloqueado')
    .analyze();
  const graves = resultados.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical');
  expect(graves, JSON.stringify(graves, null, 2)).toEqual([]);
}

test.describe('Accesibilidad (axe-core)', () => {
  test('landing sin violaciones graves', async ({ page }) => {
    await page.goto('/');
    await sinViolacionesGraves(page);
  });

  test('login sin violaciones graves', async ({ page }) => {
    await page.goto('/login');
    await sinViolacionesGraves(page);
  });

  test('registro sin violaciones graves', async ({ page }) => {
    await page.goto('/registro');
    await sinViolacionesGraves(page);
  });

  test('selector de perfil (con degradado de marca) sin violaciones graves', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type=email]', CREDENCIALES_PRUEBA.email);
    await page.fill('input[type=password]', CREDENCIALES_PRUEBA.password);
    await page.click('button[type=submit]');
    await page.waitForURL('**/selector-perfil');
    await sinViolacionesGraves(page);
  });

  test('panel del Alumno sin violaciones graves', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type=email]', CREDENCIALES_PRUEBA.email);
    await page.fill('input[type=password]', CREDENCIALES_PRUEBA.password);
    await page.click('button[type=submit]');
    await page.waitForURL('**/selector-perfil');
    await page.getByText('Sofía').click();
    await expect(page).toHaveURL(/alumno\/inicio/);
    await sinViolacionesGraves(page);
  });

  test.describe('Páginas con identidad visual por asignatura', () => {
    test.use({ storageState: 'e2e/.storage-sofia.json' });

    test('Mis Asignaturas sin violaciones graves', async ({ page }) => {
      await page.goto('/alumno/asignaturas');
      await page.waitForSelector('.asignatura-card');
      await sinViolacionesGraves(page);
    });

    test('Pruebas y Exámenes sin violaciones graves', async ({ page }) => {
      await page.goto('/alumno/evaluaciones');
      await page.waitForSelector('.conjunto-card');
      await sinViolacionesGraves(page);
    });

    test('Mis Logros sin violaciones graves', async ({ page }) => {
      await page.goto('/alumno/logros');
      await page.waitForSelector('.resumen__nivel');
      await sinViolacionesGraves(page);
    });

    test('Mis Notas sin violaciones graves', async ({ page }) => {
      await page.goto('/alumno/notas');
      await page.waitForSelector('h1');
      await sinViolacionesGraves(page);
    });

    test('Plan de Estudio sin violaciones graves', async ({ page }) => {
      await page.goto('/alumno/plan-estudio');
      await page.waitForSelector('h1');
      await sinViolacionesGraves(page);
    });

    test('Plan Lector sin violaciones graves', async ({ page }) => {
      await page.goto('/alumno/plan-lector');
      await page.waitForSelector('h1');
      await sinViolacionesGraves(page);
    });

    test('Útiles Escolares sin violaciones graves', async ({ page }) => {
      await page.goto('/alumno/utiles-escolares');
      await page.waitForSelector('h1');
      await sinViolacionesGraves(page);
    });

    test('Configuración (con el buzón de sugerencias) sin violaciones graves', async ({ page }) => {
      await page.goto('/alumno/configuracion');
      await page.waitForSelector('h1');
      await sinViolacionesGraves(page);
    });

    test('Estudiar OA (con calificación por estrellas) sin violaciones graves', async ({ page }) => {
      await page.goto('/alumno/estudiar/1');
      await page.waitForSelector('h1');
      await sinViolacionesGraves(page);
    });
  });

  test('Dashboard de Admin sin violaciones graves', async ({ page }) => {
    await page.goto('/admin/login');
    await page.fill('input[type=email]', CREDENCIALES_ADMIN.email);
    await page.fill('input[type=password]', CREDENCIALES_ADMIN.password);
    await page.click('button[type=submit]');
    await expect(page).toHaveURL(/admin\/dashboard/);
    await sinViolacionesGraves(page);
  });

  // P2 del plan de pruebas exhaustivo (planificacion/28-plan-de-pruebas-exhaustivo.md): el
  // árbol de Profesor (dashboard, detalle de curso) quedó fuera de la auditoría original —
  // sí estaban cubiertas landing/login/registro/selector-perfil/alumno/admin, pero no Profesor.
  test.describe('Rol Profesor', () => {
    test('Login/registro de Profesor sin violaciones graves', async ({ page }) => {
      await page.goto('/profesor/login');
      await sinViolacionesGraves(page);
    });

    test('Dashboard y detalle de curso de Profesor sin violaciones graves', async ({ page }) => {
      const sufijo = Date.now();
      const emailProfesor = `profesor.a11y.${sufijo}@logos.cl`;
      const passwordProfesor = 'ProfesorA11y2026!';

      await page.goto('/profesor/login');
      await page.getByText('Crear cuenta').click();
      await page.fill('input[name=nombre]', 'Profesora A11y');
      await page.fill('input[name=email]', emailProfesor);
      await page.fill('input[name=password]', passwordProfesor);
      await page.click('button[type=submit]');
      await expect(page).toHaveURL(/profesor\/dashboard/);
      await sinViolacionesGraves(page); // dashboard con aviso "pendiente de aprobación"

      await page.goto('/admin/login');
      await page.fill('input[type=email]', CREDENCIALES_ADMIN.email);
      await page.fill('input[type=password]', CREDENCIALES_ADMIN.password);
      await page.click('button[type=submit]');
      await expect(page).toHaveURL(/admin\/dashboard/);
      await page.goto('/admin/profesores');
      const filaPendiente = page.locator('tr', { hasText: emailProfesor });
      await filaPendiente.getByRole('button', { name: 'Aprobar' }).click();
      await expect(filaPendiente).not.toBeVisible();

      await page.goto('/profesor/login');
      await page.fill('input[name=email]', emailProfesor);
      await page.fill('input[name=password]', passwordProfesor);
      await page.click('button[type=submit]');
      await expect(page).toHaveURL(/profesor\/dashboard/);
      await expect(page.locator('.aviso-pendiente')).toHaveCount(0);
      await sinViolacionesGraves(page); // dashboard ya aprobado, con el formulario de crear curso

      await page.fill('input[name=nombreCurso]', `Curso A11y ${sufijo}`);
      await page.selectOption('select[name=nivelId]', { label: '4° básico' });
      await page.click('button:has-text("Crear curso")');
      await page.locator('.curso-card', { hasText: `Curso A11y ${sufijo}` }).click();
      await expect(page.locator('h1')).toContainText(`Curso A11y ${sufijo}`);
      await sinViolacionesGraves(page); // detalle de curso con roster/búsqueda/comunicados
    });
  });
});
