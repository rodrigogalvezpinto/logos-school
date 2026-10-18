from sqlmodel import Session, select

from app.domain.plan_lector.ports import LibroLectura
from app.infrastructure.persistence.orm_models import LibroPlanLector as LibroORM


class RepositorioPlanLectorSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def listar_por_nivel(self, nivel_id: int) -> list[LibroLectura]:
        filas = self._session.exec(
            select(LibroORM).where(LibroORM.nivel_id == nivel_id).order_by(LibroORM.orden)
        ).all()
        return [LibroLectura(id=f.id, titulo=f.titulo, autor=f.autor, editorial=f.editorial) for f in filas]
