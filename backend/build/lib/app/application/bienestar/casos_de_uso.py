from app.domain.bienestar.entities import RegistroAnimo
from app.domain.bienestar.ports import RepositorioBienestar
from app.domain.shared.reloj import Reloj


class ObtenerAnimoDeHoy:
    def __init__(self, repositorio: RepositorioBienestar, reloj: Reloj):
        self._repositorio = repositorio
        self._reloj = reloj

    def ejecutar(self, perfil_alumno_id: int) -> RegistroAnimo | None:
        return self._repositorio.buscar_de_fecha(perfil_alumno_id, self._reloj.ahora().date())


class RegistrarAnimoDeHoy:
    """Un check-in por alumno por día — si ya existe uno para hoy, lo devuelve tal cual
    (el primero del día manda, no se sobreescribe con reintentos)."""

    def __init__(self, repositorio: RepositorioBienestar, reloj: Reloj):
        self._repositorio = repositorio
        self._reloj = reloj

    def ejecutar(self, perfil_alumno_id: int, estado: str) -> RegistroAnimo:
        hoy = self._reloj.ahora().date()
        existente = self._repositorio.buscar_de_fecha(perfil_alumno_id, hoy)
        if existente:
            return existente
        registro = RegistroAnimo.crear(perfil_alumno_id, estado, hoy)  # lanza EstadoAnimoInvalido si corresponde
        return self._repositorio.guardar(registro)
