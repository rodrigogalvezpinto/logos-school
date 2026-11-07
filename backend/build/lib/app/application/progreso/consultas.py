"""Consultas de aplicación — a diferencia de las lecturas triviales de `contenido.py`
(router → repositorio directo, sin capa intermedia), esto combina datos de dos agregados
(Intentos + Conjuntos + Contenido) con lógica de agregación real (promedios, "más
reciente"), así que sí amerita una clase de aplicación en vez de un pass-through."""

from dataclasses import dataclass

from app.domain.contenido.ports import RepositorioContenido
from app.domain.evaluaciones.ports import RepositorioConjuntos, RepositorioIntentos, RepositorioPreguntas
from app.domain.evaluaciones.value_objects import UMBRAL_SIMULACRO_PARCIAL
from app.domain.progreso.ports import (
    CoberturaAsignatura,
    GuiaRevisada,
    ItemFaltante,
    ItemHistorial,
    NotaPorAsignatura,
    RepositorioProgreso,
)
from app.domain.shared.reloj import Reloj

TIPO_PRUEBA_UNIDAD = "prueba_unidad"
TIPO_EXAMEN_SIMULACRO = "examen_simulacro"


@dataclass(frozen=True)
class ResultadoHistorial:
    historial: list[ItemHistorial]
    guias_revisadas: list[GuiaRevisada]
    notas_por_asignatura: list[NotaPorAsignatura]


class ObtenerHistorialYNotas:
    def __init__(
        self,
        repositorio_intentos: RepositorioIntentos,
        repositorio_conjuntos: RepositorioConjuntos,
        repositorio_contenido: RepositorioContenido,
        repositorio_progreso: RepositorioProgreso,
    ):
        self._repositorio_intentos = repositorio_intentos
        self._repositorio_conjuntos = repositorio_conjuntos
        self._repositorio_contenido = repositorio_contenido
        self._repositorio_progreso = repositorio_progreso

    def ejecutar(self, perfil_alumno_id: int) -> ResultadoHistorial:
        intentos = self._repositorio_intentos.listar_entregados_por_perfil(perfil_alumno_id)
        conjunto_ids = list({i.conjunto_evaluacion_id for i in intentos})
        conjuntos = {c.id: c for c in self._repositorio_conjuntos.listar_por_ids(conjunto_ids)}

        asignaturas_cache: dict[int, str] = {}

        def nombre_asignatura(asignatura_id: int | None) -> str | None:
            if asignatura_id is None:
                return None
            if asignatura_id not in asignaturas_cache:
                asignatura = self._repositorio_contenido.obtener_asignatura(asignatura_id)
                asignaturas_cache[asignatura_id] = asignatura.nombre if asignatura else "—"
            return asignaturas_cache[asignatura_id]

        historial: list[ItemHistorial] = []
        for intento in intentos:
            conjunto = conjuntos.get(intento.conjunto_evaluacion_id)
            if not conjunto:
                continue
            historial.append(
                ItemHistorial(
                    intento_id=intento.id,
                    conjunto_id=conjunto.id,
                    tipo=conjunto.tipo,
                    asignatura_id=conjunto.asignatura_id,
                    asignatura_nombre=nombre_asignatura(conjunto.asignatura_id),
                    nombre=conjunto.nombre,
                    nota=intento.nota,
                    fecha=intento.fecha_termino,
                )
            )
        historial.sort(key=lambda i: i.fecha, reverse=True)

        notas_por_asignatura = self._calcular_notas_por_asignatura(historial)
        guias_revisadas = self._repositorio_progreso.listar_guias_revisadas(perfil_alumno_id)

        return ResultadoHistorial(historial, guias_revisadas, notas_por_asignatura)

    @staticmethod
    def _calcular_notas_por_asignatura(historial: list[ItemHistorial]) -> list[NotaPorAsignatura]:
        por_asignatura: dict[int, list[ItemHistorial]] = {}
        for item in historial:
            if item.asignatura_id is None:
                continue  # exámenes integrados de Régimen A no tienen una asignatura única
            por_asignatura.setdefault(item.asignatura_id, []).append(item)

        resultado = []
        for asignatura_id, items in por_asignatura.items():
            practicas = [i.nota for i in items if i.tipo == TIPO_PRUEBA_UNIDAD and i.nota is not None]
            nota_practica = round(sum(practicas) / len(practicas), 1) if practicas else None

            simulacros = [i for i in items if i.tipo == TIPO_EXAMEN_SIMULACRO and i.nota is not None]
            nota_simulacro = max(simulacros, key=lambda i: i.fecha).nota if simulacros else None

            resultado.append(
                NotaPorAsignatura(
                    asignatura_id=asignatura_id,
                    asignatura_nombre=items[0].asignatura_nombre or "—",
                    nota_practica=nota_practica,
                    nota_simulacro=nota_simulacro,
                )
            )
        return resultado


