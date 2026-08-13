"""Cursos/Sección del rol Profesor (Etapa 2) — ver planificacion/01-roles-y-permisos.md.
Los endpoints que crean/modifican un curso exigen `get_profesor_aprobado_actual` (cuenta
de profesor ya aprobada por un Administrador). `GET /curso-seccion/mi-curso/{id}` es la
contraparte para el Alumno/Apoderado, protegida con `verificar_perfil_propio` ya existente."""

from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from app.application.curso_seccion.casos_de_uso import (
    AgregarAlumnoACurso,
    CrearCursoSeccion,
    PublicarComunicado,
    QuitarAlumnoDeCurso,
)
from app.application.comercial.consultas import BuscarAlumnos
from app.application.curso_seccion.consultas import ObtenerMiCurso, ObtenerProgresoDeCurso
from app.core.deps import (
    get_agregar_alumno_a_curso_uc,
    get_buscar_alumnos_para_profesor_uc,
    get_crear_curso_seccion_uc,
    get_obtener_mi_curso_uc,
    get_obtener_progreso_de_curso_uc,
    get_profesor_aprobado_actual,
    get_publicar_comunicado_uc,
    get_quitar_alumno_de_curso_uc,
    get_repositorio_cursos_seccion,
    verificar_perfil_propio,
)
from app.domain.curso_seccion.exceptions import AlumnoNoEncontrado, CursoAjeno, CursoSeccionNoEncontrado
from app.domain.curso_seccion.ports import RepositorioCursosSeccion
from app.domain.profesor.entities import CuentaProfesor

router = APIRouter(tags=["curso-seccion"])


class CrearCursoRequest(BaseModel):
    nivel_id: int
    nombre: str


class CursoRespuesta(BaseModel):
    id: int
    nivel_id: int
    nombre: str


@router.post("/profesor/cursos", response_model=CursoRespuesta, status_code=status.HTTP_201_CREATED)
def crear_curso(
    datos: CrearCursoRequest,
    profesor: CuentaProfesor = Depends(get_profesor_aprobado_actual),
    uc: CrearCursoSeccion = Depends(get_crear_curso_seccion_uc),
):
    curso = uc.ejecutar(profesor.id, datos.nivel_id, datos.nombre)
    return CursoRespuesta(id=curso.id, nivel_id=curso.nivel_id, nombre=curso.nombre)


@router.get("/profesor/cursos", response_model=list[CursoRespuesta])
def listar_mis_cursos(
    profesor: CuentaProfesor = Depends(get_profesor_aprobado_actual),
    repositorio: RepositorioCursosSeccion = Depends(get_repositorio_cursos_seccion),
):
    return [
        CursoRespuesta(id=c.id, nivel_id=c.nivel_id, nombre=c.nombre)
        for c in repositorio.listar_por_profesor(profesor.id)
    ]


class AlumnoEncontradoRespuesta(BaseModel):
    perfil_alumno_id: int
    nombre: str
    apellidos: str
    rut: str


@router.get("/profesor/alumnos/buscar", response_model=list[AlumnoEncontradoRespuesta])
def buscar_alumnos(
    q: str,
    profesor: CuentaProfesor = Depends(get_profesor_aprobado_actual),
    uc: BuscarAlumnos = Depends(get_buscar_alumnos_para_profesor_uc),
):
    return [
        AlumnoEncontradoRespuesta(perfil_alumno_id=a.perfil_alumno_id, nombre=a.nombre, apellidos=a.apellidos, rut=a.rut)
        for a in uc.ejecutar(q)
    ]


@router.post("/profesor/cursos/{curso_id}/alumnos/{perfil_alumno_id}", status_code=status.HTTP_204_NO_CONTENT)
def agregar_alumno(
    curso_id: int,
    perfil_alumno_id: int,
    profesor: CuentaProfesor = Depends(get_profesor_aprobado_actual),
    uc: AgregarAlumnoACurso = Depends(get_agregar_alumno_a_curso_uc),
):
    try:
        uc.ejecutar(profesor.id, curso_id, perfil_alumno_id)
    except CursoSeccionNoEncontrado:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    except CursoAjeno:
        raise HTTPException(status_code=403, detail="Ese curso no es tuyo")
    except AlumnoNoEncontrado:
        raise HTTPException(status_code=404, detail="Alumno no encontrado")


