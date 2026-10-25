# Skill: Desarrollo Técnico — Logos School (FastAPI + Angular + PostgreSQL)

## Descripción
Patrones, convenciones y guías técnicas para el desarrollo del backend (FastAPI, arquitectura hexagonal) y frontend (Angular) de Logos School. Incluye testing, migraciones, auth, deployment, y cómo se mapea el dominio pedagógico a código.

---

## Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                      FRONTEND (Angular)                      │
│  Components → Services → HttpClient → API Gateway (REST)    │
└──────────────────────────┬──────────────────────────────────┘
                           │ HTTPS / JSON
┌──────────────────────────▼──────────────────────────────────┐
│                      BACKEND (FastAPI)                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   API       │  │  Dominio    │  │  Infraestructura    │  │
│  │   (Adapt.)  │──│  (Core)     │──│  (Adaptadores)      │  │
│  │  Endpoints  │  │  Entidades, │  │  DB (SQLAlchemy),   │  │
│  │  DTOs,      │  │  Casos uso, │  │  Auth (JWT),        │  │
│  │  Validación │  │  Eventos,   │  │  Email (Resend),    │  │
│  │  Serializ.  │  │  Reglas     │  │  Storage, Pagos     │  │
│  └─────────────┘  └─────────────┘  └─────────────────────┘  │
└──────────────────────────┬──────────────────────────────────┘
                           │
                    ┌──────▼──────┐
                    │ PostgreSQL  │
                    │   (Neon)    │
                    │  Dev / Prod │
                    │  (branches) │
                    └─────────────┘
```

### Capas (Hexagonal / Clean Architecture)

| Capa | Responsabilidad | Ubicación | Ejemplos |
|------|-----------------|-----------|----------|
| **Dominio** | Reglas de negocio puras, sin deps externas | `backend/src/dominio/` | `Alumno`, `ObjetivoAprendizaje`, `Evaluacion`, `calcular_nota()` |
| **Aplicación** | Casos de uso, orquestación, puertos | `backend/src/aplicacion/` | `RegistrarAlumnoCasoUso`, `GenerarSimulacroCasoUso` |
| **Infraestructura** | Adaptadores: BD, auth, email, storage, pagos | `backend/src/infraestructura/` | `AlumnoRepositorioSQLAlchemy`, `ServicioEmailResend` |
| **API** | Endpoints, DTOs, validación entrada/salida | `backend/src/api/` | `router_alumnos.py`, `schemas.py`, `dependencias.py` |

**Regla**: El dominio **nunca** importa de infraestructura o API. La dependencia apunta hacia adentro.

---

## Backend — FastAPI (Python 3.11+)

### Estructura de Carpetas
```
backend/
├── src/
│   ├── dominio/
│   │   ├── entidades/
│   │   ├── eventos/
│   │   ├── excepciones/
│   │   ├── reglas/
│   │   └── value_objects/
│   ├── aplicacion/
│   │   ├── casos_uso/
│   │   ├── dto/
│   │   └── puertos/
│   ├── infraestructura/
│   │   ├── persistencia/
│   │   │   ├── modelos/          # SQLAlchemy models
│   │   │   ├── repositorios/     # Implementaciones repositorios
│   │   │   └── sesion.py         # Session factory, engine
│   │   ├── autenticacion/
│   │   ├── email/
│   │   ├── almacenamiento/
│   │   └── pagos/
│   └── api/
│       ├── routers/
│       ├── schemas/              # Pydantic models (request/response)
│       ├── dependencias/         # Auth, paginación, filtros
│       └── main.py               # App factory, middleware, lifespan
├── tests/
│   ├── unitarios/dominio/
│   ├── unitarios/aplicacion/
│   ├── integracion/api/
│   └── conftest.py               # Fixtures compartidas
├── alembic/                      # Migraciones
├── scripts/                      # Scripts utilitarios
├── pyproject.toml                # Dependencias (uv)
└── pytest.ini
```

### Convenciones de Código (Backend)

#### Nombrado (en español, snake_case)
```python
# Entidades / Value Objects: PascalCase
class ObjetivoAprendizaje:
    codigo: str
    descripcion: str
    indicadores: list[IndicadorEvaluacion]

