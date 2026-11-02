import { test, expect, Page } from '@playwright/test';
import { AxeBuilder } from '@axe-core/playwright';
import { API_URL, CREDENCIALES_PRUEBA, capturarErroresConsola } from './helpers';

/** Regresión E2E del panel "Practica la pronunciación en inglés"
 * (shared/pronunciacion-ingles/pronunciacion-ingles.ts), visible solo en guías de la
 * asignatura Inglés. Perfil: Mateo (6° básico) de la cuenta de prueba existente.
 *
 * Motor REAL: los tests reenvían speechSynthesis.speak nativo (sin mock) y registran
 * getVoices + eventos start/end/error en window.__logTts. Las aserciones se ramifican
 * según haya o no una voz inglesa LOCAL en el dispositivo:
 *  - con voz local: la app debe hablar con voz en-* localService y tasa correcta;
 *  - sin voz local: la app debe mostrar el aviso "sin voz" y NO llamar a speak.
 * Ninguna rama aprueba una prueba acústica humana — se verifica el contrato del motor.
 */

type UtteranceRegistrada = { text: string; lang: string; rate: number; voice: string | null; voiceLocal: boolean | null };
type LogTts = { voces: { name: string; lang: string; localService: boolean }[]; habladas: UtteranceRegistrada[]; eventos: string[]; cancelaciones: number };

declare global {
  interface Window { __logTts?: LogTts }
}

let token = '';
let perfilMateo: { id: number; nombre: string; nivel_id: number } | null = null;
let oaInglesId = 0;

async function entrarComoMateo(page: Page) {
  if (!token) {
    const login = await page.request.post(`${API_URL}/auth/login`, { data: CREDENCIALES_PRUEBA });
    expect(login.status(), 'Login de la cuenta de prueba existente').toBe(200);
    token = (await login.json()).access_token;
    const perfiles = await page.request.get(`${API_URL}/auth/alumnos`, { headers: { Authorization: `Bearer ${token}` } });
    expect(perfiles.status()).toBe(200);
    const lista: { id: number; nombre: string; nivel_id: number }[] = await perfiles.json();
    perfilMateo = lista.find((p) => p.nombre === 'Mateo') ?? null;
    expect(perfilMateo, 'La cuenta de prueba debe incluir el perfil Mateo (6° básico)').toBeTruthy();
  }
  await page.goto('/login');
  await page.evaluate(({ t, p }) => {
    localStorage.setItem('logos_token', t);
    localStorage.setItem('logos_perfil_activo', JSON.stringify(p));
    localStorage.setItem('logos_nombre_apoderado', 'Apoderado de prueba');
  }, { t: token, p: perfilMateo });
}

async function instrumentarVoz(page: Page) {
  await page.addInitScript(() => {
    const log: LogTts = { voces: [], habladas: [], eventos: [], cancelaciones: 0 };
    window.__logTts = log;
    const s = window.speechSynthesis;
    if (!s) return;
    const cancelNativo = s.cancel.bind(s);
    s.cancel = () => { log.cancelaciones++; cancelNativo(); };
    const getVoicesNativo = s.getVoices.bind(s);
    s.getVoices = () => {
      const v = getVoicesNativo();
      log.voces = v.map((x) => ({ name: x.name, lang: x.lang, localService: x.localService }));
      return v;
    };
    const speakNativo = s.speak.bind(s);
    s.speak = (u: SpeechSynthesisUtterance) => {
      log.habladas.push({
        text: u.text, lang: u.lang, rate: u.rate,
        voice: u.voice ? u.voice.name : null,
        voiceLocal: u.voice ? u.voice.localService : null,
      });
      for (const ev of ['start', 'end', 'error'] as const) {
        const prev = (u as unknown as Record<string, unknown>)[`on${ev}`];
        (u as unknown as Record<string, unknown>)[`on${ev}`] = (e: unknown) => {
          log.eventos.push(ev);
          if (typeof prev === 'function') (prev as (e: unknown) => void)(e);
        };
      }
      speakNativo(u);
    };
  });
}

async function logTts(page: Page): Promise<LogTts> {
  return page.evaluate(() => window.__logTts ?? { voces: [], habladas: [], eventos: [], cancelaciones: 0 });
}

