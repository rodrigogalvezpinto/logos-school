from sqlmodel import Session, select

from app.domain.evaluaciones.ports import PreguntaLectura
from app.domain.evaluaciones.value_objects import PreguntaParaCorreccion
from app.infrastructure.persistence.orm_models import ObjetivoAprendizaje as ObjetivoAprendizajeORM
from app.infrastructure.persistence.orm_models import Pregunta as PreguntaORM


class RepositorioPreguntasSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def existe_objetivo(self, oa_id: int) -> bool:
        return self._session.get(ObjetivoAprendizajeORM, oa_id) is not None

    def buscar_por_oa(self, oa_id: int) -> list[PreguntaLectura]:
        filas = self._session.exec(select(PreguntaORM).where(PreguntaORM.oa_id == oa_id)).all()
        return [self._a_lectura(f) for f in filas]

    def listar_por_ids(self, ids: list[int]) -> list[PreguntaLectura]:
        filas = [self._session.get(PreguntaORM, pid) for pid in ids]
        return [self._a_lectura(f) for f in filas if f]

    def listar_para_correccion(self, ids: list[int]) -> list[PreguntaParaCorreccion]:
        filas = [self._session.get(PreguntaORM, pid) for pid in ids]
        return [
            PreguntaParaCorreccion(id=f.id, tipo=f.tipo, respuesta_correcta=f.respuesta_correcta)
            for f in filas
            if f
        ]

    @staticmethod
    def _a_lectura(fila: PreguntaORM) -> PreguntaLectura:
        return PreguntaLectura(
            id=fila.id,
            tipo=fila.tipo,
            enunciado=fila.enunciado,
            opciones=fila.opciones,
            respuesta_correcta=fila.respuesta_correcta,
            retroalimentacion=fila.retroalimentacion,
            oa_id=fila.oa_id,
        )
