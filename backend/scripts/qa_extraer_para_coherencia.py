"""QA semántico de contenido — extracción.

Saca de la base de datos, para un nivel (curso) dado, cada Pregunta vinculada a un
Objetivo de Aprendizaje junto con la guía de ese OA, en un JSON listo para que un
revisor (humano o LLM) juzgue coherencia: ¿la respuesta marcada como correcta calza con
lo que enseña la guía? ¿la pregunta evalúa algo que la guía realmente cubre?

No emite ningún juicio por sí solo — es la mitad "determinística" del pipeline (traer los
datos correctos, completos, sin alucinar contenido). El juicio semántico lo hace un
LLM/humano leyendo el JSON resultante, ver planificacion/26-qa-sistema-automatizado.md.

Uso:
    uv run python scripts/qa_extraer_para_coherencia.py "4° básico" > /tmp/qa_4basico.json
    uv run python scripts/qa_extraer_para_coherencia.py --listar-niveles
"""

import json
import sys

from sqlmodel import Session, select

from app.infrastructure.persistence.db import engine
from app.infrastructure.persistence.orm_models import Asignatura, Nivel, ObjetivoAprendizaje, Pregunta


def listar_niveles(session: Session) -> None:
    for n in session.exec(select(Nivel)).all():
        print(f"{n.id}\t{n.nombre}")


def extraer(session: Session, nombre_nivel: str) -> list[dict]:
    nivel = session.exec(select(Nivel).where(Nivel.nombre == nombre_nivel)).first()
    if not nivel:
        raise SystemExit(f"Nivel '{nombre_nivel}' no encontrado. Usa --listar-niveles para ver los nombres exactos.")

    filas = session.exec(
        select(Pregunta, ObjetivoAprendizaje, Asignatura)
        .join(ObjetivoAprendizaje, Pregunta.oa_id == ObjetivoAprendizaje.id)
        .join(Asignatura, ObjetivoAprendizaje.asignatura_id == Asignatura.id)
        .where(Asignatura.nivel_id == nivel.id)
    ).all()

    items = []
    for pregunta, oa, asignatura in filas:
        items.append({
            "asignatura": asignatura.nombre,
            "oa_codigo": oa.codigo_oficial,
            "oa_descripcion": oa.descripcion,
            "oa_guia": oa.contenido_guia,
            "pregunta_id": pregunta.id,
            "tipo": pregunta.tipo,
            "enunciado": pregunta.enunciado,
            "opciones": pregunta.opciones,
            "respuesta_correcta": pregunta.respuesta_correcta,
            "retroalimentacion": pregunta.retroalimentacion,
        })
    return items


if __name__ == "__main__":
    with Session(engine) as session:
        if "--listar-niveles" in sys.argv:
            listar_niveles(session)
            sys.exit(0)
        if len(sys.argv) < 2:
            raise SystemExit("Uso: qa_extraer_para_coherencia.py <nombre del nivel>  (o --listar-niveles)")
        items = extraer(session, sys.argv[1])
        print(json.dumps(items, ensure_ascii=False, indent=2))
