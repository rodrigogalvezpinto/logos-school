"""Herramienta de la conversión de preguntas abiertas a alternativas (decisión 2026-11-06).

Dos modos:

  listar <archivo.md>       muestra cada pregunta abierta con el bloque exacto que se
                            reemplazaría (y su entrada de pauta en pruebas/simulacros).
  aplicar <spec.py>         aplica una especificación y valida el archivo resultante.

La especificación es un módulo Python con:

  ARCHIVO = "contenido/05-basico/matematica.md"
  CAMBIOS = [
      # Guía: bloque completo de la pregunta N del OA indicado (desde la etiqueta
      # "**Pregunta N (...)**" hasta antes de la pregunta siguiente / encabezado / ---).
      G("OA 3", 3, '''**Pregunta 3 (Alternativas).** ...'''),
      # Prueba o simulacro: sustituciones dentro del bloque de la pregunta N y nueva
      # entrada de pauta (texto tras "N." en la lista, o celda clave de la tabla).
      P(5, subs=[("viejo", "nuevo")], pauta="b. Explicación..."),
      P(6, bloque='''**6.** *(Alternativas)* ...''', pauta="..."),
  ]
  GLOBAL = [("texto viejo único", "texto nuevo")]   # opcional (instrucciones, tablas)

Cada sustitución exige que el texto viejo aparezca exactamente una vez en su ámbito. Tras
aplicar, se exige: mismo número de preguntas, claves dentro de las opciones, `varias_correctas`
con 2+ claves sin marcar todas, y se informa cuántas abiertas quedan y la distribución de letras
correctas (para evitar sesgos de posición).
"""

import collections
import importlib.util
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from parser_contenido import RE_Q_START as RE_Q_GUIA  # noqa: E402
from parser_contenido import _parsear_bloque_preguntas, parsear_guia  # noqa: E402
from parser_prueba_examen import (  # noqa: E402
    RE_PAUTA_ENTRADA,
    RE_PAUTA_HEADING,
    RE_PAUTA_LIMITE,
    RE_Q_START,
    RE_TABLA_FILA,
    _celdas_tabla,
    parsear_prueba_o_examen,
)

RAIZ = Path(__file__).resolve().parents[2]
RE_OA = re.compile(r"^(##|###)\s+OA\s*(?:N?°?\s*(\d+)|\(([^)]+)\))", re.IGNORECASE | re.MULTILINE)
RE_CORTE = re.compile(r"(?m)^(?:#{1,6}\s|\s*-{3,}\s*$)")
RE_DECLARACION = re.compile(
    r"(?mi)^(?:#{1,6}[ \t]+)?\*{0,2}\(?[ \t]*(?:Lee|Lea|Observa|Utiliza|Usa|Textos?\s+\d+)\b[^\n]*\bpreguntas?\s+\d[^\n]*$"
)


def inicio_real(texto: str, m: re.Match) -> int:
    """RE_Q_START empieza con ^\\s*, que puede tragarse líneas en blanco previas: el
    bloque debe empezar en la línea de la etiqueta, conservando la separación anterior."""
    previo = texto[m.start():m.end()]
    salto = previo.rfind("\n", 0, len(previo) - len(previo.lstrip()))
    return m.start() + salto + 1 if salto >= 0 else m.start()


_CONTADOR_POSICION = [0]


def B(opciones: list[str], indice_correcta: int) -> tuple[list[str], str]:
    """Reubica la opción correcta en una posición rotativa (evita sesgo de posición de la
    clave) y conserva el orden relativo de los distractores. Devuelve (opciones, letra)."""
    n = len(opciones)
    ciclo = {2: [1, 0], 3: [2, 0, 1], 4: [2, 0, 3, 1], 5: [2, 0, 4, 1, 3]}[n]
    _CONTADOR_POSICION.append(n)
    destino = ciclo[_CONTADOR_POSICION.count(n) % len(ciclo)]
    correcta = opciones[indice_correcta]
    resto = [o for i, o in enumerate(opciones) if i != indice_correcta]
    nuevas = resto[:destino] + [correcta] + resto[destino:]
    return nuevas, "abcde"[destino]


