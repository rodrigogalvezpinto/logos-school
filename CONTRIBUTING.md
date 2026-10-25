# Contribuyendo a Logos School

Este documento describe cómo trabajar en el proyecto Logos School.

## 📋 Requisitos Previos

- Python 3.12+
- Node.js 20+ (versión LTS recomendada por Angular)
- PostgreSQL (para desarrollo local)
- Git

## 🚀 Configuración del Entorno de Desarrollo

### 1. Clonar el repositorio

```bash
git clone https://github.com/rodrigogalvezpinto/logos-school.git
cd logos-school
```

### 2. Configurar el Backend

```bash
cd backend

# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Instalar dependencias
uv sync

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus credenciales locales
```

Variables de entorno requeridas (ver `.env.example`):
- `DATABASE_URL` - URL de PostgreSQL local
- `JWT_SECRET` - Clave secreta para JWT
- `GOOGLE_CLIENT_ID` - Para login con Google (opcional en desarrollo)
- `RESEND_API_KEY` - Para correos (opcional en desarrollo)

```bash
# Ejecutar migraciones
uv run alembic upgrade head

# Iniciar servidor de desarrollo
uv run uvicorn app.main:app --reload
```

El backend estará disponible en `http://localhost:8000`

### 3. Configurar el Frontend

```bash
cd frontend

# Instalar dependencias
npm install

# Iniciar servidor de desarrollo
npm start
```

El frontend estará disponible en `http://localhost:4200`

## 🧪 Ejecutar Tests

### Backend

```bash
cd backend
uv run pytest
```

Para tests específicos:
```bash
uv run pytest tests/test_auth.py -v
uv run pytest -k "test_prueba_gratis"
```

### Frontend E2E

```bash
cd frontend
npx playwright test
```

Para ejecutar en modo visible:
```bash
npx playwright test --headed
```

Para un solo test:
```bash
npx playwright test registro.spec.ts
```

## 📂 Estructura del Proyecto

```
logos-school/
├── backend/                 # Backend FastAPI
│   ├── app/
│   │   ├── application/     # Casos de uso
│   │   ├── domain/         # Entidades y lógica de dominio
│   │   ├── infrastructure/ # Implementaciones concretas
│   │   ├── routers/        # Endpoints API
│   │   └── core/           # Configuración y dependencias
│   ├── tests/              # Tests pytest
│   ├── scripts/            # Scripts de utilidad
│   └── alembic/            # Migraciones de base de datos
├── frontend/               # Frontend Angular
│   ├── src/
│   │   ├── app/
│   │   │   ├── pages/      # Páginas principales
│   │   │   ├── shared/     # Componentes compartidos
│   │   │   └── core/       # Servicios core
│   │   └── styles.scss     # Estilos globales
│   ├── e2e/                # Tests E2E Playwright
│   └── public/             # Archivos estáticos
├── contenido/              # Contenido pedagógico (Markdown)
├── Temarios/              # Temarios oficiales Mineduc (PDF)
├── planificacion/         # Documentación del proyecto
└── scripts/               # Scripts generales
```

## 🔄 Flujo de Trabajo

### 1. Crear una rama

```bash
git checkout -b feature/nombre-de-la-funcionalidad
```

### 2. Hacer cambios y commit

```bash
git add .
git commit -m "Descripción clara del cambio"
```

### 3. Ejecutar tests

```bash
# Backend
cd backend && uv run pytest

# Frontend
cd frontend && npx playwright test
```

### 4. Push y crear Pull Request

```bash
git push origin feature/nombre-de-la-funcionalidad
```

Luego crear un Pull Request en GitHub.

## 📝 Convenciones de Commit

Usar mensajes de commit claros y descriptivos:

```
feat: agregar nueva funcionalidad X
fix: corregir bug Y
docs: actualizar documentación
refactor: refactorizar código Z
test: agregar tests para W
chore: tarea de mantenimiento
```

## 🎨 Estilo de Código

### Backend (Python)
- Seguir PEP 8
- Usar type hints
- Documentar funciones complejas con docstrings
- Arquitectura hexagonal: separar dominio, aplicación e infraestructura

### Frontend (Angular)
- Seguir estilo oficial de Angular
- Usar componentes tipados
- Preferir signals sobre observables cuando sea posible
- Separar lógica en servicios

## 🔒 Seguridad

- Nunca commitear `.env` con credenciales reales
- Usar `.env.example` como plantilla
- No commitear archivos de base de datos
- Revisar que no haya información sensible en los commits

## 📖 Documentación

Toda la documentación del proyecto está en `planificacion/`:

- `00-vision-alcance.md` - Visión general
- `11-especificacion-mvp-para-desarrollo.md` - Especificación técnica
- `17-infraestructura-y-entornos.md` - Infraestructura

Leer estos documentos antes de hacer cambios significativos.

## 🐛 Reportar Bugs

Para reportar bugs, crear un issue en GitHub con:

- Descripción del problema
- Pasos para reproducir
- Comportamiento esperado vs actual
- Capturas de pantalla si aplica
- Environment (OS, navegador, versión)

## 💡 Sugerencias

Para sugerencias de funcionalidad, crear un issue con:

- Descripción de la funcionalidad sugerida
- Caso de uso
- Beneficio esperado

## 📞 Contacto

Para preguntas sobre el proyecto, contactar al equipo de Logos School.
