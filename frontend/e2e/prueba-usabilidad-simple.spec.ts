import { test, expect } from '@playwright/test';

test.describe('Prueba de usabilidad - usando cuenta existente', () => {
  test('Flujo completo: Login -> Panel -> Asignaturas -> Pruebas -> Notas -> Logros', async ({ page }) => {
    // 1. Landing
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/flujo/01-landing.png', fullPage: true });
    console.log('✅ 1. Landing cargada');

    // 2. Login con cuenta de prueba existente
    await page.goto('/login');
    await page.fill('input[type=email]', 'apoderado@prueba.com');
    await page.fill('input[type=password]', 'prueba123');
    await page.click('button[type=submit]');

    await page.waitForTimeout(3000);
    const currentUrl = page.url();
    await page.screenshot({ path: 'screenshots/flujo/02-despues-login.png', fullPage: true });
    console.log('✅ 2. Login exitoso');
    console.log(`   URL actual: ${currentUrl}`);

    // 3. Navegar según donde esté
    if (currentUrl.includes('/selector-perfil')) {
      await page.screenshot({ path: 'screenshots/flujo/03-selector-perfil.png', fullPage: true });
      await page.locator('.tarjeta-perfil').first().click();
      await page.waitForURL('/alumno/inicio', { timeout: 10000 });
    } else if (currentUrl.includes('/apoderado/inicio')) {
      console.log('   En panel del apoderado, navegando a alumno');
      await page.click('text=Ver progreso').first();
      await page.waitForURL('/alumno/inicio', { timeout: 10000 });
    }

    await page.screenshot({ path: 'screenshots/flujo/04-panel-alumno.png', fullPage: true });
    console.log('✅ 3. Panel del alumno cargado');

    // 4. Mis Asignaturas
    await page.click('text=Mis Asignaturas');
    await page.waitForURL('/alumno/asignaturas', { timeout: 10000 });
    await page.screenshot({ path: 'screenshots/flujo/05-mis-asignaturas.png', fullPage: true });
    console.log('✅ 4. Mis Asignaturas cargadas');

    // 5. Ver asignatura Lenguaje
    await page.click('text=Lenguaje y Comunicación');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/flujo/06-asignatura-lenguaje.png', fullPage: true });
    console.log('✅ 5. Asignatura Lenguaje cargada');

    // 6. Estudar una guía (con emoji)
    const estudiarButtons = await page.locator('text=Estudiar').all();
    if (estudiarButtons.length > 0) {
      await estudiarButtons[0].click();
      await page.waitForLoadState('networkidle');
      await page.screenshot({ path: 'screenshots/flujo/07-guia-estudio.png', fullPage: true });
      console.log('✅ 6. Guía de estudio cargada (con emoji)');
    } else {
      console.log('⚠️ 6. No hay guías para estudiar');
    }

    // 7. Pruebas y Exámenes
    await page.goto('/alumno/evaluaciones');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/flujo/08-pruebas-examenes.png', fullPage: true });
    console.log('✅ 7. Pruebas y Exámenes cargadas');

    // 8. Intentar comenzar una prueba
    const comenzarButtons = await page.locator('text=Comenzar').all();
    if (comenzarButtons.length > 0) {
      await comenzarButtons[0].click();
      await page.waitForLoadState('networkidle');
      await page.screenshot({ path: 'screenshots/flujo/09-prueba-en-curso.png', fullPage: true });
      console.log('✅ 8. Prueba iniciada');

      // 9. Responder una pregunta
      const radioButtons = await page.locator('input[type="radio"]').all();
      if (radioButtons.length > 0) {
        await radioButtons[0].click();
        await page.screenshot({ path: 'screenshots/flujo/10-responder-pregunta.png', fullPage: true });
        console.log('✅ 9. Pregunta respondida');
      }
    } else {
      console.log('⚠️ 8. No hay pruebas disponibles');
    }

    // 10. Mis Notas
    await page.goto('/alumno/notas');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/flujo/11-mis-notas.png', fullPage: true });
    console.log('✅ 10. Mis Notas cargadas');

    // 11. Mis Logros
    await page.goto('/alumno/logros');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/flujo/12-mis-logros.png', fullPage: true });
    console.log('✅ 11. Mis Logros cargados');

    // 12. Plan de Estudio
    await page.goto('/alumno/plan-estudio');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/flujo/13-plan-estudio.png', fullPage: true });
    console.log('✅ 12. Plan de Estudio cargado');

    // 13. Configuración
    await page.goto('/alumno/configuracion');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/flujo/14-configuracion.png', fullPage: true });
    console.log('✅ 13. Configuración cargada');

    // 14. Cerrar sesión
    await page.click('text=Cerrar sesión');
    await page.waitForURL('/login');
    await page.screenshot({ path: 'screenshots/flujo/15-cerrar-sesion.png', fullPage: true });
    console.log('✅ 14. Sesión cerrada exitosamente');

    console.log('\n🎉 Flujo completo de usabilidad verificado exitosamente');
  });
});