def VF(n, subs=None):
    """V/F sin etiqueta que se importaba como abierta: añade opciones explícitas."""
    return P(n, subs=list(subs or []), agregar="a) Verdadero\nb) Falso")


def normalizar_tabla_cerradas(texto: str) -> str:
    """Tablas de especificaciones «| Preguntas | Cerradas | Desarrollo |»: al no quedar
    preguntas abiertas, cada fila declara como cerradas todas las preguntas listadas y 0 de
    desarrollo; la fila Total suma las filas."""
    lineas = texto.split("\n")
    salida, en_tabla, total = [], False, 0
    for linea in lineas:
        celdas = [c.strip() for c in linea.strip().strip("|").split("|")] if linea.strip().startswith("|") else None
        if celdas and len(celdas) >= 4 and celdas[-2:] == ["Cerradas", "Desarrollo"]:
            en_tabla, total = True, 0
            salida.append(linea)
            continue
        if en_tabla and celdas is None:
            en_tabla = False
        if en_tabla and celdas and not set(celdas[0]) <= set("-: "):
            if "total" in celdas[0].lower():
                celdas[-2:] = [f"**{total}**", "**0**"]
            else:
                n = len(re.findall(r"\d+", celdas[-3]))
                total += n
                celdas[-2:] = [str(n), "0"]
            linea = "| " + " | ".join(celdas) + " |"
        salida.append(linea)
    return "\n".join(salida)


NOMBRE_TIPO = {"alternativas": "Alternativas", "varias_correctas": "Varias correctas", "verdadero_falso": "Verdadero o falso"}
NOTA_RUBRICAS = ("> **Nota (2026-11-06):** todas las preguntas de este instrumento son de alternativas. "
                 "Las rúbricas de la versión de desarrollo se conservan en el historial del repositorio "
                 "(commit `e6336af`) y en `docs/banco-preguntas-abiertas/`, para reactivarlas cuando exista "
                 "un corrector validado.\n")


def normalizar_tipo_en_pauta(texto: str, tipos: dict[int, str]) -> str:
    """Columna «Tipo» de las tablas de pauta: reemplaza «Desarrollo…/Respuesta abierta» por el
    tipo real de la pregunta convertida."""
    def cambiar(m):
        numero = int(m.group(1))
        return f"| {numero} | {NOMBRE_TIPO.get(tipos.get(numero), m.group(2))} |"
    return re.sub(r"(?m)^\|\s*(\d+)\s*\|\s*((?:Desarrollo|Respuesta abierta|Pregunta abierta|Abierta)[^|]*?)\s*\|",
                  cambiar, texto)


def quitar_rubricas_desarrollo(texto: str) -> str:
    """Secciones «Rúbricas de las preguntas de desarrollo»: dejan de aplicar; se reemplazan por
    una nota que indica dónde se conservan."""
    lineas = texto.split("\n")
    salida, saltando, nivel = [], False, 0
    for linea in lineas:
        enc = re.match(r"^(#{1,6})\s+(.*)$", linea)
        if enc and re.search(r"r[úu]bricas?\b.*desarrollo|desarrollo.*r[úu]bricas?", enc.group(2), re.IGNORECASE):
            saltando, nivel = True, len(enc.group(1))
            salida.append(linea)
            salida.append("")
            salida.append(NOTA_RUBRICAS)
            continue
        if saltando and enc and len(enc.group(1)) <= nivel:
            saltando = False
        if saltando and linea.strip() == "---":
            saltando = False
        if not saltando:
            salida.append(linea)
    return "\n".join(salida)


@dataclass
class G:
    oa: str
    n: int
    bloque: str


