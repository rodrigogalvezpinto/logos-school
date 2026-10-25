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
const EMAIL_APODERADO = `apoderado.1medio.${timestamp}@logos.cl`;
const PASSWORD_PRUEBA = 'LogosMedio2026!';
const NOMBRE_APODERADO = 'Andrea Morales (Apoderada 1° Medio)';
const NOMBRE_ALUMNO = 'Ignacio';
const APELLIDOS_ALUMNO = 'Morales Silva';
const RUT_ALUMNO = rutValidoUnico();

test.describe.serial('Validación de flujo real: Apoderado y Alumno de 1° Medio', () => {
  test('1. Registro completo de Apoderado y alta de Alumno en 1° Medio', async ({ page }) => {
    const errores = capturarErroresConsola(page);

    // 1.1 Registro de Apoderado
    await page.goto('/registro');
    await expect(page).toHaveURL(/registro/);
    await page.fill('input[name=nombre]', NOMBRE_APODERADO);
    await page.fill('input[name=email]', EMAIL_APODERADO);
    await page.fill('input[name=password]', PASSWORD_PRUEBA);
    await page.click('button[type=submit]');

    // 1.2 Onboarding: Agregar primer alumno en 1° medio
    await expect(page).toHaveURL(/agregar-alumno/);
    await page.fill('input[name=nombre]', NOMBRE_ALUMNO);
    await page.fill('input[name=apellidos]', APELLIDOS_ALUMNO);
    await page.fill('input[name=fechaNacimiento]', '2011-04-18');
    await page.fill('input[name=rut]', RUT_ALUMNO);

    // Selección específica del nivel "1° medio"
    const selectNivel = page.locator('select[name=nivelId]');
    await selectNivel.selectOption({ label: '1° medio' });

    // Días de estudio vienen por defecto (Lun, Mié, Vie = 3 días)
    await page.click('button[type=submit]');

    // 1.3 Selección de Plan para el alumno
    await expect(page).toHaveURL(/seleccion-plan/);
    await expect(page.locator('h1')).toContainText(NOMBRE_ALUMNO);
    await page.click('button:has-text("Comenzar mis 5 días gratis")');

    // 1.4 Selector de perfil
    await expect(page).toHaveURL(/selector-perfil/);
    await expect(page.getByText(NOMBRE_ALUMNO)).toBeVisible();
    await expect(page.getByText('Ver como Apoderado')).toBeVisible();

    expect(errores, `Errores de consola: ${errores.join(', ')}`).toEqual([]);
  });

  test('2. Flujo del Apoderado: Dashboard, Alumno en 1° Medio y gestión familiar', async ({ page }) => {
    // Iniciar sesión y entrar como apoderado
    await page.goto('/login');
    await page.fill('input[type=email]', EMAIL_APODERADO);
    await page.fill('input[type=password]', PASSWORD_PRUEBA);
    await page.click('button[type=submit]');
    await page.waitForURL('**/selector-perfil');

    // Entrar como apoderado
    await page.getByText('Ver como Apoderado').click();
    await expect(page).toHaveURL(/apoderado\/inicio/);

    // Verificar panel del apoderado
    await expect(page.locator('h1')).toContainText('Hola');
    const alumnoCard = page.locator('.alumno-card', { hasText: `${NOMBRE_ALUMNO} ${APELLIDOS_ALUMNO}` });
    await expect(alumnoCard).toBeVisible();
    await expect(alumnoCard.locator('.chip--activo')).toContainText('Plan activo');

    // Navegación a Historial de planes / pagos
    await page.goto('/apoderado/plan');
    await expect(page).toHaveURL(/apoderado\/plan/);
    await expect(page.locator('h1')).toContainText('Plan y Pagos');

    // Navegación a Estadísticas familiares
    await page.goto('/apoderado/estadisticas');
    await expect(page).toHaveURL(/apoderado\/estadisticas/);
    await expect(page.locator('h1')).toContainText('Estadísticas');

    // Navegación a Configuración del apoderado
    await page.goto('/apoderado/configuracion');
    await expect(page).toHaveURL(/apoderado\/configuracion/);
    await expect(page.locator('h1')).toContainText('Configuración');
  });

  test('3. Flujo del Alumno: Inicio y Asignaturas Oficiales de 1° Medio (Decreto 614/2013)', async ({ page }) => {
    // Iniciar sesión y entrar como Ignacio
    await page.goto('/login');
    await page.fill('input[type=email]', EMAIL_APODERADO);
    await page.fill('input[type=password]', PASSWORD_PRUEBA);
    await page.click('button[type=submit]');
    await page.waitForURL('**/selector-perfil');

    await page.getByText(NOMBRE_ALUMNO).click();
    await expect(page).toHaveURL(/alumno\/inicio/);

    // Gestionar check-in emocional diario si aparece
    const checkin = page.locator('.checkin__opcion', { hasText: 'Tranquilo' });
    try {
      await checkin.waitFor({ state: 'visible', timeout: 3000 });
      await checkin.click();
    } catch {
      // Ya respondido o no presente
    }

    // Saludo personalizado al alumno
    await expect(page.locator('h1')).toContainText(NOMBRE_ALUMNO);

    // Contador de prueba gratuita
    await expect(page.locator('.aviso-prueba')).toContainText('5 días');

    // Ir a Mis Asignaturas
    await page.goto('/alumno/asignaturas');
    await expect(page).toHaveURL(/alumno\/asignaturas/);
    await expect(page.locator('h1')).toContainText('Mis Asignaturas');

    // Verificar las 5 asignaturas oficiales de 1° medio
    const nombresAsignaturas = await page.locator('.asignatura-card h3').allTextContents();
    
    // En 1° medio la materia oficial es "Lengua y Literatura" (no "Lenguaje y Comunicación")
    expect(nombresAsignaturas).toContain('Lengua y Literatura');
    expect(nombresAsignaturas).toContain('Matemática');
    expect(nombresAsignaturas).toContain('Ciencias Naturales');
    expect(nombresAsignaturas).toContain('Historia, Geografía y Cs. Sociales');
    expect(nombresAsignaturas).toContain('Inglés');
    expect(nombresAsignaturas.length).toBeGreaterThanOrEqual(5);
  });

  test('4. Flujo Pedagógico: Ruta de aprendizaje, Guía de Estudio y Autoevaluación', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type=email]', EMAIL_APODERADO);
    await page.fill('input[type=password]', PASSWORD_PRUEBA);
    await page.click('button[type=submit]');
    await page.waitForURL('**/selector-perfil');
    await page.getByText(NOMBRE_ALUMNO).click();
    await expect(page).toHaveURL(/alumno\/inicio/);

    // Ir a asignaturas y entrar a Lengua y Literatura
    await page.goto('/alumno/asignaturas');
    await page.locator('.asignatura-card', { hasText: 'Lengua y Literatura' }).click();
    await expect(page).toHaveURL(/asignaturas\/\d+/);

    // Verificar cabecera y lista de OA de 1° medio
    await expect(page.locator('h1')).toContainText('Lengua y Literatura');
    const oaCards = page.locator('.oa-card');
    await expect(oaCards.first()).toBeVisible();

    // Entrar a estudiar la primera guía
    await page.getByRole('link', { name: 'Estudiar guía' }).first().click();
    await expect(page).toHaveURL(/estudiar\/\d+/);

    // Validar contenido pedagógico
    const contenido = page.locator('.contenido-guia');
    await expect(contenido).not.toBeEmpty();
    // Debe renderizarse como HTML con etiquetas estructuradas
    await expect(contenido.locator('h1, h2, h3, p')).not.toHaveCount(0);
    // No debe contener markdown crudo sin procesar
    await expect(contenido).not.toContainText('###');

    // Controles de apoyo al estudiante
    await expect(page.getByRole('button', { name: '🔊 Escuchar' })).toBeVisible();
    await expect(page.locator('.descargar-pdf')).toBeVisible();

    // Calificar la guía pedagógica
    const estrella5 = page.locator('.calificar-guia__estrella').nth(4);
    await estrella5.click();
    await expect(page.locator('.calificar-guia__gracias')).toContainText('¡Gracias por tu opinión!');

    // Continuar a la práctica interactiva
    await page.getByRole('link', { name: 'Ya entendí, quiero practicar →' }).click();
    await expect(page).toHaveURL(/autoevaluacion\/\d+/);

    // Iniciar la autoevaluación
    await page.getByRole('button', { name: 'Comenzar' }).click();
    await expect(page.locator('.pregunta__enunciado')).not.toBeEmpty();
    await expect(page.getByRole('button', { name: '🔊 Escuchar' })).toBeVisible();

    // Responder la primera pregunta (en 1° medio puede ser de desarrollo o alternativas)
    const textarea = page.locator('textarea.respuesta-abierta');
    if (await textarea.isVisible()) {
      await textarea.fill('El padre busca estabilidad económica mientras el abuelo apoya su vocación artística.');
      await expect(textarea).toHaveValue(/estabilidad/);
    } else {
      const primeraOpcion = page.locator('.opcion').first();
      await expect(primeraOpcion).toBeVisible();
      await primeraOpcion.click();
      await expect(page.locator('.feedback')).toBeVisible();
    }
  });

  test('5. Plan de Estudio y Evaluaciones Oficiales de 1° Medio', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[type=email]', EMAIL_APODERADO);
    await page.fill('input[type=password]', PASSWORD_PRUEBA);
    await page.click('button[type=submit]');
    await page.waitForURL('**/selector-perfil');
    await page.getByText(NOMBRE_ALUMNO).click();
    await expect(page).toHaveURL(/alumno\/inicio/);

    // 5.1 Plan de Estudio de 1° medio
    await page.goto('/alumno/plan-estudio');
    await expect(page).toHaveURL(/alumno\/plan-estudio/);
    await expect(page.locator('h1')).toContainText('Plan de Estudio');

    // 5.2 Evaluaciones de 1° medio
    await page.goto('/alumno/evaluaciones');
    await expect(page).toHaveURL(/alumno\/evaluaciones/);
    await expect(page.locator('h1')).toContainText('Pruebas y Exámenes');

    // Debe mostrar pruebas de unidad y exámenes simulacro
    await expect(page.locator('.conjunto-card').first()).toBeVisible();
    const examenCard = page.locator('.conjunto-card--examen').first();
    await expect(examenCard).toBeVisible();

    // Validar especificación de examen de 1° medio (25 preguntas según decreto 614/2013)
    await expect(examenCard).toContainText('25 preguntas');

    // 5.3 Notas e Informe
    await page.goto('/alumno/notas');
    await expect(page).toHaveURL(/alumno\/notas/);
    await expect(page.locator('h1')).toContainText('Mis Notas');
    await expect(page.getByRole('button', { name: '⬇ Descargar informe en PDF' })).toBeVisible();

    // 5.4 Plan Lector
    await page.goto('/alumno/plan-lector');
    await expect(page).toHaveURL(/alumno\/plan-lector/);
    await expect(page.locator('h1')).toContainText('Plan Lector');

    // 5.5 Útiles Escolares
    await page.goto('/alumno/utiles-escolares');
    await expect(page).toHaveURL(/alumno\/utiles-escolares/);
    await expect(page.locator('h1')).toContainText('Útiles Escolares');
  });
});
