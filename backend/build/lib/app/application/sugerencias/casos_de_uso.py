from app.domain.auth.ports import RepositorioPerfilesAlumno
from app.domain.evaluaciones.exceptions import PerfilAlumnoNoEncontrado
from app.domain.shared.reloj import Reloj
from app.domain.sugerencias.entities import Sugerencia
from app.domain.sugerencias.exceptions import SugerenciaVacia
from app.domain.sugerencias.ports import RepositorioSugerencias


class EnviarSugerencia:
    def __init__(
        self,
        repositorio_sugerencias: RepositorioSugerencias,
        repositorio_perfiles: RepositorioPerfilesAlumno,
        reloj: Reloj,
    ):
        self._repositorio_sugerencias = repositorio_sugerencias
        self._repositorio_perfiles = repositorio_perfiles
        self._reloj = reloj

    def ejecutar(self, perfil_alumno_id: int, texto: str) -> Sugerencia:
        if not self._repositorio_perfiles.buscar_por_id(perfil_alumno_id):
            raise PerfilAlumnoNoEncontrado()
        if not texto.strip():
            raise SugerenciaVacia()

        sugerencia = Sugerencia.crear(perfil_alumno_id=perfil_alumno_id, texto=texto, fecha=self._reloj.ahora())
        return self._repositorio_sugerencias.guardar(sugerencia)


class ListarMisSugerencias:
    def __init__(self, repositorio_sugerencias: RepositorioSugerencias):
        self._repositorio_sugerencias = repositorio_sugerencias

    def ejecutar(self, perfil_alumno_id: int) -> list[Sugerencia]:
        return self._repositorio_sugerencias.listar_por_perfil(perfil_alumno_id)
