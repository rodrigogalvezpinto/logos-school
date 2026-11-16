"""Control C.4b (2026-11-16): retroalimentaciones de las guías que no explican la respuesta.

La autoevaluación de la guía muestra la retroalimentación después de responder. Muchas eran frases de reflexión
genéricas («Cada fenómeno óptico tiene una explicación física específica.») que no dicen por qué la respuesta es
correcta. Heurística: en preguntas de alternativas o «varias correctas», la retroalimentación no comparte ninguna
raíz de palabra (5 primeras letras de palabras de 4 o más letras) con la respuesta correcta. Es un detector de
candidatas: cada una se revisa a mano (`REVISADAS_A_MANO` para las que sí explican con otras palabras).

Uso: python scripts/retro_guia_pobres.py [curso]   (sale con código 1 si encuentra candidatas)
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parser_contenido import parsear_guia  # noqa: E402

CONTENIDO = Path(__file__).resolve().parents[2] / "contenido"
STOP = set(
    "el la los las un una unos unas de del al a en y o que se su sus por para con como es son lo le les más muy no si "
    "ya esta este estos estas ese esa eso entre sin sobre cuando donde porque pero también hay ser fue tiene tienen "
    "puede pueden cada otro otra otros otras todos todas solo sólo mismo misma".split()
)

# Revisadas a mano: sí explican la respuesta con otras palabras. (archivo relativo a contenido/, inicio del enunciado)
REVISADAS_A_MANO: list[tuple[str, str]] = [
    ("01-basico/ciencias-naturales.md", "¿Qué grupo tiene solo seres vivos?"),
    ("01-basico/ciencias-naturales.md", "Mira estas dos imágenes: una araucaria"),
    ("01-basico/matematica.md", "¿Cuál de estos es un problema de suma cuyo resultado es 10?"),
    ("02-basico/ciencias-naturales.md", "¿Cuáles de estas son actividad física?"),
    ("02-basico/ciencias-naturales.md", "Si dos niños hacen el mismo ejercicio"),
    ("02-basico/ciencias-naturales.md", "¿Por qué algunos animales guardan alimento"),
    ("02-basico/lenguaje-y-comunicacion.md", "¿Cuál de estas oraciones está bien escrita"),
    ("02-basico/lenguaje-y-comunicacion.md", "Quieres invitar a un compañero"),
    ("02-basico/matematica.md", "::balanza::4+7::5+6::"),
    ("03-basico/ciencias-naturales.md", "¿Cuáles de estos son hábitos alimenticios saludables?"),
    ("03-basico/lenguaje-y-comunicacion.md", "Una compañera opina:"),
    ("03-basico/matematica.md", "¿Cuál es el orden de más liviano a más pesado"),
    ("04-basico/ciencias-naturales.md", "Compara un terremoto y una erupción volcánica"),
    ("04-basico/historia-geografia-y-cs-sociales.md", "En Chile existen \"vedas\""),
    ("04-basico/lenguaje-y-comunicacion.md", "¿Por qué Wladimir juntó la leña"),
    ("04-basico/matematica.md", "Si una figura gira 180°"),
    ("05-basico/ciencias-naturales.md", "Evalúa la siguiente dieta"),
    ("05-basico/ciencias-naturales.md", "Además del lavado de manos"),
    ("05-basico/ciencias-naturales.md", "¿Cuáles de estos lugares de Chile son grandes depósitos"),
    ("05-basico/historia-geografia-y-cs-sociales.md", "¿Cuáles de estas fueron formas de relación"),
    ("05-basico/ingles.md", "Read: \"Tomás is short"),
    ("05-basico/ingles.md", "Model: \"My name is"),
    ("05-basico/lenguaje-y-comunicacion.md", "¿Qué descripción del ambiente de un mercado persa"),
    ("05-basico/lenguaje-y-comunicacion.md", "¿Qué diálogo revela un secreto"),
    ("05-basico/matematica.md", "En una fiesta quedó 6/8"),
    ("05-basico/matematica.md", "¿Cuál es la regla de formación de la secuencia 81"),
    ("06-basico/ciencias-naturales.md", "¿Cuáles son los tres elementos que una planta"),
    ("06-basico/ciencias-naturales.md", "¿Cuáles de estas prácticas son hábitos de higiene?"),
    ("06-basico/ciencias-naturales.md", "¿Cuáles de estas fuentes de energía son renovables?"),
    ("06-basico/ciencias-naturales.md", "¿Cuáles de estas son funciones de la atmósfera"),
    ("06-basico/historia-geografia-y-cs-sociales.md", "¿Cuáles de estos procesos explican cómo se conformó"),
    ("06-basico/historia-geografia-y-cs-sociales.md", "¿Qué ocurrió el 11 de septiembre de 1973"),
    ("06-basico/historia-geografia-y-cs-sociales.md", "¿Cuáles de estos elementos son rasgos físicos"),
    ("06-basico/ingles.md", "Model: \"Dear ___"),
    ("06-basico/lenguaje-y-comunicacion.md", "¿Qué sensación transmite la personificación"),
    ("06-basico/lenguaje-y-comunicacion.md", "¿Cuál de estos versos usa una hipérbole"),
    ("06-basico/lenguaje-y-comunicacion.md", "Fragmento: \"Sofía y Valentina"),
    ("06-basico/lenguaje-y-comunicacion.md", "¿Cuál de las siguientes oraciones usa vocabulario variado"),
    ("07-basico/historia-geografia-y-cs-sociales.md", "¿Por qué el ejército romano"),
    ("07-basico/historia-geografia-y-cs-sociales.md", "¿Qué tres tradiciones confluyen"),
    ("07-basico/historia-geografia-y-cs-sociales.md", "Imagina un mapa que muestra las principales civilizaciones"),
    ("07-basico/historia-geografia-y-cs-sociales.md", "Un embalse construido para regar"),
    ("07-basico/ingles.md", "Read: \"Recycling helps"),
    ("07-basico/ingles.md", "Estás escribiendo sobre un tema de Ciencias Naturales"),
    ("07-basico/ingles.md", "What does \"I'm fed up"),
    ("07-basico/ingles.md", "¿Qué oración expresa correctamente causa y efecto?"),
    ("07-basico/lengua-y-literatura.md", "¿Cuál de estos fragmentos corresponde a la voz"),
    ("07-basico/lengua-y-literatura.md", "¿Qué efecto tiene la acción de don Segundo"),
    ("07-basico/lengua-y-literatura.md", "¿Qué situación cotidiana se parece mejor"),
    ("07-basico/lengua-y-literatura.md", "¿Por qué no es adecuado escribir una carta formal"),
    ("07-basico/matematica.md", "¿En qué cuadrante se encuentra el punto C"),
    ("08-basico/ciencias-naturales.md", "¿Qué ocurre con la temperatura de un cuerpo durante un cambio"),
    ("08-basico/historia-geografia-y-cs-sociales.md", "¿Qué principios ilustrados siguen presentes"),
    ("08-basico/ingles.md", "Read: \"Renewable energy"),
    ("08-basico/ingles.md", "Read: \"Wait until"),
    ("08-basico/matematica.md", "Si un estudiante se ubica en el percentil 40"),
    ("08-basico/matematica.md", "¿Cuál de las siguientes es una forma común de manipular"),
    ("08-basico/matematica.md", "Un aviso muestra que las ventas pasaron"),
    ("01-medio/ciencias-naturales.md", "¿Cuál de las siguientes opciones corresponde a un ejemplo de estructuras homólogas?"),
    ("01-medio/ciencias-naturales.md", "\"Escuchar música con audífonos"),
    ("01-medio/ingles.md", "Read: \"In 1969"),
    ("01-medio/ingles.md", "Which option completes \"One global issue"),
    ("01-medio/ingles.md", "¿Qué tipo de información busca \"How many"),
    ("01-medio/ingles.md", "Read: \"Chess was invented"),
    ("01-medio/ingles.md", "Estás escribiendo sobre un texto que leíste acerca de un inventor"),
    ("01-medio/lengua-y-literatura.md", "¿Cuál es el conflicto central de \"El turno de las tres\"?"),
    ("01-medio/matematica.md", "Sin calcular, ¿qué se puede afirmar de (3/2)⁴"),
]


def raices(texto: str) -> set[str]:
    return {w[:5] for w in re.findall(r"[a-záéíóúñü]{4,}", str(texto).lower()) if w not in STOP}


def candidatas(curso: str | None = None):
    for ruta in sorted(CONTENIDO.glob(f"{curso or '*'}/*.md")):
        if ruta.name.startswith("00"):
            continue
        rel = str(ruta.relative_to(CONTENIDO))
        for oa in parsear_guia(ruta.read_text(encoding="utf-8")):
            for i, q in enumerate(oa.preguntas, 1):
                if q.tipo == "verdadero_falso":
                    continue
                clave = q.respuesta_correcta
                if len(raices(clave)) < 3:
                    continue
                if raices(q.retroalimentacion) & raices(clave):
                    continue
                if any(rel == a and q.enunciado.startswith(b) for a, b in REVISADAS_A_MANO):
                    continue
                yield rel, oa, i, q


def main() -> None:
    curso = sys.argv[1] if len(sys.argv) > 1 else None
    total = 0
    for rel, oa, i, q in candidatas(curso):
        total += 1
        print(f"{rel} | {oa.codigo_oficial} #{i} | {q.enunciado[:90]}\n   clave: {q.respuesta_correcta[:110]}\n"
              f"   retro: {q.retroalimentacion[:140]}")
    print(f"{total} candidatas")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
