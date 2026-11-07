from sqlmodel import Session, select

from app.domain.comercial.entities import CodigoDescuento as CodigoDescuentoDominio
from app.infrastructure.persistence.orm_models import CodigoDescuento as CodigoDescuentoORM


class RepositorioDescuentosSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def buscar_por_id(self, descuento_id: int) -> CodigoDescuentoDominio | None:
        fila = self._session.get(CodigoDescuentoORM, descuento_id)
        return self._a_dominio(fila) if fila else None

    def buscar_por_codigo(self, codigo: str) -> CodigoDescuentoDominio | None:
        fila = self._session.exec(select(CodigoDescuentoORM).where(CodigoDescuentoORM.codigo == codigo)).first()
        return self._a_dominio(fila) if fila else None

    def listar(self) -> list[CodigoDescuentoDominio]:
        filas = self._session.exec(select(CodigoDescuentoORM)).all()
        return [self._a_dominio(f) for f in filas]

    def guardar(self, descuento: CodigoDescuentoDominio) -> CodigoDescuentoDominio:
        if descuento.id is None:
            fila = CodigoDescuentoORM(
                codigo=descuento.codigo, tipo=descuento.tipo, valor=descuento.valor,
                fecha_vencimiento=descuento.fecha_vencimiento, usos_maximos=descuento.usos_maximos,
                usos_actuales=descuento.usos_actuales,
            )
        else:
            fila = self._session.get(CodigoDescuentoORM, descuento.id)
            fila.codigo = descuento.codigo
            fila.tipo = descuento.tipo
            fila.valor = descuento.valor
            fila.fecha_vencimiento = descuento.fecha_vencimiento
            fila.usos_maximos = descuento.usos_maximos
            fila.usos_actuales = descuento.usos_actuales
        self._session.add(fila)
        self._session.commit()
        self._session.refresh(fila)
        return self._a_dominio(fila)

    @staticmethod
    def _a_dominio(fila: CodigoDescuentoORM) -> CodigoDescuentoDominio:
        return CodigoDescuentoDominio(
            id=fila.id, codigo=fila.codigo, tipo=fila.tipo, valor=fila.valor,
            fecha_vencimiento=fila.fecha_vencimiento, usos_maximos=fila.usos_maximos,
            usos_actuales=fila.usos_actuales,
        )
