import { Routes } from '@angular/router';
import { Shell } from './layout/shell/shell';
import { AdminShell } from './layout/admin-shell/admin-shell';
import { ProfesorShell } from './layout/profesor-shell/profesor-shell';
import { authGuard } from './core/auth.guard';
import { perfilGuard } from './core/perfil.guard';
import { adminGuard } from './core/admin.guard';
import { profesorGuard } from './core/profesor.guard';

export const routes: Routes = [
  {
    path: '',
    loadComponent: () => import('./pages/landing/landing').then((m) => m.Landing),
  },
  {
    path: 'como-funciona',
    loadComponent: () => import('./pages/como-funciona/como-funciona').then((m) => m.ComoFunciona),
  },
  {
    path: 'preguntas-frecuentes',
    loadComponent: () =>
      import('./pages/preguntas-frecuentes/preguntas-frecuentes').then((m) => m.PreguntasFrecuentes),
  },
  {
    path: 'privacidad',
    loadComponent: () => import('./pages/privacidad/privacidad').then((m) => m.Privacidad),
  },
  {
    path: 'terminos',
    loadComponent: () => import('./pages/terminos/terminos').then((m) => m.Terminos),
  },
  {
    path: 'login',
    loadComponent: () => import('./pages/login/login').then((m) => m.Login),
  },
  {
    path: 'registro',
    loadComponent: () => import('./pages/registro/registro').then((m) => m.Registro),
  },
  {
    path: 'agregar-alumno',
    loadComponent: () => import('./pages/agregar-alumno/agregar-alumno').then((m) => m.AgregarAlumno),
  },
  {
    path: 'seleccion-plan',
    loadComponent: () => import('./pages/seleccion-plan/seleccion-plan').then((m) => m.SeleccionPlan),
  },
  {
    path: 'selector-perfil',
    loadComponent: () => import('./pages/selector-perfil/selector-perfil').then((m) => m.SelectorPerfil),
  },
  {
    path: 'examen/:id',
    loadComponent: () => import('./pages/examen-simulacro/examen-simulacro').then((m) => m.ExamenSimulacro),
    canActivate: [authGuard, perfilGuard],
  },
  {
    path: 'alumno',
    component: Shell,
    data: { modo: 'alumno' },
    canActivate: [authGuard, perfilGuard],
    children: [
      { path: 'inicio', loadComponent: () => import('./pages/alumno-inicio/alumno-inicio').then((m) => m.AlumnoInicio) },
      {
        path: 'asignaturas',
        loadComponent: () => import('./pages/asignatura/asignaturas-lista').then((m) => m.AsignaturasLista),
      },
      {
        path: 'asignaturas/:id',
        loadComponent: () => import('./pages/asignatura/asignatura-detalle').then((m) => m.AsignaturaDetalle),
      },
      {
        path: 'estudiar/:oaId',
        loadComponent: () => import('./pages/estudiar-oa/estudiar-oa').then((m) => m.EstudiarOa),
      },
      {
        path: 'evaluaciones',
        loadComponent: () => import('./pages/evaluaciones/evaluaciones').then((m) => m.Evaluaciones),
      },
      {
        path: 'autoevaluacion/:oaId',
        loadComponent: () => import('./pages/autoevaluacion/autoevaluacion').then((m) => m.Autoevaluacion),
      },
      {
        path: 'prueba/:id',
        loadComponent: () => import('./pages/prueba-unidad/prueba-unidad').then((m) => m.PruebaUnidad),
      },
      {
        path: 'notas',
        loadComponent: () => import('./pages/notas/notas').then((m) => m.Notas),
      },
      {
        path: 'plan-estudio',
        loadComponent: () => import('./pages/plan-estudio/plan-estudio').then((m) => m.PlanEstudio),
      },
      {
        path: 'logros',
        loadComponent: () => import('./pages/logros/logros').then((m) => m.Logros),
      },
      {
        path: 'plan-lector',
        loadComponent: () => import('./pages/plan-lector/plan-lector').then((m) => m.PlanLector),
      },
      {
        path: 'utiles-escolares',
        loadComponent: () =>
          import('./pages/utiles-escolares/utiles-escolares').then((m) => m.UtilesEscolares),
      },
      {
        path: 'configuracion',
        data: { contexto: 'alumno' },
        loadComponent: () => import('./pages/configuracion/configuracion').then((m) => m.Configuracion),
      },
      { path: '', redirectTo: 'inicio', pathMatch: 'full' },
    ],
  },
  {
    path: 'apoderado',
    component: Shell,
    data: { modo: 'apoderado' },
    canActivate: [authGuard],
    children: [
      {
        path: 'inicio',
        loadComponent: () => import('./pages/dashboard-apoderado/dashboard-apoderado').then((m) => m.DashboardApoderado),
      },
      {
        path: 'alumnos',
        loadComponent: () => import('./pages/dashboard-apoderado/dashboard-apoderado').then((m) => m.DashboardApoderado),
      },
      {
        path: 'plan',
        loadComponent: () => import('./pages/historial-pagos/historial-pagos').then((m) => m.HistorialPagos),
      },
      {
        path: 'progreso',
        loadComponent: () => import('./pages/progreso-alumno/progreso-alumno').then((m) => m.ProgresoAlumno),
      },
      {
        path: 'estadisticas',
        loadComponent: () => import('./pages/estadisticas-familiares/estadisticas-familiares').then((m) => m.EstadisticasFamiliares),
      },
      {
        path: 'progreso/:perfilAlumnoId',
        loadComponent: () => import('./pages/notas/notas').then((m) => m.Notas),
      },
      {
        path: 'configuracion',
        data: { contexto: 'apoderado' },
        loadComponent: () => import('./pages/configuracion/configuracion').then((m) => m.Configuracion),
      },
      { path: '', redirectTo: 'inicio', pathMatch: 'full' },
    ],
  },
  {
    path: 'admin/login',
    loadComponent: () => import('./pages/admin-login/admin-login').then((m) => m.AdminLogin),
  },
  {
    path: 'admin',
    component: AdminShell,
    canActivate: [adminGuard],
    children: [
      {
        path: 'dashboard',
        loadComponent: () => import('./pages/admin-dashboard/admin-dashboard').then((m) => m.AdminDashboard),
      },
      {
        path: 'planes',
        loadComponent: () => import('./pages/admin-planes/admin-planes').then((m) => m.AdminPlanes),
      },
      {
        path: 'descuentos',
        loadComponent: () => import('./pages/admin-descuentos/admin-descuentos').then((m) => m.AdminDescuentos),
      },
      {
        path: 'cortesias',
        loadComponent: () => import('./pages/admin-cortesias/admin-cortesias').then((m) => m.AdminCortesias),
      },
      {
        path: 'profesores',
        loadComponent: () => import('./pages/admin-profesores/admin-profesores').then((m) => m.AdminProfesores),
      },
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
    ],
  },
  {
    path: 'profesor/login',
    loadComponent: () => import('./pages/profesor-login/profesor-login').then((m) => m.ProfesorLogin),
  },
  {
    path: 'profesor',
    component: ProfesorShell,
    canActivate: [profesorGuard],
    children: [
      {
        path: 'dashboard',
        loadComponent: () => import('./pages/profesor-dashboard/profesor-dashboard').then((m) => m.ProfesorDashboard),
      },
      {
        path: 'cursos/:id',
        loadComponent: () =>
          import('./pages/profesor-curso-detalle/profesor-curso-detalle').then((m) => m.ProfesorCursoDetalle),
      },
      { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
    ],
  },
  { path: '**', redirectTo: '' },
];
