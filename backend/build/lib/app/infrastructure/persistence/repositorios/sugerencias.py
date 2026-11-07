from datetime import timezone

from sqlmodel import Session, select

from app.domain.sugerencias.entities import Sugerencia as SugerenciaDominio
from app.infrastructure.persistence.orm_models import Sugerencia as SugerenciaORM


class RepositorioSugerenciasSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def guardar(self, sugerencia: SugerenciaDominio) -> SugerenciaDominio:
        fila = SugerenciaORM(
            perfil_alumno_id=sugerencia.perfil_alumno_id, texto=sugerencia.texto, fecha=sugerencia.fecha,
        )
        self._session.add(fila)
        self._session.commit()
        self._session.refresh(fila)
        return self._a_dominio(fila)

    def listar_por_perfil(self, perfil_alumno_id: int) -> list[SugerenciaDominio]:
        filas = self._session.exec(
            select(SugerenciaORM)
            .where(SugerenciaORM.perfil_alumno_id == perfil_alumno_id)
            .order_by(SugerenciaORM.fecha.desc())
        ).all()
        return [self._a_dominio(f) for f in filas]

    @staticmethod
    def _a_dominio(fila: SugerenciaORM) -> SugerenciaDominio:
        fecha = fila.fecha if fila.fecha.tzinfo is not None else fila.fecha.replace(tzinfo=timezone.utc)
        return SugerenciaDominio(id=fila.id, perfil_alumno_id=fila.perfil_alumno_id, texto=fila.texto, fecha=fecha)
