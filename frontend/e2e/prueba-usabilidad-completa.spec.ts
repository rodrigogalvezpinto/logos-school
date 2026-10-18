import { test, expect } from '@playwright/test';

test.describe('Prueba de usabilidad completa - usuario real', () => {
  const timestamp = Date.now();
  const email = `testusabilidad${timestamp}@test.com`;
  const password = 'Test123456';

  test('Flujo completo: Registro -> Agregar Alumno -> Estudiar -> Prueba -> Resultados', async ({ page }) => {
    // 1. Landing
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/flujo/01-landing.png', fullPage: true });
    console.log('✅ 1. Landing cargada');

    // 2. Registro
    await page.click('a[href="/registro"]');
    await page.waitForURL('/registro');
    await page.screenshot({ path: 'screenshots/flujo/02-registro.png', fullPage: true });

    await page.fill('input[name=nombre]', 'Test Usabilidad');
    await page.fill('input[name=email]', email);
    await page.fill('input[name=password]', password);
    await page.click('button[type=submit]');

    // Esperar registro exitoso (redirige a agregar-alumno para el primer alumno)
    await page.waitForURL('/agregar-alumno', { timeout: 15000 });
    await page.screenshot({ path: 'screenshots/flujo/03-agregar-alumno.png', fullPage: true });
    console.log('✅ 2. Registro exitoso');

    // 3. Agregar primer alumno (formulario de agregar-alumno)
    await page.screenshot({ path: 'screenshots/flujo/04-form-alumno.png', fullPage: true });

    await page.fill('input[name=nombre]', 'Niño Test');
    await page.fill('input[name=apellidos]', 'Test Niño');
    await page.fill('input[name=fechaNacimiento]', '2015-05-15');
    await page.fill('input[name=rut]', '12345678-9');
    await page.selectOption('select[name=nivelId]', { label: '4° básico' });
    await page.screenshot({ path: 'screenshots/flujo/05-form-completo.png', fullPage: true });
    await page.click('button[type=submit]');

    await page.waitForTimeout(3000);
    const currentUrl = page.url();
    await page.screenshot({ path: 'screenshots/flujo/06-despues-submit.png', fullPage: true });
    console.log('✅ 3. Submit formulario alumno');
    console.log(`   URL actual: ${currentUrl}`);

    // 4. Navegar según el flujo real
    if (currentUrl.includes('/seleccion-plan')) {
      await page.screenshot({ path: 'screenshots/flujo/06-seleccion-plan.png', fullPage: true });
      console.log('✅ 4. Selección de plan cargada');

      await page.click('button:has-text("Comenzar mis 5 días gratis")');
      await page.waitForURL('/selector-perfil', { timeout: 10000 });
      await page.screenshot({ path: 'screenshots/flujo/07-selector-perfil.png', fullPage: true });
      console.log('✅ 5. Selector de perfil cargado');
    } else if (currentUrl.includes('/selector-perfil')) {
      await page.screenshot({ path: 'screenshots/flujo/06-selector-perfil.png', fullPage: true });
      console.log('✅ 4. Selector de perfil cargado');
    }

    // 5. Elegir perfil del alumno
    await page.locator('.tarjeta-perfil').click();
    await page.waitForURL('/alumno/inicio', { timeout: 10000 });
    await page.screenshot({ path: 'screenshots/flujo/08-panel-alumno.png', fullPage: true });
    console.log('✅ 6. Panel del alumno cargado');

    // 5. Mis Asignaturas
    await page.click('text=Mis Asignaturas');
    await page.waitForURL('/alumno/asignaturas');
    await page.screenshot({ path: 'screenshots/flujo/07-mis-asignaturas.png', fullPage: true });
    console.log('✅ 5. Mis Asignaturas cargadas');

    // 6. Ver asignatura Lenguaje
    await page.click('text=Lenguaje y Comunicación');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/flujo/08-asignatura-lenguaje.png', fullPage: true });
    console.log('✅ 6. Asignatura Lenguaje cargada');

    // 7. Estudiar una guía (con emoji)
    const estudiarButtons = await page.locator('text=Estudiar').all();
    if (estudiarButtons.length > 0) {
      await estudiarButtons[0].click();
      await page.waitForLoadState('networkidle');
      await page.screenshot({ path: 'screenshots/flujo/09-guia-estudio.png', fullPage: true });
      console.log('✅ 7. Guía de estudio cargada (con emoji)');
    } else {
      console.log('⚠️ 7. No hay guías para estudiar');
    }

    // 8. Pruebas y Exámenes
    await page.goto('/alumno/evaluaciones');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/flujo/10-pruebas-examenes.png', fullPage: true });
    console.log('✅ 8. Pruebas y Exámenes cargadas');

    // 9. Intentar comenzar una prueba
    const comenzarButtons = await page.locator('text=Comenzar').all();
    if (comenzarButtons.length > 0) {
      await comenzarButtons[0].click();
      await page.waitForLoadState('networkidle');
      await page.screenshot({ path: 'screenshots/flujo/11-prueba-en-curso.png', fullPage: true });
      console.log('✅ 9. Prueba iniciada');

      // 10. Responder una pregunta
      const radioButtons = await page.locator('input[type="radio"]').all();
      if (radioButtons.length > 0) {
        await radioButtons[0].click();
        await page.screenshot({ path: 'screenshots/flujo/12-responder-pregunta.png', fullPage: true });
        console.log('✅ 10. Pregunta respondida');
      }

      // 11. Navegar a la siguiente pregunta
      const siguienteButtons = await page.locator('text=Siguiente').all();
      if (siguienteButtons.length > 0) {
        await siguienteButtons[0].click();
        await page.waitForTimeout(500);
        console.log('✅ 11. Navegó a siguiente pregunta');
      }
    } else {
      console.log('⚠️ 9. No hay pruebas disponibles');
    }

    // 12. Mis Notas
    await page.goto('/alumno/notas');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/flujo/13-mis-notas.png', fullPage: true });
    console.log('✅ 12. Mis Notas cargadas');

    // 13. Mis Logros
    await page.goto('/alumno/logros');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/flujo/14-mis-logros.png', fullPage: true });
    console.log('✅ 13. Mis Logros cargados');

    // 14. Plan de Estudio
    await page.goto('/alumno/plan-estudio');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/flujo/15-plan-estudio.png', fullPage: true });
    console.log('✅ 14. Plan de Estudio cargado');

    // 15. Configuración
    await page.goto('/alumno/configuracion');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/flujo/16-configuracion.png', fullPage: true });
    console.log('✅ 15. Configuración cargada');

    // 16. Cerrar sesión
    await page.click('text=Cerrar sesión');
    await page.waitForURL('/login');
    await page.screenshot({ path: 'screenshots/flujo/17-cerrar-sesion.png', fullPage: true });
    console.log('✅ 16. Sesión cerrada exitosamente');

    console.log('\n🎉 Flujo completo de usabilidad verificado exitosamente');
    console.log(`📧 Email de prueba: ${email}`);
    console.log(`🔑 Contraseña: ${password}`);
  });
});
