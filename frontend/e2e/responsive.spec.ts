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

  async function sinDesbordeHorizontal(page: import('@playwright/test').Page) {
    const anchoDoc = await page.evaluate(() => document.documentElement.scrollWidth);
    const anchoViewport = await page.evaluate(() => window.innerWidth);
    expect(anchoDoc).toBeLessThanOrEqual(anchoViewport + 1);
  }

  test.describe('Páginas nuevas de Fase 1 (ver planificacion/27-plan-incorporacion-hallazgos-brincus.md)', () => {
    test.use({ storageState: 'e2e/.storage-sofia.json' });

    test('Mis Logros no se desborda en móvil', async ({ page }) => {
      await page.goto('/alumno/logros');
      await page.waitForSelector('.resumen__nivel');
      await sinDesbordeHorizontal(page);
    });

    test('Plan y Pagos no se desborda y apila nombre/detalle en pantallas chicas', async ({ page }) => {
      await page.goto('/apoderado/plan');
      await page.waitForSelector('.fila-pago');
      await sinDesbordeHorizontal(page);
      // Bug real encontrado: sin la regla de apilar, el nombre largo del alumno se
      // apretaba contra el detalle del plan en vez de quedar uno debajo del otro.
      const fila = page.locator('.fila-pago').first();
      const flexDirection = await fila.evaluate((el) => getComputedStyle(el).flexDirection);
      expect(flexDirection).toBe('column');
    });

    test('Agregar alumno inline apila los campos en pares en móvil', async ({ page }) => {
      await page.goto('/apoderado/inicio');
      await page.getByRole('button', { name: 'Agregar otro alumno' }).click();
      await page.waitForSelector('.campo-fila');
      await sinDesbordeHorizontal(page);
      const fila = page.locator('.campo-fila').first();
      const flexDirection = await fila.evaluate((el) => getComputedStyle(el).flexDirection);
      expect(flexDirection).toBe('column');
    });

    test('Plan de Estudio en vista Semanal no se desborda en móvil', async ({ page }) => {
      await page.goto('/alumno/plan-estudio');
      await page.waitForSelector('.selector-vista');
      await page.getByRole('button', { name: 'Semanal' }).click();
      await sinDesbordeHorizontal(page);
    });
  });
});
