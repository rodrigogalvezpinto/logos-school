#!/usr/bin/env python3
"""
Validador (solo lectura) de distribución de claves en exámenes de alternativas.

Regla: ninguna letra (a, b, c, d) debe superar el 45 % del total de preguntas
de alternativas con clave.

Uso: python validador_claves.py [ruta_archivo_o_directorio]

IMPORTANTE: este script NO reescribe claves. Un intento anterior de bajar el
sesgo cambiando sólo la letra de la pauta produjo 33 claves incorrectas (la
alternativa correcta quedaba en otra letra). El sesgo se corrige intercambiando
el texto de las alternativas en el enunciado, nunca la letra de la pauta.
"""

import re
import sys
import argparse
from pathlib import Path
from collections import Counter
from typing import Dict, List


RE_FILA = re.compile(r"^\|\s*(\d{1,2})\s*\|")
RE_CLAVE_BOLD = re.compile(r"\*\*([a-d])\)")
RE_CELDA_LETRA = re.compile(r"^[a-d]$")
RE_LETRA_INICIO = re.compile(r"^([a-d])\)")
# Respuesta de desarrollo con sub-ítems en la misma celda: "a) Abril...; b) 22 + ..."
# No es una clave de alternativas.
RE_SUBITEM = re.compile(r";\s*[b-e]\)")


def bloque_pauta(contenido: str) -> str:
    """Desde el heading de PAUTA DE CORRECCIÓN hasta el final del archivo."""
    m = re.search(r"^#{1,6}\s+PAUTA DE CORRECCI", contenido, re.IGNORECASE | re.MULTILINE)
    return contenido[m.start():] if m else ""


def extraer_claves(contenido: str) -> List[str]:
    """Claves de la tabla de pauta.

    Reconoce dos formatos:
      - clave en negrita dentro de una celda:  | 3 | Alternativas | **b) texto** | OA | 1 |
      - tabla compacta con la letra sola:      | 3 | b | OA1 | 1 |
    """
    claves = []
    for linea in bloque_pauta(contenido).split("\n"):
        linea = linea.strip()
        if not RE_FILA.match(linea):
            continue
        celdas = [c.strip() for c in linea.strip("|").split("|")]
        # Formato compacto de Filosofía: | 3 | b | OA1 | 1 |
        if len(celdas) == 4 and RE_CELDA_LETRA.match(celdas[1]):
            claves.append(celdas[1])
            continue
        # La clave puede estar en cualquier celda posterior al número, con o
        # sin negrita: | 3 | **b)** texto | OA |  ·  | 3 | Alternativas | b) texto | OA |
        for celda in celdas[1:]:
            m = RE_CLAVE_BOLD.match(celda)
            if m:
                claves.append(m.group(1))
                break
            m = RE_LETRA_INICIO.match(celda)
            if m:
                if RE_SUBITEM.search(celda):
                    break
                claves.append(m.group(1))
                break
    return claves


def analizar_archivo(ruta: Path) -> Dict:
    contenido = ruta.read_text(encoding="utf-8")
    claves = extraer_claves(contenido)
    if not claves:
        return {
            "archivo": str(ruta),
            "total": 0,
            "distribucion": {},
            "excede_45": False,
            "letra_max": None,
            "porcentaje_max": 0.0,
        }
    total = len(claves)
    dist = Counter(claves)
    letra_max, count_max = dist.most_common(1)[0]
    pct_max = round(count_max / total * 100, 1)
    return {
        "archivo": str(ruta),
        "total": total,
        "distribucion": dict(sorted(dist.items())),
        "excede_45": pct_max > 45,
        "letra_max": letra_max,
        "porcentaje_max": pct_max,
    }


def archivos_de(ruta: Path) -> List[Path]:
    if ruta.is_file():
        return [ruta]
    archivos = set(ruta.rglob("*-forma-b.md"))
    archivos.update(ruta.rglob("examen-integrado-forma-*.md"))
    return sorted(archivos)


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(description="Validador de distribución de claves (máx. 45 %)")
    parser.add_argument("ruta", nargs="?", default="contenido", help="Archivo o directorio a validar")
    args = parser.parse_args()

    ruta = Path(args.ruta)
    if not ruta.exists():
        print(f"[ERROR] Ruta no existe: {ruta}")
        sys.exit(1)

    resultados = []
    for archivo in archivos_de(ruta):
        r = analizar_archivo(archivo)
        resultados.append(r)
        if r["total"] == 0:
            print(f"[WARN] sin claves detectadas: {archivo}")
        elif r["excede_45"]:
            print(f"[WARN] EXCEDE 45%: {archivo} — {r['letra_max']}={r['porcentaje_max']}% ({r['distribucion']})")
        else:
            print(f"[OK] {archivo} — max {r['letra_max']} {r['porcentaje_max']}%")

    con_exceso = sum(1 for r in resultados if r["excede_45"])
    sin_claves = sum(1 for r in resultados if r["total"] == 0)
    print(f"\n[RESUMEN] {len(resultados)} archivos, {con_exceso} exceden 45%, {sin_claves} sin claves detectadas")
    sys.exit(1 if con_exceso or sin_claves else 0)


if __name__ == "__main__":
    main()
