"""Panel de administración comercial: Planes, Códigos de descuento, cuentas de cortesía y
métricas básicas — ver planificacion/18-panel-administrador.md. Todo protegido por
`get_cuenta_admin_actual` (sesión de CuentaAdmin, distinta de la del Apoderado)."""

from datetime import date, datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel

from app.application.comercial.casos_de_uso import (
    AsignarSuscripcionCortesia,
    CambiarEstadoPlan,
    CrearCodigoDescuento,
    CrearPlan,
    DesactivarCodigoDescuento,
    EditarPlan,
)
from app.application.comercial.consultas import BuscarAlumnos, ObtenerMetricas
from app.core.deps import (
    get_asignar_suscripcion_cortesia_uc,
    get_buscar_alumnos_uc,
    get_cambiar_estado_plan_uc,
    get_crear_codigo_descuento_uc,
    get_crear_plan_uc,
    get_cuenta_admin_actual,
    get_desactivar_codigo_descuento_uc,
    get_editar_plan_uc,
    get_obtener_metricas_uc,
    get_repositorio_descuentos,
    get_repositorio_planes,
)
from app.domain.comercial.exceptions import (
    AlumnoNoEncontrado,
    CodigoDescuentoDuplicado,
    CodigoDescuentoNoEncontrado,
    PlanNoEncontrado,
)
from app.domain.comercial.ports import RepositorioDescuentos, RepositorioPlanes

router = APIRouter(prefix="/admin", tags=["comercial"], dependencies=[Depends(get_cuenta_admin_actual)])


# ---------- Planes ----------

class PlanRespuesta(BaseModel):
    id: int
    nombre: str
    nivel_de_acceso: str
    precio_clp: int
    activo: bool


class CrearPlanRequest(BaseModel):
    nombre: str
    nivel_de_acceso: str
    precio_clp: int


class EditarPlanRequest(BaseModel):
    nombre: str
    nivel_de_acceso: str
    precio_clp: int


def _plan_a_respuesta(p) -> PlanRespuesta:
    return PlanRespuesta(id=p.id, nombre=p.nombre, nivel_de_acceso=p.nivel_de_acceso, precio_clp=p.precio_clp, activo=p.activo)


@router.get("/planes", response_model=list[PlanRespuesta])
def listar_planes(repositorio: RepositorioPlanes = Depends(get_repositorio_planes)):
    return [_plan_a_respuesta(p) for p in repositorio.listar()]


@router.post("/planes", response_model=PlanRespuesta, status_code=201)
def crear_plan(datos: CrearPlanRequest, uc: CrearPlan = Depends(get_crear_plan_uc)):
    try:
        plan = uc.ejecutar(datos.nombre, datos.nivel_de_acceso, datos.precio_clp)
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return _plan_a_respuesta(plan)


@router.patch("/planes/{plan_id}", response_model=PlanRespuesta)
def editar_plan(plan_id: int, datos: EditarPlanRequest, uc: EditarPlan = Depends(get_editar_plan_uc)):
    try:
        plan = uc.ejecutar(plan_id, datos.nombre, datos.nivel_de_acceso, datos.precio_clp)
    except PlanNoEncontrado:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return _plan_a_respuesta(plan)


@router.post("/planes/{plan_id}/activar", response_model=PlanRespuesta)
def activar_plan(plan_id: int, uc: CambiarEstadoPlan = Depends(get_cambiar_estado_plan_uc)):
    try:
        plan = uc.ejecutar(plan_id, activo=True)
    except PlanNoEncontrado:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    return _plan_a_respuesta(plan)


@router.post("/planes/{plan_id}/desactivar", response_model=PlanRespuesta)
def desactivar_plan(plan_id: int, uc: CambiarEstadoPlan = Depends(get_cambiar_estado_plan_uc)):
    try:
        plan = uc.ejecutar(plan_id, activo=False)
    except PlanNoEncontrado:
        raise HTTPException(status_code=404, detail="Plan no encontrado")
    return _plan_a_respuesta(plan)


# ---------- Códigos de descuento ----------

class DescuentoRespuesta(BaseModel):
    id: int
    codigo: str
    tipo: str
    valor: int
    fecha_vencimiento: date | None
    usos_maximos: int | None
    usos_actuales: int
    vigente: bool


