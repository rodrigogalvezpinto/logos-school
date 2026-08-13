"""Consultas de aplicación — a diferencia de las lecturas triviales de `contenido.py`
(router → repositorio directo, sin capa intermedia), esto combina datos de dos agregados
(Intentos + Conjuntos + Contenido) con lógica de agregación real (promedios, "más
reciente"), así que sí amerita una clase de aplicación en vez de un pass-through."""

from dataclasses import dataclass

from app.domain.contenido.ports import RepositorioContenido
from app.domain.evaluaciones.ports import RepositorioConjuntos, RepositorioIntentos
from app.domain.progreso.ports import GuiaRevisada, ItemHistorial, NotaPorAsignatura, RepositorioProgreso

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
