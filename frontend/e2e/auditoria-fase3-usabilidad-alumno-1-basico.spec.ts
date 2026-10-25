import { test, expect } from '@playwright/test';

test.describe('Auditoría Fase 3 - Usabilidad del Alumno - 1° Básico', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  const problemas: string[] = [];
  const observaciones: string[] = [];

  test('Auditar Mis Notas - 1° Básico', async ({ page }) => {
    await page.goto('/alumno/notas');
    await page.waitForLoadState('networkidle');

    // Verificar que la página carga
    const titulo = await page.locator('h1').textContent();
    if (titulo) {
      observaciones.push(`✅ Mis Notas carga: "${titulo}"`);
    } else {
      problemas.push('❌ Mis Notas no carga o no tiene título');
    }

    // Verificar nota estimada (si está disponible)
    const prediccion = await page.locator('.prediccion').all();
    if (prediccion.length > 0) {
      observaciones.push('✅ Nota estimada del examen libre visible');
    } else {
      observaciones.push('ℹ️  Nota estimada no visible (requiere más evaluaciones)');
    }

    // Verificar botón de descarga de informe
    const botonDescarga = await page.locator('text=Descargar informe en PDF').all();
    if (botonDescarga.length > 0) {
      observaciones.push('✅ Botón de descarga de informe en PDF visible');
    } else {
      problemas.push('❌ Botón de descarga de informe no visible');
    }
  });

  test('Auditar Mis Logros - 1° Básico', async ({ page }) => {
    await page.goto('/alumno/logros');
    await page.waitForLoadState('networkidle');

    // Verificar que la página carga
    const titulo = await page.locator('h1').textContent();
    if (titulo) {
      observaciones.push(`✅ Mis Logros carga: "${titulo}"`);
    } else {
      problemas.push('❌ Mis Logros no carga o no tiene título');
    }

    // Verificar nivel
    const nivel = await page.locator('text=Nivel').all();
    if (nivel.length > 0) {
      observaciones.push('✅ Información de nivel visible');
    } else {
      problemas.push('❌ Información de nivel no visible');
    }
  });

  test('Auditar Plan de Estudio - 1° Básico', async ({ page }) => {
    await page.goto('/alumno/plan-estudio');
    await page.waitForLoadState('networkidle');

    // Verificar que la página carga
    const titulo = await page.locator('h1').textContent();
    if (titulo) {
      observaciones.push(`✅ Plan de Estudio carga: "${titulo}"`);
    } else {
      problemas.push('❌ Plan de Estudio no carga o no tiene título');
    }

    // Verificar que hay contenido
    const contenido = await page.locator('body').textContent();
    if (contenido && contenido.length > 100) {
      observaciones.push('✅ Plan de Estudio tiene contenido visible');
    } else {
      problemas.push('❌ Plan de Estudio no tiene contenido visible');
    }
  });

  test('Auditar Plan Lector - 1° Básico', async ({ page }) => {
    await page.goto('/alumno/plan-lector');
    await page.waitForLoadState('networkidle');

    // Verificar que la página carga
    const titulo = await page.locator('h1').textContent();
    if (titulo) {
      observaciones.push(`✅ Plan Lector carga: "${titulo}"`);
    } else {
      problemas.push('❌ Plan Lector no carga o no tiene título');
    }

    // Verificar que hay contenido
    const contenido = await page.locator('body').textContent();
    if (contenido && contenido.length > 100) {
      observaciones.push('✅ Plan Lector tiene contenido visible');
    } else {
      problemas.push('❌ Plan Lector no tiene contenido visible');
    }
  });

  test('Auditar Útiles Escolares - 1° Básico', async ({ page }) => {
    await page.goto('/alumno/utiles-escolares');
    await page.waitForLoadState('networkidle');

    // Verificar que la página carga
    const titulo = await page.locator('h1').textContent();
    if (titulo) {
      observaciones.push(`✅ Útiles Escolares carga: "${titulo}"`);
    } else {
      problemas.push('❌ Útiles Escolares no carga o no tiene título');
    }

    // Verificar que hay contenido
    const contenido = await page.locator('body').textContent();
    if (contenido && contenido.length > 100) {
      observaciones.push('✅ Útiles Escolares tiene contenido visible');
    } else {
      problemas.push('❌ Útiles Escolares no tiene contenido visible');
    }
  });

  test('Auditar Configuración - 1° Básico', async ({ page }) => {
    await page.goto('/alumno/configuracion');
    await page.waitForLoadState('networkidle');

    // Verificar que la página carga
    const titulo = await page.locator('h1').textContent();
    if (titulo) {
      observaciones.push(`✅ Configuración carga: "${titulo}"`);
    } else {
      problemas.push('❌ Configuración no carga o no tiene título');
    }

    // Verificar que hay contenido
    const contenido = await page.locator('body').textContent();
    if (contenido && contenido.length > 100) {
      observaciones.push('✅ Configuración tiene contenido visible');
    } else {
      problemas.push('❌ Configuración no tiene contenido visible');
    }
  });

  test('Generar reporte final Fase 3', async ({ page }) => {
    console.log('\n📋 OBSERVACIONES (Fase 3 - Usabilidad del Alumno):');
    observaciones.forEach(obs => console.log(obs));

    console.log('\n🔴 PROBLEMAS ENCONTRADOS:');
    if (problemas.length === 0) {
      console.log('✅ No se encontraron problemas de usabilidad del alumno');
    } else {
      problemas.forEach(prob => console.log(prob));
    }

    console.log(`\n📊 Total: ${observaciones.length} observaciones, ${problemas.length} problemas`);
  });
});
