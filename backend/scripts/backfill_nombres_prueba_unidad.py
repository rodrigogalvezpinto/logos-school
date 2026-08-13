"""Corrige los nombres de ConjuntoEvaluacion (tipo=prueba_unidad) importados con el bug
de `ruta.stem.replace("-", " ").title()` (sin tildes, "Unidad" en mayúscula donde no
corresponde) — ver el fix en importar_contenido.py (_titulo_desde_encabezado).

Identifica el archivo fuente de cada fila comparando el enunciado de su primera pregunta
(inmutable, ya persistida) contra la primera pregunta parseada de cada archivo candidato de
`contenido/{curso}/pruebas/` que pertenezca a la misma asignatura — no por nombre, que ya
puede estar corrupto por una corrida anterior de un backfill con matching ambiguo entre
cursos (el mismo nombre de archivo, ej. "lenguaje-y-comunicacion-unidad-1.md", existe en más
de un curso).

Uso: python scripts/backfill_nombres_prueba_unidad.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select

from app.infrastructure.persistence.db import engine
from app.infrastructure.persistence.orm_models import Asignatura, ConjuntoEvaluacion, Nivel, Pregunta
from importar_contenido import CONTENIDO_DIR, CURSOS, _asignatura_por_archivo, _titulo_desde_encabezado
from parser_prueba_examen import parsear_prueba_o_examen


def main() -> None:
    total = 0
    sin_match = 0
    with Session(engine) as session:
        filas = session.exec(select(ConjuntoEvaluacion).where(ConjuntoEvaluacion.tipo == "prueba_unidad")).all()
        for fila in filas:
            if not fila.asignatura_id or not fila.pregunta_ids:
                continue
            asignatura = session.get(Asignatura, fila.asignatura_id)
            nivel = session.get(Nivel, asignatura.nivel_id)
            curso = next((c for c in CURSOS if c["nivel"]["nombre"] == nivel.nombre), None)
            if not curso:
                continue

            primera_pregunta = session.get(Pregunta, fila.pregunta_ids[0])
            dir_pruebas = CONTENIDO_DIR / curso["carpeta"] / "pruebas"
            slugs = [slug for slug, _ in curso["asignaturas"]]

            encontrado = None
            for ruta in sorted(dir_pruebas.glob("*.md")):
                slug_archivo = _asignatura_por_archivo(ruta.stem, slugs)
                slug_asignatura = next((s for s, n in curso["asignaturas"] if n == asignatura.nombre), None)
                if slug_archivo != slug_asignatura:
                    continue
                resultado = parsear_prueba_o_examen(ruta.read_text(encoding="utf-8"))
                if not resultado:
                    continue
                primera_del_archivo = resultado[0][0].enunciado
                if primera_del_archivo == primera_pregunta.enunciado:
                    encontrado = ruta
                    break

            if not encontrado:
                print(f"  ⚠️  Sin match para fila id={fila.id} ({fila.nombre!r}, asignatura={asignatura.nombre}, nivel={nivel.nombre})")
                sin_match += 1
                continue

            nombre_correcto = _titulo_desde_encabezado(encontrado)
            if nombre_correcto and nombre_correcto != fila.nombre:
                print(f"  [{nivel.nombre} / {asignatura.nombre}] {fila.nombre!r} -> {nombre_correcto!r}")
                fila.nombre = nombre_correcto
                session.add(fila)
                total += 1
        session.commit()
    print(f"\nActualizadas {total} filas. Sin match: {sin_match}.")


if __name__ == "__main__":
    main()
