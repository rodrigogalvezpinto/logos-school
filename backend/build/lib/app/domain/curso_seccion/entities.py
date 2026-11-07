from dataclasses import dataclass
from datetime import datetime


@dataclass
class CursoSeccion:
    id: int | None
    profesor_id: int
    nivel_id: int
    nombre: str

    @classmethod
    def crear(cls, profesor_id: int, nivel_id: int, nombre: str) -> "CursoSeccion":
        return cls(id=None, profesor_id=profesor_id, nivel_id=nivel_id, nombre=nombre)


@dataclass
class Comunicado:
    id: int | None
    curso_seccion_id: int
    titulo: str
    cuerpo: str
    fecha: datetime

    @classmethod
    def crear(cls, curso_seccion_id: int, titulo: str, cuerpo: str, fecha: datetime) -> "Comunicado":
        return cls(id=None, curso_seccion_id=curso_seccion_id, titulo=titulo, cuerpo=cuerpo, fecha=fecha)
