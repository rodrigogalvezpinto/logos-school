"""Control C.4c (2026-11-16): explicaciones de pruebas y simulacros que no explican la clave.

C.4 (`explicaciones_pobres.py`) detecta las explicaciones que solo repiten la clave. Este control busca las genéricas:
quitado el «x) clave.» inicial y el texto de la clave, la explicación no comparte ninguna raíz de palabra (5 primeras
letras) con la clave. Es un detector de candidatas: las que sí explican con otras palabras se registran en
`REVISADAS_A_MANO`; las demás se reescriben con `rehacer(archivo, n, None, None, texto, solo_explicacion=True)`.

Uso: python scripts/explicaciones_genericas.py [curso]   (sale con código 1 si encuentra candidatas)
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parser_prueba_examen import parsear_prueba_o_examen  # noqa: E402
from retro_guia_pobres import raices  # noqa: E402

CONTENIDO = Path(__file__).resolve().parents[2] / "contenido"

# Revisadas a mano: sí explican la clave con otras palabras. archivo relativo a contenido/ -> números de pregunta.
REVISADAS_A_MANO: dict[str, set[int]] = {}


def texto_clave(respuesta: str) -> str:
    if respuesta.startswith("["):
        try:
            return " ".join(json.loads(respuesta))
        except ValueError:
            return respuesta
    return respuesta


def sin_prefijo(explicacion: str, clave: str) -> str:
    e = re.sub(r"^\s*\**\(?[a-h](?:, [a-h])*(?: y [a-h])?[).]\s*", "", explicacion)
    return e.replace(clave, "")


def candidatas(curso: str | None = None):
    for carpeta in ("pruebas", "examenes"):
        for ruta in sorted(CONTENIDO.glob(f"{curso or '*'}/{carpeta}/*.md")):
            rel = str(ruta.relative_to(CONTENIDO))
            for p, r in parsear_prueba_o_examen(ruta.read_text(encoding="utf-8")):
                if p.tipo == "verdadero_falso" or p.numero in REVISADAS_A_MANO.get(rel, set()):
                    continue
                clave = texto_clave(r.respuesta_correcta)
                if len(raices(clave)) < 3:
                    continue
                if raices(sin_prefijo(r.retroalimentacion, clave)) & raices(clave):
                    continue
                yield rel, p, r


def main() -> None:
    curso = sys.argv[1] if len(sys.argv) > 1 else None
    total = 0
    for rel, p, r in candidatas(curso):
        total += 1
        print(f"{rel} #{p.numero} | {p.enunciado.split(chr(10) * 2)[-1][:90]}\n   clave: {r.respuesta_correcta[:110]}\n"
              f"   expl.: {r.retroalimentacion[:160]}")
    print(f"{total} candidatas")
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
