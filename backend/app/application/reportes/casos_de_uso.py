from app.domain.evaluaciones.exceptions import PerfilAlumnoNoEncontrado, PreguntaNoEncontrada
from app.domain.evaluaciones.ports import RepositorioPreguntas
from app.domain.auth.ports import RepositorioPerfilesAlumno
from app.domain.reportes.entities import ReporteError
from app.domain.reportes.exceptions import TipoContenidoInvalido
from app.domain.reportes.ports import RepositorioReportesError
from app.domain.reportes.entities import TIPOS_CONTENIDO_REPORTABLE
from app.domain.shared.reloj import Reloj


class ReportarErrorPregunta:
    """Hoy solo cubre `tipo_contenido="pregunta"` (Fase 1) — el dominio ya es genérico
    (`ReporteError.tipo_contenido`) para extender a guía/video sin migrar de nuevo."""

    def __init__(
        self,
        repositorio_reportes: RepositorioReportesError,
        repositorio_preguntas: RepositorioPreguntas,
        repositorio_perfiles: RepositorioPerfilesAlumno,
        reloj: Reloj,
    ):
        self._repositorio_reportes = repositorio_reportes
        self._repositorio_preguntas = repositorio_preguntas
        self._repositorio_perfiles = repositorio_perfiles
        self._reloj = reloj

    def ejecutar(self, pregunta_id: int, perfil_alumno_id: int, comentario: str) -> ReporteError:
        if not self._repositorio_perfiles.buscar_por_id(perfil_alumno_id):
            raise PerfilAlumnoNoEncontrado()
        if not self._repositorio_preguntas.listar_por_ids([pregunta_id]):
            raise PreguntaNoEncontrada()
        if "pregunta" not in TIPOS_CONTENIDO_REPORTABLE:
            raise TipoContenidoInvalido()

        reporte = ReporteError.crear(
            tipo_contenido="pregunta",
            contenido_id=pregunta_id,
            perfil_alumno_id=perfil_alumno_id,
            comentario=comentario,
            fecha=self._reloj.ahora(),
        )
        return self._repositorio_reportes.guardar(reporte)


class ListarReportesNoResueltos:
    """Para el panel de Admin — lectura simple, sin ceremonia de "resolver" todavía
    (Fase 1 solo pide que el reporte llegue y sea visible, ver plan)."""

    def __init__(self, repositorio_reportes: RepositorioReportesError):
        self._repositorio_reportes = repositorio_reportes

    def ejecutar(self) -> list[ReporteError]:
        return self._repositorio_reportes.listar_no_resueltos()