# Casos de uso: Verbo + Sustantivo + CasoUso
class GenerarSimulacroCasoUso:
    def ejecutar(self, curso_id: int, forma: Literal["A", "B"]) -> SimulacroGenerado: ...

# Repositorios (puerto): Interfaz en dominio, impl en infra
class AlumnoRepositorio(Protocol):
    def obtener_por_id(self, id: int) -> Alumno | None: ...
    def guardar(self, alumno: Alumno) -> Alumno: ...

# Implementación: Nombre + Tecnología
class AlumnoRepositorioSQLAlchemy(AlumnoRepositorio): ...

# Endpoints: verbo_http_recurso
@router.post("/alumnos", response_model=AlumnoRespuesta)
async def crear_alumno(...): ...

# Esquemas Pydantic: Entidad + Accion + Tipo
class AlumnoCrearRequest(BaseModel): ...
class AlumnoRespuesta(BaseModel): ...
class AlumnoActualizarRequest(BaseModel): ...
```

#### Inyección de Dependencias (FastAPI `Depends`)
```python
# backend/src/api/dependencias.py
def obtener_repo_alumnos() -> AlumnoRepositorio:
    return AlumnoRepositorioSQLAlchemy(session=obtener_sesion_db())

def obtener_caso_uso_registrar_alumno(
    repo: AlumnoRepositorio = Depends(obtener_repo_alumnos),
    servicio_email: ServicioEmail = Depends(obtener_servicio_email),
) -> RegistrarAlumnoCasoUso:
    return RegistrarAlumnoCasoUso(repo, servicio_email)

# En router:
@router.post("/alumnos")
async def crear_alumno(
    request: AlumnoCrearRequest,
    caso_uso: RegistrarAlumnoCasoUso = Depends(obtener_caso_uso_registrar_alumno),
):
    return await caso_uso.ejecutar(request)
```

#### Manejo de Errores (Dominio → HTTP)
```python
# backend/src/dominio/excepciones.py
class ErrorDominio(Exception):
    codigo: str
    mensaje_usuario: str

class AlumnoNoEncontrado(ErrorDominio):
    codigo = "ALUMNO_NO_ENCONTRADO"
    mensaje_usuario = "El alumno no existe"

class OANoTienePreguntas(ErrorDominio):
    codigo = "OA_SIN_PREGUNTAS"
    mensaje_usuario = "Este objetivo no tiene preguntas disponibles"

# backend/src/api/main.py - Exception handlers globales
@app.exception_handler(ErrorDominio)
async def manejar_error_dominio(request: Request, exc: ErrorDominio):
    return JSONResponse(
        status_code=400 if "NO_ENCONTRADO" not in exc.codigo else 404,
        content={"error": exc.codigo, "mensaje": exc.mensaje_usuario},
    )
```

#### Base de Datos (SQLAlchemy 2.0 + Async)
```python
# backend/src/infraestructura/persistencia/sesion.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)
SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def obtener_sesion_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

```python
# backend/src/infraestructura/persistencia/modelos/alumno.py
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.src.infraestructura.persistencia.modelos.base import Base

class AlumnoModelo(Base):
    __tablename__ = "alumnos"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    apellidos: Mapped[str] = mapped_column(String(150))
    fecha_nacimiento: Mapped[date]
    rut: Mapped[str] = mapped_column(String(12), unique=True, index=True)
    nivel_id: Mapped[int] = mapped_column(ForeignKey("niveles.id"))
    apoderado_id: Mapped[int] = mapped_column(ForeignKey("apoderados.id"))
    
    # Relaciones
    nivel: Mapped["NivelModelo"] = relationship(back_populates="alumnos")
    apoderado: Mapped["ApoderadoModelo"] = relationship(back_populates="alumnos")
    progresos: Mapped[list["ProgresoModelo"]] = relationship(back_populates="alumno")
```

