from datetime import timezone

from sqlmodel import Session, select

from app.domain.reportes.entities import ReporteError as ReporteDominio
from app.infrastructure.persistence.orm_models import ReporteError as ReporteORM


class RepositorioReportesErrorSQLModel:
    def __init__(self, session: Session):
        self._session = session

    def guardar(self, reporte: ReporteDominio) -> ReporteDominio:
        fila = ReporteORM(
            tipo_contenido=reporte.tipo_contenido,
            contenido_id=reporte.contenido_id,
            perfil_alumno_id=reporte.perfil_alumno_id,
            comentario=reporte.comentario,
            fecha=reporte.fecha,
            resuelto=reporte.resuelto,
        )
        self._session.add(fila)
        self._session.commit()
        self._session.refresh(fila)
        return self._a_dominio(fila)

    def listar_no_resueltos(self) -> list[ReporteDominio]:
        filas = self._session.exec(
            select(ReporteORM).where(ReporteORM.resuelto.is_(False)).order_by(ReporteORM.fecha.desc())
        ).all()
        return [self._a_dominio(f) for f in filas]

    def listar_por_perfil(self, perfil_alumno_id: int) -> list[ReporteDominio]:
        filas = self._session.exec(
            select(ReporteORM)
            .where(ReporteORM.perfil_alumno_id == perfil_alumno_id)
            .order_by(ReporteORM.fecha.desc())
        ).all()
        return [self._a_dominio(f) for f in filas]

    @staticmethod
    def _a_dominio(fila: ReporteORM) -> ReporteDominio:
        fecha = fila.fecha if fila.fecha.tzinfo is not None else fila.fecha.replace(tzinfo=timezone.utc)
        return ReporteDominio(
            id=fila.id,
            tipo_contenido=fila.tipo_contenido,
            contenido_id=fila.contenido_id,
            perfil_alumno_id=fila.perfil_alumno_id,
            comentario=fila.comentario,
            fecha=fecha,
            resuelto=fila.resuelto,
        )
