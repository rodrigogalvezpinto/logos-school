from dataclasses import dataclass

from app.application.curso_seccion.casos_de_uso import verificar_dueno
from app.application.progreso.consultas import ObtenerHistorialYNotas
from app.domain.curso_seccion.entities import Comunicado, CursoSeccion
from app.domain.curso_seccion.ports import RepositorioComunicados, RepositorioCursosSeccion
from app.domain.profesor.ports import RepositorioCuentasProfesor
from app.domain.progreso.ports import NotaPorAsignatura


@dataclass(frozen=True)
class ProgresoAlumnoDeCurso:
    perfil_alumno_id: int
    nombre: str
    apellidos: str
    notas_por_asignatura: list[NotaPorAsignatura]


@dataclass(frozen=True)
class ProgresoDeCurso:
    curso: CursoSeccion
    alumnos: list[ProgresoAlumnoDeCurso]


class ObtenerProgresoDeCurso:
    """Reutiliza `ObtenerHistorialYNotas` (Fase 1.2) tal cual, una vez por alumno del
    curso — sin reimplementar el cálculo de notas/promedios."""

    def __init__(self, repositorio_cursos: RepositorioCursosSeccion, obtener_historial_y_notas: ObtenerHistorialYNotas):
        self._repositorio_cursos = repositorio_cursos
        self._obtener_historial_y_notas = obtener_historial_y_notas

    def ejecutar(self, profesor_id: int, curso_id: int) -> ProgresoDeCurso:
        curso = verificar_dueno(self._repositorio_cursos.buscar_por_id(curso_id), profesor_id)
        alumnos = self._repositorio_cursos.listar_alumnos(curso_id)
        progreso_alumnos = [
            ProgresoAlumnoDeCurso(
                perfil_alumno_id=a.perfil_alumno_id,
                nombre=a.nombre,
                apellidos=a.apellidos,
                notas_por_asignatura=self._obtener_historial_y_notas.ejecutar(a.perfil_alumno_id).notas_por_asignatura,
            )
            for a in alumnos
        ]
        return ProgresoDeCurso(curso=curso, alumnos=progreso_alumnos)


@dataclass(frozen=True)
class MiCurso:
    nombre_curso: str
    nombre_profesor: str
    comunicados: list[Comunicado]


class ObtenerMiCurso:
    """Para el Alumno/Apoderado: a qué curso pertenece, quién es el profesor, y los
    comunicados publicados — cubre "ver comunicación adicional" sin un sistema de
    mensajería (ver planificacion, decisiones de alcance de esta fase)."""

    def __init__(
        self,
        repositorio_cursos: RepositorioCursosSeccion,
        repositorio_comunicados: RepositorioComunicados,
        repositorio_cuentas_profesor: RepositorioCuentasProfesor,
    ):
        self._repositorio_cursos = repositorio_cursos
        self._repositorio_comunicados = repositorio_comunicados
        self._repositorio_cuentas_profesor = repositorio_cuentas_profesor

    def ejecutar(self, perfil_alumno_id: int) -> MiCurso | None:
        curso = self._repositorio_cursos.buscar_curso_del_alumno(perfil_alumno_id)
        if not curso:
            return None
        profesor = self._repositorio_cuentas_profesor.buscar_por_id(curso.profesor_id)
        comunicados = self._repositorio_comunicados.listar_por_curso(curso.id)
        return MiCurso(
            nombre_curso=curso.nombre,
            nombre_profesor=profesor.nombre if profesor else "—",
            comunicados=comunicados,
        )
