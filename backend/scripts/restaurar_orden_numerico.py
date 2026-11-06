"""Restaura el orden ascendente/descendente de opciones numéricas que `rebalancear_claves.py`
desordenó con un intercambio (p. ej. «A las 5 / A las 7 / A las 6»). Las opciones numéricas
se presentan ordenadas por convención; deshace solo ese intercambio, con la misma verificación.

Uso: python backend/scripts/restaurar_orden_numerico.py [--escribir] <archivos.md...>
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import rebalancear_claves as R  # noqa: E402

RE_NUM = re.compile(r"-?\d+(?:[.,]\d+)?")


def valor(opcion: str):
    m = RE_NUM.search(opcion.replace(".", "").replace(",", ".") if re.search(r"\d\.\d{3}", opcion) else opcion.replace(",", "."))
    return float(m.group()) if m else None


def un_solo_valor(opcion: str) -> bool:
    """Opción breve con un único número («A las 5», «x = 9», «$2.000»): su orden es convencional."""
    normal = re.sub(r"(?<=\d)\.(?=\d{3}\b)", "", opcion)
    return len(opcion) <= 30 and len(RE_NUM.findall(normal)) == 1


def par_a_intercambiar(opciones: list[str]):
    if not all(un_solo_valor(o) for o in opciones):
        return None
    vals = [valor(o) for o in opciones]
    if len(opciones) < 3 or any(v is None for v in vals) or len(set(vals)) != len(vals):
        return None
    if vals in (sorted(vals), sorted(vals, reverse=True)):
        return None
    for orden in (sorted(vals), sorted(vals, reverse=True)):
        malos = [i for i, (a, b) in enumerate(zip(vals, orden)) if a != b]
        if len(malos) == 2:
            return malos
    return None


def main():
    escribir = "--escribir" in sys.argv
    total = 0
    for ruta in [Path(a) for a in sys.argv[1:] if a != "--escribir"]:
        texto = ruta.read_text(encoding="utf-8")
        referencia = R.huella(ruta, texto)
        hechos = 0
        for clave, tipo, opciones, _ in R.preguntas_parseadas(ruta, texto):
            if tipo != "alternativas" or not opciones:
                continue
            par = par_a_intercambiar(opciones)
            if not par:
                continue
            k, t = R.LETRAS[par[0]], R.LETRAS[par[1]]
            if R.es_evaluacion(ruta):
                ini, fin = R.bloques_prueba(texto)[clave]
                ini_resp = None
            else:
                oa, i = clave.split("#")
                # localizar el bloque i-ésimo del OA
                bloques = sorted((v for kk, v in R.bloques_guia(texto).items() if kk[0] == oa))
                if int(i) - 1 >= len(bloques):
                    continue
                ini, fin = bloques[int(i) - 1]
                m = R.RE_RESPUESTA_GUIA.search(texto, ini, fin)
                ini_resp = m.start() if m else None
            nuevo = R.aplicar_intercambio(texto, ini, fin, k, t, ini_resp)
            if nuevo is None:
                continue
            if R.es_evaluacion(ruta):
                for a, b in sorted(R.regiones_pauta(nuevo, clave), reverse=True):
                    nuevo = nuevo[:a] + R.intercambiar_letras(nuevo[a:b], k, t) + nuevo[b:]
            try:
                ok = R.huella(ruta, nuevo) == referencia
                ok = ok and par_a_intercambiar(dict((c, o) for c, _, o, _ in R.preguntas_parseadas(ruta, nuevo))[clave]) is None
            except Exception:  # noqa: BLE001
                ok = False
            if ok:
                texto, hechos = nuevo, hechos + 1
            else:
                print(f"  no restaurado: {ruta} {clave} {opciones}")
        if hechos:
            print(f"{ruta}: {hechos} restauradas")
            total += hechos
            if escribir:
                ruta.write_text(texto, encoding="utf-8")
    print("Total", total)


if __name__ == "__main__":
    main()
