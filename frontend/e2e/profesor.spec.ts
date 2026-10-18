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
    // El <select> de nivel no tiene garantía de traer "4° básico" preseleccionado — el
    // orden que devuelve el backend no sigue el orden curricular (mismo bug de fondo que
    // Nivel.orden en Plan de Estudio). Se elige explícito para que coincida con el nivel
    // real de Sofía (bug de test real encontrado: sin esto, "Agregar" fallaba con 400
    // "nivel distinto" de forma intermitente según qué nivel quedara primero en la lista).
    await page.selectOption('select[name=nivelId]', { label: '4° básico' });
    await page.click('button:has-text("Crear curso")');
    const tarjetaCurso = page.locator('.curso-card', { hasText: nombreCurso });
    await expect(tarjetaCurso).toBeVisible();
    await tarjetaCurso.click();
    await expect(page.locator('h1')).toContainText(nombreCurso);

    // 4. Busca y agrega a Sofía (cuenta de prueba) al curso.
    await page.fill('input[name=consulta]', 'Sofía');
    await page.click('button:has-text("Buscar")');
    const filaResultado = page.locator('.tabla-resultados-busqueda tbody tr', { hasText: 'Sofía' }).first();
    await expect(filaResultado).toBeVisible();
    await filaResultado.getByRole('button', { name: 'Agregar' }).click();

    // Distinto de `filaResultado`: la tabla de resultados de búsqueda y la del roster
    // coexisten en el DOM y ambas contienen "Sofía" — sin distinguirlas, esta
    // aserción podía pasar en falso con la fila de resultados aunque el POST de
    // agregar hubiese fallado (bug real de test encontrado al investigar un fallo
    // intermitente de este spec).
    const filaRoster = page.locator('.tabla-roster tbody tr', { hasText: 'Sofía' }).first();
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
    await expect(page.locator('.tabla-roster tbody tr', { hasText: 'Sofía' })).toHaveCount(0);
  });

  test('no se puede agregar a Sofía a un curso de un nivel distinto al suyo', async ({ page }) => {
    const emailProfesor2 = `profesor.e2e.nivel.${sufijo}@logos.cl`;

    await page.goto('/profesor/login');
    await page.getByText('Crear cuenta').click();
    await page.fill('input[name=nombre]', 'Profesora Nivel E2E');
    await page.fill('input[name=email]', emailProfesor2);
    await page.fill('input[name=password]', passwordProfesor);
    await page.click('button[type=submit]');
    await expect(page).toHaveURL(/profesor\/dashboard/);

    await page.goto('/admin/login');
    await page.fill('input[type=email]', CREDENCIALES_ADMIN.email);
    await page.fill('input[type=password]', CREDENCIALES_ADMIN.password);
    await page.click('button[type=submit]');
    await expect(page).toHaveURL(/admin\/dashboard/);
    await page.goto('/admin/profesores');
    await page.locator('tr', { hasText: emailProfesor2 }).getByRole('button', { name: 'Aprobar' }).click();

    await page.goto('/profesor/login');
    await page.fill('input[name=email]', emailProfesor2);
    await page.fill('input[name=password]', passwordProfesor);
    await page.click('button[type=submit]');
    await expect(page).toHaveURL(/profesor\/dashboard/);

    // Elige explícitamente un nivel que NO es el de Sofía (4° básico, la cuenta de
    // prueba) — cualquier otro nivel de la lista sirve para probar el bloqueo.
    const selectNivel = page.locator('select[name=nivelId]');
    const opciones = await selectNivel.locator('option').allTextContents();
    const otroNivel = opciones.find((o) => !o.includes('4° básico'));
    if (otroNivel) await selectNivel.selectOption({ label: otroNivel });

    const nombreCursoOtroNivel = `Otro nivel E2E ${sufijo}`;
    await page.fill('input[name=nombreCurso]', nombreCursoOtroNivel);
    await page.click('button:has-text("Crear curso")');
    await page.locator('.curso-card', { hasText: nombreCursoOtroNivel }).click();

    await page.fill('input[name=consulta]', 'Sofía');
    await page.click('button:has-text("Buscar")');
    await page.locator('tr', { hasText: 'Sofía' }).first().getByRole('button', { name: 'Agregar' }).click();

    await expect(page.locator('.aviso-error')).toContainText('nivel distinto');
    // El roster (primera tabla, antes de "Agregar alumno") debe seguir vacío — la
    // tabla de resultados de búsqueda (segunda tabla) sí sigue mostrando a Sofía,
    // eso es esperado, el usuario puede reintentar la búsqueda.
    await expect(page.locator('.tabla-envoltorio').first().locator('tbody tr', { hasText: 'Sofía' })).toHaveCount(0);
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
