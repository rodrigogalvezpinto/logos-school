declare const LOGOS_API_URL: string | undefined;

export const environment = {
  production: false,
  apiUrl: typeof LOGOS_API_URL === 'undefined' ? 'http://localhost:8000' : LOGOS_API_URL,
  googleClientId: '',
  sentryDsn: '',
  // Botón «Entrar con la cuenta demo» del login (solo desarrollo; ver backend/scripts/crear_cuenta_demo.py).
  cuentaDemo: { email: 'demo@logos.cl', password: 'DemoLogos2026!' } as { email: string; password: string } | null,
};
