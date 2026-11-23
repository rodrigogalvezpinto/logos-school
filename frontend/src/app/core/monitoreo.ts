import { ErrorHandler, Injectable } from '@angular/core';
import type { ErrorEvent as EventoSentry } from '@sentry/browser';

/**
 * Aviso de errores con Sentry (2026-11-22). Apagado si `environment.sentryDsn` está vacío: el SDK se carga con
 * import dinámico, así que sin DSN no se descarga. Los usuarios son menores de edad, así que solo se envía el error
 * técnico: sin migas de pan (podrían llevar texto de pantalla), sin parámetros de URL (el enlace de recuperación
 * lleva un token), sin usuario ni IP.
 */
type Sentry = typeof import('@sentry/browser');
let sentry: Sentry | null = null;

export function limpiarEvento<T extends EventoSentry>(evento: T): T {
  if (evento.request) {
    if (evento.request.url) evento.request.url = evento.request.url.split('?')[0];
    delete evento.request.query_string;
    delete evento.request.cookies;
    delete evento.request.headers;
    delete evento.request.data;
  }
  delete evento.user;
  delete evento.breadcrumbs;
  return evento;
}

export async function iniciarMonitoreo(dsn: string): Promise<void> {
  if (!dsn) return;
  const s = await import('@sentry/browser');
  s.init({
    dsn,
    environment: 'produccion',
    sendDefaultPii: false,
    maxBreadcrumbs: 0,
    beforeBreadcrumb: () => null,
    beforeSend: (e) => limpiarEvento(e),
  });
  sentry = s;
}

@Injectable()
export class ManejadorErroresLogos implements ErrorHandler {
  handleError(error: unknown): void {
    console.error(error);
    sentry?.captureException(error);
  }
}
