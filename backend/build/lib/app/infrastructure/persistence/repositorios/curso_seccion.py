from sqlmodel import Session, select

from app.domain.curso_seccion.entities import CursoSeccion as CursoSeccionDominio
from app.domain.curso_seccion.ports import AlumnoDeCurso
from app.infrastructure.persistence.orm_models import CursoSeccion as CursoSeccionORM
from app.infrastructure.persistence.orm_models import PerfilAlumno as PerfilAlumnoORM


class RepositorioCursosSeccionSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def crear(self, curso: CursoSeccionDominio) -> CursoSeccionDominio:
        fila = CursoSeccionORM(profesor_id=curso.profesor_id, nivel_id=curso.nivel_id, nombre=curso.nombre)
        self._session.add(fila)
        self._session.commit()
        self._session.refresh(fila)
        return self._a_dominio(fila)

    def buscar_por_id(self, curso_id: int) -> CursoSeccionDominio | None:
        fila = self._session.get(CursoSeccionORM, curso_id)
        return self._a_dominio(fila) if fila else None

    def listar_por_profesor(self, profesor_id: int) -> list[CursoSeccionDominio]:
        filas = self._session.exec(select(CursoSeccionORM).where(CursoSeccionORM.profesor_id == profesor_id)).all()
        return [self._a_dominio(f) for f in filas]

    def agregar_alumno(self, curso_id: int, perfil_alumno_id: int) -> None:
        perfil = self._session.get(PerfilAlumnoORM, perfil_alumno_id)
        perfil.curso_seccion_id = curso_id
        self._session.add(perfil)
        self._session.commit()

    def quitar_alumno(self, perfil_alumno_id: int) -> None:
        perfil = self._session.get(PerfilAlumnoORM, perfil_alumno_id)
        if perfil:
            perfil.curso_seccion_id = None
            self._session.add(perfil)
            self._session.commit()

    def listar_alumnos(self, curso_id: int) -> list[AlumnoDeCurso]:
        filas = self._session.exec(select(PerfilAlumnoORM).where(PerfilAlumnoORM.curso_seccion_id == curso_id)).all()
        return [AlumnoDeCurso(perfil_alumno_id=f.id, nombre=f.nombre, apellidos=f.apellidos) for f in filas]

    def buscar_curso_del_alumno(self, perfil_alumno_id: int) -> CursoSeccionDominio | None:
        perfil = self._session.get(PerfilAlumnoORM, perfil_alumno_id)
        if not perfil or not perfil.curso_seccion_id:
            return None
        return self.buscar_por_id(perfil.curso_seccion_id)

    @staticmethod
    def _a_dominio(fila: CursoSeccionORM) -> CursoSeccionDominio:
        return CursoSeccionDominio(id=fila.id, profesor_id=fila.profesor_id, nivel_id=fila.nivel_id, nombre=fila.nombre)
