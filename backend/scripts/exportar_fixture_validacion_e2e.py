"""Exporta, desde la base indicada en DATABASE_URL, el inventario completo de material
(niveles, asignaturas, guías/OA, pruebas y simulacros) con la clave de cada pregunta,
para la validación integral E2E (frontend/e2e/validacion-integral-material.spec.ts).

Uso: DATABASE_URL=... python scripts/exportar_fixture_validacion_e2e.py <salida.json>
Solo lectura. La salida contiene claves: no versionarla (está en .gitignore)."""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from sqlmodel import Session, select  # noqa: E402

from app.infrastructure.persistence.db import engine  # noqa: E402
from app.infrastructure.persistence.orm_models import (  # noqa: E402
    Asignatura, ConjuntoEvaluacion, Nivel, ObjetivoAprendizaje, Pregunta,
)


def main() -> None:
    salida = Path(sys.argv[1])
    with Session(engine) as s:
        claves = {
            p.id: {"tipo": p.tipo, "correcta": p.respuesta_correcta, "opciones": p.opciones, "oa": p.oa_id}
            for p in s.exec(select(Pregunta))
        }
        en_conjuntos = {pid for c in s.exec(select(ConjuntoEvaluacion))
                        if c.tipo in ("prueba_unidad", "examen_simulacro") for pid in c.pregunta_ids}
        niveles = []
        for n in s.exec(select(Nivel).order_by(Nivel.id)):
            asignaturas = []
            for a in s.exec(select(Asignatura).where(Asignatura.nivel_id == n.id).order_by(Asignatura.id)):
                oas = s.exec(select(ObjetivoAprendizaje).where(ObjetivoAprendizaje.asignatura_id == a.id)
                             .order_by(ObjetivoAprendizaje.id)).all()
                conjuntos = s.exec(select(ConjuntoEvaluacion).where(ConjuntoEvaluacion.asignatura_id == a.id)
                                   .order_by(ConjuntoEvaluacion.id)).all()
                asignaturas.append({
                    "id": a.id, "nombre": a.nombre,
                    "oas": [{"id": o.id, "codigo": o.codigo_oficial,
                             "preguntas": sum(1 for k, c in claves.items() if c["oa"] == o.id and k not in en_conjuntos)} for o in oas],
                    "conjuntos": [{"id": c.id, "tipo": c.tipo, "nombre": c.nombre, "preguntas": len(c.pregunta_ids)}
                                  for c in conjuntos],
                })
            integrados = s.exec(select(ConjuntoEvaluacion).where(ConjuntoEvaluacion.nivel_id == n.id,
                                                                 ConjuntoEvaluacion.asignatura_id == None)).all()  # noqa: E711
            niveles.append({"id": n.id, "nombre": n.nombre, "asignaturas": asignaturas,
                            "integrados": [{"id": c.id, "tipo": c.tipo, "nombre": c.nombre,
                                            "preguntas": len(c.pregunta_ids)} for c in integrados]})
    salida.write_text(json.dumps({"niveles": niveles, "claves": {str(k): v for k, v in claves.items()}},
                                 ensure_ascii=False), encoding="utf-8")
    total_conj = sum(len(a["conjuntos"]) for n in niveles for a in n["asignaturas"]) + sum(len(n["integrados"]) for n in niveles)
    print(f"{len(niveles)} niveles, {sum(len(a['oas']) for n in niveles for a in n['asignaturas'])} OA, "
          f"{total_conj} evaluaciones, {len(claves)} preguntas → {salida}")


if __name__ == "__main__":
    main()
