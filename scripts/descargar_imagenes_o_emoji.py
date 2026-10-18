#!/usr/bin/env python3
"""
Script para descargar imágenes desde Unsplash con fallback a emoji.
Si no se encuentra imagen en Unsplash, usa emoji como fallback.

Uso:
    python scripts/descargar_imagenes_o_emoji.py --curso 01-basico
"""

import os
import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple
import requests

# Configuración
# Usar Pixabay en lugar de Unsplash (API más liberal)
PIXABAY_API_KEY = os.getenv("PIXABAY_API_KEY", "")  # Vacío usa demo limitado
PIXABAY_API_URL = "https://pixabay.com/api/"
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

# Mapeo de descripciones a emoji (fallback) - versión simplificada
EMOJI_MAP = {
    "mariposa": "🦋", "gato": "🐱", "sapo": "🐸", "perro": "🐕", "pollo": "🐔",
    "chancho": "🐷", "queso": "🧀", "niña": "👧", "niño": "👦", "doctora": "👩‍⚕️",
    "doctor": "👨‍⚕️", "enfermera": "👩‍⚕️", "flor": "🌸", "copihue": "🌺", "enredadera": "🌿",
    "árbol": "🌳", "araucaria": "🌲", "cactus": "🌵", "planta": "🌱", "hoja": "🍃",
    "luna": "🌙", "sol": "☀️", "estrellas": "⭐", "cielo": "🌤️", "lluvia": "🌧️",
    "nube": "☁️", "estuche": "🎒", "lápices": "✏️", "lápiz": "✏️", "goma": "🧹",
    "regla": "📏", "tijeras": "✂️", "mochila": "🎒", "libro": "📚", "papel": "📄",
    "mesa": "🪑", "silla": "🪑", "cama": "🛏️", "casa": "🏠", "edificio": "🏢",
    "escuela": "🏫", "hospital": "🏥", "pelota": "⚽", "cuchara": "🥄", "cubo de hielo": "🧊",
    "agua": "💧", "pecera": "🐠", "mapa": "🗺️", "cordillera": "🏔️", "montaña": "⛰️",
    "valle": "🏞️", "desierto": "🏜️", "mar": "🌊", "rio": "🌊", "plaza": "🏞️",
    "mano": "👋", "ojos": "👀", "oídos": "👂", "nariz": "👃", "lengua": "👅",
    "corazón": "❤️", "corazones": "❤️", "fuego": "🔥", "comida": "🍽️", "fruta": "🍎",
    "verdura": "🥬", "gafas": "👓", "reloj": "⌚", "calendario": "📅", "balanza": "⚖️",
    "triángulo": "🔺", "círculo": "⭕", "cuadrado": "⬜", "rectángulo": "🔲", "dado": "🎲",
    "esfera": "🌐", "cubo": "🎲", "cono": "🍦", "cilindro": "🥫", "pirámide": "🔺",
    "paralelepípedo": "📦", "flecha": "➡️", "bandera": "🚩", "banderas": "🚩", "mundo": "🌍",
    "globo": "🌎", "tierra": "🌍", "satélite": "🛰️", "cohete": "🚀", "avión": "✈️",
    "tren": "🚂", "auto": "🚗", "bicicleta": "🚲", "camión": "🚚", "barco": "⛵",
    "bote": "⛵", "bús": "🚌", "playa": "🏖️", "arena": "🏖️", "bosque": "🌲",
    "selva": "🌴", "nieve": "❄️", "hielo": "🧊", "volcán": "🌋", "terremoto": "🌋",
    "humo": "💨", "viento": "💨", "tormenta": "⛈️", "arcoíris": "🌈", "arco iris": "🌈",
    "rayo": "⚡", "trueno": "⛈️", "temperatura": "🌡️", "termómetro": "🌡️", "clima": "🌡️",
    "llave": "🔑", "candado": "🔒", "puerta": "🚪", "ventana": "🪟", "comercio": "🏪",
    "tienda": "🏪", "supermercado": "🏪", "mercado": "🏪", "feria": "🎪", "dinero": "💰",
    "moneda": "💰", "billetes": "💵", "tarjeta": "💳", "billetera": "👛", "banco": "🏦",
    "cajero": "🏧", "atm": "🏧", "crédito": "💳", "débito": "💳", "pago": "💳",
    "compra": "🛒", "carro": "🚗", "camión": "🚚", "moto": "🏍️", "bici": "🚲",
    "autobús": "🚌", "taxi": "🚕", "metro": "🚇", "subway": "🚇", "tren": "🚂",
    "estación": "🚉", "paradero": "🚏", "señal": "🚦", "semáforo": "🚦", "paso cebra": "🚶",
    "cruce": "🚶", "peatonal": "🚶", "camino": "🛣️", "calle": "🛣️", "autopista": "🛣️",
    "carretera": "🛣️", "ruta": "🗺️", "brújula": "🧭", "gps": "📍", "ubicación": "📍",
    "destino": "📍", "origen": "📍", "llegada": "📍", "salida": "🚪", "entrada": "🚪",
    "salir": "🚪", "entrar": "🚪", "ir": "➡️", "venir": "⬅️", "volver": "⬅️",
    "regresar": "⬅️", "subir": "⬆️", "bajar": "⬇️", "arriba": "⬆️", "abajo": "⬇️",
    "izquierda": "⬅️", "derecha": "➡️", "centro": "🎯", "meta": "🎯", "objetivo": "🎯",
    "fin": "🏁", "inicio": "▶️", "final": "🏁", "pausa": "⏸️", "play": "▶️",
    "stop": "⏹️", "grabar": "⏺️", "cámara": "📷", "foto": "📷", "video": "📹",
    "película": "🎬", "cine": "🎬", "teatro": "🎭", "música": "🎵", "canción": "🎤",
    "baile": "💃", "fiesta": "🎉", "celebración": "🎉", "regalo": "🎁", "pastel": "🎂",
    "vela": "🕯️", "globos": "🎈", "confeti": "🎊", "fuegos artificiales": "🎆", "fuegos": "🎆",
    "petardos": "🎆", "champagne": "🍾", "brindis": "🥂", "copa": "🥂", "vaso": "🥂",
    "botella": "🍾", "cerveza": "🍺", "vino": "🍷", "trago": "🍷", "bebida": "🥤",
    "refresco": "🥤", "jugo": "🧃", "zumo": "🧃", "batido": "🥤", "smoothie": "🥤",
    "té": "🍵", "café": "☕", "mate": "🧉", "leche": "🥛", "huevo": "🥚",
    "huevos": "🥚", "carne": "🥩", "pescado": "🐟", "pollo": "🍗", "cerdo": "🐷",
    "cordero": "🐑", "langosta": "🦞", "camarón": "🦐", "mariscos": "🦐", "ensalada": "🥗",
    "sopa": "🍲", "postre": "🥖", "pan": "🍞", "arroz": "🍚", "pasta": "🍝",
    "pizza": "🍕", "hamburguesa": "🍔", "sándwich": "🥪", "taco": "🌮", "burrito": "🌯",
    "wrap": "🌯", "dulce": "🍬", "chocolate": "🍫", "helado": "🍦", "helados": "🍦",
    "sorbete": "🍦", "congelado": "🧊", "caliente": "🔥", "frío": "❄️", "fecha": "📅",
    "hora": "⏰", "día": "☀️", "noche": "🌙", "mañana": "🌅", "tarde": "🌆",
    "atardecer": "🌅", "amanecer": "🌅", "juego": "🎮", "juegos": "🎮", "deporte": "⚽",
    "deportes": "⚽", "fútbol": "⚽", "baloncesto": "🏀", "tenis": "🎾", "natación": "🏊",
    "ciclismo": "🚴", "atletismo": "🏃", "gimnasio": "🏋️", "entrenamiento": "🏋️", "fitness": "🏋️",
    "salud": "🏥", "bienestar": "🏥", "medicina": "💊", "ambulancia": "🚑", "botiquín": "💊",
    "píldora": "💊", "vacuna": "💉", "inyección": "💉", "cirugía": "🏥", "operación": "🏥",
    "recuperación": "🛌", "rehabilitación": "🛌", "fisioterapia": "🏋️", "terapia": "🏋️",
    "psicología": "🧠", "psiquiatra": "🧠", "psicólogo": "🧠", "consejero": "🧑‍⚕️", "asesor": "🧑‍🏫",
    "profesor": "👨‍🏫", "maestro": "👨‍🏫", "docente": "👨‍🏫", "educación": "🎓", "clase": "🏫",
    "aula": "🏫", "biblioteca": "📚", "lectura": "📖", "escritura": "✍️", "matemáticas": "📐",
    "matemática": "📐", "cálculo": "🧮", "álgebra": "📊", "geometría": "📐", "estadística": "📊",
    "física": "⚛️", "química": "⚗️", "biología": "🧬", "historia": "📜", "geografía": "🌍",
    "ciencias": "🔬", "tecnología": "💻", "informática": "💻", "computación": "💻", "programación": "💻",
    "arte": "🎨", "danza": "💃", "literatura": "📚", "idioma": "🗣️", "lenguaje": "🗣️",
    "inglés": "🇬🇧", "francés": "🇫🇷", "alemán": "🇩🇪", "italiano": "🇮🇹", "portugués": "🇵🇹",
    "ruso": "🇷🇺", "chino": "🇨🇳", "japonés": "🇯🇵", "coreano": "🇰🇷", "español": "🇪🇸",
    "chileno": "🇨🇱", "argentino": "", "peruano": "🇵🇪", "boliviano": "🇧🇴", "ecuatoriano": "🇪🇨",
    "colombiano": "🇨🇴", "venezolano": "🇻🇪", "mexicano": "🇲🇽", "estadounidense": "🇺🇸", "canadiense": "🇨🇦",
    "australiano": "🇦🇺", "neozelandés": "🇳🇿", "sudafricano": "🇿🇦", "brasileño": "🇧🇷",
}