#### Migraciones (Alembic)
```bash
# Crear migración
cd backend
alembic revision --autogenerate -m "descripcion_en_espanol"

# Aplicar en dev
alembic upgrade head

# En producción (Neon branch): automático via CI/CD
```

### Testing Backend (pytest + httpx)

#### Fixtures Base (`tests/conftest.py`)
```python
@pytest_asyncio.fixture
async def cliente_async(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.fixture
def repo_alumnos_memoria() -> AlumnoRepositorio:
    return AlumnoRepositorioMemoria()  # Fake para tests unitarios

@pytest_asyncio.fixture
async def repo_alumnos_db(sesion_db: AsyncSession) -> AlumnoRepositorio:
    return AlumnoRepositorioSQLAlchemy(sesion_db)
```

#### Tests Unitarios (Dominio / Aplicación)
```python
# tests/unitarios/dominio/test_calcular_nota.py
def test_calcular_nota_escala_1_a_7_con_exigencia_60():
    # Dado: 15 correctas de 25 (60%)
    resultado = calcular_nota(correctas=15, total=25, exigencia=0.6)
    # Entonces: nota 4.0 (mínima aprobatoria)
    assert resultado == 4.0

def test_calcular_nota_bajo_exigencia_da_1_0():
    resultado = calcular_nota(correctas=10, total=25, exigencia=0.6)
    assert resultado == 1.0
```

#### Tests de Integración (API + BD Real)
```python
# tests/integracion/api/test_alumnos.py
async def test_crear_alumno_exitoso(cliente_async: AsyncClient, apoderado_autenticado: dict):
    response = await cliente_async.post(
        "/api/v1/alumnos",
        json={
            "nombre": "Juan",
            "apellidos": "Pérez González",
            "fecha_nacimiento": "2014-03-15",
            "rut": "12.345.678-9",
            "nivel_id": 4,  # 4° básico
        },
        headers={"Authorization": f"Bearer {apoderado_autenticado['token']}"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Juan"
    assert data["nivel"]["nombre"] == "4° Básico"
```

#### Cobertura y Comandos
```bash
# Ejecutar todos (326 tests)
pytest --cov=src --cov-report=term-missing

# Solo unitarios (rápidos)
pytest tests/unitarios/ -v

# Solo integración (requiere BD)
pytest tests/integracion/ -v

# Con reporte HTML
pytest --cov=src --cov-report=html
```

---

## Frontend — Angular 18+ (Standalone Components)