class CrearDescuentoRequest(BaseModel):
    codigo: str
    tipo: str
    valor: int
    fecha_vencimiento: date | None = None
    usos_maximos: int | None = None


def _descuento_a_respuesta(d) -> DescuentoRespuesta:
    return DescuentoRespuesta(
        id=d.id, codigo=d.codigo, tipo=d.tipo, valor=d.valor,
        fecha_vencimiento=d.fecha_vencimiento, usos_maximos=d.usos_maximos, usos_actuales=d.usos_actuales,
        vigente=d.vigente(datetime.now(timezone.utc).date()),
    )


@router.get("/descuentos", response_model=list[DescuentoRespuesta])
def listar_descuentos(repositorio: RepositorioDescuentos = Depends(get_repositorio_descuentos)):
    return [_descuento_a_respuesta(d) for d in repositorio.listar()]


@router.post("/descuentos", response_model=DescuentoRespuesta, status_code=201)
def crear_descuento(datos: CrearDescuentoRequest, uc: CrearCodigoDescuento = Depends(get_crear_codigo_descuento_uc)):
    try:
        descuento = uc.ejecutar(datos.codigo, datos.tipo, datos.valor, datos.fecha_vencimiento, datos.usos_maximos)
    except CodigoDescuentoDuplicado:
        raise HTTPException(status_code=400, detail="Ya existe un código de descuento con ese código")
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return _descuento_a_respuesta(descuento)


@router.post("/descuentos/{descuento_id}/desactivar", response_model=DescuentoRespuesta)
def desactivar_descuento(descuento_id: int, uc: DesactivarCodigoDescuento = Depends(get_desactivar_codigo_descuento_uc)):
    try:
        descuento = uc.ejecutar(descuento_id)
    except CodigoDescuentoNoEncontrado:
        raise HTTPException(status_code=404, detail="Código de descuento no encontrado")
    return _descuento_a_respuesta(descuento)


# ---------- Alumnos / cortesías ----------

class AlumnoEncontradoRespuesta(BaseModel):
    perfil_alumno_id: int
    nombre: str
    apellidos: str
    rut: str
    email_apoderado: str


class AsignarCortesiaRequest(BaseModel):
    plan_id: int


@router.get("/alumnos/buscar", response_model=list[AlumnoEncontradoRespuesta])
def buscar_alumnos(q: str, uc: BuscarAlumnos = Depends(get_buscar_alumnos_uc)):
    return [
        AlumnoEncontradoRespuesta(
            perfil_alumno_id=a.perfil_alumno_id, nombre=a.nombre, apellidos=a.apellidos,
            rut=a.rut, email_apoderado=a.email_apoderado,
        )
        for a in uc.ejecutar(q)
    ]


@router.post("/alumnos/{perfil_alumno_id}/cortesia", status_code=204)
def asignar_cortesia(
    perfil_alumno_id: int, datos: AsignarCortesiaRequest,
    uc: AsignarSuscripcionCortesia = Depends(get_asignar_suscripcion_cortesia_uc),
):
    try:
        uc.ejecutar(perfil_alumno_id, datos.plan_id)
    except AlumnoNoEncontrado:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")
    except PlanNoEncontrado:
        raise HTTPException(status_code=404, detail="Plan no encontrado")


# ---------- Métricas ----------

class SuscripcionesPorPlanRespuesta(BaseModel):
    plan_id: int
    plan_nombre: str
    activas: int


class MetricasRespuesta(BaseModel):
    apoderados_registrados: int
    alumnos_registrados: int
    suscripciones_por_plan: list[SuscripcionesPorPlanRespuesta]
    ingresos_mes_aprox_clp: int


@router.get("/metricas", response_model=MetricasRespuesta)
def obtener_metricas(uc: ObtenerMetricas = Depends(get_obtener_metricas_uc)):
    m = uc.ejecutar(datetime.now(timezone.utc))
    return MetricasRespuesta(
        apoderados_registrados=m.apoderados_registrados,
        alumnos_registrados=m.alumnos_registrados,
        suscripciones_por_plan=[
            SuscripcionesPorPlanRespuesta(plan_id=s.plan_id, plan_nombre=s.plan_nombre, activas=s.activas)
            for s in m.suscripciones_por_plan
        ],
        ingresos_mes_aprox_clp=m.ingresos_mes_aprox_clp,
    )
