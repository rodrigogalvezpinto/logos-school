import { test, expect } from '@playwright/test';

test.describe('Auditoría Fase 6 - Responsive - 1° Básico', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  const problemas: string[] = [];
  const observaciones: string[] = [];

  test('Verificar responsive móvil - Landing', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    const titulo = await page.locator('h1').textContent();
    if (titulo) {
      observaciones.push('✅ Landing carga en móvil (375x667)');
    } else {
      problemas.push('❌ Landing no carga en móvil');
    }

    // Verificar que no hay scroll horizontal
    const bodyWidth = await page.evaluate(() => document.body.scrollWidth);
    const windowWidth = await page.evaluate(() => window.innerWidth);
    if (bodyWidth <= windowWidth + 1) {
      observaciones.push('✅ No hay scroll horizontal no deseado');
    } else {
      problemas.push('❌ Hay scroll horizontal no deseado');
    }
  });

  test('Verificar responsive móvil - Panel del Alumno', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    await page.goto('/alumno/inicio');
    await page.waitForLoadState('networkidle');

    const titulo = await page.locator('h1').textContent();
    if (titulo) {
      observaciones.push('✅ Panel del alumno carga en móvil');
    } else {
      problemas.push('❌ Panel del alumno no carga en móvil');
    }
  });

  test('Generar reporte final Fase 6', async ({ page }) => {
    console.log('\n📋 OBSERVACIONES (Fase 6 - Responsive):');
    observaciones.forEach(obs => console.log(obs));

    console.log('\n🔴 PROBLEMAS ENCONTRADOS:');
    if (problemas.length === 0) {
      console.log('✅ No se encontraron problemas de responsive');
    } else {
      problemas.forEach(prob => console.log(prob));
    }

    console.log(`\n📊 Total: ${observaciones.length} observaciones, ${problemas.length} problemas`);
  });
});
