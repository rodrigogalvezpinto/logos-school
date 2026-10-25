#!/usr/bin/env python3
"""
Script para descargar imágenes desde Pixabay para los marcadores [Imagen: ...]
en el contenido de los cursos.

Pixabay es mejor para este proyecto porque:
- No requiere API key para uso básico (hasta 5000 consultas/hora)
- Licencias libres para uso comercial y educativo
- Buena calidad de imágenes
- API simple y documentada

Uso:
    python scripts/descargar_imagenes_pixabay.py --curso 01-basico
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import requests

# Configuración
PIXABAY_API_URL = "https://pixabay.com/api/"
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "")  # Opcional, sin key usa demo limitado
FRONTEND_ASSETS_DIR = Path(__file__).parent.parent / "frontend" / "public" / "assets" / "imagenes"

# Mapeo de cursos a carpetas
CURSOS_MAP = {
    "01-basico": "1-basico",
    "02-basico": "2-basico",
    "03-basico": "3-basico",
    "04-basico": "4-basico",
    "05-basico": "5-basico",
    "06-basico": "6-basico",
    "07-basico": "7-basico",
    "08-basico": "8-basico",
    "01-medio": "1-medio",
    "02-medio": "2-medio",
    "03-medio": "3-medio",
    "04-medio": "4-medio",
}


def extraer_marcadores_imagen(contenido: str) -> List[Tuple[str, str]]:
    """Extrae todos los marcadores [Imagen: ...] del contenido."""
    patron = r'\[Imagen:\s*([^\]]+)\]'
    coincidencias = re.findall(patron, contenido)
    return [(f"[Imagen: {coincidencia}]", coincidencia.strip()) for coincidencia in coincidencias]


def limpiar_terminos_busqueda(descripcion: str) -> str:
    """
    Limpia y adapta la descripción para búsqueda efectiva en Pixabay.
    """
    terminos = descripcion.lower()

    # Reemplazar palabras comunes por términos más efectivos en inglés
    # (Pixabay funciona mejor con términos en inglés)
    reemplazos = {
        "mariposa": "butterfly",
        "gato": "cat",
        "sapo": "frog",
        "perro": "dog",
        "pollo": "chicken",
        "chancho": "pig",
        "queso": "cheese",
        "niña": "girl",
        "niño": "boy",
        "luna": "moon",
        "sol": "sun",
        "pez": "fish",
        "flor": "flower",
        "árbol": "tree",
        "mesa": "table",
        "estuche": "pencil case",
        "lápices": "pencils",
        "pelota": "ball",
        "estrellas": "stars",
        "cielo": "sky",
        "copihue": "flower red",  # Copihue no existe en inglés, usar flower
        "enredadera": "vine",
        "pecera": "fishbowl",
        "guanaco": "llama",  # Guanaco no existe, usar llama similar
        "pudú": "deer",  # Pudú no existe, usar deer
        "araucaria": "pine tree",
        "cactus": "cactus",
        "mochila": "backpack",
        "goma": "eraser",
        "regla": "ruler",
        "tijeras": "scissors",
        "cuchara": "spoon",
        "cubo de hielo": "ice cube",
        "hoja de papel": "paper",
        "alambre": "wire",
        "galleta": "cookie",
        "chincol": "bird",
        "búho": "owl",
        "cueca": "dance chile",  # Cueca específica
        "poncho": "poncho",
        "mapa": "map",
        "cordillera": "mountains",
        "valle": "valley",
        "plaza": "square",
        "hospital": "hospital",
        "escuela": "school",
        "doctora": "doctor",
        "enfermera": "nurse",
    }

    for espanol, ingles in reemplazos.items():
        terminos = terminos.replace(espanol, ingles)

    # Eliminar palabras muy comunes que no ayudan
    palabras_ignorar = ["de", "la", "el", "un", "una", "con", "y", "en", "para", "que", "del", "al", "los", "las", "por", "como", "muestra", "dibujada", "dibujado", "dibujadas", "colgando", "junto", "derecha", "izquierda", "arriba", "abajo", "adelante", "detras"]

    terminos = " ".join([palabra for palabra in terminos.split() if palabra not in palabras_ignorar])

    # Limitar a 3-4 palabras clave
    palabras = terminos.split()[:4]
    return " ".join(palabras)


def buscar_imagen_pixabay(descripcion: str) -> str | None:
    """
    Busca una imagen en Pixabay basada en la descripción.
    Retorna la URL de la imagen o None si no se encuentra.
    """
    try:
        terminos_busqueda = limpiar_terminos_busqueda(descripcion)

        if not terminos_busqueda:
            return None

        params = {
            "key": PIXABAY_API_KEY,
            "q": terminos_busqueda,
            "image_type": "photo",
            "per_page": 3,  # Buscar 3 opciones y tomar la primera
            "safesearch": "true",  # Solo contenido seguro
            "orientation": "horizontal",
        }

        response = requests.get(PIXABAY_API_URL, params=params, timeout=15)

        if response.status_code == 200:
            data = response.json()
            if data.get("hits") and len(data["hits"]) > 0:
                # Usar la imagen de mejor calidad disponible
                imagen = data["hits"][0]
                # Preferir largeURL si existe, sino regular, sino small
                url = imagen.get("largeImageURL") or imagen.get("webformatURL") or imagen.get("previewURL")
                return url
        else:
            print(f"  ⚠ Error en API Pixabay: {response.status_code}")

    except Exception as e:
        print(f"  ⚠ Error buscando imagen: {e}")

    return None


def descargar_imagen(url: str, ruta_destino: Path) -> bool:
    """Descarga una imagen desde una URL y la guarda en la ruta destino."""
    try:
        response = requests.get(url, timeout=30)
        if response.status_code == 200:
            ruta_destino.parent.mkdir(parents=True, exist_ok=True)
            with open(ruta_destino, "wb") as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"  ⚠ Error descargando imagen: {e}")

    return False


def generar_nombre_archivo(descripcion: str, indice: int) -> str:
    """Genera un nombre de archivo seguro basado en la descripción."""
    limpio = re.sub(r"[^a-zA-Z0-9áéíóúñ\s-]", "", descripcion)
    limpio = limpio.strip()[:50]
    limpio = limpio.replace(" ", "-").lower()
    return f"{indice:03d}-{limpio}.jpg"


def procesar_archivo_contenido(ruta_archivo: Path, curso: str) -> Dict[str, str]:
    """
    Procesa un archivo de contenido (.md), descarga las imágenes necesarias
    y retorna un diccionario con el mapeo de marcador -> ruta de imagen.
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
    carpeta_curso = FRONTEND_ASSETS_DIR / CURSOS_MAP.get(curso, curso)

    for i, (marcador, descripcion) in enumerate(marcadores, 1):
        print(f"  [{i}/{len(marcadores)}] Buscando: {descripcion}")

        # Verificar si ya existe imagen para este marcador
        nombre_archivo = generar_nombre_archivo(descripcion, i)
        ruta_imagen = carpeta_curso / nombre_archivo

        if ruta_imagen.exists():
            print(f"    ✓ Imagen ya existe: {nombre_archivo}")
            ruta_relativa = f"/assets/imagenes/{CURSOS_MAP.get(curso, curso)}/{nombre_archivo}"
            mapeo_marcadores[marcador] = ruta_relativa
            continue

        # Buscar imagen en Pixabay
        url_imagen = buscar_imagen_pixabay(descripcion)

        if url_imagen:
            # Descargar imagen
            if descargar_imagen(url_imagen, ruta_imagen):
                print(f"    ✓ Descargada: {nombre_archivo}")
                ruta_relativa = f"/assets/imagenes/{CURSOS_MAP.get(curso, curso)}/{nombre_archivo}"
                mapeo_marcadores[marcador] = ruta_relativa
            else:
                print(f"    ✗ No se pudo descargar")
        else:
            print(f"    ✗ No se encontró imagen en Pixabay")

    return mapeo_marcadores