@router.delete("/profesor/cursos/{curso_id}/alumnos/{perfil_alumno_id}", status_code=status.HTTP_204_NO_CONTENT)
def quitar_alumno(
    curso_id: int,
    perfil_alumno_id: int,
    profesor: CuentaProfesor = Depends(get_profesor_aprobado_actual),
    uc: QuitarAlumnoDeCurso = Depends(get_quitar_alumno_de_curso_uc),
):
    try:
        uc.ejecutar(profesor.id, curso_id, perfil_alumno_id)
    except CursoSeccionNoEncontrado:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    except CursoAjeno:
        raise HTTPException(status_code=403, detail="Ese curso no es tuyo")


class ComunicadoRequest(BaseModel):
    titulo: str
    cuerpo: str


class ComunicadoRespuesta(BaseModel):
    id: int
    titulo: str
    cuerpo: str
    fecha: datetime


@router.post("/profesor/cursos/{curso_id}/comunicados", response_model=ComunicadoRespuesta, status_code=201)
def publicar_comunicado(
    curso_id: int,
    datos: ComunicadoRequest,
    profesor: CuentaProfesor = Depends(get_profesor_aprobado_actual),
    uc: PublicarComunicado = Depends(get_publicar_comunicado_uc),
):
    try:
        comunicado = uc.ejecutar(profesor.id, curso_id, datos.titulo, datos.cuerpo)
    except CursoSeccionNoEncontrado:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    except CursoAjeno:
        raise HTTPException(status_code=403, detail="Ese curso no es tuyo")
    return ComunicadoRespuesta(id=comunicado.id, titulo=comunicado.titulo, cuerpo=comunicado.cuerpo, fecha=comunicado.fecha)


class AlumnoDeCursoRespuesta(BaseModel):
    perfil_alumno_id: int
    nombre: str
    apellidos: str


class NotaPorAsignaturaRespuesta(BaseModel):
    asignatura_id: int
    asignatura_nombre: str
    nota_practica: float | None
    nota_simulacro: float | None


class ProgresoAlumnoRespuesta(AlumnoDeCursoRespuesta):
    notas_por_asignatura: list[NotaPorAsignaturaRespuesta]


class ProgresoDeCursoRespuesta(BaseModel):
    curso: CursoRespuesta
    alumnos: list[ProgresoAlumnoRespuesta]


@router.get("/profesor/cursos/{curso_id}/progreso", response_model=ProgresoDeCursoRespuesta)
def obtener_progreso(
    curso_id: int,
    profesor: CuentaProfesor = Depends(get_profesor_aprobado_actual),
    uc: ObtenerProgresoDeCurso = Depends(get_obtener_progreso_de_curso_uc),
):
    try:
        resultado = uc.ejecutar(profesor.id, curso_id)
    except CursoSeccionNoEncontrado:
        raise HTTPException(status_code=404, detail="Curso no encontrado")
    except CursoAjeno:
        raise HTTPException(status_code=403, detail="Ese curso no es tuyo")
    return ProgresoDeCursoRespuesta(
        curso=CursoRespuesta(id=resultado.curso.id, nivel_id=resultado.curso.nivel_id, nombre=resultado.curso.nombre),
        alumnos=[
            ProgresoAlumnoRespuesta(
                perfil_alumno_id=a.perfil_alumno_id, nombre=a.nombre, apellidos=a.apellidos,
                notas_por_asignatura=[
                    NotaPorAsignaturaRespuesta(
                        asignatura_id=n.asignatura_id, asignatura_nombre=n.asignatura_nombre,
                        nota_practica=n.nota_practica, nota_simulacro=n.nota_simulacro,
                    )
                    for n in a.notas_por_asignatura
                ],
            )
            for a in resultado.alumnos
        ],
    )


class MiCursoRespuesta(BaseModel):
    nombre_curso: str
    nombre_profesor: str
    comunicados: list[ComunicadoRespuesta]


@router.get("/curso-seccion/mi-curso/{perfil_alumno_id}", response_model=MiCursoRespuesta | None)
def obtener_mi_curso(
    perfil_alumno_id: int = Depends(verificar_perfil_propio),
    uc: ObtenerMiCurso = Depends(get_obtener_mi_curso_uc),
):
    resultado = uc.ejecutar(perfil_alumno_id)
    if not resultado:
        return None
    return MiCursoRespuesta(
        nombre_curso=resultado.nombre_curso,
        nombre_profesor=resultado.nombre_profesor,
        comunicados=[
            ComunicadoRespuesta(id=c.id, titulo=c.titulo, cuerpo=c.cuerpo, fecha=c.fecha) for c in resultado.comunicados
        ],
    )