@dataclass
class P:
    n: int
    subs: list = field(default_factory=list)
    bloque: str | None = None
    pauta: str | None = None
    tabla: str | None = None  # celda clave nueva si la pauta es tabla
    agregar: str | None = None  # texto (p. ej. opciones) que se añade al final del bloque
    pauta_tabla: str | None = None  # variante con la clave en negrita, si la pauta es tabla


def ALT(n, opciones, correcta, explicacion="", subs=None, balancear=True, sep=". "):
    """Pregunta de prueba/simulacro convertida: añade opciones al final del bloque y arma
    la pauta. `correcta` es un índice (alternativas) o una lista de índices (varias)."""
    letras = "abcde"
    if isinstance(correcta, int):
        if balancear:
            opciones, letra = B(list(opciones), correcta)
        else:
            letra = letras[correcta]
        texto = opciones[letras.index(letra)]
        pauta = f"{letra}) {texto.rstrip('.')}" + (f"{sep}{explicacion}" if explicacion else "")
        tabla = f"**{letra}) {texto.rstrip('.')}.**" + (f" {explicacion}" if explicacion else "")
        cabecera = ""
    else:
        marcadas = [letras[i] for i in sorted(correcta)]
        clave = ", ".join(marcadas[:-1]) + " y " + marcadas[-1]
        pauta = f"{clave} — {explicacion}"
        tabla = f"**{clave}.** {explicacion}"
        cabecera = "*(Varias correctas: marca todas las alternativas correctas.)*\n\n"
    lineas = "\n".join(f"{letras[i]}) {o}" for i, o in enumerate(opciones))
    return P(n, subs=list(subs or []), agregar=cabecera + lineas, pauta=pauta, pauta_tabla=tabla)


def es_evaluacion(ruta: Path) -> bool:
    return ruta.parent.name in ("pruebas", "examenes")


# ---------------------------------------------------------------- guías

def bloques_guia(texto: str) -> dict[tuple[str, int], tuple[int, int]]:
    """(código OA, número de pregunta) -> (inicio, fin) del bloque en el texto."""
    oas = [(m.start(), f"OA {m.group(2)}" if m.group(2) else f"OA ({m.group(3).strip()})")
           for m in RE_OA.finditer(texto)]
    resultado = {}
    preguntas = list(RE_Q_GUIA.finditer(texto))
    for i, m in enumerate(preguntas):
        oa = next((c for pos, c in reversed(oas) if pos < m.start()), None)
        if oa is None:
            continue
        fin = preguntas[i + 1].start() if i + 1 < len(preguntas) else len(texto)
        corte = RE_CORTE.search(texto, m.end(), fin)
        fin = corte.start() if corte else fin
        clave = (oa, int(m.group(1)))
        if clave in resultado:
            clave = (oa, int(m.group(1)) + 1000 * sum(1 for k in resultado if k[0] == oa and k[1] % 1000 == int(m.group(1))))
        resultado[clave] = (inicio_real(texto, m), fin)
    return resultado


# ---------------------------------------------------------------- pruebas / simulacros

def partir(texto: str) -> int:
    lineas = texto.splitlines(keepends=True)
    acumulado = 0
    for linea in lineas:
        if RE_PAUTA_HEADING.match(linea.rstrip("\n")):
            return acumulado
        acumulado += len(linea)
    return len(texto)


def bloques_prueba(texto: str) -> dict[int, tuple[int, int]]:
    corte_pauta = partir(texto)
    preguntas = [m for m in RE_Q_START.finditer(texto) if m.start() < corte_pauta]
    resultado = {}
    for i, m in enumerate(preguntas):
        fin = preguntas[i + 1].start() if i + 1 < len(preguntas) else corte_pauta
        for patron in (RE_CORTE, RE_DECLARACION):
            corte = patron.search(texto, m.end(), fin)
            if corte:
                fin = min(fin, corte.start())
        resultado.setdefault(int(m.group(1)), (inicio_real(texto, m), fin))
    return resultado


