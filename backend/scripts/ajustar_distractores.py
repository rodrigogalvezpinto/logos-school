"""Corrige el sesgo de longitud: la opción correcta no debe delatarse por ser la más larga.

Medición de la auditoría 2026-11-06: en el 48 % de las preguntas de alternativas la correcta
era claramente la más larga (más larga que todas y ≥ 1,3 veces el promedio del resto),
cuando por azar no debería superar ~25 %. Este script sirve para revisar y corregir ítem
por ítem, reescribiendo distractores (errores plausibles, de largo comparable) sin tocar la
clave.

  listar <archivo.md>     muestra los ítems sesgados: id, enunciado, opciones con largo,
                          clave y retroalimentación (para no contradecirla).
  aplicar <spec.py>       aplica una spec: ARCHIVO = "..."; CAMBIOS = [D(id, {"a": "texto"})]
                          (id = número en pruebas/simulacros, "OA x#i" en guías).

Al aplicar exige: mismo número de preguntas, mismos tipos y MISMO texto de clave en todas,
y que solo cambien las opciones de los ítems indicados (nunca la correcta).
"""

import importlib.util
import sys
from dataclasses import dataclass
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import rebalancear_claves as R  # noqa: E402
from parser_prueba_examen import parsear_prueba_o_examen  # noqa: E402
from parser_contenido import parsear_guia  # noqa: E402

RAIZ = Path(__file__).resolve().parents[2]


@dataclass
class D:
    id: object
    opciones: dict


def sesgada(opciones, clave) -> bool:
    if not opciones or clave not in opciones:
        return False
    i = opciones.index(clave)
    largos = [len(o) for o in opciones]
    otros = [x for j, x in enumerate(largos) if j != i]
    media = sum(otros) / len(otros)
    # Opciones breves (nombres de figuras, cifras) no delatan la clave por unos caracteres.
    # Si algún distractor alcanza el 90 % del largo de la clave, el largo ya no la delata.
    return (largos[i] > max(otros) / 0.9 and largos[i] >= 1.3 * media and largos[i] - media >= 12)


def items(ruta: Path, texto: str):
    """id -> (tipo, enunciado, opciones, clave, retro)."""
    salida = {}
    if R.es_evaluacion(ruta):
        for p, r in parsear_prueba_o_examen(texto):
            salida[p.numero] = (p.tipo, p.enunciado, p.opciones, r.respuesta_correcta if r else None,
                                r.retroalimentacion if r else "")
    else:
        vistos = {}
        for oa in parsear_guia(texto):
            # Un mismo OA puede aparecer en dos módulos (p. ej. Ciencias para la Ciudadanía):
            # la segunda aparición se identifica como «OA 1@2#i».
            vistos[oa.codigo_oficial] = vistos.get(oa.codigo_oficial, 0) + 1
            sufijo = "" if vistos[oa.codigo_oficial] == 1 else f"@{vistos[oa.codigo_oficial]}"
            for i, q in enumerate(oa.preguntas, 1):
                salida[f"{oa.codigo_oficial}{sufijo}#{i}"] = (q.tipo, q.enunciado, q.opciones, q.respuesta_correcta,
                                                              q.retroalimentacion or "")
    return salida


