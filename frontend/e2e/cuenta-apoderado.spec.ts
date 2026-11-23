import { test, expect } from '@playwright/test';

/** Configuración del apoderado (2026-11-22): cambiar contraseña y eliminar la cuenta. Usa una cuenta nueva propia. */
const EMAIL = `cuenta.${Date.now()}@ejemplo.cl`;

test.describe.serial('Cuenta del apoderado', () => {
  test('cambia la contraseña y luego elimina la cuenta', async ({ page }) => {
    await page.goto('/registro');
    await page.fill('input[name=nombre]', 'Apoderado Cuenta');
    await page.fill('input[name=email]', EMAIL);
    await page.fill('input[name=password]', 'ClaveVieja123');
    await page.click('button[type=submit]');
    await expect(page).toHaveURL(/agregar-alumno/);

    await page.goto('/apoderado/configuracion');
    await page.fill('input[name=passActual]', 'mala-clave');
    await page.fill('input[name=passNueva]', 'ClaveNueva456');
    await page.fill('input[name=passRepetir]', 'ClaveNueva456');
    await page.getByRole('button', { name: 'Cambiar contraseña' }).click();
    await expect(page.getByText('La contraseña actual no es correcta.')).toBeVisible();

    await page.fill('input[name=passActual]', 'ClaveVieja123');
    await page.fill('input[name=passNueva]', 'ClaveNueva456');
    await page.fill('input[name=passRepetir]', 'ClaveNueva456');
    await page.getByRole('button', { name: 'Cambiar contraseña' }).click();
    await expect(page.getByRole('status')).toContainText('Contraseña cambiada');

    // La sesión sigue activa con el token nuevo: eliminar la cuenta.
    await page.getByRole('button', { name: 'Eliminar mi cuenta' }).click();
    await page.fill('input[name=passEliminar]', 'ClaveNueva456');
    await page.getByRole('button', { name: 'Eliminar definitivamente' }).click();
    await expect(page).not.toHaveURL(/configuracion/);

    // Ya no se puede entrar.
    await page.goto('/login');
    await page.fill('input[type=email]', EMAIL);
    await page.fill('input[type=password]', 'ClaveNueva456');
    await page.click('button[type=submit]');
    await expect(page.getByText('Correo o contraseña incorrectos')).toBeVisible();
  });
});
