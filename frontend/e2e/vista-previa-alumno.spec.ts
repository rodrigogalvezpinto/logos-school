import { test, expect } from '@playwright/test';

test('Capturas del flujo completo del alumno', async ({ page }) => {
  // Login directo con credenciales de prueba (asumiendo que existen)
  await page.goto('/login');
  await page.fill('input[type=email]', 'apoderado@prueba.com');
  await page.fill('input[type=password]', 'prueba123');
  await page.click('button[type=submit]');

  // Esperar a que llegue a selector-perfil o directamente al panel
  await page.waitForTimeout(2000);
  const currentUrl = page.url();

  if (currentUrl.includes('/selector-perfil')) {
    await page.screenshot({ path: 'screenshots/04-selector-perfil.png', fullPage: true });
    console.log('✅ Captura: Selector de perfil');

    // Elegir primer perfil
    await page.locator('.tarjeta-perfil').first().click();
    await page.waitForTimeout(1000);
  }

  // Capturar panel del alumno
  await page.screenshot({ path: 'screenshots/05-panel-alumno.png', fullPage: true });
  console.log('✅ Captura: Panel del alumno');

  // Mis Asignaturas
  await page.goto('/alumno/asignaturas');
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: 'screenshots/06-mis-asignaturas.png', fullPage: true });
  console.log('✅ Captura: Mis Asignaturas');

  // Pruebas y Exámenes
  await page.goto('/alumno/evaluaciones');
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: 'screenshots/07-pruebas-examenes.png', fullPage: true });
  console.log('✅ Captura: Pruebas y Exámenes');

  // Mis Notas
  await page.goto('/alumno/notas');
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: 'screenshots/08-mis-notas.png', fullPage: true });
  console.log('✅ Captura: Mis Notas');

  // Mis Logros
  await page.goto('/alumno/logros');
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: 'screenshots/09-mis-logros.png', fullPage: true });
  console.log('✅ Captura: Mis Logros');

  // Plan de Estudio
  await page.goto('/alumno/plan-estudio');
  await page.waitForLoadState('networkidle');
  await page.screenshot({ path: 'screenshots/10-plan-estudio.png', fullPage: true });
  console.log('✅ Captura: Plan de Estudio');

  console.log('\n🎉 Capturas del flujo del alumno completadas');
});