def entradas_pauta(texto: str) -> dict[int, tuple[str, int, int]]:
    """número -> ('lista', ini, fin) del cuerpo tras el número, o ('tabla', ini, fin) de la celda clave."""
    inicio_pauta = partir(texto)
    pauta = texto[inicio_pauta:]
    resultado: dict[int, tuple[str, int, int]] = {}
    entradas = list(RE_PAUTA_ENTRADA.finditer(pauta))
    for i, m in enumerate(entradas):
        fin = entradas[i + 1].start() if i + 1 < len(entradas) else len(pauta)
        limite = RE_PAUTA_LIMITE.search(pauta, m.end(), fin)
        fin = limite.start() if limite else fin
        cuerpo = pauta[m.end():fin].rstrip()
        resultado.setdefault(int(m.group(1)), ("lista", inicio_pauta + m.end(), inicio_pauta + m.end() + len(cuerpo)))
    # Tablas: celda de la columna "clave"/"respuesta" (sobrescribe la lista: el parser
    # da prioridad a la tabla).
    pos = 0
    idx_clave = None
    for linea in pauta.splitlines(keepends=True):
        limpia = linea.strip()
        if not limpia.startswith("|"):
            idx_clave = None
        elif idx_clave is None and not RE_TABLA_FILA.match(limpia):
            celdas = [c.lower() for c in _celdas_tabla(limpia)[1:-1]]
            idx_clave = next((i for i, c in enumerate(celdas) if "clave" in c or "respuesta" in c), -1)
        elif idx_clave is not None and idx_clave > 0 and RE_TABLA_FILA.match(limpia):
            numero = int(RE_TABLA_FILA.match(limpia).group(1))
            # localizar la celda idx_clave dentro de la línea original
            separadores = [j for j, c in enumerate(linea) if c == "|" and (j == 0 or linea[j - 1] != "\\")]
            if len(separadores) > idx_clave + 1:
                ini, fin = separadores[idx_clave] + 1, separadores[idx_clave + 1]
                resultado[numero] = ("tabla", inicio_pauta + pos + ini, inicio_pauta + pos + fin)
        pos += len(linea)
    return resultado


# ---------------------------------------------------------------- listar

def preguntas_parseadas(ruta: Path, texto: str):
    if es_evaluacion(ruta):
        return [(p.numero, p.tipo, p.opciones, pauta.respuesta_correcta if pauta else None)
                for p, pauta in parsear_prueba_o_examen(texto)]
    return [(f"{oa.codigo_oficial}#{i}", q.tipo, q.opciones, q.respuesta_correcta)
            for oa in parsear_guia(texto) for i, q in enumerate(oa.preguntas, 1)]


def listar(ruta: Path) -> None:
    texto = ruta.read_text(encoding="utf-8")
    if es_evaluacion(ruta):
        tipos = {p.numero: p.tipo for p, _ in parsear_prueba_o_examen(texto)}
        bloques, pautas = bloques_prueba(texto), entradas_pauta(texto)
        abiertas = [n for n, t in tipos.items() if t == "desarrollo_breve"]
        print(f"# {ruta} — {len(abiertas)} abiertas de {len(tipos)}: {abiertas}")
        for n in abiertas:
            ini, fin = bloques[n]
            print(f"\n===== P({n}) bloque =====\n{texto[ini:fin].rstrip()}")
            if n in pautas:
                clase, a, b = pautas[n]
                print(f"----- pauta [{clase}] -----\n{texto[a:b].strip()}")
            else:
                print("----- pauta: NO LOCALIZADA -----")
    else:
        bloques = bloques_guia(texto)
        total = sum(len(o.preguntas) for o in parsear_guia(texto))
        abiertas = 0
        salida = []
        for clave, (ini, fin) in bloques.items():
            parseadas = _parsear_bloque_preguntas(texto[ini:fin])
            if not parseadas or parseadas[0].tipo != "desarrollo_breve":
                continue
            abiertas += 1
            salida.append(f"\n===== G({clave[0]!r}, {clave[1]}) =====\n{texto[ini:fin].rstrip()}")
        print(f"# {ruta} — {abiertas} abiertas de {total} (bloques localizados: {len(bloques)})")
        print("\n".join(salida))


