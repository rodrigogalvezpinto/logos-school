from sqlmodel import Session, select

from app.domain.profesor.entities import CuentaProfesor as CuentaProfesorDominio
from app.infrastructure.persistence.orm_models import CuentaProfesor as CuentaProfesorORM


class RepositorioCuentasProfesorSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def buscar_por_email(self, email: str) -> CuentaProfesorDominio | None:
        fila = self._session.exec(select(CuentaProfesorORM).where(CuentaProfesorORM.email == email)).first()
        return self._a_dominio(fila) if fila else None

    def buscar_por_id(self, cuenta_profesor_id: int) -> CuentaProfesorDominio | None:
        fila = self._session.get(CuentaProfesorORM, cuenta_profesor_id)
        return self._a_dominio(fila) if fila else None

    def guardar(self, cuenta: CuentaProfesorDominio) -> CuentaProfesorDominio:
        if cuenta.id is None:
            fila = CuentaProfesorORM(
                email=cuenta.email, nombre=cuenta.nombre, password_hash=cuenta.password_hash, estado=cuenta.estado,
            )
        else:
            fila = self._session.get(CuentaProfesorORM, cuenta.id)
            fila.email = cuenta.email
            fila.nombre = cuenta.nombre
            fila.password_hash = cuenta.password_hash
            fila.estado = cuenta.estado
        self._session.add(fila)
        self._session.commit()
        self._session.refresh(fila)
        return self._a_dominio(fila)

    def listar_pendientes(self) -> list[CuentaProfesorDominio]:
        filas = self._session.exec(select(CuentaProfesorORM).where(CuentaProfesorORM.estado == "pendiente")).all()
        return [self._a_dominio(f) for f in filas]

    @staticmethod
    def _a_dominio(fila: CuentaProfesorORM) -> CuentaProfesorDominio:
        return CuentaProfesorDominio(
            id=fila.id, email=fila.email, nombre=fila.nombre, password_hash=fila.password_hash, estado=fila.estado,
        )
