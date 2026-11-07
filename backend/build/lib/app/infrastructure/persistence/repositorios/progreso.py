from datetime import datetime, timezone

from sqlmodel import Session, select

from app.domain.progreso.ports import GuiaRevisada
from app.infrastructure.persistence.orm_models import Asignatura, ObjetivoAprendizaje
from app.infrastructure.persistence.orm_models import ProgresoOA as ProgresoORM


class RepositorioProgresoSQLModel:
    """Misma normalización de timezone que RepositorioIntentosSQLModel: la columna
    `ultimo_intento_fecha` es TIMESTAMP WITHOUT TIME ZONE, así que se re-adjunta UTC al
    leer para que el dominio nunca vea un datetime naive."""

    def __init__(self, session: Session):
        self._session = session

    def marcar_guia_revisada(self, perfil_alumno_id: int, oa_id: int, fecha: datetime) -> None:
        fila = self._session.exec(
            select(ProgresoORM).where(
                ProgresoORM.perfil_alumno_id == perfil_alumno_id,
                ProgresoORM.oa_id == oa_id,
            )
        ).first()
        if fila:
            fila.ultimo_intento_fecha = fecha
            if fila.estado == "no_iniciado":
                fila.estado = "en_progreso"
        else:
            fila = ProgresoORM(
                perfil_alumno_id=perfil_alumno_id,
                oa_id=oa_id,
                estado="en_progreso",
                ultimo_intento_fecha=fecha,
            )
        self._session.add(fila)
        self._session.commit()

    def listar_guias_revisadas(self, perfil_alumno_id: int) -> list[GuiaRevisada]:
        filas = self._session.exec(
            select(ProgresoORM, ObjetivoAprendizaje, Asignatura)
            .join(ObjetivoAprendizaje, ProgresoORM.oa_id == ObjetivoAprendizaje.id)
            .join(Asignatura, ObjetivoAprendizaje.asignatura_id == Asignatura.id)
            .where(ProgresoORM.perfil_alumno_id == perfil_alumno_id)
        ).all()
        return [
            GuiaRevisada(
                oa_id=f.oa_id,
                fecha=self._con_tz(f.ultimo_intento_fecha),
                codigo_oficial=oa.codigo_oficial,
                asignatura_nombre=asignatura.nombre,
            )
            for f, oa, asignatura in filas
            if f.ultimo_intento_fecha is not None
        ]

    @staticmethod
    def _con_tz(valor: datetime) -> datetime:
        return valor if valor.tzinfo is not None else valor.replace(tzinfo=timezone.utc)