### Estructura de Carpetas
```
frontend/
├── src/
│   ├── app/
│   │   ├── core/                    # Servicios singleton, guards, interceptors
│   │   │   ├── servicios/
│   │   │   │   ├── api.service.ts
│   │   │   │   ├── auth.service.ts
│   │   │   │   ├── almacenamiento.service.ts
│   │   │   │   └── notificaciones.service.ts
│   │   │   ├── guards/
│   │   │   │   ├── auth.guard.ts
│   │   │   │   ├── rol.guard.ts
│   │   │   │   └── perfil-seleccionado.guard.ts
│   │   │   └── interceptores/
│   │   │       ├── auth.interceptor.ts
│   │   │       └── error.interceptor.ts
│   │   ├── shared/                  # Componentes, pipes, directivas reutilizables
│   │   │   ├── componentes/
│   │   │   │   ├── boton/
│   │   │   │   ├── tarjeta/
│   │   │   │   ├── modal/
│   │   │   │   ├── carga/
│   │   │   │   └── selector-perfil/
│   │   │   ├── pipes/
│   │   │   │   ├── nota.pipe.ts
│   │   │   │   ├── fecha-chilena.pipe.ts
│   │   │   │   └── rut.pipe.ts
│   │   │   └── directivas/
│   │   ├── funcionalidades/         # Feature modules (lazy loaded)
│   │   │   ├── auth/
│   │   │   ├── alumno/
│   │   │   │   ├── estudiar/
│   │   │   │   ├── rendir/
│   │   │   │   ├── historial/
│   │   │   │   ├── plan-estudio/
│   │   │   │   └── logros/
│   │   │   ├── apoderado/
│   │   │   │   ├── dashboard/
│   │   │   │   ├── alumnos/
│   │   │   │   ├── pagos/
│   │   │   │   └── agenda/
│   │   │   ├── profesor/
│   │   │   │   ├── curso-seccion/
│   │   │   │   ├── seguimiento/
│   │   │   │   └── contenidos/
│   │   │   └── admin/
│   │   │       ├── planes/
│   │   │       ├── metricas/
│   │   │       ├── simulacros/
│   │   │       └── calidad-contenido/
│   │   ├── layouts/
│   │   │   ├── layout-auth/
│   │   │   ├── layout-alumno/
│   │   │   ├── layout-apoderado/
│   │   │   ├── layout-profesor/
│   │   │   └── layout-admin/
│   │   ├── modelos/                 # Interfaces TypeScript (mirror de Pydantic)
│   │   │   ├── alumno.model.ts
│   │   │   ├── evaluacion.model.ts
│   │   │   ├── objetivo-aprendizaje.model.ts
│   │   │   └── simulacro.model.ts
│   │   ├── app.routes.ts
│   │   ├── app.config.ts
│   │   └── app.component.ts
│   ├── assets/
│   │   ├── imagenes/
│   │   ├── iconos/
│   │   └── fuentes/
│   ├── styles/
│   │   ├── _variables.scss         # Paleta, tipografía, spacing
│   │   ├── _mixins.scss
│   │   ├── _reset.scss
│   │   ├── global.scss
│   │   └── temas/
│   │       ├── basica-inicial.scss
│   │       ├── basica-media.scss
│   │       └── media.scss
│   └── main.ts
├── e2e/                            # Playwright tests
│   ├── specs/
│   │   ├── auth.spec.ts
│   │   ├── alumno-estudiar.spec.ts
│   │   ├── alumno-rendir.spec.ts
│   │   ├── apoderado-dashboard.spec.ts
│   │   └── admin-planes.spec.ts
│   ├── fixtures/
│   │   └── test-data.ts
│   └── playwright.config.ts
├── angular.json
├── package.json
├── tsconfig.json
└── tailwind.config.js              # Si se usa Tailwind (opcional)
```

### Convenciones Frontend

#### Componentes Standalone (Angular 18+)
```typescript
// alumno-estudiar-componente.ts
@Component({
  selector: 'app-alumno-estudiar',
  standalone: true,
  imports: [CommonModule, TarjetaComponent, BotonComponent, RouterModule],
  templateUrl: './alumno-estudiar.component.html',
  styleUrls: ['./alumno-estudiar.component.scss'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AlumnoEstudiarComponent implements OnInit {
  // Inputs requeridos (no opcionales si son obligatorios)
  @Input({ required: true }) cursoId!: number;
  @Input() asignaturaId?: number;
  
  // Signals para estado reactivo
  protected readonly guias = signal<GuiaEstudio[]>([]);
  protected readonly cargando = signal(false);
  protected readonly error = signal<string | null>(null);
  
  // Inyección de dependencias (constructor o inject())
  private readonly apiService = inject(ApiService);
  private readonly route = inject(ActivatedRoute);
  
  async ngOnInit(): Promise<void> {
    await this.cargarGuias();
  }
  
  private async cargarGuias(): Promise<void> {
    this.cargando.set(true);
    try {
      const data = await this.apiService.obtenerGuiasEstudio(this.cursoId, this.asignaturaId);
      this.guias.set(data);
    } catch (e) {
      this.error.set('No se pudieron cargar las guías');
    } finally {
      this.cargando.set(false);
    }
  }
}
```

#### Servicios API (Tipados, Centralizados)
```typescript
// core/servicios/api.service.ts
@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly baseUrl = environment.apiUrl;
  
  constructor(private http: HttpClient) {}
  
  // GET tipado
  obtenerGuiasEstudio(cursoId: number, asignaturaId?: number): Promise<GuiaEstudio[]> {
    const params = new HttpParams()
      .set('curso_id', cursoId)
      .appendIf(asignaturaId, 'asignatura_id', asignaturaId);
    return this.http.get<GuiaEstudio[]>(`${this.baseUrl}/guias-estudio`, { params }).toPromise();
  }
  
  // POST con body tipado
  async crearEvaluacion(request: CrearEvaluacionRequest): Promise<Evaluacion> {
    return this.http.post<Evaluacion>(`${this.baseUrl}/evaluaciones`, request).toPromise();
  }
}
```

