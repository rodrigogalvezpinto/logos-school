"""Gamificación (Fase 1, ítem 2.2 del plan de incorporación de hallazgos de Brincus — ver
planificacion/27-plan-incorporacion-hallazgos-brincus.md). MVP original deliberadamente
simple: solo XP + nivel derivado + selección libre de avatar. Profundizado el 2026-08-15
comparando en vivo contra la cuenta real de Brincus (ver
planificacion/25-analisis-competencia-brincus.md, sección Logros): agrega racha de días
y contadores de hábito (guías revisadas, evaluaciones entregadas) para premiar constancia,
no solo avance de contenido — igual que hace Brincus con sus ~40 logros, en una versión
más acotada (12 logros, 3 categorías x 3-4 niveles cada una)."""

from dataclasses import dataclass
from datetime import date, timedelta

from app.domain.gamificacion.exceptions import AvatarInvalido

XP_POR_NIVEL = 50  # histórico — ver xp_a_nivel/xp_acumulado_para_nivel para la curva actual


def xp_acumulado_para_nivel(nivel: int) -> int:
    """XP total acumulado necesario para alcanzar `nivel` (nivel 1 = 0 XP)."""
    return 25 * (nivel - 1) * nivel


def xp_a_nivel(xp: int) -> int:
    """Inverso de `xp_acumulado_para_nivel`: nivel actual dado un total de XP."""
    nivel = 1
    while xp_acumulado_para_nivel(nivel + 1) <= xp:
        nivel += 1
    return nivel

AVATARES_DISPONIBLES = [
    "monstruo_azul",
    "monstruo_verde",
    "monstruo_morado",
    "monstruo_celeste",
    "monstruo_rojo",
    "huevo_espacial",
    "planeta",
    "cohete",
]

AVATAR_POR_DEFECTO = AVATARES_DISPONIBLES[0]


@dataclass(frozen=True)
class Logro:
    id: str
    nombre: str
    descripcion: str
    icono: str
    categoria: str  # "constancia" | "contenido" | "evaluaciones" | "nivel"


# Insignias con emoji (no un archivo de imagen ni una librería de íconos nueva — mismo
# criterio ya usado para avatares/asignaturas en este proyecto: cero dependencias
# externas, cero licencias que gestionar, se ve bien en cualquier tamaño de pantalla).
CATALOGO_LOGROS: list[Logro] = [
    Logro("racha_2", "Dos días seguidos", "Entra a estudiar 2 días seguidos.", "🔥", "constancia"),
    Logro("racha_5", "Racha de una semana", "Entra a estudiar 5 días seguidos.", "🔥", "constancia"),
    Logro("racha_10", "Racha de diez días", "Entra a estudiar 10 días seguidos.", "🔥", "constancia"),
    Logro("guias_5", "Lector primerizo", "Revisa 5 guías de estudio.", "📖", "contenido"),
    Logro("guias_15", "Lector constante", "Revisa 15 guías de estudio.", "📚", "contenido"),
    Logro("guias_50", "Lector experto", "Revisa 50 guías de estudio.", "🎓", "contenido"),
    Logro("evals_1", "Primer intento", "Entrega tu primera prueba o examen.", "📝", "evaluaciones"),
    Logro("evals_5", "En práctica", "Entrega 5 pruebas o exámenes.", "✍️", "evaluaciones"),
    Logro("evals_20", "Máquina de practicar", "Entrega 20 pruebas o exámenes.", "🏅", "evaluaciones"),
    Logro("nivel_5", "Nivel 5", "Alcanza el nivel 5.", "⭐", "nivel"),
    Logro("nivel_10", "Nivel 10", "Alcanza el nivel 10.", "🌟", "nivel"),
    Logro("nivel_20", "Nivel 20", "Alcanza el nivel 20.", "💫", "nivel"),
    # Tiempo dedicado — hallazgo comparando en vivo contra Brincus (ver
    # planificacion/25-analisis-competencia-brincus.md, Paso 12: logros por "sesión más
    # larga" y "tiempo total acumulado"). Se mide con `tiempo_usado_seg`, ya calculado por
    # IntentoEvaluacion.entregar() para el cronómetro — no tiempo de sesión de toda la app
    # (eso exigiría un heartbeat cliente→servidor, fuera de alcance por ahora), sino tiempo
    # real invertido rindiendo pruebas/exámenes, que es igual de honesto como proxy de
    # dedicación y no requiere infraestructura nueva.
    Logro("tiempo_30min", "Media hora de práctica", "Acumula 30 minutos rindiendo pruebas o exámenes.", "⏱️", "tiempo"),
    Logro("tiempo_2h", "Dos horas de práctica", "Acumula 2 horas rindiendo pruebas o exámenes.", "⏳", "tiempo"),
    Logro("tiempo_5h", "Cinco horas de práctica", "Acumula 5 horas rindiendo pruebas o exámenes.", "🕰️", "tiempo"),
]


