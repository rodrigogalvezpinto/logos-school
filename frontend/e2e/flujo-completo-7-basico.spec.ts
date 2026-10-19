import { test, expect } from '@playwright/test';
import { capturarErroresConsola } from './helpers';

/** Genera un RUT chileno válido y único (Módulo 11) para evitar colisiones en BD */
function rutValidoUnico(): string {
  const cuerpo = String(10000000 + (Date.now() % 89999999) + Math.floor(Math.random() * 900));
  let suma = 0;
  let multiplicador = 2;
  for (let i = cuerpo.length - 1; i >= 0; i--) {
    suma += Number(cuerpo[i]) * multiplicador;
    multiplicador = multiplicador < 7 ? multiplicador + 1 : 2;
  }
  const resto = 11 - (suma % 11);
  const dv = resto === 11 ? '0' : resto === 10 ? 'K' : String(resto);
  return `${cuerpo}-${dv}`;
}

const timestamp = Date.now();
const EMAIL_APODERADO = `apoderado.7basico.${timestamp}@logos.cl`;
const PASSWORD_PRUEBA = 'Logos7Basico2026!';
const NOMBRE_APODERADO = 'Patricia Alarcón (Apoderada 7° Básico)';
const NOMBRE_ALUMNO = 'Gabriel';
const APELLIDOS_ALUMNO = 'Alarcón Bravo';
const RUT_ALUMNO = rutValidoUnico();

