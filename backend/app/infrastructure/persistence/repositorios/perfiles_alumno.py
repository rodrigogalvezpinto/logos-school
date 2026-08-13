from sqlmodel import Session, select

from app.domain.auth.entities import PerfilAlumno as PerfilAlumnoDominio
from app.infrastructure.persistence.orm_models import PerfilAlumno as PerfilAlumnoORM


class RepositorioPerfilesAlumnoSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def guardar(self, perfil: PerfilAlumnoDominio) -> PerfilAlumnoDominio:
        fila = PerfilAlumnoORM(
            cuenta_apoderado_id=perfil.cuenta_apoderado_id,
            nombre=perfil.nombre,
            apellidos=perfil.apellidos,
            fecha_nacimiento=perfil.fecha_nacimiento,
            rut=perfil.rut,
            nivel_id=perfil.nivel_id,
        )
        self._session.add(fila)
        self._session.commit()
        self._session.refresh(fila)
        return self._a_dominio(fila)

    def buscar_por_id(self, perfil_id: int) -> PerfilAlumnoDominio | None:
        fila = self._session.get(PerfilAlumnoORM, perfil_id)
        return self._a_dominio(fila) if fila else None

    def listar_por_cuenta(self, cuenta_apoderado_id: int) -> list[PerfilAlumnoDominio]:
        filas = self._session.exec(
            select(PerfilAlumnoORM).where(PerfilAlumnoORM.cuenta_apoderado_id == cuenta_apoderado_id)
        ).all()
        return [self._a_dominio(f) for f in filas]

    @staticmethod
    def _a_dominio(fila: PerfilAlumnoORM) -> PerfilAlumnoDominio:
        return PerfilAlumnoDominio(
            id=fila.id,
            cuenta_apoderado_id=fila.cuenta_apoderado_id,
            nombre=fila.nombre,
            apellidos=fila.apellidos,
            fecha_nacimiento=fila.fecha_nacimiento,
            rut=fila.rut,
            nivel_id=fila.nivel_id,
            fecha_creacion=fila.fecha_creacion,
        )
