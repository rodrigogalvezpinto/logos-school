# Logos School

Plataforma web para apoyar el estudio y preparación de niños, niñas y adolescentes que rendirán los **Exámenes Libres de Validación de Estudios** del Ministerio de Educación de Chile, abarcando los 12 niveles: 1° a 8° básico y 1° a 4° medio.

> **Regla de rama única:** todo el trabajo se hace en `main`. **No crear ramas nuevas.** La antigua rama `qa/fase-2-matriz-trazabilidad` se integró en `main` mediante el PR #8 y solo se conserva como referencia histórica remota.

## 🎯 Objetivo

Ser una plataforma accesible para todas las personas, con contenido de estudio 100% gratuito basado en los temarios oficiales de la Unidad de Currículum y Evaluación (UCE) del Mineduc.

## 📚 Contenido Pedagógico

- **12 cursos completos** (1° básico a 4° medio)
- **2.917 preguntas** de autoevaluación
- **408/408 Objetivos de Aprendizaje** cubiertos (temarios oficiales Mineduc)
- **156 pruebas de unidad** calibradas por edad
- **50 exámenes simulacro** (Forma A y B en 1°–4° básico; Forma B por asignatura desde 5° básico)

Los temarios oficiales están en la carpeta `Temarios/` y su análisis estructurado en `Temarios/analisis/`.

## 🏗️ Arquitectura Técnica

### Backend
- **Framework**: FastAPI (Python 3.12+)
- **Arquitectura**: Hexagonal (dominio/aplicación/infraestructura)
- **Base de datos**: PostgreSQL (Alembic para migraciones)
- **Tests**: línea base y resultados en `docs/qa/linea-base.md`

### Frontend
- **Framework**: Angular 22.1.0
- **Tests**: suite unitaria (Vitest) y E2E (Playwright) documentada en `docs/qa/linea-base.md`
- **Accesibilidad**: Auditoría con axe-core

## 🚀 Estado Actual

### ✅ Completado (Etapa 1 MVP + Etapa 2 + Fase 1 Brincus)

**Fase 1.1 - Estudiar y evaluarse**
- Guías de estudio por OA con explicación y ejemplos
- Banco de autoevaluación con retroalimentación
- Pruebas de unidad y exámenes simulacro
- Motor de evaluación con cronómetro y cálculo de notas

**Fase 1.2 - Historial y notas por materia**
- Historial completo de guías revisadas y evaluaciones rendidas
- Notas por asignatura y señal real de preparación

**Fase 1.3 - Plan de estudio con horario**
- Planificación automática de sesiones (3/4/5 días por semana)
- Habilitación progresiva de pruebas y exámenes
- Vista semanal y mensual

**Panel de Administrador**
- Gestión de planes, descuentos, cortesías y métricas
- Aprobación de profesores
- Programación de simulacros con fecha

**Rol Profesor y Curso/Sección**
- Auto-registro con aprobación manual
- Creación de cursos y gestión de alumnos
- Comunicados y reportes de progreso

**Fase 1 - Hallazgos de Brincus**
- Gamificación: logros, XP, niveles, avatares, racha de días
- Plan Lector: 4 libros curados por nivel
- Útiles Escolares: lista de materiales por nivel
- Centro de notificaciones
- Búsqueda global de contenido
- Botón de ayuda contextual
- Buzón de sugerencias
- Descarga de guía en PDF
- Reportar error de contenido
- Simulacro con fecha programada
- Onboarding con checklist
- Check-in emocional diario
- Certificado de alumno regular en PDF
- Historial de pagos
- Agregar alumno inline

### 🔴 Pendiente (bloqueantes para producción)

1. **Despliegue a producción**
   - Neon (base de datos - 2 branches: dev y prod)
   - Render (backend - 2 servicios: dev y prod)
   - Cloudflare Pages (frontend)
   - Sentry (monitoreo de errores)
   - UptimeRobot (monitoreo de disponibilidad)

2. **Credenciales de servicios externos**
   - Login con Google (`GOOGLE_CLIENT_ID`)
   - Correo transaccional Resend (`RESEND_API_KEY`)
   - Pasarela de pago (Webpay/Transbank pendiente)
   - Cloudflare Turnstile (anti-bots)

3. **Gate de cobro**
   - Bloquear acceso cuando vence la prueba gratuita sin pago

### 🟡 Pendiente (no bloquea)

4. **CI/CD** - Pipeline automático (GitHub Actions)
5. **Logo pulido** - Versión final del logo
6. **Componentes visuales de Matemática** - Recta numérica, modelo de fracciones, figuras geométricas