EMOJI_DEFAULT = ""


def extraer_marcadores_imagen(contenido: str) -> List[Tuple[str, str]]:
    """Extrae todos los marcadores [Imagen: ...] del contenido."""
    patron = r'\[Imagen:\s*([^\]]+)\]'
    coincidencias = re.findall(patron, contenido)
    return [(f"[Imagen: {coincidencia}]", coincidencia.strip()) for coincidencia in coincidencias]


def buscar_imagen_pixabay(descripcion: str) -> str | None:
    """
    Busca una imagen en Pixabay basada en la descripción.
    Retorna la URL de la imagen o None si no se encuentra.
    """
    try:
        # Traducir términos en español a inglés para mejores resultados
        terminos_busqueda = descripcion.lower()

        reemplazos = {
            "mariposa": "butterfly", "gato": "cat", "sapo": "frog", "perro": "dog",
            "pollo": "chicken", "chancho": "pig", "queso": "cheese", "niña": "girl",
            "niño": "boy", "luna": "moon", "sol": "sun", "pez": "fish", "flor": "flower",
            "árbol": "tree", "mesa": "table", "estuche": "pencil case", "lápices": "pencils",
            "pelota": "ball", "estrellas": "stars", "cielo": "sky", "copihue": "flower red",
            "enredadera": "vine", "pecera": "fishbowl", "guanaco": "llama", "pudú": "deer",
            "araucaria": "pine tree", "cactus": "cactus", "mochila": "backpack", "goma": "eraser",
            "regla": "ruler", "tijeras": "scissors", "cuchara": "spoon", "cubo de hielo": "ice cube",
            "hoja de papel": "paper", "alambre": "wire", "galleta": "cookie", "chincol": "bird",
            "búho": "owl", "cueca": "dance chile", "poncho": "poncho", "mapa": "map",
            "cordillera": "mountains", "valle": "valley", "plaza": "square", "hospital": "hospital",
            "escuela": "school", "doctora": "doctor", "enfermera": "nurse", "de colores": "colorful",
            "dibujadas": "illustration", "dibujado": "illustration", "alineados": "arranged",
            "volando": "flying", "sentado": "sitting", "verde": "green", "rojo": "red",
            "azul": "blue", "amarillo": "yellow",
        }

        for espanol, ingles in reemplazos.items():
            terminos_busqueda = terminos_busqueda.replace(espanol, ingles)

        # Eliminar palabras muy comunes que no ayudan
        palabras_ignorar = ["de", "la", "el", "un", "una", "con", "y", "en", "para", "que", "del", "al", "los", "las", "por", "como", "muestra", "dibujada", "dibujado", "dibujadas", "colgando", "junto", "derecha", "izquierda", "arriba", "abajo", "adelante", "detras"]

        terminos_busqueda = " ".join([palabra for palabra in terminos_busqueda.split() if palabra not in palabras_ignorar])

        # Limitar a 3-4 palabras clave
        palabras = terminos_busqueda.split()[:4]
        terminos_busqueda = " ".join(palabras)

        params = {
            "key": PIXABAY_API_KEY,
            "q": terminos_busqueda,
            "image_type": "photo",
            "per_page": 3,
            "safesearch": "true",
            "orientation": "horizontal" if "fila" in terminos_busqueda or "horizontal" in terminos_busqueda else "all",
        }

        response = requests.get(PIXABAY_API_URL, params=params, timeout=15)

        if response.status_code == 200:
            data = response.json()
            if data.get("hits") and len(data["hits"]) > 0:
                imagen = data["hits"][0]
                # Preferir largeURL si existe, sino regular, sino small
                url = imagen.get("largeImageURL") or imagen.get("webformatURL") or imagen.get("previewURL")
                return url
        else:
            print(f"  ⚠ Error en API Pixabay: {response.status_code}")

    except Exception as e:
        print(f"  ⚠ Error buscando imagen: {e}")

    return None


