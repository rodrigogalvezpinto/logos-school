import { chromium, FullConfig } from '@playwright/test';
import { CREDENCIALES_PRUEBA } from './helpers';

/** Se loguea UNA SOLA VEZ para todo el suite y guarda la sesión (token + perfil elegido)
 * en disco, para que los tests individuales no disparen el rate-limit real de
 * /auth/login (10/min — ver planificacion/20-seguridad-y-casos-borde.md) al correr
 * muchos tests en paralelo. Cada test que necesite sesión usa storageState en vez de
 * loguearse de nuevo. */
export default async function globalSetup(config: FullConfig) {
  const baseURL = config.projects[0].use.baseURL as string;
  const browser = await chromium.launch();
  const page = await browser.newPage({ baseURL });

  await page.goto('/login');
  await page.fill('input[type=email]', CREDENCIALES_PRUEBA.email);
  await page.fill('input[type=password]', CREDENCIALES_PRUEBA.password);
  await page.click('button[type=submit]');
  await page.waitForURL('**/selector-perfil');
  await page.getByText('Sofía').click();
  await page.waitForURL('**/alumno/inicio');

  await page.context().storageState({ path: 'e2e/.storage-sofia.json' });
  await browser.close();
}
