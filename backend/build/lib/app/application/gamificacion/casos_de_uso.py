from datetime import date

from app.domain.gamificacion.entities import PerfilGamificacion
from app.domain.gamificacion.ports import RepositorioGamificacion
from app.domain.shared.reloj import Reloj


class ObtenerPerfilGamificacion:
    def __init__(self, repositorio: RepositorioGamificacion):
        self._repositorio = repositorio

    def ejecutar(self, perfil_alumno_id: int) -> PerfilGamificacion:
        return self._repositorio.obtener_o_crear(perfil_alumno_id)


class SumarXp:
    """Se llama desde fuera del contexto Evaluaciones/Progreso cuando el alumno completa
    una acción que premia XP (entregar un intento, revisar una guía por primera vez) —
    mismo patrón de cruce legítimo entre contextos que ya usa `IniciarIntento` con
    `RepositorioPerfilesAlumno`. También registra la actividad del día (racha) y el
    contador de hábito correspondiente (guías/evaluaciones) — se engancha acá porque son
    exactamente los mismos dos puntos de disparo que ya otorgan XP, no un tercer hook
    nuevo que sincronizar."""

    def __init__(self, repositorio: RepositorioGamificacion, reloj: Reloj):
        self._repositorio = repositorio
        self._reloj = reloj

    def ejecutar(
        self,
        perfil_alumno_id: int,
        cantidad: int,
        tipo_actividad: str | None = None,
        tiempo_usado_seg: int | None = None,
    ) -> PerfilGamificacion:
        perfil = self._repositorio.obtener_o_crear(perfil_alumno_id)
        perfil.sumar_xp(cantidad)
        perfil.registrar_actividad(self._reloj.ahora().date())
        if tipo_actividad == "guia":
            perfil.incrementar_guias_revisadas()
        elif tipo_actividad == "evaluacion":
            perfil.incrementar_evaluaciones_entregadas()
            if tiempo_usado_seg:
                perfil.sumar_tiempo_evaluando(tiempo_usado_seg)
        return self._repositorio.guardar(perfil)


class CambiarAvatar:
    def __init__(self, repositorio: RepositorioGamificacion):
        self._repositorio = repositorio

    def ejecutar(self, perfil_alumno_id: int, avatar_id: str) -> PerfilGamificacion:
        perfil = self._repositorio.obtener_o_crear(perfil_alumno_id)
        perfil.cambiar_avatar(avatar_id)  # lanza AvatarInvalido si corresponde
        return self._repositorio.guardar(perfil)
