#!/usr/bin/env python3
"""
Script para descargar imágenes desde Unsplash para los marcadores [Imagen: ...]
en el contenido de los cursos.

Uso:
    python scripts/descargar_imagenes_unsplash.py --curso 1-basico

Requiere:
    - requests: pip install requests
    - Variable de entorno UNSPLASH_ACCESS_KEY (opcional, usa demo key si no está)
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import requests

# Configuración
UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY", "FaS9looUxptNJfjX-s0TDwZ6NUAM20qlg6PB0neWRME")
UNSPLASH_API_URL = "https://api.unsplash.com/search/photos"
FRONTEND_ASSETS_DIR = Path(__file__).parent.parent / "frontend" / "public" / "assets" / "imagenes"

# Mapeo de cursos a carpetas (debe coincidir con nombres reales en contenido/)
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
    """
    Extrae todos los marcadores [Imagen: ...] del contenido.
    Retorna lista de (marcador_original, descripcion)
    """
    patron = r'\[Imagen:\s*([^\]]+)\]'
    coincidencias = re.findall(patron, contenido)
    return [(f"[Imagen: {coincidencia}]", coincidencia.strip()) for coincidencia in coincidencias]


def buscar_imagen_unsplash(descripcion: str) -> str | None:
    """
    Busca una imagen en Unsplash basada en la descripción.
    Retorna la URL de la imagen o None si no se encuentra.
    """
    try:
        # Limpiar descripción para búsqueda
        terminos_busqueda = descripcion.lower()
        # Reemplazar palabras comunes por términos más efectivos
        terminos_busqueda = terminos_busqueda.replace("de colores", "colorful")
        terminos_busqueda = terminos_busqueda.replace("dibujadas", "illustration")
        terminos_busqueda = terminos_busqueda.replace("dibujado", "illustration")
        terminos_busqueda = terminos_busqueda.replace("alineados", "arranged")

        params = {
            "query": terminos_busqueda,
            "per_page": 1,
            "orientation": "landscape" if "fila" in terminos_busqueda or "horizontal" in terminos_busqueda else "all",
        }

        headers = {}
        if UNSPLASH_ACCESS_KEY != "demo":
            headers["Authorization"] = f"Client-ID {UNSPLASH_ACCESS_KEY}"

        response = requests.get(UNSPLASH_API_URL, params=params, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            if data.get("results") and len(data["results"]) > 0:
                # Usar la URL regular (no raw) para mejor calidad
                return data["results"][0]["urls"]["regular"]
        else:
            print(f"  ⚠ Error en API Unsplash: {response.status_code}")

    except Exception as e:
        print(f"  ⚠ Error buscando imagen: {e}")

    return None


def descargar_imagen(url: str, ruta_destino: Path) -> bool:
    """
    Descarga una imagen desde una URL y la guarda en la ruta destino.
    Retorna True si fue exitoso, False en caso contrario.
    """
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
    """
    Genera un nombre de archivo seguro basado en la descripción.
    """
    # Limpiar descripción: solo letras, números y guiones
    limpio = re.sub(r"[^a-zA-Z0-9áéíóúñ\s-]", "", descripcion)
    limpio = limpio.strip()[:50]  # Limitar longitud
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

        # Buscar imagen en Unsplash
        url_imagen = buscar_imagen_unsplash(descripcion)

        if url_imagen:
            # Descargar imagen
            if descargar_imagen(url_imagen, ruta_imagen):
                print(f"    ✓ Descargada: {nombre_archivo}")
                ruta_relativa = f"/assets/imagenes/{CURSOS_MAP.get(curso, curso)}/{nombre_archivo}"
                mapeo_marcadores[marcador] = ruta_relativa
            else:
                print(f"    ✗ No se pudo descargar")
        else:
            print(f"    ✗ No se encontró imagen en Unsplash")

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
        # Reemplazar [Imagen: descripcion] por ![descripcion](ruta)
        descripcion = marcador.replace("[Imagen: ", "").replace("]", "")
        etiqueta_imagen = f"\n![{descripcion}]({ruta_imagen})\n"
        contenido = contenido.replace(marcador, etiqueta_imagen)

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(contenido)

    print(f"  ✓ Archivo actualizado con {len(mapeo)} imágenes")


def procesar_curso(curso: str) -> None:
    """
    Procesa todos los archivos de contenido de un curso.
    """
    contenido_dir = Path(__file__).parent.parent / "contenido" / curso

    if not contenido_dir.exists():
        print(f"❌ No existe directorio: {contenido_dir}")
        return

    print(f"\n{'='*60}")
    print(f"🎓 Procesando curso: {curso}")
    print(f"{'='*60}")

    # Buscar todos los archivos .md del curso
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
    parser = argparse.ArgumentParser(description="Descargar imágenes desde Unsplash para el contenido de cursos")
    parser.add_argument("--curso", required=True, help="Curso a procesar (ej: 1-basico, 2-basico, etc.)")
    parser.add_argument("--archivo", help="Archivo específico a procesar (opcional)")

    args = parser.parse_args()

    if args.curso not in CURSOS_MAP:
        print(f"❌ Curso no válido: {args.curso}")
        print(f"   Cursos válidos: {', '.join(CURSOS_MAP.keys())}")
        sys.exit(1)

    # Verificar si requests está instalado
    try:
        import requests
    except ImportError:
        print("❌ Falta instalar requests: pip install requests")
        sys.exit(1)

    procesar_curso(args.curso)


if __name__ == "__main__":
    main()
