import { test, expect, Page } from '@playwright/test';
import { capturarErroresConsola } from './helpers';

/**
 * Ensayo de producción (2026-11-21): se corre contra una copia local en modo producción (ENTORNO=produccion,
 * base nueva sin datos de prueba, compilación de producción servida con el CSP de Cloudflare).
 * Uso: LOGOS_E2E_WEB_URL=http://localhost:4410 npx playwright test -c playwright.ensayo-prod.config.ts e2e/ensayo-produccion.spec.ts
 * No usa la cuenta de prueba: crea una cuenta nueva desde la pantalla de registro.
 */
function rut(): string {
  const cuerpo = String(10_000_000 + (Date.now() % 89_999_999));
  let s = 0, m = 2;
  for (let i = cuerpo.length - 1; i >= 0; i--) { s += Number(cuerpo[i]) * m; m = m < 7 ? m + 1 : 2; }
  const r = 11 - (s % 11);
  return `${cuerpo}-${r === 11 ? '0' : r === 10 ? 'K' : String(r)}`;
}
const EMAIL = `ensayo.${Date.now()}@ejemplo.cl`;
const PASSWORD = 'EnsayoProd2026!';

async function entrarComoAlumno(page: Page) {
  await page.goto('/login');
  await page.fill('input[type=email]', EMAIL);
  await page.fill('input[type=password]', PASSWORD);
  await page.click('button[type=submit]');
  await page.waitForURL('**/selector-perfil');
  await page.getByText('Lucía').click();
  await page.waitForURL('**/alumno/**');
}

test.describe.serial('Ensayo de producción', () => {
  test('login de producción: sin botón demo ni botón de Google sin Client ID', async ({ page }) => {
    const errores = capturarErroresConsola(page);
    await page.goto('/login');
    await expect(page.locator('button[type=submit]')).toBeVisible();
    await expect(page.getByText(/cuenta demo/i)).toHaveCount(0);
    await expect(page.getByText(/Google/)).toHaveCount(0);
    expect(errores).toEqual([]);
  });

  test('registro, alumno de 3.° básico y prueba gratis', async ({ page }) => {
    const errores = capturarErroresConsola(page);
    await page.goto('/registro');
    await page.fill('input[name=nombre]', 'Apoderada Ensayo');
    await page.fill('input[name=email]', EMAIL);
    await page.fill('input[name=password]', PASSWORD);
    await page.click('button[type=submit]');
    await expect(page).toHaveURL(/agregar-alumno/);
    await page.fill('input[name=nombre]', 'Lucía');
    await page.fill('input[name=apellidos]', 'Ensayo Prod');
    await page.fill('input[name=fechaNacimiento]', '2017-06-10');
    await page.fill('input[name=rut]', rut());
    await page.locator('select[name=nivelId]').selectOption({ label: '3° básico' });
    await page.click('button[type=submit]');
    await expect(page).toHaveURL(/seleccion-plan/);
    await page.click('button:has-text("Comenzar mis 5 días gratis")');
    await expect(page).toHaveURL(/selector-perfil/);
    expect(errores).toEqual([]);
  });

  test('guía con imágenes y pictogramas, sin tutor IA cuando no hay clave', async ({ page }) => {
    const errores = capturarErroresConsola(page);
    await entrarComoAlumno(page);
    await page.goto('/alumno/asignaturas');
    await page.locator('a[href*="/alumno/asignaturas/"]').first().click();
    await page.locator('a[href*="/alumno/estudiar/"]').first().click();
    await page.waitForSelector('.contenido-guia');
    await expect(page.locator('app-tutor-ia .tutor')).toHaveCount(0);
    // Toda imagen de la guía debe cargar (CSP img-src 'self').
    const rotas = await page.locator('.contenido-guia img').evaluateAll((imgs) =>
      (imgs as HTMLImageElement[]).filter((i) => i.complete && i.naturalWidth === 0).map((i) => i.src));
    expect(rotas).toEqual([]);
    // Las fuentes propias se cargan desde el sitio.
    const fuente = await page.evaluate(() => getComputedStyle(document.querySelector('h1')!).fontFamily);
    expect(fuente).toMatch(/Poppins/);
    expect(await page.evaluate(() => document.fonts.check('600 16px Poppins'))).toBe(true);
    expect(errores).toEqual([]);
  });

  test('descarga de guía en PDF (ventana de impresión) sin errores de CSP', async ({ page }) => {
    const errores = capturarErroresConsola(page);
    await entrarComoAlumno(page);
    await page.goto('/alumno/asignaturas');
    await page.locator('a[href*="/alumno/asignaturas/"]').first().click();
    await page.locator('a[href*="/alumno/estudiar/"]').first().click();
    await page.waitForSelector('.contenido-guia');
    const [ventana] = await Promise.all([
      page.waitForEvent('popup'),
      page.locator('.descargar-pdf').evaluate((b) => {
        (window as unknown as { _print: unknown })._print = window.print;
        (b as HTMLButtonElement).click();
      }),
    ]);
    const erroresVentana = capturarErroresConsola(ventana);
    await ventana.waitForLoadState();
    await expect(ventana.locator('.encabezado-impresion')).toContainText('Logos School');
    expect([...errores, ...erroresVentana]).toEqual([]);
  });

  test('juegos de práctica: Racha', async ({ page }) => {
    const errores = capturarErroresConsola(page);
    await entrarComoAlumno(page);
    await page.goto('/alumno/juegos');
    await page.getByRole('button', { name: /Racha/ }).click();
    await page.locator('.asignatura').first().click();
    await expect(page.locator('.pregunta__enunciado')).not.toBeEmpty();
    await page.locator('.opcion').first().click();
    if (await page.getByRole('button', { name: 'Responder' }).isVisible()) await page.getByRole('button', { name: 'Responder' }).click();
    await expect(page.locator('.retro')).toBeVisible();
    expect(errores).toEqual([]);
  });

  test('certificado de alumno regular en PDF', async ({ page }) => {
    await entrarComoAlumno(page);
    await page.goto('/alumno/configuracion');
    const [r] = await Promise.all([
      page.waitForResponse((x) => x.url().includes('/certificado.pdf')),
      page.getByRole('button', { name: /Descargar certificado en PDF/ }).click(),
    ]);
    expect(r.status()).toBe(200);
    expect((await r.body()).subarray(0, 5).toString()).toBe('%PDF-');
  });

  test('¿Olvidaste tu contraseña? pide el enlace sin revelar si la cuenta existe', async ({ page }) => {
    const errores = capturarErroresConsola(page);
    await page.goto('/login');
    await page.getByRole('link', { name: '¿Olvidaste tu contraseña?' }).click();
    await expect(page).toHaveURL(/recuperar/);
    await page.fill('input[name=email]', EMAIL);
    await page.getByRole('button', { name: 'Enviar enlace' }).click();
    await expect(page.getByRole('status')).toContainText('te llegará un correo');
    expect(errores).toEqual([]);
  });

  test('Plan Lector y Útiles Escolares existen para 3.° básico (no solo 4.°)', async ({ page }) => {
    const errores = capturarErroresConsola(page);
    await entrarComoAlumno(page);
    await page.goto('/alumno/plan-lector');
    await expect(page.locator('.libro-card')).toHaveCount(4);
    await expect(page.getByText('La porota')).toBeVisible();
    await page.goto('/alumno/utiles-escolares');
    await expect(page.getByText('Atlas escolar de Chile y el mundo')).toBeVisible();
    expect(errores).toEqual([]);
  });
});
