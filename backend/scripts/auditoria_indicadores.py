"""Fase 1 · control 4: muestra, por asignatura y OA, los indicadores de evaluación del temario oficial
y todas las preguntas del material (G = guía, P = prueba, S = simulacro), para revisar a mano que
cada indicador tenga al menos una pregunta.

Uso: DATABASE_URL=... python scripts/auditoria_indicadores.py "2° básico" [asignatura]
Solo lectura. Requiere pdftotext.
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))
from sqlmodel import Session, select  # noqa: E402

from auditoria_cobertura_temarios import PDFS, RE_OA, clave_asignatura, leer_pdf, numero_oa  # noqa: E402
from app.infrastructure.persistence.db import engine  # noqa: E402
from app.infrastructure.persistence.orm_models import (  # noqa: E402
    Asignatura, ConjuntoEvaluacion, Nivel, ObjetivoAprendizaje, Pregunta,
)


def indicadores(texto: str) -> dict[str, dict[int, list[str]]]:
    """{asignatura: {oa: [indicador, ...]}} leyendo la columna derecha («Indicadores de Evaluación»)."""
    res: dict[str, dict[int, list[str]]] = {}
    asig, oa, col = None, None, None
    for linea in texto.splitlines():
        cab = re.match(r"^\s{0,10}([A-ZÁÉÍÓÚ][^\d•\-]{3,60}?)[\s_]*$", linea)
        if cab and clave_asignatura(cab.group(1)):
            asig, oa = clave_asignatura(cab.group(1)), None
            res.setdefault(asig, {})
            continue
        if "Indicadores de Evaluaci" in linea:
            col = max(linea.index("Indicadores") - 12, 0)
            continue
        if not asig or col is None:
            continue
        if m := RE_OA.search(linea[: col + 6]):
            oa = int(m.group(1))
            res[asig].setdefault(oa, [])
        if oa is None:
            continue
        # La columna derecha empieza en el último bloque de 2+ espacios después de `col`.
        resto = linea[col:] if len(linea) > col else ""
        izq_restante = re.match(r"^(\S.*?)\s{2,}(\S.*)$", resto)
        derecha = (izq_restante.group(2) if izq_restante and not re.match(r"^[-•−]", resto.strip()) else resto).strip()
        if not derecha or derecha.startswith("Temario"):
            continue
        if re.match(r"^[-•−]\s*", derecha):
            res[asig][oa].append(re.sub(r"^[-•−]\s*", "", derecha))
        elif res[asig][oa]:
            res[asig][oa][-1] += " " + derecha
        else:
            res[asig][oa].append(derecha)
    # Algunos temarios no usan viñetas: un indicador por oración.
    for por_oa in res.values():
        for n, lista in por_oa.items():
            por_oa[n] = [o.strip() for t in lista for o in re.split(r"(?<=\.)\s+(?=[A-ZÁÉÍÓÚ])", t)
                         if len(o.strip()) > 8 and not re.fullmatch(r"\d+ de \d+", o.strip())]
    return res


def main() -> None:
    nivel_nombre = sys.argv[1]
    filtro = sys.argv[2].lower() if len(sys.argv) > 2 else ""
    ind = indicadores(leer_pdf(PDFS[nivel_nombre]))
    with Session(engine) as s:
        tipo = {}
        for c in s.exec(select(ConjuntoEvaluacion)):
            for pid in c.pregunta_ids or []:
                tipo[pid] = "P" if c.tipo == "prueba_unidad" else "S"
        nivel = s.exec(select(Nivel).where(Nivel.nombre == nivel_nombre)).one()
        for a in s.exec(select(Asignatura).where(Asignatura.nivel_id == nivel.id)):
            if filtro and filtro not in a.nombre.lower():
                continue
            k = clave_asignatura(a.nombre)
            print(f"\n######## {a.nombre}")
            oas = {o.id: numero_oa(o.codigo_oficial) for o in s.exec(
                select(ObjetivoAprendizaje).where(ObjetivoAprendizaje.asignatura_id == a.id))}
            por_oa: dict[int, list[str]] = {}
            for p in s.exec(select(Pregunta).where(Pregunta.asignatura_id == a.id)):
                e = re.sub(r"::[a-z]+::\S*", "", p.enunciado)
                e = re.sub(r"\s+", " ", e)
                e = e[-150:] if len(e) > 150 else e  # el final del enunciado es la pregunta
                por_oa.setdefault(oas.get(p.oa_id), []).append(f"{tipo.get(p.id, 'G')}| {e}")
            for n in sorted(set(ind.get(k, {})) | {x for x in por_oa if x}):
                print(f"\n== OA {n}")
                for i, t in enumerate(ind.get(k, {}).get(n, []), 1):
                    print(f"  IND{i}: {re.sub(r'  +', ' ', t)[:230]}")
                for q in sorted(por_oa.get(n, [])):
                    print(f"    {q}")


if __name__ == "__main__":
    main()
