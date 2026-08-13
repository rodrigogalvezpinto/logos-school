from sqlmodel import Session, select

from app.domain.auth.entities import Cuenta as CuentaDominio
from app.infrastructure.persistence.orm_models import Cuenta as CuentaORM


class RepositorioCuentasSQLModel:
    """Adaptador del puerto RepositorioCuentas — traduce entre la fila SQLModel y la
    entidad de dominio en el borde de la capa de persistencia."""

    def __init__(self, session: Session):
        self._session = session

    def buscar_por_email(self, email: str) -> CuentaDominio | None:
        fila = self._session.exec(select(CuentaORM).where(CuentaORM.email == email)).first()
        return self._a_dominio(fila) if fila else None

    def buscar_por_google_id(self, google_id: str) -> CuentaDominio | None:
        fila = self._session.exec(select(CuentaORM).where(CuentaORM.google_id == google_id)).first()
        return self._a_dominio(fila) if fila else None

    def buscar_por_id(self, cuenta_id: int) -> CuentaDominio | None:
        fila = self._session.get(CuentaORM, cuenta_id)
        return self._a_dominio(fila) if fila else None

    def guardar(self, cuenta: CuentaDominio) -> CuentaDominio:
        if cuenta.id is None:
            fila = CuentaORM(
                email=cuenta.email,
                nombre=cuenta.nombre,
                password_hash=cuenta.password_hash,
                google_id=cuenta.google_id,
                comuna_o_region=cuenta.comuna_o_region,
                pais=cuenta.pais,
            )
        else:
            fila = self._session.get(CuentaORM, cuenta.id)
            fila.email = cuenta.email
            fila.nombre = cuenta.nombre
            fila.password_hash = cuenta.password_hash
            fila.google_id = cuenta.google_id
            fila.comuna_o_region = cuenta.comuna_o_region
            fila.pais = cuenta.pais
        self._session.add(fila)
        self._session.commit()
        self._session.refresh(fila)
        return self._a_dominio(fila)

    @staticmethod
    def _a_dominio(fila: CuentaORM) -> CuentaDominio:
        return CuentaDominio(
            id=fila.id,
            email=fila.email,
            nombre=fila.nombre,
            password_hash=fila.password_hash,
            google_id=fila.google_id,
            comuna_o_region=fila.comuna_o_region,
            pais=fila.pais,
            fecha_creacion=fila.fecha_creacion,
        )
