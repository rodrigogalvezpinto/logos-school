import { test, expect } from '@playwright/test';

test.describe('Configuración — separación de datos Alumno / Apoderado', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('la vista de Configuración del Alumno no muestra los datos de la cuenta del Apoderado', async ({ page }) => {
    await page.goto('/alumno/configuracion');
    await expect(page.locator('h1')).toContainText('Configuración');
    await expect(page.getByText('Mi perfil')).toBeVisible();
    // Bug real encontrado probando la app: esta vista mostraba el nombre y correo de la
    // cuenta del Apoderado, confundiendo al alumno sobre de quién es la cuenta.
    await expect(page.getByText('Datos de la cuenta')).toHaveCount(0);
    await expect(page.locator('input[type="email"]')).toHaveCount(0);
  });

  test('la vista de Configuración del Apoderado sí muestra los datos de su cuenta', async ({ page }) => {
    await page.goto('/apoderado/configuracion');
    await expect(page.locator('h1')).toContainText('Configuración');
    await expect(page.getByText('Datos de la cuenta')).toBeVisible();
    await expect(page.getByText('Mi perfil')).toHaveCount(0);
  });
});