@dataclass
class PerfilGamificacion:
    perfil_alumno_id: int
    xp: int
    avatar_id: str
    racha_dias_actual: int = 0
    racha_dias_maxima: int = 0
    ultima_actividad_fecha: date | None = None
    guias_revisadas_total: int = 0
    evaluaciones_entregadas_total: int = 0
    tiempo_evaluando_total_seg: int = 0

    @classmethod
    def crear(cls, perfil_alumno_id: int) -> "PerfilGamificacion":
        return cls(perfil_alumno_id=perfil_alumno_id, xp=0, avatar_id=AVATAR_POR_DEFECTO)

    @property
    def nivel(self) -> int:
        """Nivel 1 arranca en 0 XP. Curva no lineal (creciente) en vez de un múltiplo fijo
        de XP por nivel — hallazgo comparando en vivo contra Brincus (Paso 12): documentan
        al alumno una curva donde subir los primeros niveles es rápido y los siguientes
        exigen cada vez más (nivel 2 = 50 XP, nivel 3 = 200 XP, nivel 4 = 1500 XP en su
        escala de 4 niveles). Acá se adopta la misma idea con una fórmula abierta (sin techo
        en 4, porque Logos ya tiene logros hasta nivel 20): el umbral acumulado para el
        nivel N es `25 * (N-1) * N` — nivel 2 = 50 XP (coincide con el umbral anterior),
        nivel 3 = 150, nivel 5 = 500, nivel 10 = 2250, nivel 20 = 9500."""
        return xp_a_nivel(self.xp)

    def sumar_xp(self, cantidad: int) -> None:
        if cantidad <= 0:
            raise ValueError("La cantidad de XP a sumar debe ser positiva")
        self.xp += cantidad

    def cambiar_avatar(self, avatar_id: str) -> None:
        if avatar_id not in AVATARES_DISPONIBLES:
            raise AvatarInvalido()
        self.avatar_id = avatar_id

    def registrar_actividad(self, hoy: date) -> None:
        """Actualiza la racha de días consecutivos — se llama junto con `sumar_xp` desde
        cualquier acción real (entregar una evaluación, revisar una guía), nunca por solo
        cargar una pantalla. Mismo día → no cambia nada (evita inflar la racha con
        múltiples acciones el mismo día); día siguiente exacto → +1; cualquier otro salto
        → la racha se corta y arranca de nuevo en 1."""
        if self.ultima_actividad_fecha == hoy:
            return
        if self.ultima_actividad_fecha == hoy - timedelta(days=1):
            self.racha_dias_actual += 1
        else:
            self.racha_dias_actual = 1
        self.racha_dias_maxima = max(self.racha_dias_maxima, self.racha_dias_actual)
        self.ultima_actividad_fecha = hoy

    def incrementar_guias_revisadas(self) -> None:
        self.guias_revisadas_total += 1

    def incrementar_evaluaciones_entregadas(self) -> None:
        self.evaluaciones_entregadas_total += 1

    def sumar_tiempo_evaluando(self, segundos: int) -> None:
        if segundos > 0:
            self.tiempo_evaluando_total_seg += segundos

    def logros_desbloqueados(self) -> set[str]:
        desbloqueados = set()
        if self.racha_dias_maxima >= 2:
            desbloqueados.add("racha_2")
        if self.racha_dias_maxima >= 5:
            desbloqueados.add("racha_5")
        if self.racha_dias_maxima >= 10:
            desbloqueados.add("racha_10")
        if self.guias_revisadas_total >= 5:
            desbloqueados.add("guias_5")
        if self.guias_revisadas_total >= 15:
            desbloqueados.add("guias_15")
        if self.guias_revisadas_total >= 50:
            desbloqueados.add("guias_50")
        if self.evaluaciones_entregadas_total >= 1:
            desbloqueados.add("evals_1")
        if self.evaluaciones_entregadas_total >= 5:
            desbloqueados.add("evals_5")
        if self.evaluaciones_entregadas_total >= 20:
            desbloqueados.add("evals_20")
        if self.nivel >= 5:
            desbloqueados.add("nivel_5")
        if self.nivel >= 10:
            desbloqueados.add("nivel_10")
        if self.nivel >= 20:
            desbloqueados.add("nivel_20")
        if self.tiempo_evaluando_total_seg >= 30 * 60:
            desbloqueados.add("tiempo_30min")
        if self.tiempo_evaluando_total_seg >= 2 * 3600:
            desbloqueados.add("tiempo_2h")
        if self.tiempo_evaluando_total_seg >= 5 * 3600:
            desbloqueados.add("tiempo_5h")
        return desbloqueados
