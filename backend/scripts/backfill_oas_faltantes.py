"""Inserta los OA que el parser antiguo descartaba, sin borrar ni reimportar el resto
de la base. Caso real que motivó este script: 4° medio Educación Ciudadana tiene un OA
cuyo número oficial no consta en el temario (aparece cortado en el PDF) y su heading es
`## OA (Democracia y sus desafíos): ...`; el regex anterior exigía un dígito y lo
descartaba en silencio, dejando la BD con 407 de los 408 OA.

Es idempotente: recorre las guías, compara códigos oficiales por asignatura e inserta
solo los que faltan, con sus preguntas de autoevaluación.

Uso:
    python scripts/backfill_oas_faltantes.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select

from app.infrastructure.persistence.db import engine
from app.infrastructure.persistence.orm_models import (
    Asignatura,
    Nivel,
    ObjetivoAprendizaje,
    Pregunta,
)
from importar_contenido import CURSOS, CONTENIDO_DIR
from parser_contenido import parsear_guia


def main() -> None:
    total_oa = 0
    total_preguntas = 0

    with Session(engine) as session:
        for curso in CURSOS:
            nivel = session.exec(
                select(Nivel).where(Nivel.nombre == curso["nivel"]["nombre"])
            ).first()
            if nivel is None:
                continue

            for slug, nombre_asignatura in curso["asignaturas"]:
                asignatura = session.exec(
                    select(Asignatura).where(
                        Asignatura.nivel_id == nivel.id,
                        Asignatura.nombre == nombre_asignatura,
                    )
                ).first()
                if asignatura is None:
                    continue

                ruta = CONTENIDO_DIR / curso["carpeta"] / f"{slug}.md"
                if not ruta.exists():
                    continue

                existentes = {
                    o.codigo_oficial
                    for o in session.exec(
                        select(ObjetivoAprendizaje).where(
                            ObjetivoAprendizaje.asignatura_id == asignatura.id
                        )
                    ).all()
                }

                for oa in parsear_guia(ruta.read_text(encoding="utf-8")):
                    if oa.codigo_oficial in existentes:
                        continue

                    fila = ObjetivoAprendizaje(
                        asignatura_id=asignatura.id,
                        codigo_oficial=oa.codigo_oficial,
                        descripcion=oa.descripcion,
                        eje_tematico=oa.eje_tematico,
                        contenido_guia=oa.contenido_guia,
                    )
                    session.add(fila)
                    session.commit()
                    session.refresh(fila)

                    for p in oa.preguntas:
                        session.add(
                            Pregunta(
                                oa_id=fila.id,
                                asignatura_id=asignatura.id,
                                tipo=p.tipo,
                                enunciado=p.enunciado,
                                opciones=p.opciones,
                                respuesta_correcta=p.respuesta_correcta,
                                retroalimentacion=p.retroalimentacion,
                            )
                        )
                    session.commit()

                    existentes.add(oa.codigo_oficial)
                    total_oa += 1
                    total_preguntas += len(oa.preguntas)
                    print(
                        f"[+] {nivel.nombre} / {nombre_asignatura}: "
                        f"{oa.codigo_oficial} ({len(oa.preguntas)} preguntas)"
                    )

    print(f"\nTotal OAs insertados: {total_oa}")
    print(f"Total preguntas insertadas: {total_preguntas}")


if __name__ == "__main__":
    main()
