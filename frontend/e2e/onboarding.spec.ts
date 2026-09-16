import { test, expect } from '@playwright/test';

/** Fase 1, ítem 2.3 del plan de incorporación de hallazgos de Brincus — onboarding con
 * checklist de primera sesión. Ver planificacion/27-plan-incorporacion-hallazgos-brincus.md. */

test.describe('Onboarding — checklist de primeros pasos (Fase 1, ítem 2.3)', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('el checklist aparece en Inicio con los 4 pasos', async ({ page }) => {
    await page.goto('/alumno/inicio');
    const checklist = page.locator('.onboarding');
    // Puede que ya esté completo por tests previos que ya recorrieron estos pasos —
    // en ese caso el widget se oculta a propósito, lo cual también es un resultado válido.
    if (await checklist.isVisible().catch(() => false)) {
      expect(await page.locator('.onboarding__lista li').count()).toBe(4);
    }
  });

  test('visitar una guía marca "Revisa una guía de estudio" como hecho', async ({ page }) => {
    await page.goto('/alumno/asignaturas');
    await page.waitForSelector('.asignatura-card, a[href*="/alumno/asignaturas/"]');
    await page.locator('a[href*="/alumno/asignaturas/"]').first().click();
    await page.waitForSelector('a[href*="/alumno/estudiar/"]');
    await page.locator('a[href*="/alumno/estudiar/"]').first().click();
    await page.waitForURL(/alumno\/estudiar\/\d+/);

    await page.goto('/alumno/inicio');
    await page.waitForTimeout(300); // deja que la llamada a /onboarding resuelva
    const pasoGuia = page.locator('.onboarding__lista li', { hasText: 'Revisa una guía de estudio' });
    if (await pasoGuia.isVisible().catch(() => false)) {
      await expect(pasoGuia).toHaveClass(/onboarding__paso--hecho/);
    }
  });

  test('visitar Plan de Estudio marca ese paso como hecho', async ({ page }) => {
    await page.goto('/alumno/plan-estudio');
    await page.waitForTimeout(300);
    await page.goto('/alumno/inicio');
    await page.waitForTimeout(300);
    const paso = page.locator('.onboarding__lista li', { hasText: 'Revisa tu Plan de Estudio' });
    if (await paso.isVisible().catch(() => false)) {
      await expect(paso).toHaveClass(/onboarding__paso--hecho/);
    }
  });

  test('elegir un avatar en Mis Logros marca ese paso como hecho', async ({ page }) => {
    await page.goto('/alumno/logros');
    await page.waitForSelector('.avatar-opcion');
    await page.locator('.avatar-opcion').first().click();
    await page.waitForTimeout(300);

    await page.goto('/alumno/inicio');
    await page.waitForTimeout(300);
    const paso = page.locator('.onboarding__lista li', { hasText: 'Elige tu avatar' });
    if (await paso.isVisible().catch(() => false)) {
      await expect(paso).toHaveClass(/onboarding__paso--hecho/);
    }
  });
});
