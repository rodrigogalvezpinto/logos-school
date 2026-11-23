import { ApplicationConfig, ErrorHandler, provideAppInitializer, provideBrowserGlobalErrorListeners } from '@angular/core';
import { provideHttpClient, withInterceptors } from '@angular/common/http';
import { provideRouter, withComponentInputBinding } from '@angular/router';

import { routes } from './app.routes';
import { authInterceptor } from './core/auth-interceptor';
import { ManejadorErroresLogos, iniciarMonitoreo } from './core/monitoreo';
import { environment } from '../environments/environment';

export const appConfig: ApplicationConfig = {
  providers: [
    provideBrowserGlobalErrorListeners(),
    provideRouter(routes, withComponentInputBinding()),
    provideHttpClient(withInterceptors([authInterceptor])),
    { provide: ErrorHandler, useClass: ManejadorErroresLogos },
    // No bloquea el arranque: si Sentry tarda o falla, la app sigue.
    provideAppInitializer(() => { iniciarMonitoreo(environment.sentryDsn).catch(() => undefined); }),
  ]
};
