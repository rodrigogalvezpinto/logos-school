import { test, expect } from '@playwright/test';

test.describe('Vista previa de flujos principales - capturas automáticas', () => {
  test('Flujo completo: Landing -> Registro -> Panel -> Asignaturas -> Prueba', async ({ page }) => {
    // 1. Landing
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/01-landing.png', fullPage: true });
    console.log('✅ Captura: Landing');

    // 2. Ir a registro
    await page.click('text=Regístrate gratis');
    await page.waitForURL('/registro');
    await page.screenshot({ path: 'screenshots/02-registro.png', fullPage: true });
    console.log('✅ Captura: Registro');

    // 3. Registro de apoderado
    await page.fill('input[name="nombre"]', 'Test Apoderado');
    await page.fill('input[name="apellido"]', 'Test Apellido');
    await page.fill('input[name="email"]', `test${Date.now()}@test.com`);
    await page.fill('input[name="password"]', 'test123456');
    await page.fill('input[name="password_confirm"]', 'test123456');
    await page.click('button[type=submit]');
    await page.waitForURL('/selector-perfil', { timeout: 15000 });
    await page.screenshot({ path: 'screenshots/03-selector-perfil.png', fullPage: true });
    console.log('✅ Captura: Selector de perfil');

    // 4. Agregar alumno si no hay
    const agregarButton = page.locator('text=Agregar otro alumno');
    if (await agregarButton.isVisible()) {
      await agregarButton.click();
      await page.fill('input[name="nombre"]', 'Test Niño');
      await page.fill('input[name="apellido"]', 'Test Niño Apellido');
      await page.fill('input[name="rut"]', '12345678-9');
      await page.fill('input[name="fecha_nacimiento"]', '2015-05-15');
      await page.fill('select[name="nivel"]', '4'); // 4° básico
      await page.click('button[type=submit]');
      await page.waitForTimeout(1000);
    }

    // 5. Elegir perfil (primer alumno)
    await page.locator('.tarjeta-perfil').first().click();
    await page.waitForURL('/alumno/inicio', { timeout: 10000 });
    await page.screenshot({ path: 'screenshots/04-panel-alumno.png', fullPage: true });
    console.log('✅ Captura: Panel del alumno');

    // 6. Mis Asignaturas
    await page.click('text=Mis Asignaturas');
    await page.waitForURL('/alumno/asignaturas', { timeout: 10000 });
    await page.screenshot({ path: 'screenshots/05-mis-asignaturas.png', fullPage: true });
    console.log('✅ Captura: Mis Asignaturas');

    // 7. Ver detalle de una asignatura (Lenguaje)
    await page.click('text=Lenguaje y Comunicación');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/06-asignatura-lenguaje.png', fullPage: true });
    console.log('✅ Captura: Asignatura Lenguaje');

    // 8. Ver una guía de estudio
    const estudiarButtons = await page.locator('text=Estudiar').all();
    if (estudiarButtons.length > 0) {
      await estudiarButtons[0].click();
      await page.waitForLoadState('networkidle');
      await page.screenshot({ path: 'screenshots/07-guia-estudio.png', fullPage: true });
      console.log('✅ Captura: Guía de estudio (con emoji)');
    } else {
      console.log('⚠️ No hay botones de Estudar');
    }

    // 9. Pruebas y Exámenes
    await page.goto('/alumno/evaluaciones');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/08-pruebas-examenes.png', fullPage: true });
    console.log('✅ Captura: Pruebas y Exámenes');

    // 10. Comenzar una prueba si existe
    const comenzarButtons = await page.locator('text=Comenzar').all();
    if (comenzarButtons.length > 0) {
      await comenzarButtons[0].click();
      await page.waitForLoadState('networkidle');
      await page.screenshot({ path: 'screenshots/09-prueba-en-curso.png', fullPage: true });
      console.log('✅ Captura: Prueba en curso');
    } else {
      console.log('⚠️ No hay botones de Comenzar');
    }

    // 11. Mis Notas
    await page.goto('/alumno/notas');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/10-mis-notas.png', fullPage: true });
    console.log('✅ Captura: Mis Notas');

    // 12. Mis Logros
    await page.goto('/alumno/logros');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/11-mis-logros.png', fullPage: true });
    console.log('✅ Captura: Mis Logros');

    // 13. Plan de Estudio
    await page.goto('/alumno/plan-estudio');
    await page.waitForLoadState('networkidle');
    await page.screenshot({ path: 'screenshots/12-plan-estudio.png', fullPage: true });
    console.log('✅ Captura: Plan de Estudio');

    console.log('\n🎉 Todas las capturas completadas en screenshots/');
  });
});
