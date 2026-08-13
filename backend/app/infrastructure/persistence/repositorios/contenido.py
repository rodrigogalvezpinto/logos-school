from sqlmodel import Session, select

from app.domain.contenido.ports import AsignaturaLectura, NivelLectura, ObjetivoLectura
from app.infrastructure.persistence.orm_models import Asignatura as AsignaturaORM
from app.infrastructure.persistence.orm_models import Nivel as NivelORM
from app.infrastructure.persistence.orm_models import ObjetivoAprendizaje as ObjetivoORM


class RepositorioContenidoSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def listar_niveles(self) -> list[NivelLectura]:
        filas = self._session.exec(select(NivelORM)).all()
        return [
            NivelLectura(
                id=f.id, nombre=f.nombre, regimen=f.regimen,
                num_preguntas_examen=f.num_preguntas_examen, duracion_examen_min=f.duracion_examen_min,
            )
            for f in filas
        ]

    def listar_asignaturas(self, nivel_id: int) -> list[AsignaturaLectura]:
        filas = self._session.exec(select(AsignaturaORM).where(AsignaturaORM.nivel_id == nivel_id)).all()
        return [AsignaturaLectura(id=f.id, nombre=f.nombre) for f in filas]

    def listar_objetivos(self, asignatura_id: int) -> list[ObjetivoLectura]:
        filas = self._session.exec(
            select(ObjetivoORM).where(ObjetivoORM.asignatura_id == asignatura_id)
        ).all()
        return [self._a_lectura(f) for f in filas]

    def obtener_objetivo(self, oa_id: int) -> ObjetivoLectura | None:
        fila = self._session.get(ObjetivoORM, oa_id)
        return self._a_lectura(fila) if fila else None

    def obtener_asignatura(self, asignatura_id: int) -> AsignaturaLectura | None:
        fila = self._session.get(AsignaturaORM, asignatura_id)
        return AsignaturaLectura(id=fila.id, nombre=fila.nombre) if fila else None

    @staticmethod
    def _a_lectura(fila: ObjetivoORM) -> ObjetivoLectura:
        return ObjetivoLectura(
            id=fila.id,
            asignatura_id=fila.asignatura_id,
            codigo_oficial=fila.codigo_oficial,
            descripcion=fila.descripcion,
            eje_tematico=fila.eje_tematico,
            contenido_guia=fila.contenido_guia,
        )
