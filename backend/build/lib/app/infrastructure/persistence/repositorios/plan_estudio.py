from sqlmodel import Session, select

from app.domain.plan_estudio.entities import PlanDeEstudio as PlanDominio
from app.domain.plan_estudio.entities import SesionEstudio as SesionDominio
from app.infrastructure.persistence.orm_models import PlanDeEstudio as PlanORM
from app.infrastructure.persistence.orm_models import SesionEstudio as SesionORM


class RepositorioPlanEstudioSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def buscar_activo_por_perfil(self, perfil_alumno_id: int) -> PlanDominio | None:
        fila_plan = self._session.exec(
            select(PlanORM).where(PlanORM.perfil_alumno_id == perfil_alumno_id)
        ).first()
        if not fila_plan:
            return None
        filas_sesiones = self._session.exec(
            select(SesionORM).where(SesionORM.plan_estudio_id == fila_plan.id)
        ).all()
        return self._a_dominio(fila_plan, filas_sesiones)

    def reemplazar_plan(self, plan: PlanDominio) -> PlanDominio:
        existente = self._session.exec(
            select(PlanORM).where(PlanORM.perfil_alumno_id == plan.perfil_alumno_id)
        ).first()
        if existente:
            for sesion_vieja in self._session.exec(
                select(SesionORM).where(SesionORM.plan_estudio_id == existente.id)
            ).all():
                self._session.delete(sesion_vieja)
            self._session.commit()  # borrar las sesiones hijas antes del plan padre (FK)
            self._session.delete(existente)
            self._session.commit()

        fila_plan = PlanORM(
            perfil_alumno_id=plan.perfil_alumno_id,
            dias_por_semana=plan.dias_por_semana,
            dias_elegidos=plan.dias_elegidos,
            fecha_inicio=plan.fecha_inicio,
            fecha_objetivo=plan.fecha_objetivo,
        )
        self._session.add(fila_plan)
        self._session.commit()
        self._session.refresh(fila_plan)

        filas_sesiones = []
        for sesion in plan.sesiones:
            fila_sesion = SesionORM(
                plan_estudio_id=fila_plan.id,
                fecha_programada=sesion.fecha_programada,
                asignatura_id=sesion.asignatura_id,
                oa_ids=sesion.oa_ids,
                incluye_prueba_unidad=sesion.incluye_prueba_unidad,
                es_repaso=sesion.es_repaso,
            )
            self._session.add(fila_sesion)
            filas_sesiones.append(fila_sesion)
        self._session.commit()
        for f in filas_sesiones:
            self._session.refresh(f)

        return self._a_dominio(fila_plan, filas_sesiones)

    def agregar_sesion(self, plan_estudio_id: int, sesion: SesionDominio) -> SesionDominio:
        fila_sesion = SesionORM(
            plan_estudio_id=plan_estudio_id,
            fecha_programada=sesion.fecha_programada,
            asignatura_id=sesion.asignatura_id,
            oa_ids=sesion.oa_ids,
            incluye_prueba_unidad=sesion.incluye_prueba_unidad,
            es_repaso=sesion.es_repaso,
        )
        self._session.add(fila_sesion)
        self._session.commit()
        self._session.refresh(fila_sesion)
        return SesionDominio(
            id=fila_sesion.id, plan_estudio_id=fila_sesion.plan_estudio_id,
            fecha_programada=fila_sesion.fecha_programada, asignatura_id=fila_sesion.asignatura_id,
            oa_ids=list(fila_sesion.oa_ids), incluye_prueba_unidad=fila_sesion.incluye_prueba_unidad,
            es_repaso=fila_sesion.es_repaso,
        )

    @staticmethod
    def _a_dominio(fila_plan: PlanORM, filas_sesiones: list[SesionORM]) -> PlanDominio:
        sesiones = [
            SesionDominio(
                id=f.id, plan_estudio_id=f.plan_estudio_id, fecha_programada=f.fecha_programada,
                asignatura_id=f.asignatura_id, oa_ids=list(f.oa_ids),
                incluye_prueba_unidad=f.incluye_prueba_unidad, es_repaso=f.es_repaso,
            )
            for f in filas_sesiones
        ]
        return PlanDominio(
            id=fila_plan.id, perfil_alumno_id=fila_plan.perfil_alumno_id,
            dias_por_semana=fila_plan.dias_por_semana, dias_elegidos=list(fila_plan.dias_elegidos),
            fecha_inicio=fila_plan.fecha_inicio, fecha_objetivo=fila_plan.fecha_objetivo,
            sesiones=sesiones,
        )
