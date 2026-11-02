declare const LOGOS_API_URL: string | undefined;

export const environment = {
  production: false,
  apiUrl: typeof LOGOS_API_URL === 'undefined' ? 'http://localhost:8000' : LOGOS_API_URL,
  googleClientId: '',
};
