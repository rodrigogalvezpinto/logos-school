"""Tarea 8 (2026-11-16): arma un simulacro Forma A a partir de la Forma B del mismo curso y asignatura.

Copia el encabezado (hasta la primera sección de preguntas) y la cola (desde «# HOJA DE RESPUESTAS») de la Forma B,
reemplaza las preguntas por las nuevas y las filas de la pauta por las nuevas explicaciones. La clave se escribe primero
en la lista de opciones y se ubica en la letra pedida (así se controla la distribución de letras).

Uso desde Python:
    from forma_a import P, armar
    preguntas = [P(seccion, encabezado, enunciado, [clave, d1, d2, d3], "c", explicacion, oa, extra), ...]
    armar(ruta_b, ruta_a, preguntas, fila=lambda i, p, clave: f"| {i} | ... |", reemplazos={"Forma B": "Forma A"})

Para «varias correctas», `letra` es una cadena como "acd" y las opciones van en su orden final.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class P:
    seccion: str          # texto a insertar antes de la pregunta ("" si no abre sección)
    encabezado: str       # p. ej. "**Pregunta 3.** (1 punto)" con {n} para el número
    enunciado: str
    opciones: list[str]   # alternativas: la clave primero; varias correctas: en su orden final
    letra: str            # letra donde queda la clave ("acd" para varias correctas)
    explicacion: str      # explica la clave (sin repetirla al inicio)
    oa: str = ""
    extra: dict = field(default_factory=dict)

    def ordenadas(self) -> list[str]:
        if not self.opciones:          # verdadero o falso: sin alternativas escritas
            return []
        if len(self.letra) > 1:
            return list(self.opciones)
        resto = self.opciones[1:]
        i = "abcd".index(self.letra)
        return resto[:i] + [self.opciones[0]] + resto[i:]

    def clave_texto(self) -> str:
        if not self.opciones:
            return self.extra.get("clave", "True (Verdadero)" if self.letra == "V" else "False (Falso)")
        if len(self.letra) > 1:
            ls = list(self.letra)
            return (", ".join(ls[:-1]) + " y " + ls[-1]) if len(ls) > 1 else ls[0]
        return f"{self.letra}) {self.opciones[0]}"


def bloque(n: int, p: P, nota_varias: str = "*(Varias correctas: marca todas las alternativas correctas.)*") -> str:
    cab = p.encabezado.format(n=n)
    partes = [p.seccion] if p.seccion else []
    sep = " " if cab.endswith(" ") else ("\n\n" if p.enunciado.startswith(("> ", "|")) else "\n")
    partes.append(f"{cab.rstrip(' ')}{sep}{p.enunciado}\n\n")
    if len(p.letra) > 1 and nota_varias:
        partes.append(nota_varias + "\n\n")
    if p.opciones:
        partes.append("\n".join(f"{l}) {o}" for l, o in zip("abcd", p.ordenadas())) + "\n\n")
    partes.append("---\n\n")
    return "".join(partes)


def sesgos(preguntas: list[P]) -> list[int]:
    """Números de las preguntas cuya clave es claramente la más larga (criterio C.6 de `ajustar_distractores.sesgada`)."""
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from ajustar_distractores import sesgada
    return [i for i, p in enumerate(preguntas, 1) if p.opciones and len(p.letra) == 1 and sesgada(p.ordenadas(), p.opciones[0])]


def armar(ruta_b: Path, ruta_a: Path, preguntas: list[P], fila, reemplazos: dict[str, str] | None = None,
          inicio_preguntas: str | None = None, separador_pauta: str = r"^\|[-| ]+\|$", nota_varias=None) -> None:
    b = ruta_b.read_text(encoding="utf-8")
    corte = b.index(inicio_preguntas) if inicio_preguntas else re.search(r"^## ", b[b.index("\n---\n", 5) + 5:], re.M).start() + b.index("\n---\n", 5) + 5
    cabeza = b[:corte]
    cola = b[b.index("# HOJA DE RESPUESTAS"):]
    for viejo, nuevo in (reemplazos or {}).items():
        cabeza = cabeza.replace(viejo, nuevo)
        cola = cola.replace(viejo, nuevo)
    kw = {"nota_varias": nota_varias} if nota_varias is not None else {}
    cuerpo = "".join(bloque(i, p, **kw) for i, p in enumerate(preguntas, 1))
    # Pauta: la tabla que sigue a «PAUTA DE CORRECCIÓN»; se reemplazan sus filas de datos.
    ip = cola.index("PAUTA DE CORRECCIÓN")
    lineas = cola[ip:].split("\n")
    k = next(i for i, l in enumerate(lineas) if re.match(separador_pauta, l.strip()))
    fin = k + 1
    while fin < len(lineas) and lineas[fin].startswith("|"):
        fin += 1
    nuevas = [fila(i, p, p.clave_texto()) for i, p in enumerate(preguntas, 1)]
    cola = cola[:ip] + "\n".join(lineas[: k + 1] + nuevas + lineas[fin:])
    ruta_a.write_text(cabeza + cuerpo + cola, encoding="utf-8")
    malas = sesgos(preguntas)
    if malas:
        print(f"⚠️  {ruta_a.name}: clave claramente más larga en {malas}")