#### Modelos TypeScript (Espejo de Pydantic)
```typescript
// modelos/objetivo-aprendizaje.model.ts
export interface ObjetivoAprendizaje {
  id: number;
  codigo: string;           // ej: "OA12_LENG_4B"
  enunciado: string;
  indicadores: IndicadorEvaluacion[];
  ejeTematico: string;
  habilidadCognitiva: 'recordar' | 'comprender' | 'aplicar' | 'analizar' | 'evaluar' | 'crear';
  nivelId: number;
  asignaturaId: number;
}

export interface IndicadorEvaluacion {
  id: number;
  descripcion: string;
  oaId: number;
}
```

#### Estilos — Sistema Visual Logos School
```scss
// styles/_variables.scss
// Paleta oficial (ver planificacion/15-diseno-visual-y-marca.md)
$color-indigo: #5B4FE9;        // Primario
$color-indigo-hover: #4A3FD9;
$color-indigo-claro: #EDEBFE;

$color-coral: #FF6B4A;         // Secundario / Acciones destacadas
$color-coral-hover: #E85A3D;
$color-coral-claro: #FFEDE8;

// Semánticos
$color-exito: #10B981;
$color-advertencia: #F59E0B;
$color-error: #EF4444;
$color-info: #3B82F6;

// Neutros
$gris-50: #F9FAFB;
$gris-100: #F3F4F6;
$gris-500: #6B7280;
$gris-900: #111827;

// Tipografía
$font-heading: 'Poppins', sans-serif;   // Títulos, marca
$font-body: 'Inter', sans-serif;        // Texto, UI

// Espaciado (base 4px)
$espacio-1: 0.25rem;  // 4px
$espacio-2: 0.5rem;   // 8px
$espacio-3: 0.75rem;  // 12px
$espacio-4: 1rem;     // 16px
$espacio-6: 1.5rem;   // 24px
$espacio-8: 2rem;     // 32px

// Breakpoints
$bp-movil: 640px;
$bp-tablet: 768px;
$bp-desktop: 1024px;
$bp-grande: 1280px;

// Temas por ciclo (madurez visual)
@mixin tema-basica-inicial {
  // Colores más saturados, bordes redondeados grandes, iconos grandes
  --radio-borde: 16px;
  --tamano-icono: 2.5rem;
}

@mixin tema-basica-media {
  --radio-borde: 12px;
  --tamano-icono: 2rem;
}

@mixin tema-media {
  // Más sobrio, menos decorativo, más densidad informativa
  --radio-borde: 8px;
  --tamano-icono: 1.5rem;
}
```

#### Guards y Rutas (Lazy Loading)
```typescript
// app.routes.ts
export const routes: Routes = [
  { path: '', redirectTo: '/auth/login', pathMatch: 'full' },
  
  // Auth (sin layout)
  { path: 'auth', loadChildren: () import('./funcionalidades/auth/auth.routes') },
  
  // Alumno (layout + guards)
  {
    path: 'alumno',
    component: LayoutAlumnoComponent,
    canActivate: [authGuard, rolGuard(['ALUMNO']), perfilSeleccionadoGuard],
    children: [
      { path: 'estudiar', loadChildren: () => import('./funcionalidades/alumno/estudiar/estudiar.routes') },
      { path: 'rendir', loadChildren: () => import('./funcionalidades/alumno/rendir/rendir.routes') },
      { path: 'historial', loadChildren: () => import('./funcionalidades/alumno/historial/historial.routes') },
      { path: 'plan-estudio', loadChildren: () => import('./funcionalidades/alumno/plan-estudio/plan-estudio.routes') },
      { path: 'logros', loadChildren: () => import('./funcionalidades/alumno/logros/logros.routes') },
    ],
  },
  
  // Apoderado, Profesor, Admin... (estructura similar)
];
```