@dataclass(frozen=True)
class ResultadoFaltantes:
    faltantes: list[ItemFaltante]
    coberturas: list[CoberturaAsignatura]


class ObtenerFaltantes:
    """Pruebas/exámenes que el alumno aún no rinde, con su estado de habilitación —
    ver planificacion/13-plan-de-estudio.md, sección "Requisitos adicionales", reglas de
    habilitación progresiva. Una prueba de unidad se habilita cuando todas las OA que cubre
    (derivadas de `Pregunta.oa_id`, sin modelar una relación nueva) ya fueron revisadas; un
    examen simulacro completo (Forma A/B) se habilita al 100% de cobertura de la asignatura."""

    def __init__(
        self,
        repositorio_conjuntos: RepositorioConjuntos,
        repositorio_intentos: RepositorioIntentos,
        repositorio_preguntas: RepositorioPreguntas,
        repositorio_contenido: RepositorioContenido,
        repositorio_progreso: RepositorioProgreso,
        reloj: Reloj,
    ):
        self._repositorio_conjuntos = repositorio_conjuntos
        self._repositorio_intentos = repositorio_intentos
        self._repositorio_preguntas = repositorio_preguntas
        self._repositorio_contenido = repositorio_contenido
        self._repositorio_progreso = repositorio_progreso
        self._reloj = reloj

    def ejecutar(self, perfil_alumno_id: int, nivel_id: int) -> ResultadoFaltantes:
        entregados_ids = {
            i.conjunto_evaluacion_id for i in self._repositorio_intentos.listar_entregados_por_perfil(perfil_alumno_id)
        }
        revisadas = {g.oa_id for g in self._repositorio_progreso.listar_guias_revisadas(perfil_alumno_id)}

        faltantes: list[ItemFaltante] = []
        coberturas: list[CoberturaAsignatura] = []

        for asignatura in self._repositorio_contenido.listar_asignaturas(nivel_id):
            oa_ids_asignatura = {oa.id for oa in self._repositorio_contenido.listar_objetivos(asignatura.id)}
            cobertura = len(oa_ids_asignatura & revisadas) / len(oa_ids_asignatura) if oa_ids_asignatura else 0.0

            for conjunto in self._repositorio_conjuntos.listar_por_asignatura(asignatura.id):
                if conjunto.id in entregados_ids:
                    continue
                if conjunto.tipo == TIPO_PRUEBA_UNIDAD:
                    oa_de_la_prueba = {
                        p.oa_id
                        for p in self._repositorio_preguntas.listar_por_ids(conjunto.pregunta_ids)
                        if p.oa_id is not None
                    }
                    habilitado = oa_de_la_prueba.issubset(revisadas) if oa_de_la_prueba else True
                else:
                    habilitado = cobertura >= 1.0

                # Simulacro con fecha programada por el Admin (Fase 1, ítem 2.1): si tiene
                # fecha y todavía no llega, queda "próximamente" sin importar la cobertura.
                if conjunto.fecha_programada is not None and self._reloj.ahora() < conjunto.fecha_programada:
                    habilitado = False

                faltantes.append(
                    ItemFaltante(
                        conjunto_id=conjunto.id, tipo=conjunto.tipo, nombre=conjunto.nombre,
                        asignatura_id=asignatura.id, habilitado=habilitado,
                        fecha_programada=conjunto.fecha_programada,
                    )
                )

            coberturas.append(
                CoberturaAsignatura(
                    asignatura_id=asignatura.id,
                    asignatura_nombre=asignatura.nombre,
                    cobertura_pct=round(cobertura * 100, 1),
                    simulacro_parcial_disponible=cobertura >= UMBRAL_SIMULACRO_PARCIAL,
                )
            )

        return ResultadoFaltantes(faltantes=faltantes, coberturas=coberturas)
