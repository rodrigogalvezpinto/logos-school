from datetime import timezone

from sqlmodel import Session, select

from app.domain.calificaciones.entities import CalificacionGuia as CalificacionDominio
from app.infrastructure.persistence.orm_models import CalificacionGuia as CalificacionORM


class RepositorioCalificacionesSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def guardar_o_actualizar(self, calificacion: CalificacionDominio) -> CalificacionDominio:
        fila = self._session.exec(
            select(CalificacionORM).where(
                CalificacionORM.oa_id == calificacion.oa_id,
                CalificacionORM.perfil_alumno_id == calificacion.perfil_alumno_id,
            )
        ).first()
        if fila:
            fila.estrellas = calificacion.estrellas
            fila.fecha = calificacion.fecha
        else:
            fila = CalificacionORM(
                oa_id=calificacion.oa_id, perfil_alumno_id=calificacion.perfil_alumno_id,
                estrellas=calificacion.estrellas, fecha=calificacion.fecha,
            )
        self._session.add(fila)
        self._session.commit()
        self._session.refresh(fila)
        return self._a_dominio(fila)

    def buscar_mia(self, oa_id: int, perfil_alumno_id: int) -> CalificacionDominio | None:
        fila = self._session.exec(
            select(CalificacionORM).where(
                CalificacionORM.oa_id == oa_id, CalificacionORM.perfil_alumno_id == perfil_alumno_id,
            )
        ).first()
        return self._a_dominio(fila) if fila else None

    @staticmethod
    def _a_dominio(fila: CalificacionORM) -> CalificacionDominio:
        fecha = fila.fecha if fila.fecha.tzinfo is not None else fila.fecha.replace(tzinfo=timezone.utc)
        return CalificacionDominio(
            id=fila.id, oa_id=fila.oa_id, perfil_alumno_id=fila.perfil_alumno_id,
            estrellas=fila.estrellas, fecha=fecha,
        )
