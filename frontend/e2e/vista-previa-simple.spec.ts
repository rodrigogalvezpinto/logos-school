import { test, expect } from '@playwright/test';

test('Capturas simples del flujo principal', async ({ page }) => {
  // 1. Landing
  await page.goto('/');
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: 'screenshots/01-landing.png', fullPage: true });
  console.log('✅ Captura: Landing');

  // 2. Login
  await page.goto('/login');
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: 'screenshots/02-login.png', fullPage: true });
  console.log('✅ Captura: Login');

  // 3. Registro
  await page.goto('/registro');
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: 'screenshots/03-registro.png', fullPage: true });
  console.log('✅ Captura: Registro');

  console.log('\n🎉 Capturas básicas completadas');
});
