#!/usr/bin/env python3
"""
Script para convertir marcadores [Imagen: ...] a emoji grandes en el contenido.
Esta es una solución rápida que no requiere APIs externas ni descargas de imágenes.

Los emoji se mostrarán en un componente Angular especial que los hace visualmente
atractivos y educativos.

Uso:
    python scripts/convertir_marcadores_a_emoji.py --curso 01-basico
"""

import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple

# Mapeo de descripciones a emoji
EMOJI_MAP = {
    # Animales
    "mariposa": "🦋",
    "gato": "🐱",
    "sapo": "🐸",
    "perro": "🐕",
    "pollo": "🐔",
    "chancho": "🐷",
    "pez": "🐟",
    "pescado": "🐟",
    "guanaco": "🦙",
    "pudú": "🦌",
    "chincol": "🐦",
    "búho": "🦉",
    "ave": "🐦",
    "pajaro": "🐦",

    # Personas
    "niña": "👧",
    "niño": "👦",
    "doctora": "👩‍⚕️",
    "doctor": "👨‍⚕️",
    "enfermera": "👩‍⚕️",
    "profesor": "👨‍🏫",
    "pareja": "👫",
    "adulto": "🧑",

    # Naturaleza
    "flor": "🌸",
    "copihue": "🌺",
    "enredadera": "🌿",
    "árbol": "🌳",
    "araucaria": "🌲",
    "cactus": "🌵",
    "planta": "🌱",
    "hoja": "🍃",

    # Cielo y clima
    "luna": "🌙",
    "sol": "☀️",
    "estrellas": "⭐",
    "cielo": "🌤️",
    "lluvia": "🌧️",
    "nube": "☁️",
    "tormenta": "⛈️",

    # Objetos escolares
    "estuche": "🎒",
    "lápices": "✏️",
    "lápiz": "✏️",
    "goma": "🧹",
    "regla": "📏",
    "tijeras": "✂️",
    "mochila": "🎒",
    "libro": "📚",
    "papel": "📄",
    "hoja de papel": "📄",

    # Comida
    "queso": "🧀",
    "galleta": "🍪",
    "empanada": "🥟",
    "pan": "🍞",

    # Hogar
    "mesa": "🪑",
    "silla": "🪑",
    "cama": "🛏️",
    "casa": "🏠",
    "edificio": "🏢",
    "escuela": "🏫",
    "hospital": "🏥",

    # Materiales
    "pelota": "⚽",
    "alambre": "🧵",
    "cuchara": "🥄",
    "cubo de hielo": "🧊",
    "agua": "💧",
    "pecera": "🐠",

    # Geografía
    "mapa": "🗺️",
    "cordillera": "🏔️",
    "montaña": "⛰️",
    "valle": "🏞️",
    "plaza": "🏞️",
    "desierto": "🏜️",
    "mar": "🌊",
    "rio": "🌊",

    # Abstracciones
    "mano": "👋",
    "ojos": "👀",
    "oídos": "👂",
    "nariz": "👃",
    "lengua": "👅",
    "corazón": "❤️",

    # Acciones
    "caminando": "🚶",
    "durmiendo": "😴",
    "comiendo": "🍽️",
    "bailando": "💃",
    "corriendo": "🏃",
}

# Emoji por defecto cuando no hay mapeo específico
EMOJI_DEFAULT = "🎨"


def extraer_marcadores_imagen(contenido: str) -> List[Tuple[str, str]]:
    """Extrae todos los marcadores [Imagen: ...] del contenido."""
    patron = r'\[Imagen:\s*([^\]]+)\]'
    coincidencias = re.findall(patron, contenido)
    return [(f"[Imagen: {coincidencia}]", coincidencia.strip()) for coincidencia in coincidencias]


