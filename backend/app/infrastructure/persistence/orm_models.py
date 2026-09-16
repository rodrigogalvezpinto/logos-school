"""Modelos de datos — reflejan 1:1 planificacion/11-especificacion-mvp-para-desarrollo.md
y las extensiones de planificacion/18-panel-administrador.md (Plan/Suscripcion/CodigoDescuento).
"""

from datetime import datetime, date, timezone
from typing import Optional

from sqlalchemy import Column, Index, JSON, UniqueConstraint, text
from sqlmodel import Field, SQLModel


def _ahora_utc() -> datetime:
    return datetime.now(timezone.utc)


class Cuenta(SQLModel, table=True):
    """El Apoderado (o cualquier adulto que matricula) — única entidad con login real."""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: Optional[str] = None  # nullable: puede registrarse solo con Google
    google_id: Optional[str] = Field(default=None, unique=True, index=True)
    nombre: str
    comuna_o_region: Optional[str] = None
    pais: Optional[str] = None
    fecha_creacion: datetime = Field(default_factory=_ahora_utc)
    sesion_version: int = Field(default=0)


class CuentaAdmin(SQLModel, table=True):
    """Cuenta del panel de administración comercial (planificacion/18-panel-administrador.md)
    — entidad separada de `Cuenta` (Apoderado) a propósito: login, sesión y JWT distintos,
    sin endpoint de auto-registro (se crea con scripts/crear_admin.py)."""

    __tablename__ = "cuenta_admin"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    nombre: str
    fecha_creacion: datetime = Field(default_factory=_ahora_utc)


class CuentaProfesor(SQLModel, table=True):
    """Cuenta del rol Profesor (Etapa 2, planificacion/01-roles-y-permisos.md) — entidad
    separada de `Cuenta` y `CuentaAdmin`, mismo criterio: login/sesión/JWT propios. A
    diferencia de `CuentaAdmin`, sí tiene auto-registro, pero nace `estado="pendiente"` y
    la aprueba un Administrador desde el panel comercial (`CuentaAdmin`)."""

    __tablename__ = "cuenta_profesor"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    nombre: str
    estado: str = "pendiente"  # "pendiente" | "aprobado" | "rechazado"
    fecha_creacion: datetime = Field(default_factory=_ahora_utc)


class Nivel(SQLModel, table=True):
    """Dato semilla — uno de los 12 niveles, cargado desde Temarios/analisis/."""

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(unique=True)  # "4° básico"
    regimen: str  # "A" | "B" | "C"
    decreto: str
    formato_examen: str  # "integrado" | "separado_por_asignatura"
    num_preguntas_examen: int
    duracion_examen_min: int
    materiales_permitidos: Optional[str] = None
    # Orden curricular real (1 = 1° básico ... 12 = 4° medio) — el `id` NO sirve para esto:
    # en la base de Desarrollo, 4° básico (el piloto) se importó primero y quedó con id=1,
    # antes que 1°-3° básico. Bug real encontrado construyendo "repasar años anteriores"
    # (ver planificacion/25-analisis-competencia-brincus.md): comparar por `id` dejaba a
    # 4° básico sin ningún "nivel anterior" disponible, cuando obviamente sí los tiene.
    orden: Optional[int] = None


