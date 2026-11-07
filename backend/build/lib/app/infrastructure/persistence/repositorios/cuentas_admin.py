from sqlmodel import Session, select

from app.domain.admin.entities import CuentaAdmin as CuentaAdminDominio
from app.infrastructure.persistence.orm_models import CuentaAdmin as CuentaAdminORM


class RepositorioCuentasAdminSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def buscar_por_email(self, email: str) -> CuentaAdminDominio | None:
        fila = self._session.exec(select(CuentaAdminORM).where(CuentaAdminORM.email == email)).first()
        return self._a_dominio(fila) if fila else None

    def buscar_por_id(self, cuenta_admin_id: int) -> CuentaAdminDominio | None:
        fila = self._session.get(CuentaAdminORM, cuenta_admin_id)
        return self._a_dominio(fila) if fila else None

    @staticmethod
    def _a_dominio(fila: CuentaAdminORM) -> CuentaAdminDominio:
        return CuentaAdminDominio(id=fila.id, email=fila.email, nombre=fila.nombre, password_hash=fila.password_hash)