def actualizar_contenido_con_imagenes(ruta_archivo: Path, mapeo: Dict[str, str]) -> None:
    """
    Actualiza el archivo de contenido reemplazando los marcadores de imagen
    por etiquetas de imagen Markdown reales.
    """
    if not mapeo:
        return

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        contenido = f.read()

    for marcador, ruta_imagen in mapeo.items():
        descripcion = marcador.replace("[Imagen: ", "").replace("]", "")
        etiqueta_imagen = f"\n![{descripcion}]({ruta_imagen})\n"
        contenido = contenido.replace(marcador, etiqueta_imagen)

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(contenido)

    print(f"  ✓ Archivo actualizado con {len(mapeo)} imágenes")


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
    total_descargadas = 0

    for archivo in archivos_md:
        mapeo = procesar_archivo_contenido(archivo, curso)
        total_marcadores += len(mapeo)
        total_descargadas += len(mapeo)

        if mapeo:
            actualizar_contenido_con_imagenes(archivo, mapeo)

    print(f"\n{'='*60}")
    print(f"✅ Resumen del curso {curso}:")
    print(f"   Total marcadores procesados: {total_marcadores}")
    print(f"   Total imágenes descargadas: {total_descargadas}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="Descargar imágenes desde Pixabay para el contenido de cursos")
    parser.add_argument("--curso", required=True, help="Curso a procesar (ej: 01-basico, 02-basico, etc.)")

    args = parser.parse_args()

    if args.curso not in CURSOS_MAP:
        print(f"❌ Curso no válido: {args.curso}")
        print(f"   Cursos válidos: {', '.join(CURSOS_MAP.keys())}")
        sys.exit(1)

    procesar_curso(args.curso)


if __name__ == "__main__":
    main()
