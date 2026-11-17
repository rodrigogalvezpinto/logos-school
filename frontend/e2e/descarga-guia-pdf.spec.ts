import { test, expect } from '@playwright/test';

/** Descarga de guía en PDF. Desde 2026-11-17 el botón abre la guía ya dibujada en una ventana para imprimir o
 * «Guardar como PDF» (fiel a la pantalla: fotos, pictogramas, mapas, gráficos); antes era un PDF del servidor que
 * descartaba emoji, mapas e imágenes. */

test.describe('Descargar guía en PDF', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('el botón abre la guía completa lista para imprimir, con imágenes y sin emoji de texto', async ({ page }) => {
    await page.goto('/alumno/asignaturas');
    await page.waitForSelector('a[href*="/alumno/asignaturas/"]');
    await page.locator('a[href*="/alumno/asignaturas/"]').first().click();
    await page.waitForSelector('a[href*="/alumno/estudiar/"]');
    await page.locator('a[href*="/alumno/estudiar/"]').first().click();
    await page.waitForURL(/alumno\/estudiar\/\d+/);
    await page.waitForSelector('.contenido-guia');

    const boton = page.locator('.descargar-pdf');
    await expect(boton).toBeVisible();
    const [ventana] = await Promise.all([
      page.waitForEvent('popup'),
      boton.evaluate((b) => {
        // En la prueba no se abre el diálogo real de impresión.
        (window as unknown as { _print: unknown })._print = window.print;
        (b as HTMLButtonElement).click();
      }),
    ]);
    await ventana.waitForLoadState();
    await expect(ventana.locator('.encabezado-impresion')).toContainText('Logos School');
    const textoGuia = await page.locator('.contenido-guia').innerText();
    const textoImpreso = await ventana.locator('.contenido-guia').innerText();
    expect(textoImpreso.slice(0, 200)).toBe(textoGuia.slice(0, 200));
  });
});