def obtener_emoji_fallback(descripcion: str) -> str:
    """Obtiene emoji para fallback si no se encuentra imagen."""
    descripcion_lower = descripcion.lower()

    # Buscar coincidencia exacta primero
    if descripcion_lower in EMOJI_MAP:
        return EMOJI_MAP[descripcion_lower]

    # Buscar coincidencia parcial
    for clave, emoji in EMOJI_MAP.items():
        if clave in descripcion_lower:
            return emoji

    return EMOJI_DEFAULT


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
    Procesa un archivo de contenido, descarga imágenes de Unsplash
    y genera formato con imagen + emoji fallback.
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
            emoji_fallback = obtener_emoji_fallback(descripcion)
            mapeo_marcadores[marcador] = f"\n![{descripcion}]({ruta_relativa})\n\n::emoji::{emoji_fallback}::{descripcion}::\n"
            continue

        # Buscar imagen en Pixabay
        url_imagen = buscar_imagen_pixabay(descripcion)

        if url_imagen:
            # Descargar imagen
            if descargar_imagen(url_imagen, ruta_imagen):
                print(f"    ✓ Descargada: {nombre_archivo}")
                ruta_relativa = f"/assets/imagenes/{CURSOS_MAP.get(curso, curso)}/{nombre_archivo}"
                emoji_fallback = obtener_emoji_fallback(descripcion)
                mapeo_marcadores[marcador] = f"\n![{descripcion}]({ruta_relativa})\n\n::emoji::{emoji_fallback}::{descripcion}::\n"
            else:
                print(f"    ✗ No se pudo descargar, usando emoji fallback")
                emoji_fallback = obtener_emoji_fallback(descripcion)
                mapeo_marcadores[marcador] = f"\n::emoji::{emoji_fallback}::{descripcion}::\n"
        else:
            print(f"    ✗ No se encontró imagen en Unsplash, usando emoji fallback")
            emoji_fallback = obtener_emoji_fallback(descripcion)
            mapeo_marcadores[marcador] = f"\n::emoji::{emoji_fallback}::{descripcion}::\n"

    return mapeo_marcadores


