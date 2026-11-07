from sqlmodel import Session, select

from app.domain.gamificacion.entities import AVATAR_POR_DEFECTO, PerfilGamificacion as PerfilDominio
from app.infrastructure.persistence.orm_models import PerfilGamificacion as PerfilORM


class RepositorioGamificacionSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def obtener_o_crear(self, perfil_alumno_id: int) -> PerfilDominio:
        fila = self._session.exec(
            select(PerfilORM).where(PerfilORM.perfil_alumno_id == perfil_alumno_id)
        ).first()
        if fila:
            return self._a_dominio(fila)

        fila = PerfilORM(perfil_alumno_id=perfil_alumno_id, xp=0, avatar_id=AVATAR_POR_DEFECTO)
        self._session.add(fila)
        self._session.commit()
        self._session.refresh(fila)
        return self._a_dominio(fila)

    def guardar(self, perfil: PerfilDominio) -> PerfilDominio:
        fila = self._session.exec(
            select(PerfilORM).where(PerfilORM.perfil_alumno_id == perfil.perfil_alumno_id)
        ).first()
        fila.xp = perfil.xp
        fila.avatar_id = perfil.avatar_id
        fila.racha_dias_actual = perfil.racha_dias_actual
        fila.racha_dias_maxima = perfil.racha_dias_maxima
        fila.ultima_actividad_fecha = perfil.ultima_actividad_fecha
        fila.guias_revisadas_total = perfil.guias_revisadas_total
        fila.evaluaciones_entregadas_total = perfil.evaluaciones_entregadas_total
        fila.tiempo_evaluando_total_seg = perfil.tiempo_evaluando_total_seg
        self._session.add(fila)
        self._session.commit()
        self._session.refresh(fila)
        return self._a_dominio(fila)

    @staticmethod
    def _a_dominio(fila: PerfilORM) -> PerfilDominio:
        return PerfilDominio(
            perfil_alumno_id=fila.perfil_alumno_id,
            xp=fila.xp,
            avatar_id=fila.avatar_id,
            racha_dias_actual=fila.racha_dias_actual,
            racha_dias_maxima=fila.racha_dias_maxima,
            ultima_actividad_fecha=fila.ultima_actividad_fecha,
            guias_revisadas_total=fila.guias_revisadas_total,
            evaluaciones_entregadas_total=fila.evaluaciones_entregadas_total,
            tiempo_evaluando_total_seg=fila.tiempo_evaluando_total_seg,
        )
