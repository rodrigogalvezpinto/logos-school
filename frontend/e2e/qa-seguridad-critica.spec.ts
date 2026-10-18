import { test, expect } from '@playwright/test';

test.describe('QA Crítico - Seguridad y Validaciones', () => {
  const problemas: string[] = [];
  const observaciones: string[] = [];

  test('Test 1.1: Validación de RUT - RUT inválido', async ({ page }) => {
    await page.goto('/registro');
    await page.waitForLoadState('networkidle');
    
    // Intentar registrar con RUT inválido
    await page.fill('input[name="rut"]', '12.345.678-9'); // Dígito verificador incorrecto
    await page.fill('input[name="email"]', 'test@prueba-qa.com');
    await page.fill('input[name="password"]', 'password123');
    await page.fill('input[name="nombre"]', 'Test QA');
    
    const btn = page.locator('button[type="submit"]');
    await btn.click();
    await page.waitForTimeout(2000);
    
    // Verificar que muestra error o que no se redirige
    const url = page.url();
    if (url.includes('/registro') || url.includes('/error')) {
      observaciones.push('✅ RUT inválido es rechazado (se queda en registro o muestra error)');
    } else {
      problemas.push('❌ RUT inválido NO es rechazado - Posible vulnerabilidad');
    }
  });

  test('Test 1.2: Protección de rutas - Acceder sin sesión', async ({ page }) => {
    // Intentar acceder a ruta protegida sin sesión
    await page.goto('/alumno/inicio');
    await page.waitForLoadState('networkidle');
    
    const url = page.url();
    if (url.includes('/login') || url.includes('/registro') || url.includes('/landing')) {
      observaciones.push('✅ Ruta protegida redirige a login/registro/landing sin sesión');
    } else {
      problemas.push('❌ Ruta protegida NO redirige - VULNERABILIDAD');
    }
  });

  test('Test 1.6: Email inválido - Formato incorrecto', async ({ page }) => {
    await page.goto('/registro');
    await page.waitForLoadState('networkidle');
    
    await page.fill('input[name="email"]', 'invalid-email');
    await page.fill('input[name="password"]', 'password123');
    await page.fill('input[name="nombre"]', 'Test User');
    await page.fill('input[name="rut"]', '12.345.678-5');
    
    await page.click('button[type="submit"]');
    await page.waitForTimeout(2000);
    
    const url = page.url();
    if (url.includes('/registro') || url.includes('/error')) {
      observaciones.push('✅ Email inválido es rechazado');
    } else {
      problemas.push('❌ Email inválido NO es rechazado');
    }
  });

  test('Test 1.7: Password inválido - Menos de 8 caracteres', async ({ page }) => {
    await page.goto('/registro');
    await page.waitForLoadState('networkidle');
    
    await page.fill('input[name="email"]', 'test@prueba-qa.com');
    await page.fill('input[name="password"]', '123'); // Solo 3 caracteres
    await page.fill('input[name="nombre"]', 'Test User');
    await page.fill('input[name="rut"]', '12.345.678-5');
    
    await page.click('button[type="submit"]');
    await page.waitForTimeout(2000);
    
    const url = page.url();
    if (url.includes('/registro') || url.includes('/error')) {
      observaciones.push('✅ Password corto es rechazado');
    } else {
      problemas.push('❌ Password corto NO es rechazado');
    }
  });

  test('Test 1.8: Password vacío', async ({ page }) => {
    await page.goto('/registro');
    await page.waitForLoadState('networkidle');
    
    await page.fill('input[name="email"]', 'test@prueba-qa.com');
    await page.fill('input[name="password"]', ''); // Vacío
    await page.fill('input[name="nombre"]', 'Test User');
    await page.fill('input[name="rut"]', '12.345.678-5');
    
    await page.click('button[type="submit"]');
    await page.waitForTimeout(2000);
    
    const url = page.url();
    if (url.includes('/registro') || url.includes('/error')) {
      observaciones.push('✅ Password vacío es rechazado');
    } else {
      problemas.push('❌ Password vacío NO es rechazado');
    }
  });

  test('Generar reporte de seguridad', async ({ page }) => {
    console.log('\n📋 OBSERVACIONES (Seguridad):');
    observaciones.forEach(obs => console.log(obs));

    console.log('\n🔴 PROBLEMAS CRÍTICOS (Vulnerabilidades):');
    if (problemas.length === 0) {
      console.log('✅ No se encontraron vulnerabilidades críticas en validaciones básicas');
    } else {
      problemas.forEach(prob => console.log(prob));
    }

    console.log(`\n📊 Total: ${observaciones.length} validaciones pasadas, ${problemas.length} problemas encontrados`);
  });
});