def actualizar_contenido_con_imagenes(ruta_archivo: Path, mapeo: Dict[str, str]) -> None:
    """
    Actualiza el archivo de contenido reemplazando los marcadores por imágenes
    con emoji fallback.
    """
    if not mapeo:
        return

    with open(ruta_archivo, "r", encoding="utf-8") as f:
        contenido = f.read()

    for marcador, contenido_imagen in mapeo.items():
        contenido = contenido.replace(marcador, contenido_imagen)

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        f.write(contenido)

    print(f"  ✓ Archivo actualizado con {len(mapeo)} entradas (imagen + emoji fallback)")


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
    total_imagenes = 0
    total_emoji_fallback = 0

    for archivo in archivos_md:
        mapeo = procesar_archivo_contenido(archivo, curso)
        total_marcadores += len(mapeo)

        if mapeo:
            actualizar_contenido_con_imagenes(archivo, mapeo)
            # Contar cuántos tienen imagen real vs solo emoji
            con_imagen = sum(1 for contenido in mapeo.values() if contenido.startswith("\n!"))
            total_imagenes += con_imagen
            total_emoji_fallback += len(mapeo) - con_imagen

    print(f"\n{'='*60}")
    print(f"✅ Resumen del curso {curso}:")
    print(f"   Total marcadores procesados: {total_marcadores}")
    print(f"   Imágenes reales descargadas: {total_imagenes}")
    print(f"   Emoji fallback: {total_emoji_fallback}")
    print(f"{'='*60}")


def main():
    parser = argparse.ArgumentParser(description="Descargar imágenes de Unsplash con fallback a emoji")
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
