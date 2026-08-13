import { inject } from '@angular/core';
import { CanActivateFn, Router } from '@angular/router';
import { SesionService } from './sesion.service';

/** Protege las rutas /alumno/* — si no hay un Perfil de Alumno elegido (ej. se recargó la
 * página en un deep-link, o se navegó directo por URL), manda al selector en vez de
 * quedar con pantallas vacías silenciosas (bug real encontrado probando la app). */
export const perfilGuard: CanActivateFn = () => {
  const sesion = inject(SesionService);
  const router = inject(Router);
  if (sesion.perfilActivo()) return true;
  return router.parseUrl('/selector-perfil');
};
