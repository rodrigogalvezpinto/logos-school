from datetime import date

from sqlmodel import Session, select

from app.infrastructure.persistence.orm_models import AgendaFamiliarConversada


class RepositorioAgendaFamiliarSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def ya_conversada(self, perfil_alumno_id: int, semana_inicio: date) -> bool:
        fila = self._session.exec(
            select(AgendaFamiliarConversada).where(
                AgendaFamiliarConversada.perfil_alumno_id == perfil_alumno_id,
                AgendaFamiliarConversada.semana_inicio == semana_inicio,
            )
        ).first()
        return fila is not None

    def marcar_conversada(self, perfil_alumno_id: int, semana_inicio: date) -> None:
        if self.ya_conversada(perfil_alumno_id, semana_inicio):
            return  # idempotente — marcar dos veces la misma semana no hace nada
        fila = AgendaFamiliarConversada(perfil_alumno_id=perfil_alumno_id, semana_inicio=semana_inicio)
        self._session.add(fila)
        self._session.commit()
