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
REVISADAS_A_MANO: dict[str, set[int]] = {
    "01-basico/pruebas/ciencias-naturales-unidad-ciencias-de-la-vida.md": {5},
    "01-basico/pruebas/historia-unidad-formacion-ciudadana.md": {1, 3},
    "01-basico/examenes/examen-integrado-forma-a.md": {16},
    "01-basico/examenes/examen-integrado-forma-b.md": {14, 16, 18, 19},
    "02-basico/pruebas/historia-unidad-historia.md": {1, 7},
    "02-basico/pruebas/lenguaje-y-comunicacion-unidad-1.md": {5},
    "02-basico/pruebas/lenguaje-y-comunicacion-unidad-2.md": {2, 5},
    "02-basico/examenes/examen-integrado-forma-b.md": {13},
    "03-basico/pruebas/ciencias-naturales-unidad-ciencias-de-la-vida.md": {9},
    "03-basico/pruebas/historia-unidad-historia.md": {8},
    "03-basico/pruebas/matematica-unidad-medicion-datos-probabilidades.md": {6},
    "03-basico/examenes/examen-integrado-forma-a.md": {13},
    "04-basico/pruebas/ciencias-naturales-unidad-ciencias-de-la-vida.md": {3},
    "04-basico/pruebas/ciencias-naturales-unidad-tierra-y-universo.md": {6},
    "04-basico/pruebas/historia-unidad-geografia.md": {6},
    "04-basico/examenes/examen-integrado-forma-b.md": {5},
    "05-basico/pruebas/ciencias-naturales-unidad-ciencias-de-la-vida.md": {4, 10},
    "05-basico/pruebas/ciencias-naturales-unidad-fisicas-y-quimicas.md": {12},
    "05-basico/pruebas/ciencias-naturales-unidad-tierra-y-universo.md": {8},
    "05-basico/pruebas/historia-unidad-formacion-ciudadana.md": {1},
    "05-basico/pruebas/historia-unidad-geografia.md": {5, 10},
    "05-basico/pruebas/historia-unidad-historia.md": {1, 6},
    "05-basico/pruebas/ingles-unidad-1.md": {12},
    "05-basico/pruebas/ingles-unidad-2.md": {5},
    "05-basico/pruebas/lenguaje-y-comunicacion-unidad-2.md": {9},
    "05-basico/pruebas/matematica-unidad-geometria.md": {7},
    "05-basico/pruebas/matematica-unidad-patrones-y-algebra.md": {5},
    "05-basico/examenes/historia-geografia-y-cs-sociales-examen-forma-b.md": {1, 10},
    "05-basico/examenes/ingles-examen-forma-b.md": {2, 9, 20},
    "05-basico/examenes/lenguaje-y-comunicacion-examen-forma-b.md": {9, 10, 13, 20, 23},
    "06-basico/pruebas/ciencias-naturales-unidad-ciencias-de-la-vida.md": {8},
    "06-basico/pruebas/ingles-unidad-1.md": {12},
    "06-basico/pruebas/ingles-unidad-2.md": {5},
    "06-basico/examenes/ciencias-naturales-examen-forma-b.md": {6},
    "06-basico/examenes/ingles-examen-forma-b.md": {6, 19, 20},
    "06-basico/examenes/lenguaje-y-comunicacion-examen-forma-b.md": {6, 19, 22},
    "06-basico/examenes/matematica-examen-forma-b.md": {25},
    "07-basico/examenes/ingles-examen-forma-b.md": {1, 6, 16, 17, 18},
    "07-basico/examenes/lengua-y-literatura-examen-forma-b.md": {4, 11, 12},
    "07-basico/pruebas/ciencias-naturales-unidad-biologia.md": {11},
    "07-basico/pruebas/historia-unidad-geografia.md": {7},
    "07-basico/pruebas/ingles-unidad-1.md": {5, 6},
    "07-basico/pruebas/ingles-unidad-2.md": {5, 6, 14},
    "07-basico/pruebas/lengua-y-literatura-unidad-1.md": {1, 2, 4, 5, 7, 10, 11},
    "07-basico/pruebas/lengua-y-literatura-unidad-2.md": {1, 4, 5, 6, 9, 11},
    "07-basico/pruebas/matematica-unidad-datos-y-probabilidades.md": {5},
    "07-basico/pruebas/matematica-unidad-patrones-y-algebra.md": {13},
    "08-basico/examenes/ciencias-naturales-examen-forma-b.md": {8, 11, 20},
    "08-basico/examenes/ingles-examen-forma-b.md": {4, 6, 17, 18},
    "08-basico/pruebas/ciencias-naturales-unidad-quimica.md": {4},
    "08-basico/pruebas/historia-unidad-formacion-ciudadana.md": {4, 8},
    "08-basico/pruebas/historia-unidad-geografia.md": {5, 9},
    "08-basico/pruebas/historia-unidad-historia.md": {13},
    "08-basico/pruebas/ingles-unidad-1.md": {1, 4, 6, 12},
    "08-basico/pruebas/lengua-y-literatura-unidad-1.md": {1, 12, 15},
    "08-basico/pruebas/lengua-y-literatura-unidad-2.md": {9, 12},
    "08-basico/pruebas/matematica-unidad-datos-y-probabilidades.md": {13},
    "01-medio/examenes/ciencias-naturales-examen-forma-b.md": {9, 13, 23},
    "01-medio/examenes/historia-geografia-y-cs-sociales-examen-forma-b.md": {25},
    "01-medio/examenes/ingles-examen-forma-b.md": {5, 17, 18},
    "01-medio/examenes/lengua-y-literatura-examen-forma-b.md": {17, 21},
    "01-medio/pruebas/ciencias-naturales-unidad-biologia.md": {12, 13},
    "01-medio/pruebas/ciencias-naturales-unidad-fisica.md": {7, 13},
    "01-medio/pruebas/ciencias-naturales-unidad-quimica.md": {1},
    "01-medio/pruebas/historia-unidad-geografia.md": {1, 12, 13},
    "01-medio/pruebas/ingles-unidad-1.md": {5},
    "02-medio/examenes/ciencias-naturales-examen-forma-b.md": {10, 14, 15, 21},
    "02-medio/examenes/historia-geografia-y-cs-sociales-examen-forma-b.md": {24},
    "02-medio/examenes/ingles-examen-forma-b.md": {5, 17, 18},
    "02-medio/examenes/lengua-y-literatura-examen-forma-b.md": {22},
    "02-medio/examenes/matematica-examen-forma-b.md": {10, 13},
    "02-medio/pruebas/ciencias-naturales-unidad-biologia.md": {12},
    "02-medio/pruebas/ciencias-naturales-unidad-quimica.md": {3},
    "02-medio/pruebas/historia-unidad-formacion-ciudadana.md": {9},
    "02-medio/pruebas/historia-unidad-geografia.md": {7},
    "02-medio/pruebas/historia-unidad-historia.md": {2, 9, 12},
    "02-medio/pruebas/ingles-unidad-1.md": {4, 5, 7},
    "02-medio/pruebas/ingles-unidad-2.md": {6, 14},
    "02-medio/pruebas/matematica-unidad-algebra-y-funciones.md": {12},
    "03-medio/examenes/ciencias-para-la-ciudadania-examen-forma-b.md": {25},
    "03-medio/examenes/educacion-ciudadana-examen-forma-b.md": {21},
    "03-medio/examenes/filosofia-examen-forma-b.md": {6, 10, 24},
    "03-medio/examenes/ingles-examen-forma-b.md": {1, 2, 4, 8, 9, 10, 11, 14, 15, 16, 18, 19, 22, 24, 25},
    "03-medio/examenes/lengua-y-literatura-examen-forma-b.md": {24},
    "03-medio/examenes/matematica-examen-forma-b.md": {6},
    "03-medio/pruebas/ciencias-para-la-ciudadania-unidad-bienestar-y-salud.md": {4, 7, 13},
    "03-medio/pruebas/ciencias-para-la-ciudadania-unidad-seguridad-prevencion-autocuidado.md": {4, 10},
    "03-medio/pruebas/educacion-ciudadana-unidad-1.md": {6},
    "03-medio/pruebas/ingles-unidad-1.md": {4, 12},
    "03-medio/pruebas/ingles-unidad-2.md": {4, 6, 7, 9, 14},
    "03-medio/pruebas/matematica-unidad-algebra-y-funciones.md": {10},
    "03-medio/pruebas/matematica-unidad-geometria.md": {14},
    "03-medio/pruebas/matematica-unidad-probabilidad-y-estadistica.md": {8},
    "04-medio/examenes/ciencias-para-la-ciudadania-examen-forma-b.md": {5, 17},
    "04-medio/examenes/ingles-examen-forma-b.md": {4, 11, 17, 22, 23},
    "04-medio/examenes/lengua-y-literatura-examen-forma-b.md": {2, 9, 22, 24, 25},
    "04-medio/examenes/matematica-examen-forma-b.md": {17},
    "04-medio/pruebas/educacion-ciudadana-unidad-democracia-y-desafios.md": {1, 4},
    "04-medio/pruebas/educacion-ciudadana-unidad-medios-y-participacion.md": {11, 14},
    "04-medio/pruebas/ingles-unidad-2.md": {14},
    "04-medio/pruebas/lengua-y-literatura-unidad-2.md": {1, 4},
    "04-medio/pruebas/matematica-unidad-algebra-y-funciones.md": {13},
}


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