test.describe.serial('Auditoría Integral y Flujo Real: 7° Básico (Apoderado y Alumno)', () => {
  test('1. Registro de Apoderado y alta de Alumno en 7° Básico', async ({ page }) => {
    const errores = capturarErroresConsola(page);

    // Registro del apoderado
    await page.goto('/registro');
    await expect(page).toHaveURL(/registro/);
    await page.fill('input[name=nombre]', NOMBRE_APODERADO);
    await page.fill('input[name=email]', EMAIL_APODERADO);
    await page.fill('input[name=password]', PASSWORD_PRUEBA);
    await page.click('button[type=submit]');

    // Onboarding de alumno en 7° básico
    await expect(page).toHaveURL(/agregar-alumno/);
    await page.fill('input[name=nombre]', NOMBRE_ALUMNO);
    await page.fill('input[name=apellidos]', APELLIDOS_ALUMNO);
    await page.fill('input[name=fechaNacimiento]', '2013-05-10'); // 13 años
    await page.fill('input[name=rut]', RUT_ALUMNO);

    // Seleccionar curso: 7° básico
    await page.locator('select[name=nivelId]').selectOption({ label: '7° básico' });
    await page.click('button[type=submit]');

    // Selección de plan
    await expect(page).toHaveURL(/seleccion-plan/);
    await expect(page.locator('h1')).toContainText(NOMBRE_ALUMNO);
    await page.click('button:has-text("Comenzar mis 5 días gratis")');

    // Selector de perfiles
    await expect(page).toHaveURL(/selector-perfil/);
    await expect(page.getByText(NOMBRE_ALUMNO)).toBeVisible();
    await expect(page.getByText('Ver como Apoderado')).toBeVisible();

    expect(errores, `Errores de consola: ${errores.join(', ')}`).toEqual([]);
  });

  test('2. Panel del Apoderado supervisando a alumno de 7° Básico', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type=email]', EMAIL_APODERADO);
    await page.fill('input[type=password]', PASSWORD_PRUEBA);
    await page.click('button[type=submit]');
    await page.waitForURL('**/selector-perfil');

    await page.getByText('Ver como Apoderado').click();
    await expect(page).toHaveURL(/apoderado\/inicio/);

    // Saludo y tarjeta de alumno en 7° básico con plan activo
    await expect(page.locator('h1')).toContainText('Hola');
    const alumnoCard = page.locator('.alumno-card', { hasText: `${NOMBRE_ALUMNO} ${APELLIDOS_ALUMNO}` });
    await expect(alumnoCard).toBeVisible();
    await expect(alumnoCard.locator('.chip--activo')).toContainText('Plan activo');

    // Navegar a Plan y Pagos
    await page.goto('/apoderado/plan');
    await expect(page).toHaveURL(/apoderado\/plan/);
    await expect(page.locator('h1')).toContainText('Plan y Pagos');

    // Navegar a Estadísticas
    await page.goto('/apoderado/estadisticas');
    await expect(page).toHaveURL(/apoderado\/estadisticas/);
    await expect(page.locator('h1')).toContainText('Estadísticas');
  });

  test('3. Inicio del Alumno y las 5 Asignaturas Oficiales de 7° Básico (Decreto 614/2013)', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type=email]', EMAIL_APODERADO);
    await page.fill('input[type=password]', PASSWORD_PRUEBA);
    await page.click('button[type=submit]');
    await page.waitForURL('**/selector-perfil');

    await page.getByText(NOMBRE_ALUMNO).click();
    await expect(page).toHaveURL(/alumno\/inicio/);

    // Resolver check-in si aparece
    const checkin = page.locator('.checkin__opcion', { hasText: 'Tranquilo' });
    try {
      await checkin.waitFor({ state: 'visible', timeout: 3000 });
      await checkin.click();
    } catch {
      // Ignorar si no aparece
    }

    await expect(page.locator('h1')).toContainText(NOMBRE_ALUMNO);
    await expect(page.locator('.aviso-prueba')).toContainText('5 días');

    // Ir a Mis Asignaturas
    await page.goto('/alumno/asignaturas');
    await expect(page).toHaveURL(/alumno\/asignaturas/);
    await expect(page.locator('h1')).toContainText('Mis Asignaturas');

    // En 7° básico cambia a Lengua y Literatura (Decreto 614/2013)
    const asignaturas = await page.locator('.asignatura-card h3').allTextContents();
    expect(asignaturas).toContain('Lengua y Literatura');
    expect(asignaturas).toContain('Matemática');
    expect(asignaturas).toContain('Ciencias Naturales');
    expect(asignaturas).toContain('Historia, Geografía y Cs. Sociales');
    expect(asignaturas).toContain('Inglés');
    expect(asignaturas.length).toBeGreaterThanOrEqual(5);
  });

  test('4. Estudio de Guías en Asignaturas de 7° Básico y Autoevaluación', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type=email]', EMAIL_APODERADO);
    await page.fill('input[type=password]', PASSWORD_PRUEBA);
    await page.click('button[type=submit]');
    await page.waitForURL('**/selector-perfil');
    await page.getByText(NOMBRE_ALUMNO).click();
    await expect(page).toHaveURL(/alumno\/inicio/);

    // 4.1 Entrar a Lengua y Literatura de 7° Básico
    await page.goto('/alumno/asignaturas');
    await page.locator('.asignatura-card', { hasText: 'Lengua y Literatura' }).click();
    await expect(page).toHaveURL(/asignaturas\/\d+/);
    await expect(page.locator('h1')).toContainText('Lengua y Literatura');

    // Abrir primera guía
    await page.getByRole('link', { name: 'Estudiar guía' }).first().click();
    await expect(page).toHaveURL(/estudiar\/\d+/);

    // Verificar contenido de 7° básico
    const contenido = page.locator('.contenido-guia');
    await expect(contenido).not.toBeEmpty();
    await expect(contenido).not.toContainText('###');
    await expect(page.getByRole('button', { name: '🔊 Escuchar' })).toBeVisible();
    await expect(page.locator('.descargar-pdf')).toBeVisible();

    // Calificar guía
    const estrella = page.locator('.calificar-guia__estrella').nth(4);
    await estrella.click();
    await expect(page.locator('.calificar-guia__gracias')).toContainText('¡Gracias por tu opinión!');

    // Practicar autoevaluación
    await page.getByRole('link', { name: 'Ya entendí, quiero practicar →' }).click();
    await expect(page).toHaveURL(/autoevaluacion\/\d+/);
    await page.getByRole('button', { name: 'Comenzar' }).click();
    await expect(page.locator('.pregunta__enunciado')).not.toBeEmpty();

    // Responder la primera pregunta (abierta o alternativa)
    const textarea = page.locator('textarea.respuesta-abierta');
    if (await textarea.isVisible()) {
      await textarea.fill('Respuesta de prueba 7 basico');
      await expect(textarea).toHaveValue(/prueba/);
    } else {
      const opcion = page.locator('.opcion').first();
      await expect(opcion).toBeVisible();
      await opcion.click();
      await expect(page.locator('.feedback')).toBeVisible();
    }

    // 4.2 Entrar a Matemática de 7° Básico
    await page.goto('/alumno/asignaturas');
    await page.locator('.asignatura-card', { hasText: 'Matemática' }).click();
    await expect(page).toHaveURL(/asignaturas\/\d+/);
    await expect(page.locator('h1')).toContainText('Matemática');
    await page.getByRole('link', { name: 'Estudiar guía' }).first().click();
    await expect(page).toHaveURL(/estudiar\/\d+/);
    await expect(page.locator('.contenido-guia')).not.toBeEmpty();
  });

  test('5. Rendición completa de una Prueba de Unidad de 7° Básico', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type=email]', EMAIL_APODERADO);
    await page.fill('input[type=password]', PASSWORD_PRUEBA);
    await page.click('button[type=submit]');
    await page.waitForURL('**/selector-perfil');
    await page.getByText(NOMBRE_ALUMNO).click();
    await expect(page).toHaveURL(/alumno\/inicio/);

    // Ir a evaluaciones
    await page.goto('/alumno/evaluaciones');
    await expect(page).toHaveURL(/alumno\/evaluaciones/);

    // Tomar la primera prueba de unidad
    const primeraPruebaBoton = page.locator('.conjunto-card:not(.conjunto-card--examen) .conjunto-card__boton').first();
    await primeraPruebaBoton.click();
    await expect(page).toHaveURL(/alumno\/prueba\/\d+/);

    // Comenzar la prueba
    await page.getByRole('button', { name: 'Comenzar' }).click();
    await expect(page.locator('.pregunta__enunciado')).toBeVisible();

    // Responder la primera pregunta (abierta o alternativa)
    const textarea = page.locator('textarea.respuesta-abierta');
    if (await textarea.isVisible()) {
      await textarea.fill('Respuesta de prueba 7 basico');
    } else {
      await page.locator('.opcion').first().click();
    }

    // Finalizar intento
    await page.getByRole('button', { name: 'Finalizar intento' }).click();

    // Confirmar envío en el modal de preguntas incompletas
    await page.getByRole('button', { name: 'Enviar de todas formas' }).click();

    // Validar pantalla de resultado con nota calculada por el backend
    await expect(page.locator('.resultado')).toBeVisible();
    await expect(page.locator('.resultado__nota')).toContainText('Nota:');

    // Botón volver a evaluaciones
    await page.getByRole('button', { name: 'Volver' }).click();
    await expect(page).toHaveURL(/alumno\/evaluaciones/);
  });

  test('6. Rendición completa de Examen Simulacro de 7° Básico (Régimen B: 25 preguntas)', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type=email]', EMAIL_APODERADO);
    await page.fill('input[type=password]', PASSWORD_PRUEBA);
    await page.click('button[type=submit]');
    await page.waitForURL('**/selector-perfil');
    await page.getByText(NOMBRE_ALUMNO).click();
    await expect(page).toHaveURL(/alumno\/inicio/);

    // Ir a evaluaciones
    await page.goto('/alumno/evaluaciones');
    await expect(page).toHaveURL(/alumno\/evaluaciones/);

    // Ubicar examen simulacro (en Régimen B tiene 25 preguntas por examen)
    const examenCard = page.locator('.conjunto-card--examen').first();
    await expect(examenCard).toContainText('25 preguntas');

    const examenBoton = examenCard.locator('.conjunto-card__boton');
    await examenBoton.click();
    await expect(page).toHaveURL(/examen\/\d+/);

    // Comenzar el examen simulacro
    await page.getByRole('button', { name: 'Comenzar' }).click();
    await expect(page.locator('.pregunta__enunciado')).toBeVisible();
    await expect(page.locator('.runner__cronometro')).toBeVisible();

    // Responder la primera pregunta
    const textarea = page.locator('textarea.respuesta-abierta');
    if (await textarea.isVisible()) {
      await textarea.fill('Respuesta de examen 7 basico');
    } else {
      await page.locator('.opcion').first().click();
    }

    // Finalizar examen
    await page.getByRole('button', { name: 'Finalizar intento' }).click();

    // Confirmar entrega en el modal
    await page.getByRole('button', { name: 'Enviar de todas formas' }).click();

    // Validar pantalla de resultado con nota oficial calculada
    await expect(page.locator('.resultado')).toBeVisible();
    await expect(page.locator('.resultado__nota')).toContainText('Nota:');
  });

  test('7. Plan de Estudio, Historial de Notas y Gamificación (XP)', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type=email]', EMAIL_APODERADO);
    await page.fill('input[type=password]', PASSWORD_PRUEBA);
    await page.click('button[type=submit]');
    await page.waitForURL('**/selector-perfil');
    await page.getByText(NOMBRE_ALUMNO).click();
    await expect(page).toHaveURL(/alumno\/inicio/);

    // 7.1 Plan de estudio
    await page.goto('/alumno/plan-estudio');
    await expect(page).toHaveURL(/alumno\/plan-estudio/);
    await expect(page.locator('h1')).toContainText('Plan de Estudio');

    // 7.2 Mis Notas: deben reflejar las evaluaciones rendidas
    await page.goto('/alumno/notas');
    await expect(page).toHaveURL(/alumno\/notas/);
    await expect(page.locator('h1')).toContainText('Mis Notas');
    await expect(page.locator('.fila-historial, .prediccion, table').first()).toBeVisible();

    // 7.3 Mis Logros: XP acumulada y cambio de avatar
    await page.goto('/alumno/logros');
    await expect(page).toHaveURL(/alumno\/logros/);
    await expect(page.locator('h1')).toContainText('Mis Logros');
    await expect(page.locator('.resumen__xp')).toBeVisible();

    // Seleccionar otro avatar
    const opcionAvatar = page.locator('.avatar-opcion').nth(2);
    if (await opcionAvatar.isVisible()) {
      await opcionAvatar.click();
    }

    // 7.4 Plan Lector y Útiles Escolares
    await page.goto('/alumno/plan-lector');
    await expect(page).toHaveURL(/alumno\/plan-lector/);
    await expect(page.locator('h1')).toContainText('Plan Lector');

    await page.goto('/alumno/utiles-escolares');
    await expect(page).toHaveURL(/alumno\/utiles-escolares/);
    await expect(page.locator('h1')).toContainText('Útiles Escolares');
  });
});
