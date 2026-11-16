"""Lista las preguntas de las pruebas de unidad y de los simulacros que repiten textualmente una
autoevaluación de la guía del mismo curso (tarea 7 de docs/auditorias/COLA-TRABAJO-AUTONOMO.md).

Por qué importa: si la prueba repite la práctica, mide memoria de la respuesta ya vista y no el
aprendizaje. La prueba debe evaluar el mismo OA y la misma dificultad, con otro contexto, otros
números u otro texto.

Uso: python scripts/solapamiento_pruebas_guias.py [carpeta-curso ...]   (por defecto, los 12)
Solo lectura. Compara enunciado y alternativas normalizados: minúsculas, sin puntuación ni marcas de formato.
"""
import re
import sys
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parser_contenido import parsear_guia  # noqa: E402
from parser_prueba_examen import parsear_prueba_o_examen  # noqa: E402

CONTENIDO = Path(__file__).resolve().parents[2] / "contenido"


def normalizar(texto: str) -> str:
    t = unicodedata.normalize("NFKC", texto).lower()
    # La prueba agrega «¿Verdadero o falso?» al enunciado V/F de la guía: es la misma pregunta.
    t = re.sub(r"¿?\s*verdadero o falso\s*\??", " ", t)
    return re.sub(r"\W+", " ", t).strip()


def huella(enunciado: str, opciones) -> str:
    """Enunciado + alternativas: «¿Cuál es la palabra bien escrita para este dibujo?» con otro
    dibujo y otras alternativas es otra pregunta (los marcadores visuales se pierden al normalizar).
    Solo cuenta el último bloque del enunciado: en las pruebas, el parser antepone la lectura
    compartida («Lee el texto… preguntas 1 a 5») y la guía no la trae, así que con la lectura la
    huella nunca coincidía y las copias con estímulo quedaban fuera del control (2026-11-15)."""
    pregunta = enunciado.split("\n\n")[-1]
    return normalizar(pregunta + " | " + " | ".join(sorted(opciones or [])))


def _numeros(texto: str) -> set[str]:
    return {n.rstrip(".,") for n in re.findall(r"\d[\d.,]*", texto)}


# Casi copias revisadas a mano (2026-11-15): misma plantilla de pregunta sobre un texto propio distinto
# del de la guía (otros personajes, otro relato) o sobre otro gráfico; solo comparten distractores genéricos.
REVISADAS_A_MANO = {
    "05-basico/pruebas/lenguaje-y-comunicacion-unidad-1.md": {1, 3, 4},
    "06-basico/pruebas/lenguaje-y-comunicacion-unidad-1.md": {1, 4},
    "06-basico/pruebas/lenguaje-y-comunicacion-unidad-2.md": {1, 4},
    "08-basico/pruebas/lengua-y-literatura-unidad-1.md": {15},
    "02-medio/pruebas/ciencias-naturales-unidad-fisica.md": {1},
    "02-basico/examenes/examen-integrado-forma-b.md": {18},  # pregunta por el invierno; la guía, por el verano
    "01-basico/pruebas/matematica-unidad-medicion-datos-probabilidades.md": {1},  # lápices de otros largos (5 y 9)
    "01-basico/examenes/examen-integrado-forma-b.md": {13},  # lápices 7 y 4, y pregunta cuál es más corto
    "01-basico/pruebas/lenguaje-y-comunicacion-unidad-1.md": {1},  # sílabas de otra palabra ("mesa")
    "02-basico/pruebas/historia-unidad-geografia.md": {3},  # mapa con las letras en otros países
    "02-basico/pruebas/lenguaje-y-comunicacion-unidad-1.md": {4},  # misma regla (c antes de e/i) con otra palabra
    "02-basico/pruebas/matematica-unidad-medicion-datos-probabilidades.md": {5},  # otros datos (6 caras y 4 sellos)
}


