"""Las etiquetas de formato de pregunta («— *Alternativas*», «*(Varias correctas)*») no deben
llegar al enunciado que ve el alumno (hallazgo 2026-11-07: 48 enunciados de Historia 5°B–2°M
empezaban con «— Alternativas»), pero sí deben seguir determinando el tipo."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from parser_prueba_examen import RE_ETIQUETA_TIPO  # noqa: E402


def _limpia(texto: str) -> str:
    return " ".join(RE_ETIQUETA_TIPO.sub(" ", texto).split())


def test_quita_etiqueta_inicial_con_guion():
    assert _limpia("— Alternativas ¿Por qué se dice?") == "¿Por qué se dice?"


def test_quita_etiqueta_entre_parentesis_tras_imagen():
    assert _limpia("[Imagen: una mochila] (Varias correctas) ¿Qué materiales?") == "[Imagen: una mochila] ¿Qué materiales?"


def test_no_toca_la_instruccion_ni_el_contenido():
    instruccion = "(Varias correctas: marca todas las alternativas correctas.) ¿Cuáles?"
    assert _limpia(instruccion) == instruccion
    assert _limpia("Elige entre las alternativas correctas.") == "Elige entre las alternativas correctas."
