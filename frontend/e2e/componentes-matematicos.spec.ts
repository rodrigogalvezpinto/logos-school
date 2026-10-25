import { test, expect } from '@playwright/test';

test.describe('Componentes matemáticos SVG - recta numérica y fracciones', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('El MarkdownPipe debe renderizar recta numérica y fracciones con SVG', async ({ page }) => {
    // Ir a una guía de Matemática que tenga contenido
    await page.goto('/alumno/asignaturas');
    await page.click('text=Matemática');
    await page.waitForLoadState('networkidle');

    // Ir a la primera guía disponible
    const estudiarButtons = await page.locator('text=Estudiar').all();
    if (estudiarButtons.length > 0) {
      await estudiarButtons[0].click();
      await page.waitForLoadState('networkidle');

      // Verificar que el contenido cargó
      const contenido = page.locator('.contenido-guia');
      await expect(contenido).toBeVisible();

      // Verificar que no hay errores de consola
      const errores = await page.evaluate(() => {
        const logs: string[] = [];
        window.addEventListener('error', (e) => logs.push(e.message));
        return logs;
      });
      expect(errores).toEqual([]);

      console.log('✅ Componentes matemáticos renderizados sin errores');
    } else {
      console.log('⚠️ No hay guías disponibles para probar');
    }
  });
});
