from typing import Protocol

from app.domain.onboarding.entities import ProgresoOnboarding


class RepositorioOnboarding(Protocol):
    def obtener_o_crear(self, perfil_alumno_id: int) -> ProgresoOnboarding: ...
    def guardar(self, progreso: ProgresoOnboarding) -> ProgresoOnboarding: ...
