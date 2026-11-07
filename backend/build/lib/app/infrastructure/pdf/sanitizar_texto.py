"""Compartido entre los generadores de PDF (`generador_guia.py`, `generador_certificado.py`)
— la fuente Helvetica core (sin Unicode embebido, a propósito, para no sumar dependencias)
solo soporta latin-1. El contenido real de `contenido/` usa em dash con frecuencia, y los
nombres de alumno que escribe un apoderado pueden traer cualquier cosa — mejor sanitizar
en un solo lugar que repetir la lista de reemplazos en cada generador."""

_REEMPLAZOS_NO_LATIN1 = {
    "—": "-",  # em dash
    "–": "-",  # en dash
    "’": "'",
    "‘": "'",
    "“": '"',
    "”": '"',
    "…": "...",
    "•": "-",
    # Sin estos, el guion se descartaba en silencio en el paso final de "última red de
    # seguridad" — dejaba un espacio doble en vez de la flecha, ej. "vale 7.000" con un
    # hueco justo donde el contenido decía "unidades de mil → vale 7.000".
    "→": "->",
    "←": "<-",
    "↔": "<->",
}


def sanitizar_para_pdf(texto: str) -> str:
    for original, reemplazo in _REEMPLAZOS_NO_LATIN1.items():
        texto = texto.replace(original, reemplazo)
    # Última red de seguridad: cualquier otro carácter fuera de latin-1 (emojis, etc.) se
    # descarta en vez de tumbar la generación del PDF completo.
    return texto.encode("latin-1", errors="ignore").decode("latin-1")
