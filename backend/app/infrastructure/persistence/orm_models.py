"""Modelos de datos — reflejan 1:1 planificacion/11-especificacion-mvp-para-desarrollo.md
y las extensiones de planificacion/18-panel-administrador.md (Plan/Suscripcion/CodigoDescuento).
"""

from datetime import datetime, date, timezone
from typing import Optional

from sqlalchemy import Column, JSON
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


class IntentoEvaluacion(SQLModel, table=True):
    __tablename__ = "intento_evaluacion"

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
