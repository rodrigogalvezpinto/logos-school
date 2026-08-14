"""Reconstruye el banco de preguntas de autoevaluación (todas las guías, los 12 cursos)
desde los archivos fuente, con parser_contenido.py ya corregido (letra de pauta resuelta a
texto real, emojis, True/False bilingüe, opciones con word-wrap). Necesario porque el fix de
word-wrap cambia también el `enunciado` (ya no incluye el texto contaminado de la opción
siguiente), así que un backfill por enunciado ya no encuentra las filas viejas para
actualizarlas — hay que recrearlas.

No toca `ObjetivoAprendizaje` (el seguimiento de "guía revisada" se guarda por
perfil_alumno_id + oa_id, no por pregunta_id) ni las cuentas demo — solo borra y recrea
`Pregunta` con oa_id no nulo.

Uso: python scripts/reimportar_banco_autoevaluacion.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select

from app.infrastructure.persistence.db import engine
from app.infrastructure.persistence.orm_models import Asignatura, Nivel, ObjetivoAprendizaje, Pregunta
from importar_contenido import CONTENIDO_DIR, CURSOS
from parser_contenido import parsear_guia


def main() -> None:
    with Session(engine) as session:
        total_borradas = session.exec(select(Pregunta).where(Pregunta.oa_id.is_not(None))).all()
        n_borradas = len(total_borradas)
        for p in total_borradas:
            session.delete(p)
        session.commit()
        print(f"Borradas {n_borradas} preguntas del banco de autoevaluación.")

        total_creadas = 0
        for curso in CURSOS:
            nivel = session.exec(select(Nivel).where(Nivel.nombre == curso["nivel"]["nombre"])).first()
            if not nivel:
                continue
            for slug, nombre_asignatura in curso["asignaturas"]:
                asignatura = session.exec(
                    select(Asignatura).where(Asignatura.nivel_id == nivel.id, Asignatura.nombre == nombre_asignatura)
                ).first()
                if not asignatura:
                    continue
                ruta_guia = CONTENIDO_DIR / curso["carpeta"] / f"{slug}.md"
                if not ruta_guia.exists():
                    continue
                objetivos = parsear_guia(ruta_guia.read_text(encoding="utf-8"))
                oas_por_codigo = {
                    oa.codigo_oficial: oa.id
                    for oa in session.exec(
                        select(ObjetivoAprendizaje).where(ObjetivoAprendizaje.asignatura_id == asignatura.id)
                    ).all()
                }
                for oa_parseado in objetivos:
                    oa_id = oas_por_codigo.get(oa_parseado.codigo_oficial)
                    if not oa_id:
                        continue
                    for p in oa_parseado.preguntas:
                        session.add(
                            Pregunta(
                                oa_id=oa_id,
                                asignatura_id=asignatura.id,
                                tipo=p.tipo,
                                enunciado=p.enunciado,
                                opciones=p.opciones,
                                respuesta_correcta=p.respuesta_correcta,
                                retroalimentacion=p.retroalimentacion,
                            )
                        )
                        total_creadas += 1
            session.commit()
            print(f"  {curso['nivel']['nombre']}: importado.")

    print(f"\nTotal preguntas recreadas: {total_creadas}.")


if __name__ == "__main__":
    main()