### Testing Frontend (Playwright)

#### Configuración (`e2e/playwright.config.ts`)
```typescript
export default defineConfig({
  testDir: './specs',
  fullyParallel: true,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 2 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:4200',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
  },
  projects: [
    { name: 'chromium', use: { ...devices['Desktop Chrome'] } },
    { name: 'mobile-chrome', use: { ...devices['Pixel 5'] } },
    { name: 'mobile-safari', use: { ...devices['iPhone 12'] } },
  ],
  webServer: {
    command: 'npm run start',
    url: 'http://localhost:4200',
    reuseExistingServer: !process.env.CI,
    timeout: 120000,
  },
});
```

#### Test E2E Típico
```typescript
// e2e/specs/alumno-rendir.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Alumno - Rendir Evaluación', () => {
  test.beforeEach(async ({ page }) => {
    await page.goto('/auth/login');
    await page.fill('[data-test="email"]', 'alumno@test.cl');
    await page.fill('[data-test="password"]', 'password123');
    await page.click('[data-test="btn-login"]');
    await expect(page).toHaveURL(/\/alumno\/dashboard/);
  });

  test('debe rendir una prueba de unidad y ver resultado', async ({ page }) => {
    await page.goto('/alumno/estudiar');
    await page.click('[data-test="btn-rendir-prueba"]:first-child');
    
    // Verificar cronómetro visible
    await expect(page.locator('[data-test="cronometro"]')).toBeVisible();
    
    // Responder preguntas
    for (let i = 0; i < 8; i++) {
      await page.click(`[data-test="opcion-${i}-0"]`); // Primera opción
      if (i < 7) await page.click('[data-test="btn-siguiente"]');
    }
    
    // Finalizar
    await page.click('[data-test="btn-finalizar"]');
    await page.click('[data-test="btn-confirmar"]');
    
    // Ver resumen
    await expect(page.locator('[data-test="nota-final"]')).toBeVisible();
    await expect(page.locator('[data-test="desglose-oa"]')).toBeVisible();
  });
});
```

#### Comandos Testing
```bash
# Ejecutar todos (69 tests)
npm run test:e2e

# Solo Chromium
npm run test:e2e -- --project=chromium

# Con UI mode (debug)
npm run test:e2e -- --ui

# Ver reporte HTML
npm run test:e2e:report
```

---

## Mapeo Dominio Pedagógico → Código

### Entidades Principales (Backend Dominio)
```python
# backend/src/dominio/entidades/objetivo_aprendizaje.py
@dataclass(frozen=True)
class ObjetivoAprendizaje:
    id: int
    codigo: str                    # "OA12_LENG_4B"
    enunciado: str
    indicadores: tuple[IndicadorEvaluacion, ...]
    eje_tematico: str
    habilidad_cognitiva: HabilidadCognitiva  # Enum Bloom
    nivel_id: int
    asignatura_id: int
    regimen: RegimenExamen         # Enum: A, B, C

# backend/src/dominio/entidades/evaluacion.py
@dataclass
class Evaluacion:
    id: int
    tipo: TipoEvaluacion           # PRUEBA_UNIDAD | SIMULACRO
    curso_id: int
    asignatura_id: int | None      # None si integrada (Régimen A)
    forma: Literal["A", "B"] | None
    preguntas: list[Pregunta]
    tiempo_limite_minutos: int
    configuracion: ConfiguracionEvaluacion

@dataclass
class Pregunta:
    id: int
    enunciado: str
    opciones: tuple[Opcion, ...]   # Exactamente 4, una correcta
    oa_codigo: str                 # Referencia al OA
    dificultad: Dificultad         # Enum: BAJA, MEDIA, ALTA
    retroalimentacion: dict[str, str]  # Por opción
```

