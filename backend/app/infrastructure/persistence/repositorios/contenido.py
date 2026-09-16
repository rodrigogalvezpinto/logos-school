from sqlmodel import Session, select

from app.domain.contenido.ports import AsignaturaLectura, NivelLectura, ObjetivoLectura
from app.infrastructure.persistence.orm_models import Asignatura as AsignaturaORM
from app.infrastructure.persistence.orm_models import Nivel as NivelORM
from app.infrastructure.persistence.orm_models import ObjetivoAprendizaje as ObjetivoORM


class RepositorioContenidoSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def existe_nivel(self, nivel_id: int) -> bool:
        return self._session.get(NivelORM, nivel_id) is not None

    def obtener_nivel(self, nivel_id: int) -> NivelLectura | None:
        fila = self._session.get(NivelORM, nivel_id)
        return self._nivel_a_lectura(fila) if fila else None

    def listar_niveles(self) -> list[NivelLectura]:
        # `order_by(orden)` es obligatorio acá: sin él, Postgres no garantiza ningún
        # orden en particular (ver Nivel.orden en orm_models.py) — un <select> de nivel
        # en el frontend que asume "el primero es el más bajo" (ej. profesor-dashboard.ts
        # al crear un Curso/Sección) quedaba a merced del orden físico de la tabla.
        filas = self._session.exec(select(NivelORM).order_by(NivelORM.orden)).all()
        return [self._nivel_a_lectura(f) for f in filas]

    @staticmethod
    def _nivel_a_lectura(fila: NivelORM) -> NivelLectura:
        return NivelLectura(
            id=fila.id, nombre=fila.nombre, regimen=fila.regimen,
            num_preguntas_examen=fila.num_preguntas_examen, duracion_examen_min=fila.duracion_examen_min,
            orden=fila.orden,
        )

    def listar_asignaturas(self, nivel_id: int) -> list[AsignaturaLectura]:
        filas = self._session.exec(select(AsignaturaORM).where(AsignaturaORM.nivel_id == nivel_id)).all()
        return [AsignaturaLectura(id=f.id, nombre=f.nombre, nivel_id=f.nivel_id) for f in filas]

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
        return AsignaturaLectura(id=fila.id, nombre=fila.nombre, nivel_id=fila.nivel_id) if fila else None

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
