import { test, expect } from '@playwright/test';
import { CREDENCIALES_PRUEBA } from './helpers';

const CREDENCIALES_ADMIN = {
  email: 'admin.prueba@logos.cl',
  password: 'AdminLogos2026!',
};

// Cuenta de profesor única por corrida — la base de Desarrollo no se resetea entre
// corridas del suite, un correo fijo colisionaría con "correo ya registrado".
const sufijo = Date.now();
const emailProfesor = `profesor.e2e.${sufijo}@logos.cl`;
const passwordProfesor = 'ProfesorE2E2026!';
const nombreCurso = `6° básico E2E ${sufijo}`;
const tituloComunicado = `Aviso E2E ${sufijo}`;

test.describe('Rol Profesor', () => {
  test('flujo completo: registro, aprobación, curso, alumno, progreso y comunicado', async ({ page, context }) => {
    // 1. Registro — queda pendiente, el dashboard muestra aviso en vez de la lista de cursos.
    await page.goto('/profesor/login');
    await page.getByText('Crear cuenta').click();
    await page.fill('input[name=nombre]', 'Profesora E2E');
    await page.fill('input[name=email]', emailProfesor);
    await page.fill('input[name=password]', passwordProfesor);
    await page.click('button[type=submit]');
    await expect(page).toHaveURL(/profesor\/dashboard/);
    await expect(page.locator('.aviso-pendiente')).toContainText('revisión');

    // 2. Un administrador aprueba la cuenta desde el panel comercial.
    await page.goto('/admin/login');
    await page.fill('input[type=email]', CREDENCIALES_ADMIN.email);
    await page.fill('input[type=password]', CREDENCIALES_ADMIN.password);
    await page.click('button[type=submit]');
    await expect(page).toHaveURL(/admin\/dashboard/);

    await page.goto('/admin/profesores');
    const filaPendiente = page.locator('tr', { hasText: emailProfesor });
    await expect(filaPendiente).toBeVisible();
    await filaPendiente.getByRole('button', { name: 'Aprobar' }).click();
    await expect(filaPendiente).not.toBeVisible();

    // 3. El profesor vuelve a entrar, ya aprobado puede crear un curso.
    await page.goto('/profesor/login');
    await page.fill('input[name=email]', emailProfesor);
    await page.fill('input[name=password]', passwordProfesor);
    await page.click('button[type=submit]');
    await expect(page).toHaveURL(/profesor\/dashboard/);
    await expect(page.locator('.aviso-pendiente')).toHaveCount(0);

    await page.fill('input[name=nombreCurso]', nombreCurso);
    await page.click('button:has-text("Crear curso")');
    const tarjetaCurso = page.locator('.curso-card', { hasText: nombreCurso });
    await expect(tarjetaCurso).toBeVisible();
    await tarjetaCurso.click();
    await expect(page.locator('h1')).toContainText(nombreCurso);

    // 4. Busca y agrega a Sofía (cuenta de prueba) al curso.
    await page.fill('input[name=consulta]', 'Sofía');
    await page.click('button:has-text("Buscar")');
    const filaResultado = page.locator('tr', { hasText: 'Sofía' }).first();
    await expect(filaResultado).toBeVisible();
    await filaResultado.getByRole('button', { name: 'Agregar' }).click();

    const filaRoster = page.locator('tbody tr', { hasText: 'Sofía' }).first();
    await expect(filaRoster).toBeVisible();

    // 5. Publica un comunicado.
    await page.fill('input[name=tituloComunicado]', tituloComunicado);
    await page.fill('textarea[name=cuerpoComunicado]', 'Recuerden traer sus materiales mañana.');
    await page.click('button:has-text("Publicar comunicado")');

    // 6. Sofía ve su curso y el comunicado en /alumno/inicio.
    const paginaSofia = await context.newPage();
    await paginaSofia.goto('/login');
    await paginaSofia.fill('input[type=email]', CREDENCIALES_PRUEBA.email);
    await paginaSofia.fill('input[type=password]', CREDENCIALES_PRUEBA.password);
    await paginaSofia.click('button[type=submit]');
    await paginaSofia.waitForURL('**/selector-perfil');
    await paginaSofia.getByText('Sofía').click();
    await expect(paginaSofia).toHaveURL(/alumno\/inicio/);

    await expect(paginaSofia.locator('.mi-curso')).toContainText(nombreCurso);
    await expect(paginaSofia.locator('.mi-curso')).toContainText(tituloComunicado);
    await paginaSofia.close();

    // 7. Quitar al alumno del curso lo saca del roster.
    await filaRoster.getByRole('button', { name: 'Quitar' }).click();
    await expect(page.locator('tbody tr', { hasText: 'Sofía' })).toHaveCount(0);
  });

  test('login con credenciales incorrectas muestra error', async ({ page }) => {
    await page.goto('/profesor/login');
    await page.fill('input[name=email]', emailProfesor);
    await page.fill('input[name=password]', 'clave-incorrecta');
    await page.click('button[type=submit]');
    await expect(page.locator('.error')).toBeVisible();
    await expect(page).toHaveURL(/profesor\/login/);
  });

  test('sin sesión, /profesor/dashboard redirige a /profesor/login', async ({ page }) => {
    await page.goto('/profesor/dashboard');
    await expect(page).toHaveURL(/profesor\/login/);
  });
});