def casi_copias(curso: Path, carpeta: str) -> dict[str, list[int]]:
    """Preguntas que no son copia exacta, pero repiten la pregunta de la guía con retoques mínimos:
    enunciado casi igual (≥ 0,93) y, además, 2 o más alternativas iguales o los mismos datos
    numéricos. Si los números difieren, es la misma plantilla con datos nuevos: eso sí es válido."""
    guia = []
    for ruta in curso.glob("*.md"):
        for oa in parsear_guia(ruta.read_text(encoding="utf-8")):
            for q in oa.preguntas:
                guia.append((normalizar(q.enunciado), _numeros(q.enunciado), {normalizar(o) for o in q.opciones or []}))
    exactas = {huella(q.enunciado, q.opciones) for ruta in curso.glob("*.md")
               for oa in parsear_guia(ruta.read_text(encoding="utf-8")) for q in oa.preguntas}
    resultado: dict[str, list[int]] = {}
    for ruta in sorted((curso / carpeta).glob("*.md")):
        for p, _ in parsear_prueba_o_examen(ruta.read_text(encoding="utf-8")):
            if huella(p.enunciado, p.opciones) in exactas or p.numero in REVISADAS_A_MANO.get(str(ruta.relative_to(CONTENIDO)), set()):
                continue
            pregunta = p.enunciado.split("\n\n")[-1]
            e, n, ops = normalizar(pregunta), _numeros(pregunta), {normalizar(o) for o in p.opciones or []}
            for ge, gn, gops in guia:
                if abs(len(e) - len(ge)) > 0.15 * max(len(e), len(ge), 1):
                    continue
                if (n or gn) and n != gn:
                    continue
                if p.tipo == "verdadero_falso":
                    # Una V/F con otra letra, otro nombre u otro dato («la letra T…» frente a «la letra M…»)
                    # es otra afirmación: solo cuenta si usa exactamente las mismas palabras.
                    if set(e.split()) == set(ge.split()):
                        resultado.setdefault(str(ruta.relative_to(CONTENIDO)), []).append(p.numero)
                        break
                    continue
                comunes = len(ops & gops)
                if SequenceMatcher(None, e, ge).ratio() >= 0.93 and (comunes >= 2 or (n and n == gn)):
                    resultado.setdefault(str(ruta.relative_to(CONTENIDO)), []).append(p.numero)
                    break
    return resultado


def _sin_marcadores(texto: str) -> str:
    return re.sub(r"\[imagen[^\]]*\]|::[^:]*::[^:]*::", "", texto, flags=re.I)


def misma_clave(curso: Path, carpeta: str) -> dict[str, list[int]]:
    """Tercer criterio (2026-11-15): la pregunta se parece a una de la guía (≥ 0,6), comparte 3 o más
    alternativas y tiene **la misma respuesta correcta**. Atrapa reformulaciones del enunciado, marcadores
    de imagen agregados y datos reutilizados («según la tabla del Ejemplo 1»). Excluye V/F y REVISADAS_A_MANO."""
    guia = []
    for ruta in curso.glob("*.md"):
        if ruta.name.startswith("00"):
            continue
        for oa in parsear_guia(ruta.read_text(encoding="utf-8")):
            for q in oa.preguntas:
                guia.append((normalizar(_sin_marcadores(q.enunciado)), {normalizar(o) for o in q.opciones or []},
                             normalizar(q.respuesta_correcta)))
    resultado: dict[str, list[int]] = {}
    for ruta in sorted((curso / carpeta).glob("*.md")):
        rel = str(ruta.relative_to(CONTENIDO))
        for p, r in parsear_prueba_o_examen(ruta.read_text(encoding="utf-8")):
            if p.tipo == "verdadero_falso" or p.numero in REVISADAS_A_MANO.get(rel, set()):
                continue
            e = normalizar(_sin_marcadores(p.enunciado.split("\n\n")[-1]))
            ops, clave = {normalizar(o) for o in p.opciones or []}, normalizar(r.respuesta_correcta)
            if any(clave == gk and len(ops & gops) >= 3 and SequenceMatcher(None, e, ge).ratio() >= 0.6
                   for ge, gops, gk in guia):
                resultado.setdefault(rel, []).append(p.numero)
    return resultado


