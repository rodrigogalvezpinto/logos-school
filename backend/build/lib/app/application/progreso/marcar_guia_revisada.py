from app.domain.progreso.ports import RepositorioProgreso
from app.domain.shared.reloj import Reloj


class MarcarGuiaRevisada:
    """Caso de uso trivial pero con un `Reloj` inyectado (no `datetime.now()` directo en
    el repositorio) para mantener la misma disciplina de testabilidad que el resto del
    dominio — aunque hoy no proteja ninguna invariante de negocio."""

    def __init__(self, repositorio_progreso: RepositorioProgreso, reloj: Reloj):
        self._repositorio_progreso = repositorio_progreso
        self._reloj = reloj

    def ejecutar(self, perfil_alumno_id: int, oa_id: int) -> None:
        self._repositorio_progreso.marcar_guia_revisada(perfil_alumno_id, oa_id, self._reloj.ahora())
