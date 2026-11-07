"""Lista las preguntas de las pruebas de unidad que repiten textualmente una autoevaluación de la
guía del mismo curso (tarea 7 de docs/auditorias/COLA-TRABAJO-AUTONOMO.md).

Por qué importa: si la prueba repite la práctica, mide memoria de la respuesta ya vista y no el
aprendizaje. La prueba debe evaluar el mismo OA y la misma dificultad, con otro contexto, otros
números u otro texto.

Uso: python scripts/solapamiento_pruebas_guias.py [carpeta-curso ...]   (por defecto, los 12)
Solo lectura. Compara enunciado y alternativas normalizados: minúsculas, sin puntuación ni marcas de formato.
"""
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parser_contenido import parsear_guia  # noqa: E402
from parser_prueba_examen import parsear_prueba_o_examen  # noqa: E402

CONTENIDO = Path(__file__).resolve().parents[2] / "contenido"


def normalizar(texto: str) -> str:
    return re.sub(r"\W+", " ", unicodedata.normalize("NFKC", texto).lower()).strip()


def huella(enunciado: str, opciones) -> str:
    """Enunciado + alternativas: «¿Cuál es la palabra bien escrita para este dibujo?» con otro
    dibujo y otras alternativas es otra pregunta (los marcadores visuales se pierden al normalizar)."""
    return normalizar(enunciado + " | " + " | ".join(sorted(opciones or [])))


def solapamiento(curso: Path) -> tuple[int, int, dict[str, list[int]]]:
    guia = {huella(q.enunciado, q.opciones) for ruta in curso.glob("*.md")
            for oa in parsear_guia(ruta.read_text(encoding="utf-8")) for q in oa.preguntas}
    total, repetidas, por_archivo = 0, 0, {}
    for ruta in sorted((curso / "pruebas").glob("*.md")):
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
        rep, tot, archivos = solapamiento(curso)
        print(f"{curso.name}: {rep}/{tot} preguntas de prueba repiten la guía ({100 * rep / max(tot, 1):.0f} %)")
        for ruta, nums in archivos.items():
            print(f"  {ruta}: {', '.join(map(str, nums))}")


if __name__ == "__main__":
    main()
