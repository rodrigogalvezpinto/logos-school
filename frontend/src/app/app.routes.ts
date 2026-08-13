import { Routes } from '@angular/router';
import { Shell } from './layout/shell/shell';
import { authGuard } from './core/auth.guard';
import { perfilGuard } from './core/perfil.guard';

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
        loadComponent: () => import('./pages/seleccion-plan/seleccion-plan').then((m) => m.SeleccionPlan),
      },
      { path: '', redirectTo: 'inicio', pathMatch: 'full' },
    ],
  },
  {
    path: 'configuracion',
    component: Shell,
    data: { modo: 'alumno' },
    canActivate: [authGuard],
    children: [
      { path: '', loadComponent: () => import('./pages/configuracion/configuracion').then((m) => m.Configuracion) },
    ],
  },
  { path: '**', redirectTo: '' },
];