def bloque_de(ruta: Path, texto: str, ident):
    if R.es_evaluacion(ruta):
        ini, fin = R.bloques_prueba(texto)[ident]
        return ini, fin, None
    oa, i = ident.split("#")
    oa, _, aparicion = oa.partition("@")
    grupo = int(aparicion or 1) - 1
    bloques = sorted(v for k, v in R.bloques_guia(texto).items() if k[0] == oa and k[1] // 1000 == grupo)
    ini, fin = bloques[int(i) - 1]
    m = R.RE_RESPUESTA_GUIA.search(texto, ini, fin)
    return ini, fin, (m.start() if m else None)


def listar(ruta: Path) -> None:
    texto = ruta.read_text(encoding="utf-8")
    n = 0
    for ident, (tipo, enun, ops, clave, retro) in items(ruta, texto).items():
        if tipo != "alternativas" or not sesgada(ops, clave):
            continue
        n += 1
        print(f"=== {ident!r}")
        print("  Q:", " ".join(enun.split())[-300:])
        for j, o in enumerate(ops):
            print(f"  {'*' if o == clave else ' '}{R.LETRAS[j]}) [{len(o)}] {o}")
        print("  R:", " ".join((retro or "").split())[:260])
    print(f"# {n} ítems sesgados en {ruta}")


def aplicar_en(ruta: Path, cambios: list, estricto: bool = True):
    """Aplica [D(id, {letra: texto})] a un archivo y verifica. Devuelve (ok, reemplazos) donde
    reemplazos = [(clave, opciones_originales, {texto_viejo: texto_nuevo})] para propagar."""
    original = ruta.read_text(encoding="utf-8")
    texto = original
    antes = items(ruta, original)
    reemplazos = []
    for c in cambios:
        ini, fin, ini_resp = bloque_de(ruta, texto, c.id)
        bloque = texto[ini:fin]
        corte = (ini_resp - ini) if ini_resp is not None else len(bloque)
        if ini_resp is not None:
            corte = bloque.rfind("\n", 0, corte) + 1
        ext = R.extensiones_opciones(bloque, corte)
        tipo, _, ops, clave, _ = antes[c.id]
        letra_clave = R.LETRAS[ops.index(clave)]
        mapa = {}
        for letra, nuevo in sorted(c.opciones.items(), key=lambda kv: -ext[kv[0]][0]):
            if letra == letra_clave:
                raise SystemExit(f"{c.id}: no se reescribe la clave ({letra})")
            a, b = ext[letra]
            mapa[ops[R.LETRAS.index(letra)]] = " ".join(nuevo.split())
            bloque = bloque[:a] + nuevo.strip() + bloque[b:]
        texto = texto[:ini] + bloque + texto[fin:]
        reemplazos.append((clave, tuple(sorted(ops)), mapa))
    despues = items(ruta, texto)
    errores = []
    if list(antes) != list(despues):
        errores.append("cambió la lista de preguntas")
    ids = {c.id for c in cambios}
    for ident in antes:
        ta, ea, oa_, ca, _ = antes[ident]
        td, ed, od, cd, _ = despues.get(ident, (None,) * 5)
        if (ta, ca) != (td, cd):
            errores.append(f"{ident}: cambió tipo o clave")
        if ident not in ids and oa_ != od:
            errores.append(f"{ident}: cambiaron opciones no indicadas")
        if od and len(set(od)) != len(od):
            errores.append(f"{ident}: opciones repetidas")
    if errores:
        print("\n".join(errores))
        if estricto:
            raise SystemExit(f"{ruta}: NO se escribió")
        return False, []
    ruta.write_text(texto, encoding="utf-8")
    quedan = sum(1 for t, _, o, k, _ in despues.values() if t == "alternativas" and sesgada(o, k))
    print(f"OK {ruta.relative_to(RAIZ)}: {len(cambios)} ítems ajustados; quedan {quedan} sesgados")
    return True, reemplazos


def propagar(origen: Path, reemplazos) -> None:
    """Aplica los mismos reemplazos de distractores a los ítems gemelos (misma clave y mismo
    conjunto de opciones) de otros archivos: guía ↔ prueba ↔ simulacro."""
    if not reemplazos:
        return
    firmas = {(clave, ops): mapa for clave, ops, mapa in reemplazos}
    for ruta in sorted((RAIZ / "contenido").rglob("*.md")):
        if ruta.name.startswith("00-") or ruta == origen:
            continue
        texto = ruta.read_text(encoding="utf-8")
        if not any(clave in texto for clave, _ in firmas):
            continue
        cambios = []
        for ident, (tipo, _, ops, clave, _) in items(ruta, texto).items():
            if tipo != "alternativas" or not ops or clave not in ops:
                continue
            mapa = firmas.get((clave, tuple(sorted(ops))))
            if mapa:
                cambios.append(D(ident, {R.LETRAS[ops.index(v)]: n for v, n in mapa.items()}))
        if cambios:
            try:
                aplicar_en(ruta, cambios, estricto=False)
            except (KeyError, ValueError, IndexError) as error:
                print(f"  (gemelo omitido en {ruta.relative_to(RAIZ)}: formato no localizable, {error!r})")


def aplicar(ruta_spec: Path) -> None:
    espacio = {"D": D}
    exec(compile(ruta_spec.read_text(encoding="utf-8"), str(ruta_spec), "exec"), espacio)
    ruta = RAIZ / espacio["ARCHIVO"]
    ok, reemplazos = aplicar_en(ruta, espacio["CAMBIOS"])
    if ok and espacio.get("PROPAGAR", True):
        propagar(ruta, reemplazos)


if __name__ == "__main__":
    modo, ruta = sys.argv[1], Path(sys.argv[2])
    {"listar": listar, "aplicar": aplicar}[modo](ruta)
