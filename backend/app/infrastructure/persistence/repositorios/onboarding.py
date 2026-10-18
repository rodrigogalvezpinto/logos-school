from sqlmodel import Session, select

from app.domain.onboarding.entities import ProgresoOnboarding as ProgresoDominio
from app.infrastructure.persistence.orm_models import ProgresoOnboarding as ProgresoORM


class RepositorioOnboardingSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def obtener_o_crear(self, perfil_alumno_id: int) -> ProgresoDominio:
        fila = self._session.exec(
            select(ProgresoORM).where(ProgresoORM.perfil_alumno_id == perfil_alumno_id)
        ).first()
        if fila:
            return self._a_dominio(fila)

        fila = ProgresoORM(perfil_alumno_id=perfil_alumno_id, pasos_completados=[])
        self._session.add(fila)
        self._session.commit()
        self._session.refresh(fila)
        return self._a_dominio(fila)

    def guardar(self, progreso: ProgresoDominio) -> ProgresoDominio:
        fila = self._session.exec(
            select(ProgresoORM).where(ProgresoORM.perfil_alumno_id == progreso.perfil_alumno_id)
        ).first()
        fila.pasos_completados = sorted(progreso.pasos_completados)
        self._session.add(fila)
        self._session.commit()
        self._session.refresh(fila)
        return self._a_dominio(fila)

    @staticmethod
    def _a_dominio(fila: ProgresoORM) -> ProgresoDominio:
        return ProgresoDominio(perfil_alumno_id=fila.perfil_alumno_id, pasos_completados=set(fila.pasos_completados))
