from datetime import datetime, timezone

from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.domain.evaluaciones.entities import IntentoEvaluacion as IntentoDominio
from app.infrastructure.persistence.orm_models import IntentoEvaluacion as IntentoORM


class RepositorioIntentosSQLModel:
    """Acá vive el workaround de timezone: Postgres devuelve datetimes naive para una
    columna TIMESTAMP WITHOUT TIME ZONE aunque se haya guardado un valor aware — se
    normaliza a UTC-aware al cargar, para que el dominio nunca vea un datetime naive."""

    def __init__(self, session: Session):
        self._session = session

    def buscar_por_id(self, intento_id: int) -> IntentoDominio | None:
        fila = self._session.get(IntentoORM, intento_id)
        return self._a_dominio(fila) if fila else None

    def buscar_activo(self, perfil_alumno_id: int, conjunto_evaluacion_id: int) -> IntentoDominio | None:
        fila = self._session.exec(
            select(IntentoORM).where(
                IntentoORM.perfil_alumno_id == perfil_alumno_id,
                IntentoORM.conjunto_evaluacion_id == conjunto_evaluacion_id,
                IntentoORM.fecha_termino.is_(None),
            )
        ).first()
        return self._a_dominio(fila) if fila else None

    def listar_entregados_por_perfil(self, perfil_alumno_id: int) -> list[IntentoDominio]:
        filas = self._session.exec(
            select(IntentoORM).where(
                IntentoORM.perfil_alumno_id == perfil_alumno_id,
                IntentoORM.fecha_termino.is_not(None),
            )
        ).all()
        return [self._a_dominio(f) for f in filas]

    def guardar(self, intento: IntentoDominio) -> IntentoDominio:
        if intento.id is None:
            fila = IntentoORM(
                perfil_alumno_id=intento.perfil_alumno_id,
                conjunto_evaluacion_id=intento.conjunto_evaluacion_id,
                fecha_inicio=intento.fecha_inicio,
                fecha_termino=intento.fecha_termino,
                respuestas=intento.respuestas,
                puntaje=intento.puntaje,
                nota=intento.nota,
                tiempo_usado_seg=intento.tiempo_usado_seg,
            )
        else:
            fila = self._session.get(IntentoORM, intento.id)
            fila.fecha_termino = intento.fecha_termino
            fila.respuestas = intento.respuestas
            fila.puntaje = intento.puntaje
            fila.nota = intento.nota
            fila.tiempo_usado_seg = intento.tiempo_usado_seg
        self._session.add(fila)
        try:
            self._session.commit()
        except IntegrityError:
            # Condición de carrera: otro request ganó la creación del intento activo
            # para este (alumno, conjunto) entre el "buscar_activo" y este "guardar" del
            # caso de uso (ver índice único parcial en IntentoEvaluacion.__table_args__).
            # En vez de propagar un 500, se devuelve ese intento — es exactamente lo que
            # IniciarIntento habría devuelto si hubiera llegado un instante después.
            self._session.rollback()
            existente = self.buscar_activo(intento.perfil_alumno_id, intento.conjunto_evaluacion_id)
            if existente:
                return existente
            raise
        self._session.refresh(fila)
        return self._a_dominio(fila)

    @staticmethod
    def _con_tz(valor: datetime | None) -> datetime | None:
        if valor is None:
            return None
        return valor if valor.tzinfo is not None else valor.replace(tzinfo=timezone.utc)

    @classmethod
    def _a_dominio(cls, fila: IntentoORM) -> IntentoDominio:
        return IntentoDominio(
            id=fila.id,
            perfil_alumno_id=fila.perfil_alumno_id,
            conjunto_evaluacion_id=fila.conjunto_evaluacion_id,
            fecha_inicio=cls._con_tz(fila.fecha_inicio),
            fecha_termino=cls._con_tz(fila.fecha_termino),
            respuestas=dict(fila.respuestas),
            puntaje=fila.puntaje,
            nota=fila.nota,
            tiempo_usado_seg=fila.tiempo_usado_seg,
        )