# ---------------------------------------------------------------- aplicar

def sustituir_unico(texto: str, viejo: str, nuevo: str, ambito: str) -> str:
    cuenta = texto.count(viejo)
    if cuenta == 1:
        return texto.replace(viejo, nuevo)
    # Tolerar saltos de línea/espacios distintos (el Markdown original corta líneas a ~90 col).
    patron = r"\s+".join(re.escape(parte) for parte in viejo.split())
    coincidencias = list(re.finditer(patron, texto))
    if len(coincidencias) != 1:
        raise SystemExit(f"[{ambito}] el texto viejo aparece {cuenta} veces (flexible: {len(coincidencias)}): {viejo[:120]!r}")
    m = coincidencias[0]
    return texto[:m.start()] + nuevo + texto[m.end():]


def aplicar(ruta_spec: Path) -> None:
    spec_mod = importlib.util.spec_from_file_location("spec_conversion", ruta_spec)
    modulo = importlib.util.module_from_spec(spec_mod)
    modulo.G, modulo.P = G, P
    sys.modules["spec_conversion"] = modulo
    codigo = ruta_spec.read_text(encoding="utf-8")
    espacio = {**modulo.__dict__, "G": G, "P": P, "B": B, "ALT": ALT, "VF": VF}
    exec(compile(codigo, str(ruta_spec), "exec"), espacio)
    modulo.__dict__.update(espacio)
    ruta = RAIZ / modulo.ARCHIVO
    original = ruta.read_text(encoding="utf-8")
    texto = original
    antes = preguntas_parseadas(ruta, original)

    for viejo, nuevo in getattr(modulo, "GLOBAL", []):
        texto = sustituir_unico(texto, viejo, nuevo, "GLOBAL")

    cambios = list(modulo.CAMBIOS)
    if es_evaluacion(ruta):
        # Primero la pauta (está al final), luego los bloques de abajo hacia arriba, para no
        # invalidar posiciones.
        for c in cambios:
            if c.pauta is None and c.tabla is not None:
                c.pauta = c.tabla
        for c in sorted(cambios, key=lambda c: -c.n):
            entradas = entradas_pauta(texto)
            if c.pauta is not None:
                if c.n not in entradas:
                    raise SystemExit(f"P({c.n}): entrada de pauta no localizada")
                clase, a, b = entradas[c.n]
                if clase == "tabla" and c.pauta_tabla:
                    c.pauta = c.pauta_tabla
                nuevo = c.pauta if clase == "lista" else f" {c.pauta.strip()} "
                if clase == "lista" and c.pauta_tabla and c.pauta_tabla.startswith("**"):
                    # Pautas «**N. clave.** explicación»: la negrita abierta antes del cuerpo
                    # debe cerrarse tras la clave.
                    inicio_linea = texto.rfind("\n", 0, a) + 1
                    if texto[inicio_linea:a].count("**") % 2 == 1:
                        nuevo = c.pauta_tabla[2:]
                if clase == "lista":
                    texto = texto[:a].rstrip(" \t") + " " + nuevo.strip() + texto[b:]
                else:
                    texto = texto[:a] + nuevo + texto[b:]
        for c in sorted(cambios, key=lambda c: -c.n):
            ini, fin = bloques_prueba(texto)[c.n]
            bloque = texto[ini:fin]
            if c.bloque is not None:
                bloque_nuevo = c.bloque.strip("\n") + (bloque[len(bloque.rstrip()):] or "\n\n")
            else:
                bloque_nuevo = bloque
                for viejo, nuevo in c.subs:
                    bloque_nuevo = sustituir_unico(bloque_nuevo, viejo, nuevo, f"P({c.n})")
                if c.agregar:
                    # Las líneas de respuesta en blanco («_____») eran espacio para escribir.
                    bloque_nuevo = re.sub(r"(?m)^[ \t]*_{5,}[ \t]*\n?", "", bloque_nuevo)
                    bloque_nuevo = re.sub(r"```[ \t]*\n(?:[ \t]*\n)*[ \t]*```[ \t]*\n?", "", bloque_nuevo)
                    bloque_nuevo = re.sub(r"\n{3,}", "\n\n", bloque_nuevo)
                    cola = bloque_nuevo[len(bloque_nuevo.rstrip()):] or "\n\n"
                    bloque_nuevo = bloque_nuevo.rstrip() + "\n\n" + c.agregar.strip("\n") + cola
            texto = texto[:ini] + bloque_nuevo + texto[fin:]
    else:
        posiciones = bloques_guia(texto)
        for c in sorted(cambios, key=lambda c: -posiciones[(c.oa, c.n)][0]):
            ini, fin = bloques_guia(texto)[(c.oa, c.n)]
            texto = texto[:ini] + c.bloque.strip("\n") + "\n\n" + texto[fin:].lstrip("\n")

    despues = preguntas_parseadas(ruta, texto)
    for funcion in getattr(modulo, "POST", []):
        texto = funcion(texto)
    if not any(t == "desarrollo_breve" for _, t, _, _ in despues):
        texto = normalizar_tabla_cerradas(texto)
        if es_evaluacion(ruta):
            texto = normalizar_tipo_en_pauta(texto, {k: t for k, t, _, _ in despues})
            texto = quitar_rubricas_desarrollo(texto)
        despues = preguntas_parseadas(ruta, texto)
    errores = validar(antes, despues)
    if errores:
        print("\n".join(errores))
        raise SystemExit(f"{ruta}: NO se escribió el archivo ({len(errores)} errores)")
    ruta.write_text(texto, encoding="utf-8")
    resumen(ruta, despues)


