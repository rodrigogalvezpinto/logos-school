from pathlib import Path

import rebalancear_claves as R
from parser_prueba_examen import parsear_prueba_o_examen


def _prueba(n):
    preguntas = "\n\n".join(
        f"**{i}. (Alternativas)** Pregunta {i}?\n\na) Uno {i}\nb) Correcta {i}\nc) Tres {i}\nd) Cuatro {i}"
        for i in range(1, n + 1)
    )
    pauta = "\n".join(f"{i}. b) Correcta {i}. La a) es un distractor." for i in range(1, n + 1))
    return f"# Prueba\n\n{preguntas}\n\n## Pauta de respuestas\n\n{pauta}\n"


def test_rebalancea_sin_cambiar_texto_de_clave_y_actualiza_referencias(tmp_path):
    carpeta = tmp_path / "pruebas"
    carpeta.mkdir()
    ruta = carpeta / "x.md"
    ruta.write_text(_prueba(8), encoding="utf-8")
    antes = {p.numero: r.respuesta_correcta for p, r in parsear_prueba_o_examen(ruta.read_text())}
    aplicados, _ = R.procesar(Path(ruta), escribir=True)
    assert aplicados > 0
    texto = ruta.read_text()
    despues = parsear_prueba_o_examen(texto)
    letras = []
    for p, r in despues:
        assert r.respuesta_correcta == antes[p.numero]
        letras.append("abcd"[p.opciones.index(r.respuesta_correcta)])
    assert letras.count("b") <= 2
    # Si «Uno N» (antes a) cambió de lugar, la explicación debe apuntar a su nueva letra.
    for p, r in despues:
        letra_uno = "abcd"[p.opciones.index(f"Uno {p.numero}")]
        assert f"La {letra_uno}) es un distractor" in r.retroalimentacion


def test_no_mueve_opciones_cuyo_orden_importa():
    assert R.RE_ORDEN_IMPORTA.search("Todas las anteriores")
    assert R.RE_ORDEN_IMPORTA.search("a y b son correctas")
