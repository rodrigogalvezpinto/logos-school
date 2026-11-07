from sqlmodel import Session, select

from app.domain.comercial.entities import Plan as PlanDominio
from app.infrastructure.persistence.orm_models import Plan as PlanORM


class RepositorioPlanesSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def buscar_por_id(self, plan_id: int) -> PlanDominio | None:
        fila = self._session.get(PlanORM, plan_id)
        return self._a_dominio(fila) if fila else None

    def listar(self) -> list[PlanDominio]:
        filas = self._session.exec(select(PlanORM)).all()
        return [self._a_dominio(f) for f in filas]

    def guardar(self, plan: PlanDominio) -> PlanDominio:
        if plan.id is None:
            fila = PlanORM(
                nombre=plan.nombre, nivel_de_acceso=plan.nivel_de_acceso,
                precio_clp=plan.precio_clp, activo=plan.activo,
            )
        else:
            fila = self._session.get(PlanORM, plan.id)
            fila.nombre = plan.nombre
            fila.nivel_de_acceso = plan.nivel_de_acceso
            fila.precio_clp = plan.precio_clp
            fila.activo = plan.activo
        self._session.add(fila)
        self._session.commit()
        self._session.refresh(fila)
        return self._a_dominio(fila)

    @staticmethod
    def _a_dominio(fila: PlanORM) -> PlanDominio:
        return PlanDominio(
            id=fila.id, nombre=fila.nombre, nivel_de_acceso=fila.nivel_de_acceso,
            precio_clp=fila.precio_clp, activo=fila.activo,
        )