def obtener_emoji_descripcion(descripcion: str) -> str:
    """
    Obtiene el emoji más apropiado para una descripción.
    Busca coincidencias parciales en el mapeo.
    """
    descripcion_lower = descripcion.lower()

    # Buscar coincidencia exacta primero
    if descripcion_lower in EMOJI_MAP:
        return EMOJI_MAP[descripcion_lower]

    # Buscar coincidencia parcial
    for clave, emoji in EMOJI_MAP.items():
        if clave in descripcion_lower:
            return emoji

    # Si no hay coincidencia, usar emoji por defecto
    return EMOJI_DEFAULT


def generar_etiqueta_emoji(descripcion: str) -> str:
    """
    Genera una etiqueta de emoji grande con formato especial para el componente Angular.
    """
    emoji = obtener_emoji_descripcion(descripcion)
    # Formato: ::emoji::descripcion::
    return f"::emoji::{emoji}::{descripcion}::"


def procesar_archivo_contenido(ruta_archivo: Path) -> Dict[str, str]:
    """
    Procesa un archivo de contenido (.md), convierte los marcadores a emoji
    y retorna un diccionario con el mapeo de marcador -> etiqueta emoji.
    """
    print(f"\n📄 Procesando: {ruta_archivo.name}")

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        contenido = f.read()

    marcadores = extraer_marcadores_imagen(contenido)

    if not marcadores:
        print("  ✓ No hay marcadores de imagen")
        return {}

    print(f"  📸 Encontrados {len(marcadores)} marcadores de imagen")

    mapeo_marcadores: Dict[str, str] = {}

    for marcador, descripcion in marcadores:
        etiqueta_emoji = generar_etiqueta_emoji(descripcion)
        mapeo_marcadores[marcador] = etiqueta_emoji
        emoji = obtener_emoji_descripcion(descripcion)
        print(f"  • {descripcion} → {emoji}")

    return mapeo_marcadores


def actualizar_contenido_con_emoji(ruta_archivo: Path, mapeo: Dict[str, str]) -> None:
    """
    Actualiza el archivo de contenido reemplazando los marcadores de imagen
    por etiquetas de emoji.
    """
    if not mapeo:
        return

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        contenido = f.read()

    for marcador, etiqueta_emoji in mapeo.items():
        contenido = contenido.replace(marcador, etiqueta_emoji)

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(contenido)

    print(f"  ✓ Archivo actualizado con {len(mapeo)} emoji")


def procesar_curso(curso: str) -> None:
    """Procesa todos los archivos de contenido de un curso."""
    contenido_dir = Path(__file__).parent.parent / "contenido" / curso

    if not contenido_dir.exists():
        print(f"❌ No existe directorio: {contenido_dir}")
        return

    print(f"\n{'='*60}")
    print(f"🎓 Procesando curso: {curso}")
    print(f"{'='*60}")

    archivos_md = list(contenido_dir.glob("*.md"))

    if not archivos_md:
        print("❌ No se encontraron archivos .md")
        return

    print(f"📁 Encontrados {len(archivos_md)} archivos de contenido")

    total_marcadores = 0

    for archivo in archivos_md:
        mapeo = procesar_archivo_contenido(archivo)
        total_marcadores += len(mapeo)

        if mapeo:
            actualizar_contenido_con_emoji(archivo, mapeo)

    print(f"\n{'='*60}")
    print(f"✅ Resumen del curso {curso}:")
    print(f"   Total marcadores convertidos: {total_marcadores}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="Convertir marcadores de imagen a emoji en el contenido")
    parser.add_argument("--curso", required=True, help="Curso a procesar (ej: 01-basico, 02-basico, etc.)")

    args = parser.parse_args()

    cursos_validos = [
        "01-basico", "02-basico", "03-basico", "04-basico",
        "05-basico", "06-basico", "07-basico", "08-basico",
        "01-medio", "02-medio", "03-medio", "04-medio"
    ]

    if args.curso not in cursos_validos:
        print(f"❌ Curso no válido: {args.curso}")
        print(f"   Cursos válidos: {', '.join(cursos_validos)}")
        sys.exit(1)

    procesar_curso(args.curso)


if __name__ == "__main__":
    main()
