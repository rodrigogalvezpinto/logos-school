"""Lista las preguntas de pruebas y simulacros cuya «explicación» solo repite la clave (control C.4,
auditoría Fase 1, 2026-11-15). En el resumen final el alumno ve esa explicación: «c) Alcalde» no le enseña
por qué se equivocó. Uso: python scripts/explicaciones_pobres.py   (sale con código 1 si encuentra alguna)
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parser_prueba_examen import parsear_prueba_o_examen  # noqa: E402

CONTENIDO = Path(__file__).resolve().parents[2] / "contenido"


def _norm(texto) -> str:
    return re.sub(r"[\W_]+", "", str(texto).lower())


def es_pobre(clave: str, retro: str | None) -> bool:
    """True si la explicación, sin la letra inicial ni «Verdadero/Falso», no agrega nada a la clave."""
    # Letra inicial («c)», «**c.**») o varias letras de «varias correctas» («a, b y c.»; 2026-11-16 había 11 así).
    r = re.sub(r"^\s*\(?\**[a-h](?:, [a-h])*(?: y [a-h])?\)?\.?\**\s*[—:-]?\s*", "", retro or "").strip()
    r = re.sub(r"^\**(Verdadero|Falso|True|False)\**\.?\s*(\((Verdadero|Falso)\))?\.?\s*$", "", r).strip()
    if isinstance(clave, str) and clave.startswith("["):
        try:
            clave = "".join(json.loads(clave))
        except ValueError:
            pass
    nr, nc = _norm(r), _norm(clave)
    return nr == "" or nr == nc or (len(nr) <= len(nc) + 2 and nr in nc + "verdaderofalsotruefalse")


def buscar() -> dict[str, list[int]]:
    resultado = {}
    for ruta in sorted(CONTENIDO.glob("*/pruebas/*.md")) + sorted(CONTENIDO.glob("*/examenes/*.md")):
        numeros = [p.numero for p, r in parsear_prueba_o_examen(ruta.read_text(encoding="utf-8"))
                   if es_pobre(r.respuesta_correcta, r.retroalimentacion)]
        if numeros:
            resultado[str(ruta.relative_to(CONTENIDO))] = numeros
    return resultado


if __name__ == "__main__":
    hallados = buscar()
    for archivo, numeros in hallados.items():
        print(f"{archivo}: {', '.join(map(str, numeros))}")
    print(f"{sum(map(len, hallados.values()))} explicaciones que solo repiten la clave")
    sys.exit(1 if hallados else 0)
