declare const LOGOS_API_URL: string | undefined;
declare const LOGOS_GOOGLE_CLIENT_ID: string | undefined;
declare const LOGOS_SENTRY_DSN: string | undefined;

export const environment = {
  production: true,
  // Se fija al compilar (scripts/desplegar/frontend.sh): --define "LOGOS_API_URL='https://…'".
  // Sin definir queda el valor de ejemplo, que no existe: obliga a configurarlo antes de publicar.
  apiUrl: typeof LOGOS_API_URL === 'undefined' ? 'https://api.logos.cl' : LOGOS_API_URL,
  googleClientId: typeof LOGOS_GOOGLE_CLIENT_ID === 'undefined' ? '' : LOGOS_GOOGLE_CLIENT_ID,
  // Aviso de errores (Sentry). Vacío = apagado y el SDK ni siquiera se descarga.
  sentryDsn: typeof LOGOS_SENTRY_DSN === 'undefined' ? '' : LOGOS_SENTRY_DSN,
  // En producción no hay cuenta demo: el botón del login no aparece.
  cuentaDemo: null as { email: string; password: string } | null,
};
