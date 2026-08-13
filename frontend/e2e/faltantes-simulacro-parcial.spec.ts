import { test, expect } from '@playwright/test';

test.describe('Faltantes y simulacro parcial (Fase 1.3)', () => {
  test.use({ storageState: 'e2e/.storage-sofia.json' });

  test('cubrir la mitad del temario de una asignatura habilita el simulacro parcial', async ({ page, request }) => {
    await page.goto('/alumno/inicio');
    const token = await page.evaluate(() => localStorage.getItem('logos_token'));
    const perfilCrudo = await page.evaluate(() => localStorage.getItem('logos_perfil_activo'));
    const perfil = JSON.parse(perfilCrudo!);
    const headers = { Authorization: `Bearer ${token}` };

    const asignaturas = await (
      await request.get(`http://localhost:8000/contenido/niveles/${perfil.nivel_id}/asignaturas`, { headers })
    ).json();
    const asignatura = asignaturas[0];

    const objetivos = await (
      await request.get(`http://localhost:8000/contenido/asignaturas/${asignatura.id}/objetivos`, { headers })
    ).json();

    // Revisa la mitad (redondeando hacia arriba) de las guías de esa asignatura — cumple
    // el umbral de 50% de cobertura que habilita el simulacro parcial.
    const mitad = Math.ceil(objetivos.length / 2);
    for (const oa of objetivos.slice(0, mitad)) {
      await request.post(`http://localhost:8000/progreso/${perfil.id}/guias/${oa.id}/revisada`, { headers });
    }

    await page.goto('/alumno/notas');
    const aviso = page.locator('.aviso-simulacro-parcial', { hasText: asignatura.nombre });
    await expect(aviso).toBeVisible();

    await aviso.getByRole('button', { name: 'Rendir simulacro parcial' }).click();
    await expect(page).toHaveURL(/examen\/\d+/);
    await page.getByRole('button', { name: 'Comenzar' }).click();
    await expect(page.locator('.pregunta').first()).toBeVisible();
  });
});
