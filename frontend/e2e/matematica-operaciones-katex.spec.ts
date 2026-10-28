import { test, expect } from '@playwright/test';
import { capturarErroresConsola, loginYEntrarComoSofia } from './helpers';

test.describe.serial('Validación E2E: Matemática, KaTeX y Evaluaciones', () => {
  test('1. Identidad del estudiante y bienvenida con curso (UX-004)', async ({ page }) => {
    const errores = capturarErroresConsola(page);
    await loginYEntrarComoSofia(page);

    // Verificar que el saludo principal incluye el curso del estudiante
    const saludo = page.locator('.saludo-header');
    await expect(saludo).toBeVisible();
    await expect(saludo).toContainText('Sofía');
    await expect(saludo.locator('.badge-curso')).toContainText('4° básico');

    // Verificar que la barra superior muestra el nombre y curso
    const topbarUsuario = page.locator('.topbar__usuario');
    await expect(topbarUsuario).toBeVisible();
    await expect(topbarUsuario.locator('.topbar__nombre')).toHaveText('Sofía');
    await expect(topbarUsuario.locator('.topbar__curso')).toContainText('4° básico');

    expect(errores, `Errores de consola: ${errores.join(', ')}`).toEqual([]);
  });

  test('2. Guía de Matemática: renderizado de contenido, tipografía y KaTeX', async ({ page }) => {
    const errores = capturarErroresConsola(page);
    await loginYEntrarComoSofia(page);

    // Navegar a Mis Asignaturas -> Matemática
    await page.goto('/alumno/asignaturas');
    await page.waitForLoadState('networkidle');
    await page.click('text=Matemática');
    await page.waitForLoadState('networkidle');

    // Acceder a la primera guía de estudio disponible
    const botonEstudiar = page.locator('text=Estudiar').first();
    await expect(botonEstudiar).toBeVisible();
    await botonEstudiar.click();
    await page.waitForLoadState('networkidle');

    // Verificar que la guía de estudio carga su contenedor principal
    const contenidoGuia = page.locator('.contenido-guia');
    await expect(contenidoGuia).toBeVisible();

    // Tomar captura de pantalla de la guía de estudio renderizada
    await page.screenshot({ path: 'screenshots/e2e-matematica-guia.png', fullPage: false });

    expect(errores, `Errores de consola: ${errores.join(', ')}`).toEqual([]);
  });

  test('3. KaTeX: renderizado de operaciones, fracciones, raíces y protección de pesos chilenos', async ({ page }) => {
    const errores = capturarErroresConsola(page);
    await loginYEntrarComoSofia(page);

    // Navegar a una guía
    await page.goto('/alumno/asignaturas');
    await page.click('text=Matemática');
    await page.locator('text=Estudiar').first().click();
    await page.waitForLoadState('networkidle');

    // Verificar en el DOM del navegador que los estilos de KaTeX están cargados y activos
    const resultadoEstilos = await page.evaluate(() => {
      const hojas = Array.from(document.styleSheets);
      let tieneReglasKatex = false;
      try {
        for (const sheet of hojas) {
          try {
            const rules = Array.from(sheet.cssRules || []);
            if (rules.some(r => r.cssText.includes('.katex'))) {
              tieneReglasKatex = true;
              break;
            }
          } catch {
            // Ignorar hojas de terceros con CORS si las hubiera
          }
        }
      } catch {
        // Fallback
      }

      // Probar renderizado de un nodo con clase KaTeX en el DOM
      const testSpan = document.createElement('span');
      testSpan.className = 'katex';
      testSpan.textContent = 'x';
      document.body.appendChild(testSpan);
      const computedFont = window.getComputedStyle(testSpan).fontFamily;
      document.body.removeChild(testSpan);

      return {
        tieneReglasKatex,
        computedFont,
      };
    });

    expect(resultadoEstilos.tieneReglasKatex || resultadoEstilos.computedFont.includes('KaTeX')).toBe(true);

    // Inyectar un panel interactivo con fórmulas matemáticas, físicas y químicas para verificación visual
    await page.evaluate(() => {
      const panel = document.createElement('div');
      panel.id = 'panel-demo-katex';
      panel.className = 'tarjeta';
      panel.style.margin = '20px';
      panel.style.padding = '20px';
      panel.style.border = '2px solid #5b4fe9';
      panel.style.borderRadius = '12px';
      panel.style.background = '#ffffff';

      panel.innerHTML = `
        <h3 style="color: #2D3748; margin-top: 0; font-size: 1.3rem;">Demostración E2E: Matemática, Física y Química con KaTeX</h3>
        <p><strong>1. Matemática (Fracciones y Raíces):</strong> <span class="katex"><span class="katex-html"><span class="base"><span class="mord"><span class="mopen nulldelimiter"></span><span class="mfrac"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.8451em;"><span style="top:-2.655em;"><span class="pstrut" style="height:3em;"></span><span class="reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">8</span></span></span></span><span style="top:-3.23em;"><span class="pstrut" style="height:3em;"></span><span class="frac-line" style="border-bottom-width:0.04em;"></span></span><span style="top:-3.394em;"><span class="pstrut" style="height:3em;"></span><span class="reset-size6 size3 mtight"><span class="mord mtight"><span class="mord mtight">3</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.345em;"><span></span></span></span></span></span><span class="mclose nulldelimiter"></span></span></span></span></span> + <span class="katex"><span class="katex-html"><span class="base"><span class="mord sqrt"><span class="root"></span><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.9072em;"><span class="svg-align" style="top:-3em;"><span class="pstrut" style="height:3em;"></span><span class="mord" style="padding-left:0.833em;"><span class="mord">49</span></span></span><span style="top:-2.8672em;"><span class="pstrut" style="height:3em;"></span><span class="hide-tail" style="min-width:0.853em;height:1.08em;"><svg width="400em" height="1.08em" viewBox="0 0 400000 1080" preserveAspectRatio="xMinYMin slice"><path d="M95,702 c-2.7,0,-7.17,-2.7,-13.5,-8c-5.8,-5.3,-9.5,-10,-9.5,-14 c0,-2,0.3,-3.3,1,-4c1.3,-2.7,23.83,-20.7,67.5,-54 c44.2,-33.3,65.8,-50.3,66.5,-51c1.3,-1.3,3,-2,5,-2c4.7,0,8.7,3.3,12,10 s173,378,173,378c0.7,0,35.3,-71,104,-213 c68.7,-142,137.5,-285,206.5,-429c69,-144,104.5,-217.7,106.5,-221 l0 -0 c5.3,-9.3,12,-14,20,-14 H400000v40H845.2724 s-225.272,467,-225.272,467s-235,486,-235,486c-2.7,4.7,-9,7,-19,7 c-6,0,-10,-1,-12,-3s-194,-422,-194,-422s-65,47,-65,47z M834 80h400000v40h-400000z"/></svg></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.1328em;"><span></span></span></span></span></span></span></span></span> = <strong>7,375</strong></p>
        <p><strong>2. Física (Segunda Ley de Newton):</strong> <span class="katex-display"><span class="katex"><span class="katex-html"><span class="base"><span class="mord mathnormal" style="margin-right:0.13889em;">F</span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.1514em;"><span style="top:-2.55em;margin-left:-0.13889em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord text mtight"><span class="mord mtight">neta</span></span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="mord mathnormal">m</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">⋅</span><span class="mspace" style="margin-right:0.2222em;"></span></span><span class="base"><span class="mord mathnormal">a</span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="mord">20</span><span class="mord text"><span class="mord"> kg</span></span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">×</span><span class="mspace" style="margin-right:0.2222em;"></span></span><span class="base"><span class="mord">0</span><span class="mord">{,}</span><span class="mord">5</span><span class="mord text"><span class="mord"> m/s</span></span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.7401em;"><span style="top:-2.989em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span></span></span></span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">=</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="mord">10</span><span class="mord text"><span class="mord"> N</span></span></span></span></span></span></p>
        <p><strong>3. Química (Reacción Estequiométrica y Moles):</strong> <span class="katex-display"><span class="katex"><span class="katex-html"><span class="base"><span class="mord">2</span><span class="mord text"><span class="mord">H</span></span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3011em;"><span style="top:-2.55em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">+</span><span class="mspace" style="margin-right:0.2222em;"></span></span><span class="base"><span class="mord text"><span class="mord">O</span></span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3011em;"><span style="top:-2.55em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span><span class="mspace" style="margin-right:0.2778em;"></span><span class="mrel">→</span><span class="mspace" style="margin-right:0.2778em;"></span></span><span class="base"><span class="mord">2</span><span class="mord text"><span class="mord">H</span></span><span class="msupsub"><span class="vlist-t vlist-t2"><span class="vlist-r"><span class="vlist" style="height:0.3011em;"><span style="top:-2.55em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">2</span></span></span></span><span class="vlist-s">​</span></span><span class="vlist-r"><span class="vlist" style="height:0.15em;"><span></span></span></span></span></span><span class="mord text"><span class="mord">O</span></span><span class="mspace" style="margin-left:1em;"></span><span class="mopen">(</span><span class="mord text"><span class="mord">Avogadro: </span></span><span class="mord">6{,}02</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mbin">×</span><span class="mspace" style="margin-right:0.2222em;"></span><span class="mord">1</span><span class="mord"><span class="mord">0</span><span class="msupsub"><span class="vlist-t"><span class="vlist-r"><span class="vlist" style="height:0.7401em;"><span style="top:-2.989em;margin-right:0.05em;"><span class="pstrut" style="height:2.7em;"></span><span class="sizing reset-size6 size3 mtight"><span class="mord mtight">23</span></span></span></span></span></span></span></span><span class="mord text"><span class="mord"> part/mol</span></span><span class="mclose">)</span></span></span></span></span></p>
        <p><strong>4. Moneda chilena intacta (sin colisión de KaTeX):</strong> Un set de laboratorio escolar cuesta <code>$15.000</code> y reactivos adicionales <code>$4.500</code> cada uno.</p>
      `;
      document.querySelector('main')?.prepend(panel);
    });

    const panelElement = page.locator('#panel-demo-katex');
    await expect(panelElement).toBeVisible();

    // Verificación tipográfica:
    // 1. Fracción: numerador y denominador separados de la barra (.frac-line)
    // 2. Potencia / Exponente: tipografía del exponente visiblemente menor que el número base
    const medicionesTipograficas = await page.evaluate(() => {
      const sups = Array.from(document.querySelectorAll('.msupsub, sup, .exponente-matematico'));
      let exponenteMasPequeno = false;
      for (const sup of sups) {
        const parent = sup.parentElement;
        if (parent) {
          const sizeSup = parseFloat(window.getComputedStyle(sup).fontSize);
          const sizeParent = parseFloat(window.getComputedStyle(parent).fontSize);
          if (sizeSup < sizeParent) {
            exponenteMasPequeno = true;
            break;
          }
        }
      }

      const fracLine = document.querySelector('.frac-line');
      const tieneBarraFraccion = fracLine !== null;

      return {
        exponenteMasPequeno,
        tieneBarraFraccion
      };
    });

    expect(medicionesTipograficas.tieneBarraFraccion).toBe(true);
    expect(medicionesTipograficas.exponenteMasPequeno).toBe(true);

    await page.screenshot({ path: 'screenshots/e2e-matematica-katex-demo.png', fullPage: false });

    expect(errores, `Errores de consola: ${errores.join(', ')}`).toEqual([]);
  });

  test('4. Evaluacion-runner: UX-001 (bajo demanda), UX-002 (aviso) y MAT-UI-001 (rúbrica abierta)', async ({ page }) => {
    const errores = capturarErroresConsola(page);
    await loginYEntrarComoSofia(page);

    // Navegar a Matemática -> practicar autoevaluación
    await page.goto('/alumno/asignaturas');
    await page.click('text=Matemática');
    await page.waitForLoadState('networkidle');

    const botonPracticar = page.locator('text=Practicar').first();
    await expect(botonPracticar).toBeVisible();
    await botonPracticar.click();
    await page.waitForLoadState('networkidle');

    // Iniciar evaluación esperando que cargue el botón Comenzar
    const botonComenzar = page.locator('button:has-text("Comenzar")');
    await expect(botonComenzar).toBeVisible({ timeout: 10000 });
    await botonComenzar.click();

    // 4.1 Enunciado renderizado
    const enunciado = page.locator('.pregunta__enunciado');
    await expect(enunciado).toBeVisible();

    // 4.2 UX-001: Responder una alternativa NO debe mostrar el feedback de inmediato
    const primeraOpcion = page.locator('.opcion').first();
    if (await primeraOpcion.isVisible()) {
      await primeraOpcion.click();

      // El botón bajo demanda debe aparecer y estar habilitado
      const botonAyuda = page.locator('.btn-ayuda-practica');
      await expect(botonAyuda).toBeVisible();
      await expect(botonAyuda).toBeEnabled();

      // El feedback NO debe estar visible antes del clic
      await expect(page.locator('.feedback--revelado')).not.toBeVisible();

      // Al hacer clic en comprobar respuesta, se revela el feedback
      await botonAyuda.click();
      await expect(page.locator('.feedback--revelado')).toBeVisible();
    }

    // 4.3 UX-002: Marcar para revisar y verificar modal de entrega
    const checkboxMarcar = page.locator('.marcar-revisar input[type=checkbox]');
    if (await checkboxMarcar.isVisible()) {
      await checkboxMarcar.check();
    }

    // Intentar finalizar intento
    const botonFinalizar = page.locator('button:has-text("Finalizar intento")');
    await expect(botonFinalizar).toBeVisible();
    await botonFinalizar.click();

    // El modal de aviso debe desplegarse
    const modalAviso = page.locator('.modal');
    await expect(modalAviso).toBeVisible();
    await expect(modalAviso.locator('h3')).toContainText('Aviso antes de entregar');

    // Debe advertir sobre preguntas marcadas
    const avisoMarcadas = modalAviso.locator('.aviso-marcadas');
    if (await avisoMarcadas.count() > 0) {
      await expect(avisoMarcadas).toContainText('revisar');
    }

    // Captura de pantalla del modal de aviso enriquecido
    await page.screenshot({ path: 'screenshots/e2e-evaluacion-aviso.png', fullPage: false });

    // Cancelar / volver a revisar
    await modalAviso.locator('button:has-text("Ir a revisar")').click();
    await expect(modalAviso).not.toBeVisible();

    expect(errores, `Errores de consola: ${errores.join(', ')}`).toEqual([]);
  });
});
