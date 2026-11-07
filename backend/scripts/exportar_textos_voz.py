"""Exporta guías y preguntas de los niveles indicados para pregrabar su lectura en voz alta
(scripts/voz/generar_audios.sh). Solo lectura; la salida no trae claves de respuesta.

Uso: DATABASE_URL=... python scripts/exportar_textos_voz.py <salida.json> "1° básico" "2° básico"
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from sqlmodel import Session, select  # noqa: E402

from app.domain.evaluaciones.value_objects import quitar_numeracion_de_rangos  # noqa: E402
from app.infrastructure.persistence.db import engine  # noqa: E402
from app.infrastructure.persistence.orm_models import (  # noqa: E402
    Asignatura, Nivel, ObjetivoAprendizaje, Pregunta,
)


def main() -> None:
    salida, niveles = Path(sys.argv[1]), sys.argv[2:]
    with Session(engine) as s:
        ids_asig = [a.id for n in s.exec(select(Nivel).where(Nivel.nombre.in_(niveles)))
                    for a in s.exec(select(Asignatura).where(Asignatura.nivel_id == n.id))]
        guias = [o.contenido_guia for o in s.exec(
            select(ObjetivoAprendizaje).where(ObjetivoAprendizaje.asignatura_id.in_(ids_asig))) if o.contenido_guia]
        # Pruebas y simulacros entregan el enunciado sin «preguntas 1 a 5» (routers/evaluaciones.py):
        # se exportan ambas variantes para que el audio coincida con el texto que ve el alumno.
        preguntas = [{"tipo": p.tipo, "enunciado": e, "opciones": p.opciones}
                     for p in s.exec(select(Pregunta).where(Pregunta.asignatura_id.in_(ids_asig)))
                     for e in dict.fromkeys([p.enunciado, quitar_numeracion_de_rangos(p.enunciado)])]
    salida.write_text(json.dumps({"guias": guias, "preguntas": preguntas}, ensure_ascii=False))
    print(f"{len(guias)} guías y {len(preguntas)} preguntas de {', '.join(niveles)} → {salida}")


if __name__ == "__main__":
    main()
