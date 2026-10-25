import { test, expect } from '@playwright/test';

test.describe('Verificar contenido de emojis en base de datos vs archivos locales', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('Comparar contenido de guía entre DB y archivo Markdown local', async ({ page }) => {
    await page.goto('/alumno/asignaturas');
    await page.click('text=Lenguaje y Comunicación');
    await page.waitForLoadState('networkidle');

    const estudiarButtons = await page.locator('text=Estudiar').all();
    if (estudiarButtons.length > 0) {
      await estudiarButtons[0].click();
      await page.waitForLoadState('networkidle');

      const contenidoHTML = await page.locator('.contenido-guia').innerHTML();
      
      // Verificar si hay marcadores de emoji en el HTML renderizado
      if (contenidoHTML.includes('emoji-educativo')) {
        console.log('✅ El contenido de la DB tiene emojis renderizados');
      } else {
        console.log('❌ El contenido de la DB NO tiene emojis renderizados');
        console.log('📝 Posible causa: Los archivos Markdown locales tienen ::emoji:: pero la DB no fue actualizada');
        console.log('🔧 Solución: Reimportar contenido desde archivos Markdown locales a la DB');
      }

      // Verificar si hay marcadores de emoji sin procesar (texto plano)
      if (contenidoHTML.includes('::emoji::')) {
        console.log('⚠️ Hay marcadores de emoji sin procesar en el HTML');
      }
    }
  });
});
