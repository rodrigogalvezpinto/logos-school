from sqlmodel import Session, select

from app.domain.evaluaciones.ports import ConjuntoLectura
from app.infrastructure.persistence.orm_models import ConjuntoEvaluacion as ConjuntoORM


class RepositorioConjuntosSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def buscar_por_id(self, conjunto_id: int) -> ConjuntoLectura | None:
        fila = self._session.get(ConjuntoORM, conjunto_id)
        return self._a_lectura(fila) if fila else None

    def listar_por_asignatura(self, asignatura_id: int) -> list[ConjuntoLectura]:
        filas = self._session.exec(
            select(ConjuntoORM).where(ConjuntoORM.asignatura_id == asignatura_id)
        ).all()
        return [self._a_lectura(f) for f in filas]

    def listar_por_nivel(self, nivel_id: int) -> list[ConjuntoLectura]:
        filas = self._session.exec(select(ConjuntoORM).where(ConjuntoORM.nivel_id == nivel_id)).all()
        return [self._a_lectura(f) for f in filas]

    @staticmethod
    def _a_lectura(fila: ConjuntoORM) -> ConjuntoLectura:
        return ConjuntoLectura(
            id=fila.id,
            tipo=fila.tipo,
            nombre=fila.nombre,
            forma=fila.forma,
            tiempo_sugerido_min=fila.tiempo_sugerido_min,
            pregunta_ids=list(fila.pregunta_ids),
        )
