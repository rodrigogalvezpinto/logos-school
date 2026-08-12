"""Importa el contenido ya escrito en contenido/{curso}/*.md a la base de datos.

Uso:
    python scripts/importar_contenido.py

Ver planificacion/11-especificacion-mvp-para-desarrollo.md (Paso 3 del plan de
desarrollo). Idempotente a nivel de Nivel: si el Nivel ya existe en la base, se omite
(no duplica datos si se corre más de una vez).
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select

from app.core.db import engine, crear_tablas
from app.models import Asignatura, Nivel, ObjetivoAprendizaje, Pregunta
from parser_contenido import parsear_guia

CONTENIDO_DIR = Path(__file__).parent.parent.parent / "contenido"

# Configuración de los cursos a importar — se agregan más a medida que el roadmap
# avance a más niveles (ver planificacion/03-roadmap-etapas.md).
CURSOS = [
    {
        "carpeta": "04-basico",
        "nivel": {
            "nombre": "4° básico",
            "regimen": "A",
            "decreto": "439/2012",
            "formato_examen": "integrado",
            "num_preguntas_examen": 20,
            "duracion_examen_min": 90,
            "materiales_permitidos": "Ninguno",
        },
        "asignaturas": [
            ("lenguaje-y-comunicacion", "Lenguaje y Comunicación"),
            ("matematica", "Matemática"),
            ("ciencias-naturales", "Ciencias Naturales"),
            ("historia-geografia-y-cs-sociales", "Historia, Geografía y Cs. Sociales"),
        ],
    },
    {
        "carpeta": "06-basico",
        "nivel": {
            "nombre": "6° básico",
            "regimen": "B",
            "decreto": "439/2012",
            "formato_examen": "separado_por_asignatura",
            "num_preguntas_examen": 25,
            "duracion_examen_min": 90,
            "materiales_permitidos": "Calculadora, diccionario de inglés",
        },
        "asignaturas": [
            ("lenguaje-y-comunicacion", "Lenguaje y Comunicación"),
            ("matematica", "Matemática"),
            ("ciencias-naturales", "Ciencias Naturales"),
            ("historia-geografia-y-cs-sociales", "Historia, Geografía y Cs. Sociales"),
            ("ingles", "Inglés"),
        ],
    },
]


def importar_curso(session: Session, curso: dict) -> None:
    nombre_nivel = curso["nivel"]["nombre"]
    existente = session.exec(select(Nivel).where(Nivel.nombre == nombre_nivel)).first()
    if existente:
        print(f"  {nombre_nivel}: ya estaba importado, se omite.")
        return

    nivel = Nivel(**curso["nivel"])
    session.add(nivel)
    session.commit()
    session.refresh(nivel)

    total_oa = 0
    total_preguntas = 0

    for archivo, nombre_asignatura in curso["asignaturas"]:
        ruta = CONTENIDO_DIR / curso["carpeta"] / f"{archivo}.md"
        if not ruta.exists():
            print(f"    ⚠️  No existe {ruta}, se omite esta asignatura.")
            continue

        asignatura = Asignatura(nivel_id=nivel.id, nombre=nombre_asignatura)
        session.add(asignatura)
        session.commit()
        session.refresh(asignatura)

        objetivos = parsear_guia(ruta.read_text(encoding="utf-8"))
        for oa_parseado in objetivos:
            oa = ObjetivoAprendizaje(
                asignatura_id=asignatura.id,
                codigo_oficial=oa_parseado.codigo_oficial,
                descripcion=oa_parseado.descripcion,
                eje_tematico=oa_parseado.eje_tematico,
                contenido_guia=oa_parseado.contenido_guia,
            )
            session.add(oa)
            session.commit()
            session.refresh(oa)
            total_oa += 1

            for p in oa_parseado.preguntas:
                session.add(
                    Pregunta(
                        oa_id=oa.id,
                        tipo=p.tipo,
                        enunciado=p.enunciado,
                        opciones=p.opciones,
                        respuesta_correcta=p.respuesta_correcta,
                        retroalimentacion=p.retroalimentacion,
                    )
                )
                total_preguntas += 1
        session.commit()
        print(f"    {nombre_asignatura}: {len(objetivos)} OA, {sum(len(o.preguntas) for o in objetivos)} preguntas")

    print(f"  {nombre_nivel}: TOTAL {total_oa} OA, {total_preguntas} preguntas importadas.")


def main() -> None:
    crear_tablas()
    with Session(engine) as session:
        for curso in CURSOS:
            print(f"Importando {curso['nivel']['nombre']}...")
            importar_curso(session, curso)


if __name__ == "__main__":
    main()
