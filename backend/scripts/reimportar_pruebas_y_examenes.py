"""Reconstruye TODAS las pruebas de unidad y exámenes simulacro (los 12 cursos) desde los
archivos fuente, con el parser ya corregido (RE_Q_START tolera negrita o etiqueta de tipo
entre paréntesis en cursiva — ver parser_prueba_examen.py). Necesario porque los cursos
importados antes de ese fix pueden tener preguntas de menos (o cero) si su formato usaba
"1. *(Alternativas)*" en vez de "**1.**".

No toca el banco de autoevaluación de las guías (`parser_contenido.py` es un parser aparte,
no afectado por este fix) ni Niveles/Asignaturas/OA — solo borra y recrea ConjuntoEvaluacion
de tipo prueba_unidad/examen_simulacro, sus Pregunta asociadas, y los IntentoEvaluacion que
las referenciaban (datos de prueba/demo, no hay usuarios reales todavía).

Uso: python scripts/reimportar_pruebas_y_examenes.py
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select

from app.infrastructure.persistence.db import engine
from app.infrastructure.persistence.orm_models import (
    Asignatura,
    ConjuntoEvaluacion,
    IntentoEvaluacion,
    Nivel,
    ObjetivoAprendizaje,
    Pregunta,
)
from importar_contenido import CONTENIDO_DIR, CURSOS, _asignatura_por_archivo, _importar_conjunto, _titulo_desde_encabezado


def main() -> None:
    with Session(engine) as session:
        # 1) Borra todo lo existente de tipo prueba_unidad/examen_simulacro.
        conjuntos = session.exec(
            select(ConjuntoEvaluacion).where(ConjuntoEvaluacion.tipo.in_(["prueba_unidad", "examen_simulacro"]))
        ).all()
        total_borrados = len(conjuntos)
        for c in conjuntos:
            for intento in session.exec(
                select(IntentoEvaluacion).where(IntentoEvaluacion.conjunto_evaluacion_id == c.id)
            ).all():
                session.delete(intento)
            for pid in c.pregunta_ids:
                p = session.get(Pregunta, pid)
                if p:
                    session.delete(p)
            session.delete(c)
        session.commit()
        print(f"Borrados {total_borrados} ConjuntoEvaluacion (prueba_unidad/examen_simulacro) y sus preguntas.")

        # 2) Reimporta desde cero para los 12 cursos.
        total_pruebas = total_examenes = 0
        for curso in CURSOS:
            nivel = session.exec(select(Nivel).where(Nivel.nombre == curso["nivel"]["nombre"])).first()
            if not nivel:
                print(f"  ⚠️  Nivel {curso['nivel']['nombre']} no existe, se omite.")
                continue

            asignaturas_por_slug = {}
            oas_por_asignatura = {}
            for slug, nombre in curso["asignaturas"]:
                a = session.exec(
                    select(Asignatura).where(Asignatura.nivel_id == nivel.id, Asignatura.nombre == nombre)
                ).first()
                if a:
                    asignaturas_por_slug[slug] = a
                    oas = session.exec(select(ObjetivoAprendizaje).where(ObjetivoAprendizaje.asignatura_id == a.id)).all()
                    oas_por_asignatura[a.id] = {oa.codigo_oficial: oa.id for oa in oas}
            slugs = list(asignaturas_por_slug.keys())

            dir_pruebas = CONTENIDO_DIR / curso["carpeta"] / "pruebas"
            n_pruebas = 0
            if dir_pruebas.exists():
                for ruta in sorted(dir_pruebas.glob("*.md")):
                    slug = _asignatura_por_archivo(ruta.stem, slugs)
                    if not slug:
                        continue
                    asignatura = asignaturas_por_slug[slug]
                    n = _importar_conjunto(
                        session, ruta, tipo="prueba_unidad",
                        nombre=_titulo_desde_encabezado(ruta) or ruta.stem.replace("-", " ").title(),
                        forma=None, asignatura_id=asignatura.id, nivel_id=None,
                        tiempo_sugerido_min=None, oas_por_codigo=oas_por_asignatura.get(asignatura.id, {}),
                    )
                    if n:
                        n_pruebas += 1

            dir_examenes = CONTENIDO_DIR / curso["carpeta"] / "examenes"
            n_examenes = 0
            if dir_examenes.exists():
                for ruta in sorted(dir_examenes.glob("*.md")):
                    forma_m = re.search(r"forma-([ab])", ruta.stem, re.IGNORECASE)
                    forma = forma_m.group(1).upper() if forma_m else None

                    if ruta.stem.startswith("examen-integrado"):
                        n = _importar_conjunto(
                            session, ruta, tipo="examen_simulacro",
                            nombre=f"Examen integrado Forma {forma}", forma=forma,
                            asignatura_id=None, nivel_id=nivel.id,
                            tiempo_sugerido_min=nivel.duracion_examen_min, oas_por_codigo={},
                        )
                    else:
                        slug = _asignatura_por_archivo(ruta.stem, slugs)
                        if not slug:
                            continue
                        asignatura = asignaturas_por_slug[slug]
                        n = _importar_conjunto(
                            session, ruta, tipo="examen_simulacro",
                            nombre=f"Examen {asignatura.nombre} Forma {forma}", forma=forma,
                            asignatura_id=asignatura.id, nivel_id=None,
                            tiempo_sugerido_min=nivel.duracion_examen_min,
                            oas_por_codigo=oas_por_asignatura.get(asignatura.id, {}),
                        )
                    if n:
                        n_examenes += 1

            print(f"  {curso['nivel']['nombre']}: {n_pruebas} pruebas, {n_examenes} exámenes.")
            total_pruebas += n_pruebas
            total_examenes += n_examenes

    print(f"\nTotal: {total_pruebas} pruebas de unidad, {total_examenes} exámenes simulacro.")


if __name__ == "__main__":
    main()
