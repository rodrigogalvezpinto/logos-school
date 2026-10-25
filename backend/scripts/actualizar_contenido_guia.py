"""Actualiza el contenido_guia de los OAs existentes desde archivos Markdown locales.

Este script lee los archivos Markdown de contenido/ y actualiza el campo contenido_guia
de los OAs correspondientes en la base de datos, preservando todas las demás estructuras.

Uso:
    python scripts/actualizar_contenido_guia.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select

from app.infrastructure.persistence.db import engine
from app.infrastructure.persistence.orm_models import ObjetivoAprendizaje, Asignatura, Nivel

CONTENIDO_DIR = Path(__file__).parent.parent.parent / "contenido"


def actualizar_oa(session: Session, archivo_md: Path, nivel_id: int):
    """Actualiza el contenido_guia de un OA desde un archivo Markdown."""
    contenido = archivo_md.read_text(encoding="utf-8")
    
    # Mapeo simple de archivos a asignaturas
    asignacion_por_archivo = {
        "lenguaje-y-comunicacion": "Lenguaje y Comunicación",
        "matematica": "Matemática",
        "ciencias-naturales": "Ciencias Naturales",
        "historia-geografia-y-cs-sociales": "Historia, Geografía y Cs. Sociales",
    }
    
    nombre_archivo = archivo_md.stem
    nombre_asignatura = asignacion_por_archivo.get(nombre_archivo)
    
    if nombre_asignatura:
        # Buscar la asignatura
        asignatura = session.execute(
            select(Asignatura)
            .where(Asignatura.nivel_id == nivel_id)
            .where(Asignatura.nombre == nombre_asignatura)
        ).first()
        
        if asignatura:
            # Buscar el primer OA de esa asignatura
            oa = session.execute(
                select(ObjetivoAprendizaje)
                .where(ObjetivoAprendizaje.asignatura_id == asignatura.id)
                .order_by(ObjetivoAprendizaje.id)
            ).first()
            
            if oa:
                oa.contenido_guia = contenido
                session.add(oa)
                session.commit()
                print(f"✅ Actualizado: {archivo_md.name} -> OA {oa.id} ({oa.descripcion[:50]}...)")
            else:
                print(f"⚠️  No se encontró OA para asignatura {asignatura.nombre}")
        else:
            print(f"⚠️  No se encontró asignatura {nombre_asignatura} en nivel {nivel_id}")
    else:
        print(f"⚠️  Archivo no reconocido: {archivo_md.name}")


def main():
    with Session(engine) as session:
        # 1° básico (nivel_id = 1)
        # Lenguaje (asignatura_id = 1)
        nivel_1_basico = 1
        
        # Buscar todos los archivos de 1° básico
        curso_dir = CONTENIDO_DIR / "01-basico"
        if curso_dir.exists():
            for archivo_md in curso_dir.glob("*.md"):
                if archivo_md.name != "00-estado-contenido.md":
                    actualizar_oa(session, archivo_md, nivel_1_basico)


if __name__ == "__main__":
    main()
