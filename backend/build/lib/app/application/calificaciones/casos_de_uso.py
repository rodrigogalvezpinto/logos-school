from app.domain.auth.ports import RepositorioPerfilesAlumno
from app.domain.calificaciones.entities import CalificacionGuia
from app.domain.calificaciones.ports import RepositorioCalificaciones
from app.domain.evaluaciones.exceptions import PerfilAlumnoNoEncontrado
from app.domain.shared.reloj import Reloj


class CalificarGuia:
    def __init__(
        self,
        repositorio_calificaciones: RepositorioCalificaciones,
        repositorio_perfiles: RepositorioPerfilesAlumno,
        reloj: Reloj,
    ):
        self._repositorio_calificaciones = repositorio_calificaciones
        self._repositorio_perfiles = repositorio_perfiles
        self._reloj = reloj

    def ejecutar(self, oa_id: int, perfil_alumno_id: int, estrellas: int) -> CalificacionGuia:
        if not self._repositorio_perfiles.buscar_por_id(perfil_alumno_id):
            raise PerfilAlumnoNoEncontrado()

        calificacion = CalificacionGuia.crear(
            oa_id=oa_id, perfil_alumno_id=perfil_alumno_id, estrellas=estrellas, fecha=self._reloj.ahora(),
        )
        return self._repositorio_calificaciones.guardar_o_actualizar(calificacion)


class ObtenerMiCalificacion:
    def __init__(self, repositorio_calificaciones: RepositorioCalificaciones):
        self._repositorio_calificaciones = repositorio_calificaciones

    def ejecutar(self, oa_id: int, perfil_alumno_id: int) -> CalificacionGuia | None:
        return self._repositorio_calificaciones.buscar_mia(oa_id, perfil_alumno_id)
