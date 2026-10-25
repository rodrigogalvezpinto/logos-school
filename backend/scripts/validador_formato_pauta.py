#!/usr/bin/env python3
"""
Validador (solo lectura) de pautas de corrección en exámenes.

Comprueba, sin modificar jamás el archivo:
  - que exista una sección de pauta;
  - que no queden marcadores de plantilla sin reemplazar;
  - que haya una fila de pauta por cada pregunta del examen;
  - que el puntaje total declarado coincida con la suma de la columna Puntaje;
  - la distribución de claves (letra a/b/c/d) para detectar sesgos.

Uso: python validador_formato_pauta.py [ruta_archivo_o_directorio]

IMPORTANTE: este script NO escribe archivos. La versión anterior reescribía la
tabla de pauta con una plantilla y destruyó las claves de 48 exámenes
(commit 5421485 + corridas locales). No volver a agregar un modo --fix que
reconstruya la tabla: la pauta es contenido editorial y debe editarse a mano.
"""

import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Optional

MARCADOR_PLANTILLA = "MANTENER FILAS ORIGINALES"
LIMITE_SESGO = 0.45


def extraer_numeros_preguntas(contenido: str) -> List[int]:
    """Números de pregunta del enunciado del examen."""
    patrones = [
        r"^\*\*(\d{1,2})\.\*\*",
        r"^\*\*(\d{1,2})\.\s*\(",
        r"^\*\*(\d{1,2})\.\s",
        r"^\*\*Pregunta\s+(\d{1,2})\b",
        r"^###\s+(\d{1,2})\.\s",
        r"^(\d{1,2})\.\s*\*\(",
    ]
    numeros = set()
    for patron in patrones:
        for m in re.finditer(patron, contenido, re.MULTILINE):
            numeros.add(int(m.group(1)))
    return sorted(n for n in numeros if 1 <= n <= 60)


def bloque_pauta(contenido: str) -> Optional[str]:
    """Sección de pauta: desde su heading hasta el siguiente heading de nivel
    igual o superior (los subheadings ### sí pertenecen a la pauta)."""
    lineas = contenido.split("\n")
    inicio = nivel = None
    for i, linea in enumerate(lineas):
        m = re.match(r"^(#{1,6})\s+PAUTA DE CORRECCI", linea, re.IGNORECASE)
        if m:
            inicio, nivel = i, len(m.group(1))
            break
    if inicio is None:
        return None
    fin = len(lineas)
    for i in range(inicio + 1, len(lineas)):
        m = re.match(r"^(#{1,6})\s+\S", lineas[i])
        if m and len(m.group(1)) <= nivel:
            fin = i
            break
    return "\n".join(lineas[inicio:fin])


def filas_pauta(texto_pauta: str) -> List[List[str]]:
    filas = []
    for linea in texto_pauta.split("\n"):
        linea = linea.strip()
        if not linea.startswith("|"):
            continue
        if re.match(r"^\|[\s:|-]+\|$", linea):
            continue
        celdas = [c.strip() for c in linea.strip("|").split("|")]
        if celdas and re.fullmatch(r"\d{1,2}", celdas[0]):
            filas.append(celdas)
    return filas


def suma_puntajes(filas: List[List[str]]) -> Optional[int]:
    """Suma la última columna si es numérica (columna 'Puntaje')."""
    total = 0
    encontrado = False
    for celdas in filas:
        ultimo = celdas[-1]
        m = re.fullmatch(r"\**(\d{1,3})\**", ultimo)
        if m:
            total += int(m.group(1))
            encontrado = True
    return total if encontrado else None


def total_declarado(contenido: str) -> Optional[int]:
    patrones = [
        r"\*\*Puntaje total(?: de la prueba)?:\s*(\d{1,3})\s*puntos",
        r"Puntaje total[:\s*]*\**(\d{1,3})\**\s*puntos",
        r"\*\*Puntaje total:\*\*\s*(\d{1,3})",
    ]
    for patron in patrones:
        m = re.search(patron, contenido, re.IGNORECASE)
        if m:
            return int(m.group(1))
    return None


def distribucion_claves(filas: List[List[str]]) -> Dict[str, int]:
    conteo: Dict[str, int] = {}
    for celdas in filas:
        texto = " ".join(celdas)
        m = re.search(r"\*\*([a-d])\)", texto)
        if not m:
            m = re.search(r"\b([a-d])\)", texto)
        if not m:
            # Formato compacto: la clave es una celda que sólo contiene la letra
            for celda in celdas[1:]:
                if re.fullmatch(r"[a-d]", celda.strip()):
                    m = re.match(r"([a-d])", celda.strip())
                    break
        if m:
            clave = m.group(1)
            conteo[clave] = conteo.get(clave, 0) + 1
    return conteo


