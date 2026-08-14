from sqlmodel import Session, func, or_, select

from app.domain.auth.entities import PerfilAlumno as PerfilAlumnoDominio
from app.domain.auth.value_objects import limpiar_rut
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

    def buscar_por_rut(self, rut: str) -> PerfilAlumnoDominio | None:
        # Compara normalizado (sin puntos/guión) para que "21.345.678-4" y "21345678-4"
        # se detecten como el mismo RUT — la tabla es pequeña (alumnos, no la población de
        # Chile), así que filtrar en Python es aceptable y evita depender de una función
        # SQL específica de motor para limpiar el string en la query.
        objetivo = limpiar_rut(rut)
        filas = self._session.exec(select(PerfilAlumnoORM)).all()
        for fila in filas:
            if limpiar_rut(fila.rut) == objetivo:
                return self._a_dominio(fila)
        return None

    def listar_por_cuenta(self, cuenta_apoderado_id: int) -> list[PerfilAlumnoDominio]:
        filas = self._session.exec(
            select(PerfilAlumnoORM).where(PerfilAlumnoORM.cuenta_apoderado_id == cuenta_apoderado_id)
        ).all()
        return [self._a_dominio(f) for f in filas]

    def buscar_por_texto(self, consulta: str) -> list[PerfilAlumnoDominio]:
        """Búsqueda no acotada a una cuenta — la usa el panel de administración para
        encontrar cualquier alumno por nombre, apellido o RUT (a diferencia de
        `listar_por_cuenta`, que un Apoderado usa solo para los suyos)."""
        patron = f"%{consulta}%"
        filas = self._session.exec(
            select(PerfilAlumnoORM).where(
                or_(
                    PerfilAlumnoORM.nombre.ilike(patron),
                    PerfilAlumnoORM.apellidos.ilike(patron),
                    PerfilAlumnoORM.rut.ilike(patron),
                )
            )
        ).all()
        return [self._a_dominio(f) for f in filas]

    def contar(self) -> int:
        return self._session.exec(select(func.count()).select_from(PerfilAlumnoORM)).one()

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
