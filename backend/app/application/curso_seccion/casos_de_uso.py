from app.domain.auth.ports import RepositorioPerfilesAlumno
from app.domain.curso_seccion.entities import Comunicado, CursoSeccion
from app.domain.curso_seccion.exceptions import AlumnoNoEncontrado, CursoAjeno, CursoSeccionNoEncontrado
from app.domain.curso_seccion.ports import RepositorioComunicados, RepositorioCursosSeccion
from app.domain.shared.reloj import Reloj


def verificar_dueno(curso: CursoSeccion | None, profesor_id: int) -> CursoSeccion:
    if not curso:
        raise CursoSeccionNoEncontrado()
    if curso.profesor_id != profesor_id:
        raise CursoAjeno()
    return curso


class CrearCursoSeccion:
    def __init__(self, repositorio: RepositorioCursosSeccion):
        self._repositorio = repositorio

    def ejecutar(self, profesor_id: int, nivel_id: int, nombre: str) -> CursoSeccion:
        curso = CursoSeccion.crear(profesor_id=profesor_id, nivel_id=nivel_id, nombre=nombre)
        return self._repositorio.crear(curso)


class AgregarAlumnoACurso:
    def __init__(self, repositorio_cursos: RepositorioCursosSeccion, repositorio_perfiles: RepositorioPerfilesAlumno):
        self._repositorio_cursos = repositorio_cursos
        self._repositorio_perfiles = repositorio_perfiles

    def ejecutar(self, profesor_id: int, curso_id: int, perfil_alumno_id: int) -> None:
        curso = verificar_dueno(self._repositorio_cursos.buscar_por_id(curso_id), profesor_id)
        if not self._repositorio_perfiles.buscar_por_id(perfil_alumno_id):
            raise AlumnoNoEncontrado()
        self._repositorio_cursos.agregar_alumno(curso.id, perfil_alumno_id)


class QuitarAlumnoDeCurso:
    def __init__(self, repositorio_cursos: RepositorioCursosSeccion):
        self._repositorio_cursos = repositorio_cursos

    def ejecutar(self, profesor_id: int, curso_id: int, perfil_alumno_id: int) -> None:
        verificar_dueno(self._repositorio_cursos.buscar_por_id(curso_id), profesor_id)
        self._repositorio_cursos.quitar_alumno(perfil_alumno_id)


class PublicarComunicado:
    def __init__(self, repositorio_cursos: RepositorioCursosSeccion, repositorio_comunicados: RepositorioComunicados, reloj: Reloj):
        self._repositorio_cursos = repositorio_cursos
        self._repositorio_comunicados = repositorio_comunicados
        self._reloj = reloj

    def ejecutar(self, profesor_id: int, curso_id: int, titulo: str, cuerpo: str) -> Comunicado:
        curso = verificar_dueno(self._repositorio_cursos.buscar_por_id(curso_id), profesor_id)
        comunicado = Comunicado.crear(curso_seccion_id=curso.id, titulo=titulo, cuerpo=cuerpo, fecha=self._reloj.ahora())
        return self._repositorio_comunicados.crear(comunicado)
