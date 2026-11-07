declare const LOGOS_API_URL: string | undefined;
declare const LOGOS_GOOGLE_CLIENT_ID: string | undefined;

export const environment = {
  production: true,
  // Se fija al compilar (scripts/desplegar/frontend.sh): --define "LOGOS_API_URL='https://…'".
  // Sin definir queda el valor de ejemplo, que no existe: obliga a configurarlo antes de publicar.
  apiUrl: typeof LOGOS_API_URL === 'undefined' ? 'https://api.logos.cl' : LOGOS_API_URL,
  googleClientId: typeof LOGOS_GOOGLE_CLIENT_ID === 'undefined' ? '' : LOGOS_GOOGLE_CLIENT_ID,
};