class Plan(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    nivel_de_acceso: str  # "entrada" | "completo"
    precio_clp: int = 0
    activo: bool = True


class PerfilAlumno(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    cuenta_apoderado_id: int = Field(foreign_key="cuenta.id")
    nombre: str
    apellidos: str
    fecha_nacimiento: date
    rut: str
    nivel_id: int = Field(foreign_key="nivel.id")
    # Nullable: un alumno en autoestudio puro nunca pertenece a un Curso/Sección — solo se
    # llena si un Profesor lo agrega (el alumno no puede autoagregarse, ver
    # planificacion/01-roles-y-permisos.md). Un alumno pertenece a un curso a la vez.
    curso_seccion_id: Optional[int] = Field(default=None, foreign_key="curso_seccion.id")
    fecha_creacion: datetime = Field(default_factory=_ahora_utc)


class CodigoDescuento(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    codigo: str = Field(unique=True)
    tipo: str  # "porcentaje" | "monto_fijo"
    valor: int
    fecha_vencimiento: Optional[date] = None
    usos_maximos: Optional[int] = None
    usos_actuales: int = 0


class Suscripcion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    perfil_alumno_id: int = Field(foreign_key="perfilalumno.id")
    plan_id: int = Field(foreign_key="plan.id")
    fecha_inicio: datetime = Field(default_factory=_ahora_utc)
    fecha_termino: Optional[datetime] = None
    estado: str = "activa"  # "activa" | "vencida" | "cancelada"
    origen: str = "pago"  # "pago" | "cortesia"
    codigo_descuento_id: Optional[int] = Field(default=None, foreign_key="codigodescuento.id")


class Asignatura(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nivel_id: int = Field(foreign_key="nivel.id")
    nombre: str


class ObjetivoAprendizaje(SQLModel, table=True):
    __tablename__ = "objetivo_aprendizaje"

    id: Optional[int] = Field(default=None, primary_key=True)
    asignatura_id: int = Field(foreign_key="asignatura.id")
    codigo_oficial: str  # "OA 7"
    descripcion: str
    eje_tematico: Optional[str] = None
    contenido_guia: str = ""


class Pregunta(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    # Nullable: las preguntas del banco de autoevaluación siempre tienen oa_id; las de
    # pruebas de unidad/exámenes simulacro se vinculan a un OA "best effort" (se busca por
    # código en la pauta) y pueden quedar sin vínculo exacto sin que eso bloquee el import.
    oa_id: Optional[int] = Field(default=None, foreign_key="objetivo_aprendizaje.id")
    asignatura_id: Optional[int] = Field(default=None, foreign_key="asignatura.id")
    tipo: str  # "alternativas" | "verdadero_falso" | "desarrollo_breve" | ...
    enunciado: str
    opciones: Optional[list[str]] = Field(default=None, sa_column=Column(JSON))
    respuesta_correcta: str
    retroalimentacion: str = ""
    nivel_dificultad: Optional[str] = None


class ConjuntoEvaluacion(SQLModel, table=True):
    __tablename__ = "conjunto_evaluacion"

    id: Optional[int] = Field(default=None, primary_key=True)
    tipo: str  # "prueba_unidad" | "examen_simulacro"
    asignatura_id: Optional[int] = Field(default=None, foreign_key="asignatura.id")
    nivel_id: Optional[int] = Field(default=None, foreign_key="nivel.id")
    nombre: str
    forma: Optional[str] = None  # "A" | "B"
    pregunta_ids: list[int] = Field(default_factory=list, sa_column=Column(JSON))
    tiempo_sugerido_min: Optional[int] = None  # null si no tiene cronómetro (pruebas de unidad)
    # Simulacro con fecha programada por el Admin (Fase 1, ítem 2.1 del plan de
    # incorporación de hallazgos de Brincus) — null = disponibilidad normal por cobertura,
    # como hoy. Si tiene valor, el conjunto queda "próximamente" hasta esa fecha/hora.
    fecha_programada: Optional[datetime] = None


class IntentoEvaluacion(SQLModel, table=True):
    __tablename__ = "intento_evaluacion"
    __table_args__ = (
        # Como máximo un intento SIN terminar por (alumno, conjunto) — sin esto, dos
        # requests simultáneos a "iniciar intento" (doble clic, dos pestañas cargando a
        # la vez) podían crear dos intentos activos distintos para la misma prueba, en
        # vez de reanudar el mismo (bug real encontrado con un test de concurrencia:
        # 10 requests simultáneos crearon 3 intentos en vez de 1).
        Index(
            "ix_intento_evaluacion_activo_unico",
            "perfil_alumno_id",
            "conjunto_evaluacion_id",
            unique=True,
            postgresql_where=text("fecha_termino IS NULL"),
        ),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    perfil_alumno_id: int = Field(foreign_key="perfilalumno.id")
    conjunto_evaluacion_id: int = Field(foreign_key="conjunto_evaluacion.id")
    fecha_inicio: datetime = Field(default_factory=_ahora_utc)
    fecha_termino: Optional[datetime] = None
    respuestas: dict[str, str] = Field(default_factory=dict, sa_column=Column(JSON))
    puntaje: Optional[float] = None
    nota: Optional[float] = None
    tiempo_usado_seg: Optional[int] = None


class ProgresoOA(SQLModel, table=True):
    __tablename__ = "progreso_oa"

    id: Optional[int] = Field(default=None, primary_key=True)
    perfil_alumno_id: int = Field(foreign_key="perfilalumno.id")
    oa_id: int = Field(foreign_key="objetivo_aprendizaje.id")
    estado: str = "no_iniciado"  # "no_iniciado" | "en_progreso" | "dominado"
    ultimo_intento_fecha: Optional[datetime] = None


class PlanDeEstudio(SQLModel, table=True):
    __tablename__ = "plan_de_estudio"

    id: Optional[int] = Field(default=None, primary_key=True)
    perfil_alumno_id: int = Field(foreign_key="perfilalumno.id")
    dias_por_semana: int
    dias_elegidos: list[str] = Field(default_factory=list, sa_column=Column(JSON))
    fecha_inicio: date
    fecha_objetivo: Optional[date] = None


class SesionEstudio(SQLModel, table=True):
    __tablename__ = "sesion_estudio"

    id: Optional[int] = Field(default=None, primary_key=True)
    plan_estudio_id: int = Field(foreign_key="plan_de_estudio.id")
    fecha_programada: date
    asignatura_id: int = Field(foreign_key="asignatura.id")
    oa_ids: list[int] = Field(default_factory=list, sa_column=Column(JSON))
    incluye_prueba_unidad: bool = False
    es_repaso: bool = False
    # Sin columna `estado` a propósito — se calcula al leer, comparando oa_ids contra las
    # guías revisadas actuales (ver domain/plan_estudio/entities.py, SesionEstudio.esta_cumplida).


class CursoSeccion(SQLModel, table=True):
    __tablename__ = "curso_seccion"

    id: Optional[int] = Field(default=None, primary_key=True)
    profesor_id: int = Field(foreign_key="cuenta_profesor.id")
    nivel_id: int = Field(foreign_key="nivel.id")
    nombre: str  # "6° básico A"


class Comunicado(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    curso_seccion_id: int = Field(foreign_key="curso_seccion.id")
    titulo: str
    cuerpo: str
    fecha: datetime = Field(default_factory=_ahora_utc)


class PerfilGamificacion(SQLModel, table=True):
    """Gamificación (Fase 1, ítem 2.2 — ver
    planificacion/27-plan-incorporacion-hallazgos-brincus.md). Una fila por alumno,
    creada on-demand (`obtener_o_crear`) la primera vez que gana XP o consulta su perfil."""

    __tablename__ = "perfil_gamificacion"

    id: Optional[int] = Field(default=None, primary_key=True)
    perfil_alumno_id: int = Field(foreign_key="perfilalumno.id", unique=True)
    xp: int = 0
    avatar_id: str = "monstruo_azul"
    racha_dias_actual: int = 0
    racha_dias_maxima: int = 0
    ultima_actividad_fecha: Optional[date] = None
    guias_revisadas_total: int = 0
    evaluaciones_entregadas_total: int = 0
    tiempo_evaluando_total_seg: int = 0


class ProgresoOnboarding(SQLModel, table=True):
    """Onboarding con checklist de primera sesión (Fase 1, ítem 2.3 — ver
    planificacion/27-plan-incorporacion-hallazgos-brincus.md). Una fila por alumno,
    creada on-demand igual que `PerfilGamificacion`."""

    __tablename__ = "progreso_onboarding"

    id: Optional[int] = Field(default=None, primary_key=True)
    perfil_alumno_id: int = Field(foreign_key="perfilalumno.id", unique=True)
    pasos_completados: list[str] = Field(default_factory=list, sa_column=Column(JSON))


class RegistroAnimo(SQLModel, table=True):
    """Check-in emocional diario (Fase 1, ítem 2.4 — ver
    planificacion/27-plan-incorporacion-hallazgos-brincus.md). Único índice
    (perfil_alumno_id, fecha) — un registro por alumno por día."""

    __tablename__ = "registro_animo"
    __table_args__ = (Index("ix_registro_animo_perfil_fecha", "perfil_alumno_id", "fecha", unique=True),)

    id: Optional[int] = Field(default=None, primary_key=True)
    perfil_alumno_id: int = Field(foreign_key="perfilalumno.id")
    estado: str
    fecha: date


class AgendaFamiliarConversada(SQLModel, table=True):
    """Idea 7 del boceto de innovación (2026-08-17): "ya conversamos" de la agenda familiar
    del domingo — un registro por (alumno, semana) para que la tarjeta no insista una vez
    marcada, mismo patrón de índice único que `RegistroAnimo`."""

    __tablename__ = "agenda_familiar_conversada"
    __table_args__ = (Index("ix_agenda_familiar_perfil_semana", "perfil_alumno_id", "semana_inicio", unique=True),)

    id: Optional[int] = Field(default=None, primary_key=True)
    perfil_alumno_id: int = Field(foreign_key="perfilalumno.id")
    semana_inicio: date


class LibroPlanLector(SQLModel, table=True):
    """Plan Lector curado por nivel (título/autor/editorial) — hallazgo comparando en vivo
    contra Brincus: tiene un Plan Lector real por curso, contenido de valor percibido alto
    y costo de mantención bajo, que Logos no tenía pese a tener Lenguaje como asignatura
    central. Piloto en 4° básico (ver planificacion/25-analisis-competencia-brincus.md);
    misma lógica de "no inventar, elegir con criterio pedagógico propio" que el resto del
    contenido (planificacion/04-modo-de-operacion.md) — libros reales y ampliamente usados
    en colegios chilenos para esta edad, no una lista arbitraria."""

    __tablename__ = "libro_plan_lector"

    id: Optional[int] = Field(default=None, primary_key=True)
    nivel_id: int = Field(foreign_key="nivel.id")
    orden: int
    titulo: str
    autor: str
    editorial: str


class UtilEscolar(SQLModel, table=True):
    """Lista de útiles escolares por nivel — hallazgo comparando en vivo contra Brincus
    (sección "Informaciones", ver planificacion/25-analisis-competencia-brincus.md, Paso
    12): un listado simple de materiales a comprar por curso, contenido estático de costo de
    mantención bajísimo que hoy un apoderado de Logos tendría que buscar aparte. `asignatura`
    es opcional (algunos útiles son generales, ej. "estuche", no de una materia puntual)."""

    __tablename__ = "util_escolar"

    id: Optional[int] = Field(default=None, primary_key=True)
    nivel_id: int = Field(foreign_key="nivel.id")
    orden: int
    nombre: str
    cantidad: Optional[str] = None
    asignatura: Optional[str] = None


class Sugerencia(SQLModel, table=True):
    """Buzón de sugerencias (Fase 1 — ver planificacion/27-plan-incorporacion-hallazgos-brincus.md,
    Paso 13, hallazgo comparando en vivo contra Brincus: canal explícito y visible para
    proponer mejoras, no escondido en un correo de soporte)."""

    __tablename__ = "sugerencia"

    id: Optional[int] = Field(default=None, primary_key=True)
    perfil_alumno_id: int = Field(foreign_key="perfilalumno.id")
    texto: str
    fecha: datetime = Field(default_factory=_ahora_utc)


class CalificacionGuia(SQLModel, table=True):
    """Calificación con estrellas por guía (Fase 1 — ver
    planificacion/27-plan-incorporacion-hallazgos-brincus.md, cuarta pasada): señal de
    calidad de contenido más liviana y positiva que "Reportar error". Un alumno puede
    recalificar la misma guía — se actualiza la fila existente, no se acumulan duplicados
    (índice único sobre oa_id + perfil_alumno_id)."""

    __tablename__ = "calificacion_guia"
    __table_args__ = (UniqueConstraint("oa_id", "perfil_alumno_id", name="ix_calificacion_guia_oa_perfil"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    oa_id: int = Field(foreign_key="objetivo_aprendizaje.id")
    perfil_alumno_id: int = Field(foreign_key="perfilalumno.id")
    estrellas: int
    fecha: datetime = Field(default_factory=_ahora_utc)


class ReporteError(SQLModel, table=True):
    """Reportar error de contenido (Fase 1, ítems 2.1 y 2.6 — ver
    planificacion/27-plan-incorporacion-hallazgos-brincus.md). `tipo_contenido` genérico
    ("pregunta" hoy, "guia"/"video" a futuro) para no migrar de nuevo al extenderlo."""

    __tablename__ = "reporte_error"

    id: Optional[int] = Field(default=None, primary_key=True)
    tipo_contenido: str
    contenido_id: int
    perfil_alumno_id: int = Field(foreign_key="perfilalumno.id")
    comentario: str
    fecha: datetime = Field(default_factory=_ahora_utc)
    resuelto: bool = False
