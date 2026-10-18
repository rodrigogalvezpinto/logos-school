/** Identidad visual (ícono + color) por asignatura — una sola fuente de verdad para que la
 * misma asignatura se vea igual en "Mis Asignaturas", "Pruebas y Exámenes" e Inicio (antes
 * cada página tenía su propia lógica parcial, y el color ni siquiera dependía del nombre).
 * Coincide con las 9 asignaturas reales que existen en los 12 cursos (ver
 * backend/scripts/importar_contenido.py). Se matchea por palabra clave, no por nombre
 * exacto, porque el mismo nombre cambia entre régimen A/B/C (ej. "Lenguaje y Comunicación"
 * en básica vs. "Lengua y Literatura" desde 7° básico).
 *
 * Los colores están ajustados para pasar WCAG AA (4.5:1) tanto como texto sobre blanco como
 * fondo con texto blanco encima — el contraste es simétrico, así que un solo tono sirve para
 * ambos casos. Verificado con axe-core (e2e/accesibilidad.spec.ts): el verde, naranjo y verde
 * azulado "de catálogo" (#16A34A/#EA580C/#0D9488) no pasaban (3.2:1-3.7:1) — se oscurecieron
 * hasta calzar. */
export interface EstiloAsignatura {
  color: string;
  icono: string;
}

const REGLAS: Array<{ patron: RegExp; estilo: EstiloAsignatura }> = [
  { patron: /matem[aá]tica/i, estilo: { icono: 'regla', color: '#7C3AED' } },
  { patron: /lenguaje|lengua y literatura/i, estilo: { icono: 'libro', color: '#D62674' } },
  { patron: /ciencias naturales/i, estilo: { icono: 'hoja', color: '#12853C' } },
  { patron: /historia|geograf[ií]a/i, estilo: { icono: 'mapa', color: '#C4490A' } },
  { patron: /ingl[eé]s/i, estilo: { icono: 'ingles', color: '#2563EB' } },
  { patron: /filosof[ií]a/i, estilo: { icono: 'filosofia', color: '#4338CA' } },
  { patron: /ciudadan[ií]a/i, estilo: { icono: 'balanza', color: '#0B7F74' } },
];

const POR_DEFECTO: EstiloAsignatura = { icono: 'libro', color: '#5B4FE9' };

export function estiloAsignatura(nombre: string): EstiloAsignatura {
  return REGLAS.find((r) => r.patron.test(nombre))?.estilo ?? POR_DEFECTO;
}
