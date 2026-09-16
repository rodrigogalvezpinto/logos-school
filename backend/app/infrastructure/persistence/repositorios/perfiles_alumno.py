from sqlmodel import Session, func, or_, select

from app.domain.auth.entities import PerfilAlumno as PerfilAlumnoDominio
from app.domain.auth.value_objects import limpiar_rut
from app.infrastructure.persistence.orm_models import (
    AgendaFamiliarConversada,
    CalificacionGuia,
    IntentoEvaluacion,
    PerfilAlumno as PerfilAlumnoORM,
    PerfilGamificacion,
    PlanDeEstudio,
    ProgresoOA,
    ProgresoOnboarding,
    RegistroAnimo,
    ReporteError,
    SesionEstudio,
    Sugerencia,
    Suscripcion,
)


class RepositorioPerfilesAlumnoSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def guardar(self, perfil: PerfilAlumnoDominio) -> PerfilAlumnoDominio:
        fila = PerfilAlumnoORM(
            cuenta_apoderado_id=perfil.cuenta_apoderado_id,
            nombre=perfil.nombre,
            apellidos=perfil.apellidos,
            fecha_nacimiento=perfil.fecha_nacimiento,
            rut=perfil.rut,
            nivel_id=perfil.nivel_id,
        )
        self._session.add(fila)
        self._session.commit()
        self._session.refresh(fila)
        return self._a_dominio(fila)

    def buscar_por_id(self, perfil_id: int) -> PerfilAlumnoDominio | None:
        fila = self._session.get(PerfilAlumnoORM, perfil_id)
        return self._a_dominio(fila) if fila else None

    def buscar_por_rut(self, rut: str) -> PerfilAlumnoDominio | None:
        # Compara normalizado (sin puntos/guión) para que "21.345.678-4" y "21345678-4"
        # se detecten como el mismo RUT — la tabla es pequeña (alumnos, no la población de
        # Chile), así que filtrar en Python es aceptable y evita depender de una función
        # SQL específica de motor para limpiar el string en la query.
        objetivo = limpiar_rut(rut)
        filas = self._session.exec(select(PerfilAlumnoORM)).all()
        for fila in filas:
            if limpiar_rut(fila.rut) == objetivo:
                return self._a_dominio(fila)
        return None

    def listar_por_cuenta(self, cuenta_apoderado_id: int) -> list[PerfilAlumnoDominio]:
        filas = self._session.exec(
            select(PerfilAlumnoORM).where(PerfilAlumnoORM.cuenta_apoderado_id == cuenta_apoderado_id)
        ).all()
        return [self._a_dominio(f) for f in filas]

    def buscar_por_texto(self, consulta: str) -> list[PerfilAlumnoDominio]:
        """Búsqueda no acotada a una cuenta — la usa el panel de administración para
        encontrar cualquier alumno por nombre, apellido o RUT (a diferencia de
        `listar_por_cuenta`, que un Apoderado usa solo para los suyos)."""
        patron = f"%{consulta}%"
        filas = self._session.exec(
            select(PerfilAlumnoORM).where(
                or_(
                    PerfilAlumnoORM.nombre.ilike(patron),
                    PerfilAlumnoORM.apellidos.ilike(patron),
                    PerfilAlumnoORM.rut.ilike(patron),
                )
            )
        ).all()
        return [self._a_dominio(f) for f in filas]

    def contar(self) -> int:
        return self._session.exec(select(func.count()).select_from(PerfilAlumnoORM)).one()

    def eliminar_en_cascada(self, perfil_id: int) -> None:
        # Los planes de estudio tienen su propia tabla hija (sesiones) que hay que borrar
        # primero por la FK — mismo orden que ya usa `reemplazar_plan` en
        # repositorios/plan_estudio.py.
        for plan in self._session.exec(select(PlanDeEstudio).where(PlanDeEstudio.perfil_alumno_id == perfil_id)).all():
            for sesion in self._session.exec(select(SesionEstudio).where(SesionEstudio.plan_estudio_id == plan.id)).all():
                self._session.delete(sesion)
            self._session.commit()  # confirmar el borrado de las sesiones antes del plan padre (FK)
            self._session.delete(plan)
            self._session.commit()

        tablas_hijas = [
            Suscripcion, IntentoEvaluacion, ProgresoOA, PerfilGamificacion, ProgresoOnboarding,
            RegistroAnimo, AgendaFamiliarConversada, Sugerencia, CalificacionGuia, ReporteError,
        ]
        for tabla in tablas_hijas:
            for fila in self._session.exec(select(tabla).where(tabla.perfil_alumno_id == perfil_id)).all():
                self._session.delete(fila)
        self._session.commit()  # confirmar el borrado de las tablas hijas antes del perfil padre (FK)

        fila_perfil = self._session.get(PerfilAlumnoORM, perfil_id)
        if fila_perfil:
            self._session.delete(fila_perfil)

        self._session.commit()

    @staticmethod
    def _a_dominio(fila: PerfilAlumnoORM) -> PerfilAlumnoDominio:
        return PerfilAlumnoDominio(
            id=fila.id,
            cuenta_apoderado_id=fila.cuenta_apoderado_id,
            nombre=fila.nombre,
            apellidos=fila.apellidos,
            fecha_nacimiento=fila.fecha_nacimiento,
            rut=fila.rut,
            nivel_id=fila.nivel_id,
            fecha_creacion=fila.fecha_creacion,
        )