## 📖 Documentación

### Estructura Principal

**`planificacion/`** - Planificación del producto y decisiones tomadas
- `00-vision-alcance.md` - Visión general y decisiones tomadas
- `01-roles-y-permisos.md` - Perfiles de usuario y permisos
- `02-modelo-de-datos-conceptual.md` - Entidades y relaciones
- `03-roadmap-etapas.md` - Etapas de construcción
- `04-modo-de-operacion.md` - Cómo opera el agente experto
- `05-tipos-de-contenido.md` - Tipos de contenido por curso
- `07-experto-examenes-libres.md` - Trámite administrativo real
- `08-diseno-pruebas-vs-examenes.md` - Diseño de evaluaciones
- `09-modelo-de-negocio.md` - Modelo de sostenibilidad financiera
- `10-privacidad-y-datos-de-menores.md` - Marco legal y registro
- `11-especificacion-mvp-para-desarrollo.md` - Especificación técnica
- `12-motor-de-evaluacion.md` - Flujo de evaluación
- `13-plan-de-estudio.md` - Horario de estudio
- `14-preguntas-frecuentes-apoderados.md` - Copy base de ventas
- `15-diseno-visual-y-marca.md` - Paleta de colores y tipografía
- `16-navegacion-y-panel-de-control.md` - Flujo de navegación
- `17-infraestructura-y-entornos.md` - Infraestructura y despliegue
- `21-accesibilidad-lectura-y-contenido-visual.md` - Accesibilidad
- `22-analisis-de-brechas.md` - Auditoría de qué falta
- `25-analisis-competencia-brincus.md` - Análisis de competencia
- `27-plan-incorporacion-hallazgos-brincus.md` - Plan de incorporación

**`docs/`** - Documentación técnica y auditorías
- `docs/README.md` - Índice de documentación
- `docs/auditorias/00-CENTRO-DE-CONTROL-AUDITORIA.md` - Centro de control de auditorías
- `docs/auditorias/AUDITORIA_MAESTRA.md` - Auditoría consolidada del contenido
- `docs/auditorias/matematica/` - Auditoría específica de Matemática
- `docs/auditorias/ux-ui/` - Hallazgos UX/UI
- `docs/planes/` - Planes y especificaciones técnicas
- `docs/qa/` - Calidad, pruebas y línea base

**Archivos de guía rápida**
- `CLAUDE.md` - Memoria del proyecto (contexto para agentes IA)
- `ACCESO-Y-PRUEBAS.md` - Guía de acceso rápido y credenciales
- `DOCKER-SETUP.md` - Configuración Docker para desarrollo local

## 🛠️ Desarrollo Local

### Opción 1: Con Docker (Recomendado)

Requiere Docker Desktop instalado. Ejecuta un solo comando:

```bash
./iniciar-con-docker.sh
```

Este script:
- Levanta PostgreSQL en Docker
- Aplica migraciones
- Importa contenido
- Crea datos de prueba
- Inicia backend (puerto 8000) y frontend (puerto 4200)

Ver `DOCKER-SETUP.md` para más detalles.

### Opción 2: Manual

**Backend:**
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # o .venv\Scripts\activate en Windows
uv sync
cp .env.example .env  # Completar las variables de entorno
uv run alembic upgrade head
uv run uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

**Tests:**
```bash
# Backend
cd backend
uv run pytest

# Frontend E2E
cd frontend
npx playwright test
```

### Credenciales de Prueba

Ver `ACCESO-Y-PRUEBAS.md` para credenciales de prueba (apoderado, profesor, admin).

## 🗺️ Roadmap

Ver `planificacion/03-roadmap-etapas.md` para el detalle completo de las etapas:

- **Etapa 0** ✅ - Cimientos (temarios, modelo de datos, curso piloto)
- **Etapa 1** ✅ - MVP: piloto de 4° básico, modo autoestudio
- **Etapa 2** ✅ - Rol Profesor y Curso/Sección
- **Etapa 3** - Expandir a más niveles (1°-3° básico)
- **Etapa 4** - Extender al Régimen B (5° básico en adelante)
- **Etapa 5** - Extender al Régimen C (3°-4° medio)
- **Etapa 6** ✅ - Cobertura completa (los 12 niveles)

## 📄 Licencia

Este proyecto es propiedad de Logos School.

## 🤝 Contribución

Este es un proyecto privado. Para colaborar, contactar al equipo de Logos School.
