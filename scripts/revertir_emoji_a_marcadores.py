#!/usr/bin/env python3
"""
Script para revertir la conversión de emoji a marcadores [Imagen: ...]
Esto es necesario antes de usar el script de descarga de imágenes de Unsplash.

Uso:
    python scripts/revertir_emoji_a_marcadores.py --curso 01-basico
"""

import re
import sys
import argparse
from pathlib import Path

# Mapeo de cursos
CURSOS_VALIDOS = [
    "01-basico", "02-basico", "03-basico", "04-basico",
    "05-basico", "06-basico", "07-basico", "08-basico",
    "01-medio", "02-medio", "03-medio", "04-medio"
]


def revertir_emoji_a_marcadores(contenido: str) -> str:
    """
    Revierte la conversión de emoji a marcadores originales.
    Convierte ::emoji::🦋::descripcion:: de vuelta a [Imagen: descripcion]
    """
    # Patrón: ::emoji::🦋::una mariposa de colores volando::
    patron = r'::emoji::[^:]+::([^:]+)::'

    def reemplazar(match):
        descripcion = match.group(1)
        return f"[Imagen: {descripcion}]"

    return re.sub(patron, reemplazar, contenido)


def procesar_archivo(ruta_archivo: Path) -> int:
    """Procesa un archivo, revierte emoji a marcadores."""
    print(f"📄 Procesando: {ruta_archivo.name}")

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        contenido = f.read()

    contenido_modificado = revertir_emoji_a_marcadores(contenido)

    if contenido != contenido_modificado:
        with open(ruta_archivo, "w", encoding="utf-8") as f:
            f.write(contenido_modificado)
        print(f"  ✓ Revertido emoji a marcadores")
        return 1
    else:
        print(f"  - No hay emoji para revertir")
        return 0


def procesar_curso(curso: str) -> None:
    """Procesa todos los archivos de contenido de un curso."""
    contenido_dir = Path(__file__).parent.parent / "contenido" / curso

    if not contenido_dir.exists():
        print(f"❌ No existe directorio: {contenido_dir}")
        return

    print(f"\n{'='*60}")
    print(f"🔄 Revirtiendo emoji a marcadores: {curso}")
    print(f"{'='*60}")

    archivos_md = list(contenido_dir.glob("*.md"))

    if not archivos_md:
        print("❌ No se encontraron archivos .md")
        return

    print(f"📁 Encontrados {len(archivos_md)} archivos de contenido")

    total_revertidos = 0

    for archivo in archivos_md:
        total_revertidos += procesar_archivo(archivo)

    print(f"\n{'='*60}")
    print(f"✅ Resumen del curso {curso}:")
    print(f"   Total archivos revertidos: {total_revertidos}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="Revertir emoji a marcadores de imagen")
    parser.add_argument("--curso", required=True, help="Curso a procesar (ej: 01-basico, 02-basico, etc.)")

    args = parser.parse_args()

    if args.curso not in CURSOS_VALIDOS:
        print(f"❌ Curso no válido: {args.curso}")
        print(f"   Cursos válidos: {', '.join(CURSOS_VALIDOS)}")
        sys.exit(1)

    procesar_curso(args.curso)


if __name__ == "__main__":
    main()
