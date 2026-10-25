import { test, expect } from '@playwright/test';

test.describe('Auditoría Fase 5 - Usabilidad del Profesor - 1° Básico', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  const problemas: string[] = [];
  const observaciones: string[] = [];

  test('Auditar Flujo del Profesor - 1° Básico', async ({ page }) => {
    // Verificar que existe la ruta para el profesor
    await page.goto('/profesor/login');
    await page.waitForLoadState('networkidle');

    const titulo = await page.locator('h1').textContent();
    if (titulo) {
      observaciones.push(`✅ Login de profesor existe: "${titulo}"`);
    } else {
      problemas.push('❌ Login de profesor no carga o no tiene título');
    }
  });

  test('Generar reporte final Fase 5', async ({ page }) => {
    console.log('\n📋 OBSERVACIONES (Fase 5 - Usabilidad del Profesor):');
    observaciones.forEach(obs => console.log(obs));

    console.log('\n🔴 PROBLEMAS ENCONTRADOS:');
    if (problemas.length === 0) {
      console.log('✅ No se encontraron problemas de usabilidad del profesor');
    } else {
      problemas.forEach(prob => console.log(prob));
    }

    console.log(`\n📊 Total: ${observaciones.length} observaciones, ${problemas.length} problemas`);
  });
});
