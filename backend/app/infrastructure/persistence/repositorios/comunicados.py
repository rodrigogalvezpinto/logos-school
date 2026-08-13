from datetime import datetime, timezone

from sqlmodel import Session, select

from app.domain.curso_seccion.entities import Comunicado as ComunicadoDominio
from app.infrastructure.persistence.orm_models import Comunicado as ComunicadoORM


class RepositorioComunicadosSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def crear(self, comunicado: ComunicadoDominio) -> ComunicadoDominio:
        fila = ComunicadoORM(
            curso_seccion_id=comunicado.curso_seccion_id, titulo=comunicado.titulo,
            cuerpo=comunicado.cuerpo, fecha=comunicado.fecha,
        )
        self._session.add(fila)
        self._session.commit()
        self._session.refresh(fila)
        return self._a_dominio(fila)

    def listar_por_curso(self, curso_id: int) -> list[ComunicadoDominio]:
        filas = self._session.exec(
            select(ComunicadoORM).where(ComunicadoORM.curso_seccion_id == curso_id).order_by(ComunicadoORM.fecha.desc())
        ).all()
        return [self._a_dominio(f) for f in filas]

    @staticmethod
    def _con_tz(valor: datetime) -> datetime:
        return valor if valor.tzinfo is not None else valor.replace(tzinfo=timezone.utc)

    @classmethod
    def _a_dominio(cls, fila: ComunicadoORM) -> ComunicadoDominio:
        return ComunicadoDominio(
            id=fila.id, curso_seccion_id=fila.curso_seccion_id, titulo=fila.titulo,
            cuerpo=fila.cuerpo, fecha=cls._con_tz(fila.fecha),
        )