test.describe.serial('Panel de pronunciación en inglés (motor TTS real, perfil Mateo 6°B)', () => {
  test.beforeEach(async ({ page }) => {
    await instrumentarVoz(page);
    await entrarComoMateo(page);
    if (!oaInglesId) {
      const headers = { Authorization: `Bearer ${token}` };
      const asignaturas = await page.request.get(`${API_URL}/contenido/niveles/${perfilMateo!.nivel_id}/asignaturas`);
      expect(asignaturas.status()).toBe(200);
      const lista: { id: number; nombre: string }[] = await asignaturas.json();
      const ingles = lista.find((a) => a.nombre.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase().includes('ingles'));
      expect(ingles, '6° básico debe tener asignatura Inglés').toBeTruthy();
      const objetivos = await page.request.get(`${API_URL}/contenido/asignaturas/${ingles!.id}/objetivos`);
      expect(objetivos.status()).toBe(200);
      const oas: { id: number }[] = await objetivos.json();
      expect(oas.length).toBeGreaterThan(0);
      oaInglesId = oas[0].id;
    }
    await page.goto(`/alumno/estudiar/${oaInglesId}`);
    await expect(page.locator('app-pronunciacion-ingles .pronunciacion')).toBeVisible();
  });

  test('estructura, límites de texto y teclado', async ({ page }) => {
    const errores = capturarErroresConsola(page);
    const campo = page.locator('.pronunciacion__campo');
    const estado = page.locator('.pronunciacion__estado');
    const escuchar = page.getByRole('button', { name: 'Escuchar en inglés' });
    const repetir = page.getByRole('button', { name: 'Repetir' });
    const detener = page.getByRole('button', { name: 'Detener' });

    // Etiquetado accesible y campo en inglés
    await expect(page.locator('.pronunciacion__etiqueta')).toHaveAttribute('for', await campo.getAttribute('id') ?? '');
    await expect(campo).toHaveAttribute('lang', 'en');
    await expect(campo).toHaveAttribute('maxlength', '120');
    await expect(estado).toHaveAttribute('aria-live', 'polite');
    await expect(repetir).toBeDisabled();
    await expect(detener).toBeDisabled();

    // Vacío → aviso sin hablar
    await escuchar.click();
    await expect(estado).toContainText('Escribe o pega primero');

    // >20 palabras → aviso sin hablar
    await campo.fill(Array.from({ length: 21 }, () => 'word').join(' '));
    await escuchar.click();
    await expect(estado).toContainText('máximo 20 palabras');
    let log = await logTts(page);
    expect(log.habladas.length, 'No debe llamar a speak con texto inválido').toBe(0);

    // Enter en el campo equivale al botón Escuchar
    await campo.fill('good morning');
    await campo.press('Enter');
    await expect(estado).not.toContainText('máximo 20 palabras');
    log = await logTts(page);
    if (log.habladas.length > 0) {
      expect(log.habladas[0].text).toBe('good morning');
      expect(log.habladas[0].lang.toLowerCase().startsWith('en')).toBeTruthy();
      expect(log.habladas[0].voiceLocal).toBe(true);
      expect(log.habladas[0].rate).toBe(1);
    } else {
      await expect(estado).toContainText('No encontramos una voz en inglés');
    }
    expect(errores, `Errores de consola: ${errores.join(', ')}`).toEqual([]);
  });

  test('velocidad lenta, repetir y detener con el motor nativo', async ({ page }) => {
    const campo = page.locator('.pronunciacion__campo');
    const estado = page.locator('.pronunciacion__estado');
    const escuchar = page.getByRole('button', { name: 'Escuchar en inglés' });
    const repetir = page.getByRole('button', { name: 'Repetir' });
    const detener = page.getByRole('button', { name: 'Detener' });
    await expect(page.locator('.pronunciacion__velocidad legend')).toHaveText('Velocidad');

    // Frase de 20 palabras a velocidad lenta para maximizar la ventana de síntesis activa.
    const fraseLarga = Array.from({ length: 20 }, (_, i) => `word${i}`).join(' ');
    await campo.fill(fraseLarga);
    await page.locator('.pronunciacion__velocidad label', { hasText: 'Lenta' }).click();
    await escuchar.click();

    let log = await logTts(page);
    if (log.habladas.length === 0) {
      // Rama sin voz inglesa local: Repetir nunca se habilita y el aviso es claro.
      await expect(estado).toContainText('No encontramos una voz en inglés');
      await expect(repetir).toBeDisabled();
      return;
    }
    expect(log.habladas[0].rate).toBeCloseTo(0.7, 5);
    expect(log.habladas[0].lang.toLowerCase().startsWith('en')).toBeTruthy();
    expect(log.habladas[0].voiceLocal).toBe(true);
    await expect(estado).toContainText('Reproduciendo en inglés');

    // Detener/cancelación con el motor nativo: cada nuevo leer() llama detener() →
    // speechSynthesis.cancel() antes de hablar de nuevo — observable sin depender del
    // timing de los eventos end/error (que en Chromium headless son erráticos: a veces
    // llegan al instante, a veces el utterance queda "speaking" decenas de segundos).
    await campo.fill('thank you very much');
    await escuchar.click();
    log = await logTts(page);
    expect(log.habladas.length).toBe(2);
    expect(log.cancelaciones, 'El segundo Escuchar debe cancelar la síntesis previa').toBeGreaterThanOrEqual(1);

    // Repetir reutiliza la última frase aunque el campo cambie
    await campo.fill('otra cosa');
    await repetir.click();
    log = await logTts(page);
    expect(log.habladas.length).toBe(3);
    expect(log.habladas[2].text).toBe('thank you very much');
    expect(log.habladas[2].rate).toBeCloseTo(0.7, 5);

    // Estado final: si el último utterance sigue activo, Detener está habilitado y se
    // ejerce el click real (cancel + anuncio). Si el motor ya terminó, el botón debe
    // estar deshabilitado y el log debe registrar el evento end/error que lo liberó.
    await page.waitForTimeout(5000);
    log = await logTts(page);
    if (await detener.isEnabled()) {
      await detener.click();
      await expect(estado).toContainText('Reproducción detenida');
      await expect(detener).toBeDisabled();
      log = await logTts(page);
      expect(log.cancelaciones).toBeGreaterThanOrEqual(2);
    } else {
      expect(
        log.eventos.includes('end') || log.eventos.includes('error'),
        'Si Detener está deshabilitado, el motor debió informar end/error del último utterance',
      ).toBeTruthy();
      await expect(estado).not.toContainText('Reproduciendo en inglés');
    }

    // Eventos nativos reenviados por speak: registrados para el informe.
    log = await logTts(page);
    console.log(`TTS nativo — voces: ${log.voces.length}, locales-en: ${log.voces.filter((v) => v.localService && v.lang.toLowerCase().startsWith('en')).length}, habladas: ${log.habladas.length}, cancelaciones: ${log.cancelaciones}, eventos: ${log.eventos.join(',') || 'ninguno'}`);

    // Eventos nativos reenviados por speak: se registran para el informe. En motores
    // headless sin salida de audio, start/end pueden no dispararse — se reporta, no se exige.
    await page.waitForTimeout(3000);
    log = await logTts(page);
    console.log(`TTS nativo — voces: ${log.voces.length}, habladas: ${log.habladas.length}, eventos: ${log.eventos.join(',') || 'ninguno'}`);
  });

  test('accesibilidad axe y contraste del texto de ayuda', async ({ page }) => {
    // Contraste corregido: --texto-secundario (#6b7280 ≈4.15:1 sobre #eeecfd, fallaba AA)
    // reemplazado por --texto-principal (#1f2937).
    const ayuda = page.locator('.pronunciacion__ayuda');
    await expect(ayuda).toBeVisible();
    const color = await ayuda.evaluate((el) => getComputedStyle(el).color);
    expect(color).toBe('rgb(31, 41, 55)');

    const resultados = await new AxeBuilder({ page })
      .exclude('.fila-historial--bloqueada')
      .exclude('.logro-card--bloqueado')
      .analyze();
    const graves = resultados.violations.filter((v) => v.impact === 'serious' || v.impact === 'critical');
    expect(graves, JSON.stringify(graves, null, 2)).toEqual([]);
  });
});
