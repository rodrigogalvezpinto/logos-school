import { test, expect } from '@playwright/test';

/** Página del enlace del correo (/restablecer?token=…), con el backend simulado (2026-11-21). */
test.describe('Restablecer contraseña', () => {
  test('con un enlace válido guarda la contraseña nueva y limpia el token de la barra', async ({ page }) => {
    let cuerpo: unknown;
    await page.route('**/auth/restablecer-password', async (r) => { cuerpo = r.request().postDataJSON(); await r.fulfill({ status: 204 }); });
    await page.goto('/restablecer?token=token-de-prueba-123');
    await expect(page).not.toHaveURL(/token=/);
    await page.fill('input[name=password]', 'ClaveNueva456');
    await page.fill('input[name=repetir]', 'ClaveNueva456');
    await page.getByRole('button', { name: 'Guardar contraseña' }).click();
    await expect(page.getByRole('status')).toContainText('Tu contraseña cambió');
    expect(cuerpo).toEqual({ token: 'token-de-prueba-123', password: 'ClaveNueva456' });
  });

  test('si el enlace venció ofrece pedir uno nuevo', async ({ page }) => {
    await page.route('**/auth/restablecer-password', (r) => r.fulfill({ status: 400, json: { detail: 'vencido' } }));
    await page.goto('/restablecer?token=vencido-0000000');
    await page.fill('input[name=password]', 'ClaveNueva456');
    await page.fill('input[name=repetir]', 'ClaveNueva456');
    await page.getByRole('button', { name: 'Guardar contraseña' }).click();
    await expect(page.getByText('El enlace venció o ya se usó.')).toBeVisible();
    await expect(page.getByRole('link', { name: 'Pedir un enlace nuevo' })).toBeVisible();
  });

  test('las contraseñas deben coincidir', async ({ page }) => {
    await page.goto('/restablecer?token=cualquiera-000000');
    await page.fill('input[name=password]', 'ClaveNueva456');
    await page.fill('input[name=repetir]', 'OtraDistinta');
    await page.getByRole('button', { name: 'Guardar contraseña' }).click();
    await expect(page.getByText('no coinciden')).toBeVisible();
  });
});
