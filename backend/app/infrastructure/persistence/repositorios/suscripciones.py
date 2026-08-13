from datetime import date, datetime

from sqlmodel import Session, select

from app.domain.comercial.ports import ActivasPorPlan
from app.infrastructure.persistence.orm_models import Plan as PlanORM
from app.infrastructure.persistence.orm_models import Suscripcion as SuscripcionORM


class RepositorioSuscripcionesSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def asignar_cortesia(self, perfil_alumno_id: int, plan_id: int, ahora: datetime) -> None:
        fila = self._session.exec(
            select(SuscripcionORM)
            .where(SuscripcionORM.perfil_alumno_id == perfil_alumno_id)
            .order_by(SuscripcionORM.fecha_inicio.desc())
        ).first()
        if fila:
            fila.plan_id = plan_id
            fila.origen = "cortesia"
            fila.estado = "activa"
            fila.fecha_inicio = ahora
            fila.fecha_termino = None
        else:
            fila = SuscripcionORM(
                perfil_alumno_id=perfil_alumno_id, plan_id=plan_id,
                fecha_inicio=ahora, estado="activa", origen="cortesia",
            )
        self._session.add(fila)
        self._session.commit()

    def asignar_prueba_gratis(
        self, perfil_alumno_id: int, plan_id: int, ahora: datetime, fecha_termino: datetime
    ) -> None:
        fila = self._session.exec(
            select(SuscripcionORM)
            .where(SuscripcionORM.perfil_alumno_id == perfil_alumno_id)
            .order_by(SuscripcionORM.fecha_inicio.desc())
        ).first()
        if fila:
            fila.plan_id = plan_id
            fila.origen = "prueba_gratis"
            fila.estado = "activa"
            fila.fecha_inicio = ahora
            fila.fecha_termino = fecha_termino
        else:
            fila = SuscripcionORM(
                perfil_alumno_id=perfil_alumno_id, plan_id=plan_id,
                fecha_inicio=ahora, fecha_termino=fecha_termino, estado="activa", origen="prueba_gratis",
            )
        self._session.add(fila)
        self._session.commit()

    def contar_activas_por_plan(self) -> list[ActivasPorPlan]:
        filas = self._session.exec(
            select(SuscripcionORM.plan_id, SuscripcionORM.id).where(SuscripcionORM.estado == "activa")
        ).all()
        conteo: dict[int, int] = {}
        for plan_id, _ in filas:
            conteo[plan_id] = conteo.get(plan_id, 0) + 1
        return [ActivasPorPlan(plan_id=plan_id, cantidad=cantidad) for plan_id, cantidad in conteo.items()]

    def sumar_ingresos_mes_pago(self, anio: int, mes: int) -> int:
        inicio_mes = date(anio, mes, 1)
        inicio_mes_siguiente = date(anio + 1, 1, 1) if mes == 12 else date(anio, mes + 1, 1)

        filas = self._session.exec(
            select(SuscripcionORM, PlanORM)
            .join(PlanORM, SuscripcionORM.plan_id == PlanORM.id)
            .where(SuscripcionORM.origen == "pago")
        ).all()

        total = 0
        for suscripcion, plan in filas:
            fecha = suscripcion.fecha_inicio.date()
            if inicio_mes <= fecha < inicio_mes_siguiente:
                total += plan.precio_clp
        return total