### Endpoints Clave (API v1)
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/api/v1/auth/login` | Login email/password |
| POST | `/api/v1/auth/google` | Login Google OAuth |
| POST | `/api/v1/auth/refresh` | Refresh JWT |
| GET | `/api/v1/alumnos/{id}/progreso` | Progreso por OA/asignatura |
| GET | `/api/v1/cursos/{id}/guias-estudio` | Guías de estudio (filtrar por asignatura) |
| POST | `/api/v1/evaluaciones/iniciar` | Iniciar prueba/simulacro (crea intento) |
| GET | `/api/v1/intentos/{id}/pregunta/{n}` | Obtener pregunta n (con autosave) |
| PUT | `/api/v1/intentos/{id}/responder` | Guardar respuesta (autosave) |
| POST | `/api/v1/intentos/{id}/finalizar` | Calcular nota, guardar resultado |
| GET | `/api/v1/intentos/{id}/resultado` | Ver resumen con desglose por OA |
| GET | `/api/v1/apoderados/{id}/alumnos` | Listar alumnos del apoderado |
| POST | `/api/v1/admin/simulacros/programar` | Programar simulacro (Admin) |
| GET | `/api/v1/admin/metricas` | Métricas comerciales (Admin) |

---

## Deployment y Entornos (Regla: Dev/Prod Separados desde Día 1)

### Variables de Entorno (`.env.dev` / `.env.prod`)
```bash
# backend/.env.dev
DATABASE_URL=postgresql+asyncpg://user:pass@ep-xxx.us-east-1.aws.neon.tech/logos_dev
JWT_SECRET=dev-secret-change-in-prod
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=30
REFRESH_EXPIRATION_DAYS=7
GOOGLE_CLIENT_ID=xxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=xxx
RESEND_API_KEY=re_xxx
FRONTEND_URL=http://localhost:4200
ENVIRONMENT=development

# backend/.env.prod
DATABASE_URL=postgresql+asyncpg://user:pass@ep-yyy.us-east-1.aws.neon.tech/logos_prod
JWT_SECRET=prod-super-secret-from-vault
# ... credenciales reales de Google, Resend, pasarela de pagos
FRONTEND_URL=https://logosschool.cl
ENVIRONMENT=production
```

### Neon Branches (BD por entorno)
```
Proyecto Neon: logos-school
├── Main branch (producción) → logos_prod
└── Dev branch (desarrollo) → logos_dev
    ├── feature/auth-refactor
    ├── feature/nuevo-simulacro
    └── fix/calculo-nota
```
**Regla**: Cada PR crea branch temporal en Neon → migraciones automáticas → tests → merge a dev → deploy a Render staging.

### Render (Backend) + Cloudflare Pages (Frontend)
```yaml
# render.yaml (backend)
services:
  - type: web
    name: logos-backend
    runtime: python
    buildCommand: "pip install -r requirements.txt && alembic upgrade head"
    startCommand: "uvicorn src.api.main:app --host 0.0.0.0 --port $PORT"
    envVars:
      - key: DATABASE_URL
        fromDatabase: logos-postgres
      - key: JWT_SECRET
        generateValue: true
      - key: GOOGLE_CLIENT_ID
        sync: false
      # ... otras secrets

# cloudflare-pages (frontend)
# Build command: npm run build
# Output directory: dist/frontend/browser
# Environment variables: VITE_API_URL=https://api.logosschool.cl
```

---

## Scripts de Calidad y QA

### `scripts/qa_completo.sh`
```bash
#!/bin/bash
set -e

echo "🔍 QA COMPLETO - Logos School"
echo "================================"

# 1. Backend
cd backend
echo "📦 Instalando dependencias..."
uv sync

echo "🧪 Tests unitarios + integración..."
pytest --cov=src --cov-fail-under=80 -q

echo "🔧 Linting (ruff)..."
ruff check src/
ruff format --check src/

echo "🔐 Security (bandit)..."
bandit -r src/ -q

# 2. Frontend
cd ../frontend
echo "📦 Instalando dependencias..."
npm ci

echo "🔧 Linting (ESLint)..."
npm run lint

echo "🎨 Formato (Prettier)..."
npm run format:check