def escenarios_copiados(curso: Path, carpeta: str) -> dict[str, list[int]]:
    """Cuarto criterio (2026-11-15): una oración de situación o con datos (declarativa, o con números), de 50 o más
    caracteres, del enunciado de la pregunta, que aparece tal cual en la guía. Atrapa escenarios reutilizados con
    otras alternativas («Un ciclista va cuesta abajo y, sin pedalear…»). Las preguntas genéricas («¿Cuál es la tesis
    del autor?») no cuentan. Excluye REVISADAS_A_MANO."""
    guia = " ".join(normalizar(r.read_text(encoding="utf-8")) for r in curso.glob("*.md") if not r.name.startswith("00"))
    resultado: dict[str, list[int]] = {}
    for ruta in sorted((curso / carpeta).glob("*.md")):
        rel = str(ruta.relative_to(CONTENIDO))
        for p, _ in parsear_prueba_o_examen(ruta.read_text(encoding="utf-8")):
            if p.numero in REVISADAS_A_MANO.get(rel, set()):
                continue
            for frase in re.split(r"(?<=[.!?»\"])\s+", p.enunciado.split("\n\n")[-1]):
                n = normalizar(frase)
                if len(n) >= 50 and n in guia and ("?" not in frase or re.search(r"\d", frase)):
                    resultado.setdefault(rel, []).append(p.numero)
                    break
    return resultado


def lecturas_copiadas(curso: Path, carpeta: str) -> dict[str, int]:
    """Líneas citadas (`>`) de las lecturas de pruebas o simulacros que están tal cual en la guía.
    Una prueba que reutiliza el texto de la guía mide memoria del texto ya trabajado (2026-11-15)."""
    guia = " ".join(normalizar(r.read_text(encoding="utf-8")) for r in curso.glob("*.md") if not r.name.startswith("00"))
    resultado = {}
    for ruta in sorted((curso / carpeta).glob("*.md")):
        # Umbral bajo (líneas de más de 30 caracteres): las lecturas de 1.° y 2.° básico tienen líneas
        # cortas («Fui a jugar a la plaza con Tomás.»). Se exigen 2 líneas para no marcar frases sueltas.
        # Una sola línea larga (un párrafo completo de 150 o más caracteres) también cuenta.
        lineas = {normalizar(l)[:120]: len(l) for l in ruta.read_text(encoding="utf-8").splitlines()
                  if l.startswith(">") and len(l) > 30}
        coinciden = [largo for k, largo in lineas.items() if len(k) > 22 and k in guia]
        iguales = len(coinciden)
        if iguales >= 2 or any(largo >= 150 for largo in coinciden):
            resultado[str(ruta.relative_to(CONTENIDO))] = iguales
    return resultado


def solapamiento(curso: Path, carpeta: str = "pruebas") -> tuple[int, int, dict[str, list[int]]]:
    guia = {huella(q.enunciado, q.opciones) for ruta in curso.glob("*.md")
            for oa in parsear_guia(ruta.read_text(encoding="utf-8")) for q in oa.preguntas}
    total, repetidas, por_archivo = 0, 0, {}
    for ruta in sorted((curso / carpeta).glob("*.md")):
        numeros = []
        for p, _ in parsear_prueba_o_examen(ruta.read_text(encoding="utf-8")):
            total += 1
            if huella(p.enunciado, p.opciones) in guia:
                numeros.append(p.numero)
        repetidas += len(numeros)
        if numeros:
            por_archivo[str(ruta.relative_to(CONTENIDO))] = numeros
    return repetidas, total, por_archivo


def main() -> None:
    cursos = [CONTENIDO / c for c in sys.argv[1:]] or sorted(p for p in CONTENIDO.iterdir() if p.is_dir() and (p / "pruebas").exists())
    for curso in cursos:
        for carpeta, nombre in (("pruebas", "prueba"), ("examenes", "simulacro")):
            rep, tot, archivos = solapamiento(curso, carpeta)
            print(f"{curso.name}: {rep}/{tot} preguntas de {nombre} repiten la guía ({100 * rep / max(tot, 1):.0f} %)")
            for ruta, nums in archivos.items():
                print(f"  {ruta}: {', '.join(map(str, nums))}")
            for ruta, nums in casi_copias(curso, carpeta).items():
                print(f"  {ruta}: casi copias {', '.join(map(str, nums))}")
            for ruta, nums in escenarios_copiados(curso, carpeta).items():
                print(f"  {ruta}: escenario de la guía repetido {', '.join(map(str, nums))}")
            for ruta, nums in misma_clave(curso, carpeta).items():
                print(f"  {ruta}: misma pregunta y clave {', '.join(map(str, nums))}")
            for ruta, n in lecturas_copiadas(curso, carpeta).items():
                print(f"  {ruta}: {n} líneas de lectura iguales a la guía")


if __name__ == "__main__":
    main()
