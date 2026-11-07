from datetime import date

from sqlmodel import Session, select

from app.domain.bienestar.entities import RegistroAnimo as RegistroDominio
from app.infrastructure.persistence.orm_models import RegistroAnimo as RegistroORM


class RepositorioBienestarSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def buscar_de_fecha(self, perfil_alumno_id: int, fecha: date) -> RegistroDominio | None:
        fila = self._session.exec(
            select(RegistroORM).where(
                RegistroORM.perfil_alumno_id == perfil_alumno_id,
                RegistroORM.fecha == fecha,
            )
        ).first()
        return self._a_dominio(fila) if fila else None

    def guardar(self, registro: RegistroDominio) -> RegistroDominio:
        fila = RegistroORM(perfil_alumno_id=registro.perfil_alumno_id, estado=registro.estado, fecha=registro.fecha)
        self._session.add(fila)
        self._session.commit()
        self._session.refresh(fila)
        return self._a_dominio(fila)

    @staticmethod
    def _a_dominio(fila: RegistroORM) -> RegistroDominio:
        return RegistroDominio(id=fila.id, perfil_alumno_id=fila.perfil_alumno_id, estado=fila.estado, fecha=fila.fecha)
