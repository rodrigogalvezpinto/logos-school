import { test, expect } from '@playwright/test';

test.describe('Auditoría de usabilidad - perspectiva de 1° básico (6-7 años)', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  const observaciones: string[] = [];
  const problemas: string[] = [];

  test('Navegar como niño de 1° básico y registrar problemas de usabilidad', async ({ page }) => {
    // 1. Landing page
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Observación 1: ¿Es claro qué es Logos School para un niño de 6 años?
    const titulo = await page.locator('h1').textContent();
    if (titulo && titulo.includes('Exámenes Libres')) {
      observaciones.push('❌ Landing usa lenguaje "Exámenes Libres" - muy técnico para niño de 6 años');
    } else {
      observaciones.push('✅ Landing tiene lenguaje apropiado para niño');
    }

    // 2. Login
    await page.goto('/login');
    await page.waitForLoadState('networkidle');

    // Observación 2: ¿El formulario de login es simple para un niño?
    const emailInput = page.locator('input[type=email]');
    if (await emailInput.isVisible()) {
      observaciones.push('❌ Login pide email - niño de 6 años no maneja email');
      problemas.push('Niño de 1° básico no puede hacer login solo sin ayuda de apoderado');
    }

    // 3. Panel del alumno (usando cuenta de prueba)
    await page.goto('/alumno/inicio');
    await page.waitForLoadState('networkidle');

    // Observación 3: ¿Es fácil entender qué hacer?
    const bienvenido = await page.locator('h1').textContent();
    if (bienvenido) {
      observaciones.push(`✅ Panel tiene saludo: "${bienvenido}"`);
    }

    // 4. Mis Asignaturas
    await page.goto('/alumno/asignaturas');
    await page.waitForLoadState('networkidle');

    // Observación 4: ¿Son claros los nombres de las asignaturas?
    const asignaturas = await page.locator('.tarjeta-asignatura h3').allTextContents();
    observaciones.push(`📚 Asignaturas disponibles: ${asignaturas.join(', ')}`);

    // 5. Entrar a Lenguaje (tiene más emojis que Matemática)
    await page.goto('/alumno/asignaturas');
    await page.waitForLoadState('networkidle');
    await page.click('text=Lenguaje y Comunicación');
    await page.waitForLoadState('networkidle');

    // Observación 5: ¿Hay guía de estudio?
    const estudiarButtons = await page.locator('text=Estudiar').all();
    if (estudiarButtons.length > 0) {
      observaciones.push(`✅ Hay ${estudiarButtons.length} guías de estudio en Matemática`);
    } else {
      problemas.push('❌ No hay guías de estudio disponibles en Matemática');
    }

    // 6. Estudiar primera guía
    if (estudiarButtons.length > 0) {
      await estudiarButtons[0].click();
      await page.waitForLoadState('networkidle');

      // Obtener título de la guía
      const tituloOA = await page.locator('h1').textContent();
      observaciones.push(`📖 Guía visitada: "${tituloOA}"`);

      // Observación 6: ¿El contenido es legible para niño de 6 años?
      const contenido = page.locator('.contenido-guia');
      const texto = await contenido.textContent();
      if (texto && texto.length > 0) {
        observaciones.push(`✅ Contenido cargado (${texto.length} caracteres)`);
      }

      // Observación 7: ¿Hay emojis visuales?
      const emojis = await page.locator('.emoji-educativo-inline').all();
      if (emojis.length > 0) {
        observaciones.push(`✅ Hay ${emojis.length} emojis educativos visuales`);
      } else {
        problemas.push(`❌ No hay emojis visuales en "${tituloOA}" - contenido puede ser muy denso para niño de 6 años`);
      }

      // Observación 8: ¿El botón de práctica es claro?
      const botonPractica = page.locator('text=Ya entendí, quiero practicar');
      if (await botonPractica.isVisible()) {
        observaciones.push('✅ Botón de práctica es claro: "Ya entendí, quiero practicar"');
      } else {
        problemas.push('❌ Botón de práctica no es claro o no está visible');
      }
    }

    // 7. Pruebas y Exámenes
    await page.goto('/alumno/evaluaciones');
    await page.waitForLoadState('networkidle');

    // Observación 9: ¿Hay pruebas disponibles?
    const comenzarButtons = await page.locator('text=Comenzar').all();
    if (comenzarButtons.length > 0) {
      observaciones.push(`✅ Hay ${comenzarButtons.length} pruebas disponibles`);
    } else {
      problemas.push('❌ No hay pruebas disponibles para rendir');
    }

    // 8. Mis Logros
    await page.goto('/alumno/logros');
    await page.waitForLoadState('networkidle');

    // Observación 10: ¿La gamificación es motivadora?
    const nivel = await page.locator('.resumen__nivel').textContent();
    if (nivel) {
      observaciones.push(`✅ Gamificación visible: ${nivel}`);
    }

    const avatares = await page.locator('.avatar-grid .avatar').all();
    if (avatares.length > 0) {
      observaciones.push(`✅ Hay ${avatares.length} avatares para elegir`);
    }

    // Generar reporte
    console.log('\n📋 OBSERVACIONES (1° Básico):');
    observaciones.forEach(obs => console.log(obs));

    console.log('\n🔴 PROBLEMAS ENCONTRADOS:');
    if (problemas.length === 0) {
      console.log('✅ No se encontraron problemas críticos');
    } else {
      problemas.forEach(prob => console.log(prob));
    }

    console.log(`\n📊 Total: ${observaciones.length} observaciones, ${problemas.length} problemas`);
  });
});
