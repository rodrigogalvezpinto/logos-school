import { test, expect, devices } from '@playwright/test';
import { CREDENCIALES_PRUEBA } from './helpers';

const CREDENCIALES_ADMIN = {
  email: 'admin.prueba@logos.cl',
  password: 'AdminLogos2026!',
};

test.describe('Responsive / móvil', () => {
  test.use({ viewport: devices['iPhone 13'].viewport });

  test('landing no se desborda horizontalmente y el CTA es visible', async ({ page }) => {
    await page.goto('/');
    const anchoDoc = await page.evaluate(() => document.documentElement.scrollWidth);
    const anchoViewport = await page.evaluate(() => window.innerWidth);
    expect(anchoDoc).toBeLessThanOrEqual(anchoViewport + 1);
    await expect(page.locator('.landing__nav-links .btn--primario')).toBeVisible();
  });

  test('el sidebar del Alumno está oculto por defecto y se abre con el botón hamburguesa', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type=email]', CREDENCIALES_PRUEBA.email);
    await page.fill('input[type=password]', CREDENCIALES_PRUEBA.password);
    await page.click('button[type=submit]');
    await page.waitForURL('**/selector-perfil');
    await page.getByText('Sofía').click();
    await expect(page).toHaveURL(/alumno\/inicio/);

    const anchoDoc = await page.evaluate(() => document.documentElement.scrollWidth);
    const anchoViewport = await page.evaluate(() => window.innerWidth);
    expect(anchoDoc).toBeLessThanOrEqual(anchoViewport + 1);

    await expect(page.getByRole('link', { name: 'Mis Asignaturas' })).not.toBeVisible();
    await page.getByRole('button', { name: 'Abrir menú' }).click();
    await expect(page.getByRole('link', { name: 'Mis Asignaturas' })).toBeVisible();

    // Navegar cierra el menú automáticamente.
    await page.getByRole('link', { name: 'Mis Asignaturas' }).click();
    await expect(page).toHaveURL(/alumno\/asignaturas/);
    await expect(page.getByRole('link', { name: 'Mis Asignaturas' })).not.toBeVisible();
  });

  test('el sidebar del Admin también colapsa en móvil', async ({ page }) => {
    await page.goto('/admin/login');
    await page.fill('input[type=email]', CREDENCIALES_ADMIN.email);
    await page.fill('input[type=password]', CREDENCIALES_ADMIN.password);
    await page.click('button[type=submit]');
    await expect(page).toHaveURL(/admin\/dashboard/);

    const anchoDoc = await page.evaluate(() => document.documentElement.scrollWidth);
    const anchoViewport = await page.evaluate(() => window.innerWidth);
    expect(anchoDoc).toBeLessThanOrEqual(anchoViewport + 1);

    await expect(page.getByRole('link', { name: 'Planes' })).not.toBeVisible();
    await page.getByRole('button', { name: 'Abrir menú' }).click();
    await expect(page.getByRole('link', { name: 'Planes' })).toBeVisible();
  });
});
