import { test, expect, Page } from '@playwright/test';

const CREDENCIALES_ADMIN = {
  email: 'admin.prueba@logos.cl',
  password: 'AdminLogos2026!',
};

async function loginAdmin(page: Page) {
  await page.goto('/admin/login');
  await page.fill('input[type=email]', CREDENCIALES_ADMIN.email);
  await page.fill('input[type=password]', CREDENCIALES_ADMIN.password);
  await page.click('button[type=submit]');
  await expect(page).toHaveURL(/admin\/dashboard/);
}

test.describe('Panel de Administrador', () => {
  test('login incorrecto muestra error, no navega', async ({ page }) => {
    await page.goto('/admin/login');
    await page.fill('input[type=email]', CREDENCIALES_ADMIN.email);
    await page.fill('input[type=password]', 'clave-incorrecta');
    await page.click('button[type=submit]');
    await expect(page.locator('.error')).toBeVisible();
    await expect(page).toHaveURL(/admin\/login/);
  });

  test('sin sesión, /admin/dashboard redirige a /admin/login', async ({ page }) => {
    await page.goto('/admin/dashboard');
    await expect(page).toHaveURL(/admin\/login/);
  });

  test('login correcto entra al dashboard con métricas reales', async ({ page }) => {
    await loginAdmin(page);
    await expect(page.locator('h1')).toContainText('Dashboard');
    await expect(page.locator('.resumen-card').first()).toBeVisible();
  });

  // Nombre/código únicos por corrida — la base de Desarrollo no se resetea entre corridas
  // del suite, así que un nombre fijo colisionaría con filas de una corrida anterior.
  const sufijo = Date.now();
  const nombrePlan = `Plan E2E ${sufijo}`;
  const codigoDescuento = `E2E${sufijo}`;

  test('crear un plan lo deja ver en la tabla', async ({ page }) => {
    await loginAdmin(page);
    await page.goto('/admin/planes');
    await page.fill('input[name=nombre]', nombrePlan);
    await page.fill('input[name=nivelDeAcceso]', 'completo');
    await page.fill('input[name=precioClp]', '12345');
    await page.click('button:has-text("Crear plan")');
    await expect(page.locator('td', { hasText: nombrePlan })).toBeVisible();
  });

  test('desactivar un plan cambia su estado', async ({ page }) => {
    await loginAdmin(page);
    await page.goto('/admin/planes');
    const fila = page.locator('tr', { hasText: nombrePlan });
    await fila.getByRole('button', { name: 'Desactivar' }).click();
    await expect(fila.locator('.chip')).toContainText('Inactivo');
  });

  test('crear un código de descuento lo deja ver como vigente', async ({ page }) => {
    await loginAdmin(page);
    await page.goto('/admin/descuentos');
    await page.fill('input[name=codigo]', codigoDescuento);
    await page.fill('input[name=valor]', '20');
    await page.click('button:has-text("Crear código")');
    const fila = page.locator('tr', { hasText: codigoDescuento });
    await expect(fila.locator('.chip')).toContainText('Vigente');
  });

  test('buscar un alumno de la cuenta de prueba y asignarle cortesía', async ({ page }) => {
    await loginAdmin(page);
    await page.goto('/admin/cortesias');
    await page.fill('input[name=consulta]', 'Sofía');
    await page.click('button:has-text("Buscar")');
    const fila = page.locator('tr', { hasText: 'Sofía' }).first();
    await expect(fila).toBeVisible();
    await fila.getByRole('button', { name: 'Asignar cortesía' }).click();
    await expect(page.locator('.mensaje')).toContainText('Cortesía asignada');
  });

  test('cerrar sesión vuelve al login admin', async ({ page }) => {
    await loginAdmin(page);
    await page.getByText('Cerrar sesión').click();
    await expect(page).toHaveURL(/admin\/login/);
  });
});