echo "🧪 Tests unitarios (Vitest/Jest)..."
npm run test:unit

echo "🌐 Tests E2E (Playwright)..."
npm run test:e2e

# 3. Contenido
cd ..
echo "📚 Validando calidad contenido..."
python scripts/validar_calidad_contenido.py --strict

echo "✅ QA COMPLETO EXITOSO"
```

### `scripts/validar_calidad_contenido.py` (Resumen)
```python
# Verifica:
# - 408 OA tienen guía + preguntas + prueba_unidad + presencia en simulacro
# - Metadatos completos (codigo, nivel, asignatura, dificultad, bloom)
# - Distribución simulacro por régimen (Decreto 439/2012, 614/2013, 193/2019)
# - Preguntas: 1 correcta, 3 distractores, retroalimentación por opción
# - No duplicados (enunciado + opciones)
# - Cobertura 100% OA oficiales
```

---

## Checklist de Desarrollo (Antes de PR)

### Backend
- [ ] Tests unitarios dominio/aplicación: 100% pasando
- [ ] Tests integración API: cubren happy path + errores dominio
- [ ] Cobertura ≥ 80% (excluyendo migraciones, config)
- [ ] Ruff: 0 errores, 0 warnings
- [ ] Migración Alembic generada y probada en dev branch
- [ ] No imports circulares (verificar `python -m pyflakes src/`)
- [ ] Docstrings en casos de uso públicos y entidades

### Frontend
- [ ] Build exitoso (`npm run build`)
- [ ] ESLint: 0 errores
- [ ] Prettier: formato correcto
- [ ] Tests unitarios componentes críticos: pasando
- [ ] Tests E2E: 69/69 en verde
- [ ] Accesibilidad: axe-core sin errores críticos
- [ ] Responsive: probado en móvil (375px), tablet (768px), desktop (1440px)
- [ ] Temas visuales: básico-inicial, básico-media, media aplicados correctamente

### Contenido
- [ ] `python scripts/validar_calidad_contenido.py` pasa sin errores
- [ ] Cambios en OA reflejados en guías, preguntas, pruebas, simulacros
- [ ] Régimen C (3°-4° medio) auditado por separado (asignaturas únicas)

---

## Referencias Cruzadas

| Documento | Qué define |
|-----------|------------|
| `planificacion/02-modelo-de-datos-conceptual.md` | Entidades, relaciones, cardinalidades |
| `planificacion/11-especificacion-mvp-para-desarrollo.md` | Modelo de datos con campos, pantallas, flujos, reglas MVP |
| `planificacion/12-motor-de-evaluacion.md` | Cálculo nota 1.0-7.0, exigencia 60%, cronómetro, autosave |
| `planificacion/17-infraestructura-y-entornos.md` | Dev/Prod separados, Neon branches, Render, Cloudflare, Resend, Sentry |
| `planificacion/22-analisis-de-brechas.md` | Auditoría real: qué está conectado, qué falta, qué no funciona |
| `contenido/00-estado-contenido.md` | Qué contenido existe por curso/asignatura (fuente de verdad para importar) |

---

## Comandos Útiles Diarios

```bash
# Backend
cd backend
uv run uvicorn src.api.main:app --reload --port 8000    # Dev server
uv run pytest tests/ -v --tb=short                      # Tests
uv run ruff check src/ && uv run ruff format src/       # Lint + format
alembic upgrade head                                     # Migraciones

# Frontend
cd frontend
npm run start                                           # Dev server (4200)
npm run build                                           # Build prod
npm run test:e2e                                        # Playwright
npm run lint && npm run format:check                    # Calidad código

# Full stack (desde raíz)
./scripts/qa_completo.sh                                # QA completo
```

---

## Actualización
- Basado en código verificado 2026-08-14 (326 backend tests, 69 frontend tests)
- Arquitectura hexagonal implementada en `backend/src/`
- Angular 18+ standalone components en `frontend/src/app/`
- Próxima revisión: antes de Fase 2 Brincus (IA, Juegos, Biblioteca) o deployment