def validar(antes, despues) -> list[str]:
    errores = []
    if len(antes) != len(despues):
        errores.append(f"cambió el número de preguntas: {len(antes)} -> {len(despues)}")
    for clave, tipo, opciones, correcta in despues:
        if tipo == "alternativas" and (not opciones or correcta not in opciones):
            errores.append(f"{clave}: clave {correcta!r} no está entre las opciones {opciones}")
        if tipo == "alternativas" and opciones and len(set(opciones)) != len(opciones):
            errores.append(f"{clave}: opciones repetidas")
        if tipo == "varias_correctas":
            try:
                lista = json.loads(correcta or "")
            except ValueError:
                lista = None
            if not isinstance(lista, list) or len(lista) < 2 or not set(lista) < set(opciones or []):
                errores.append(f"{clave}: varias_correctas inválida {correcta!r}")
        if tipo == "verdadero_falso" and correcta not in ("Verdadero", "Falso"):
            errores.append(f"{clave}: V/F con clave {correcta!r}")
    return errores


def resumen(ruta: Path, preguntas) -> None:
    tipos = collections.Counter(t for _, t, _, _ in preguntas)
    letras = collections.Counter()
    for _, tipo, opciones, correcta in preguntas:
        if tipo == "alternativas" and opciones and correcta in opciones:
            letras["abcde"[opciones.index(correcta)]] += 1
    abiertas = [str(k) for k, t, _, _ in preguntas if t == "desarrollo_breve"]
    print(f"OK {ruta.relative_to(RAIZ)}: {dict(tipos)} | letras alternativas {dict(sorted(letras.items()))}"
          + (f" | QUEDAN ABIERTAS: {abiertas}" if abiertas else ""))


if __name__ == "__main__":
    modo, objetivo = sys.argv[1], Path(sys.argv[2])
    if modo == "listar":
        listar(objetivo if objetivo.is_absolute() else RAIZ / objetivo)
    elif modo == "aplicar":
        aplicar(objetivo)
    elif modo == "resumen":
        r = objetivo if objetivo.is_absolute() else RAIZ / objetivo
        resumen(r, preguntas_parseadas(r, r.read_text(encoding="utf-8")))
    else:
        raise SystemExit(__doc__)
