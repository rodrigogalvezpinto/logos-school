import { Page } from '@playwright/test';

/** Captura errores de consola del navegador — la "lectura de logs" del loop de pruebas. */
export function capturarErroresConsola(page: Page): string[] {
  const errores: string[] = [];
  page.on('console', (msg) => {
    if (msg.type() === 'error') errores.push(msg.text());
  });
  page.on('pageerror', (err) => errores.push(err.message));
  return errores;
}
