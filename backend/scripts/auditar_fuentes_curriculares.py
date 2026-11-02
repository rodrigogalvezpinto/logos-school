import argparse
import hashlib
import json
import re
from pathlib import Path

from pypdf import PdfReader


def extraer_oa(texto: str) -> list[int]:
    return sorted({int(numero) for numero in re.findall(
        r"(?:OA|Objetivo\s+de\s+Aprendizaje)\s*(?:N[°ºo.]?\s*)?(\d{1,2})\b",
        texto, flags=re.IGNORECASE,
    )})


def paginas_ingles(paginas: list[str]) -> list[int]:
    for numero, texto in enumerate(paginas, 1):
        if re.search(r"idioma\s+extranjero\s*[:\-–—]?\s*ingl[eé]s", texto, re.IGNORECASE):
            return list(range(numero, len(paginas) + 1))
    return []


def auditar_pdf(ruta: Path, incluir_texto: bool = False) -> dict:
    paginas = [pagina.extract_text() or "" for pagina in PdfReader(ruta).pages]
    seleccionadas = paginas_ingles(paginas)
    resultado = {
        "fuente": str(ruta),
        "sha256": hashlib.sha256(ruta.read_bytes()).hexdigest(),
        "paginas_totales": len(paginas),
        "paginas_ingles": seleccionadas,
        "oa_en_paginas_ingles": extraer_oa("\n".join(paginas[n - 1] for n in seleccionadas)),
        "limite": "Extracción textual sin OCR ni verificación visual; confirmar continuidad de páginas y lectura disciplinar.",
    }
    if incluir_texto:
        resultado["texto"] = [{"pagina": n, "texto": paginas[n - 1]} for n in seleccionadas]
    return resultado


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("archivos", nargs="+", type=Path)
    parser.add_argument("--texto", action="store_true")
    args = parser.parse_args()
    print(json.dumps([auditar_pdf(ruta, args.texto) for ruta in args.archivos], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
