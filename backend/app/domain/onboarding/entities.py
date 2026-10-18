"""Onboarding con checklist de primera sesión (Fase 1, ítem 2.3 del plan de incorporación
de hallazgos de Brincus — ver planificacion/27-plan-incorporacion-hallazgos-brincus.md).
Adaptado de los 7 pasos que verificó el análisis en Brincus a lo que Logos sí tiene hoy en
Fase 1 (sin Clases en Vivo, Profesor Virtual, Biblioteca ni Juegos, todos Fase 2)."""

from dataclasses import dataclass, field

from app.domain.onboarding.exceptions import PasoInvalido

PASOS_ONBOARDING = [
    "ver_guia",
    "autoevaluacion",
    "plan_estudio",
    "elegir_avatar",
]


@dataclass
class ProgresoOnboarding:
    perfil_alumno_id: int
    pasos_completados: set[str] = field(default_factory=set)

    @classmethod
    def crear(cls, perfil_alumno_id: int) -> "ProgresoOnboarding":
        return cls(perfil_alumno_id=perfil_alumno_id, pasos_completados=set())

    @property
    def completo(self) -> bool:
        return set(PASOS_ONBOARDING).issubset(self.pasos_completados)

    def completar_paso(self, paso_id: str) -> None:
        if paso_id not in PASOS_ONBOARDING:
            raise PasoInvalido()
        self.pasos_completados = self.pasos_completados | {paso_id}
