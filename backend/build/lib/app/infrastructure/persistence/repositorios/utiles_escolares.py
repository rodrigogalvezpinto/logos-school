from sqlmodel import Session, select

from app.domain.utiles_escolares.ports import UtilEscolarLectura
from app.infrastructure.persistence.orm_models import UtilEscolar as UtilEscolarORM


class RepositorioUtilesEscolaresSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def listar_por_nivel(self, nivel_id: int) -> list[UtilEscolarLectura]:
        filas = self._session.exec(
            select(UtilEscolarORM).where(UtilEscolarORM.nivel_id == nivel_id).order_by(UtilEscolarORM.orden)
        ).all()
        return [
            UtilEscolarLectura(id=f.id, nombre=f.nombre, cantidad=f.cantidad, asignatura=f.asignatura)
            for f in filas
        ]
