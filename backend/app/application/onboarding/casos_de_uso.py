from app.domain.onboarding.entities import ProgresoOnboarding
from app.domain.onboarding.ports import RepositorioOnboarding


class ObtenerProgresoOnboarding:
    def __init__(self, repositorio: RepositorioOnboarding):
        self._repositorio = repositorio

    def ejecutar(self, perfil_alumno_id: int) -> ProgresoOnboarding:
        return self._repositorio.obtener_o_crear(perfil_alumno_id)


class CompletarPasoOnboarding:
    def __init__(self, repositorio: RepositorioOnboarding):
        self._repositorio = repositorio

    def ejecutar(self, perfil_alumno_id: int, paso_id: str) -> ProgresoOnboarding:
        progreso = self._repositorio.obtener_o_crear(perfil_alumno_id)
        progreso.completar_paso(paso_id)  # lanza PasoInvalido si corresponde
        return self._repositorio.guardar(progreso)
