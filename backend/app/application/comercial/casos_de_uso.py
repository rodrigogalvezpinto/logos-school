from app.domain.comercial.entities import CodigoDescuento, Plan
from app.domain.comercial.exceptions import AlumnoNoEncontrado, CodigoDescuentoNoEncontrado, PlanNoEncontrado
from app.domain.comercial.ports import RepositorioDescuentos, RepositorioPlanes, RepositorioSuscripciones
from app.domain.auth.ports import RepositorioPerfilesAlumno
from app.domain.shared.reloj import Reloj


class CrearPlan:
    def __init__(self, repositorio_planes: RepositorioPlanes):
        self._repositorio_planes = repositorio_planes

    def ejecutar(self, nombre: str, nivel_de_acceso: str, precio_clp: int) -> Plan:
        plan = Plan.crear(nombre, nivel_de_acceso, precio_clp)
        return self._repositorio_planes.guardar(plan)


class EditarPlan:
    def __init__(self, repositorio_planes: RepositorioPlanes):
        self._repositorio_planes = repositorio_planes

    def ejecutar(self, plan_id: int, nombre: str, nivel_de_acceso: str, precio_clp: int) -> Plan:
        plan = self._repositorio_planes.buscar_por_id(plan_id)
        if not plan:
            raise PlanNoEncontrado()
        plan.editar(nombre, nivel_de_acceso, precio_clp)
        return self._repositorio_planes.guardar(plan)


class CambiarEstadoPlan:
    """Cubre activar/desactivar — misma forma, invierte el booleano que ejecuta."""

    def __init__(self, repositorio_planes: RepositorioPlanes):
        self._repositorio_planes = repositorio_planes

    def ejecutar(self, plan_id: int, activo: bool) -> Plan:
        plan = self._repositorio_planes.buscar_por_id(plan_id)
        if not plan:
            raise PlanNoEncontrado()
        plan.activar() if activo else plan.desactivar()
        return self._repositorio_planes.guardar(plan)


class CrearCodigoDescuento:
    def __init__(self, repositorio_descuentos: RepositorioDescuentos):
        self._repositorio_descuentos = repositorio_descuentos

    def ejecutar(
        self, codigo: str, tipo: str, valor: int, fecha_vencimiento, usos_maximos: int | None
    ) -> CodigoDescuento:
        descuento = CodigoDescuento.crear(codigo, tipo, valor, fecha_vencimiento, usos_maximos)
        return self._repositorio_descuentos.guardar(descuento)


class DesactivarCodigoDescuento:
    def __init__(self, repositorio_descuentos: RepositorioDescuentos, reloj: Reloj):
        self._repositorio_descuentos = repositorio_descuentos
        self._reloj = reloj

    def ejecutar(self, descuento_id: int) -> CodigoDescuento:
        descuento = self._repositorio_descuentos.buscar_por_id(descuento_id)
        if not descuento:
            raise CodigoDescuentoNoEncontrado()
        descuento.desactivar(self._reloj.ahora().date())
        return self._repositorio_descuentos.guardar(descuento)


class AsignarSuscripcionCortesia:
    def __init__(
        self,
        repositorio_suscripciones: RepositorioSuscripciones,
        repositorio_perfiles: RepositorioPerfilesAlumno,
        repositorio_planes: RepositorioPlanes,
        reloj: Reloj,
    ):
        self._repositorio_suscripciones = repositorio_suscripciones
        self._repositorio_perfiles = repositorio_perfiles
        self._repositorio_planes = repositorio_planes
        self._reloj = reloj

    def ejecutar(self, perfil_alumno_id: int, plan_id: int) -> None:
        if not self._repositorio_perfiles.buscar_por_id(perfil_alumno_id):
            raise AlumnoNoEncontrado()
        if not self._repositorio_planes.buscar_por_id(plan_id):
            raise PlanNoEncontrado()
        self._repositorio_suscripciones.asignar_cortesia(perfil_alumno_id, plan_id, self._reloj.ahora())