def validar_archivo(ruta: Path) -> Dict:
    contenido = ruta.read_text(encoding="utf-8")
    resultado = {
        "archivo": str(ruta),
        "problemas": [],
        "avisos": [],
    }

    texto_pauta = bloque_pauta(contenido)
    if texto_pauta is None:
        resultado["problemas"].append("sin sección 'PAUTA DE CORRECCIÓN'")
        return resultado

    if MARCADOR_PLANTILLA in contenido:
        resultado["problemas"].append("contiene marcador de plantilla sin reemplazar")

    filas = filas_pauta(texto_pauta)
    if not filas:
        resultado["problemas"].append("la tabla de pauta no tiene filas numeradas")
        return resultado

    preguntas = extraer_numeros_preguntas(contenido)
    filas_num = [int(c[0]) for c in filas]
    # Las preguntas de desarrollo suelen tener criterio en prosa ("**Pregunta 4 (OA1, 3 pts).**")
    cubiertas_prosa = {
        int(m.group(1))
        for m in re.finditer(r"Pregunta\s+(\d{1,2})\b", texto_pauta, re.IGNORECASE)
    }
    cubiertas = set(filas_num) | cubiertas_prosa

    if preguntas:
        faltan = sorted(set(preguntas) - cubiertas)
        sobran = sorted(set(filas_num) - set(preguntas))
        if faltan:
            resultado["problemas"].append(f"preguntas sin fila de pauta: {faltan}")
        if sobran:
            resultado["avisos"].append(f"filas de pauta sin pregunta asociada: {sobran}")

    duplicados = sorted({n for n in filas_num if filas_num.count(n) > 1})
    if duplicados:
        resultado["problemas"].append(f"números de fila duplicados: {duplicados}")

    suma = suma_puntajes(filas)
    declarado = total_declarado(contenido)
    if suma is not None and declarado is not None:
        if suma > declarado:
            resultado["problemas"].append(
                f"la suma de la pauta ({suma}) supera el puntaje declarado ({declarado})"
            )
        elif suma < declarado:
            resultado["avisos"].append(
                f"la tabla suma {suma} de {declarado} pts declarados "
                f"(el resto se corrige con criterios en prosa)"
            )

    claves = distribucion_claves(filas)
    total_claves = sum(claves.values())
    # El indicador de sesgo sólo es interpretable si casi todas las preguntas
    # son de alternativas (en exámenes con V/F, pareados o desarrollo mezclados
    # la proporción de letras no representa la dificultad real).
    if total_claves >= 8 and total_claves / len(filas) >= 0.8:
        for letra, n in sorted(claves.items()):
            if n / total_claves > LIMITE_SESGO:
                resultado["avisos"].append(
                    f"clave '{letra}' concentra {n}/{total_claves} "
                    f"({n / total_claves:.0%} > {LIMITE_SESGO:.0%})"
                )

    return resultado


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    parser = argparse.ArgumentParser(
        description="Validador de pautas de corrección (solo lectura)"
    )
    parser.add_argument("ruta", nargs="?", default="contenido", help="Archivo o directorio")
    args = parser.parse_args()

    ruta = Path(args.ruta)
    if not ruta.exists():
        print(f"[ERROR] Ruta no existe: {ruta}")
        sys.exit(1)

    if ruta.is_file():
        archivos = [ruta]
    else:
        archivos = [
            a for a in ruta.rglob("*.md")
            if "examen" in a.name.lower()
            or re.search(r"forma-[ab]\b", a.name.lower())
        ]

    print(f"[SCAN] Analizando {len(archivos)} archivos de examen...")

    con_problemas = 0
    con_avisos = 0

    for archivo in sorted(archivos):
        r = validar_archivo(archivo)
        if r["problemas"]:
            con_problemas += 1
            print(f"\n[ERROR] {archivo}")
            for p in r["problemas"]:
                print(f"   - {p}")
        if r["avisos"]:
            con_avisos += 1
            print(f"\n[AVISO] {archivo}")
            for a in r["avisos"]:
                print(f"   - {a}")

    print("\n[RESUMEN]")
    print(f"   Archivos de examen: {len(archivos)}")
    print(f"   Con problemas: {con_problemas}")
    print(f"   Con avisos: {con_avisos}")

    if con_problemas:
        sys.exit(1)


if __name__ == "__main__":
    main()
