"""Fase 1 de la auditoría del material: cobertura de los temarios oficiales (solo lectura).

Para cada curso cruza el PDF oficial del temario (Temarios/*.pdf, fuente de verdad) con el material
importado en la base indicada por DATABASE_URL:
  - OA que el temario declara por asignatura (y sus indicadores de evaluación, en texto);
  - OA presentes en el material, con cuántas preguntas tiene cada uno en la guía, en las pruebas
    de unidad y en los simulacros;
  - reglas generales del examen que declara el temario (número de preguntas, duración).

Uso: DATABASE_URL=... python scripts/auditoria_cobertura_temarios.py [salida.md]
Requiere `pdftotext` (poppler). No modifica nada.
"""
import collections
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from sqlmodel import Session, select  # noqa: E402

from app.infrastructure.persistence.db import engine  # noqa: E402
from app.infrastructure.persistence.orm_models import (  # noqa: E402
    Asignatura, ConjuntoEvaluacion, Nivel, ObjetivoAprendizaje, Pregunta,
)

RAIZ = Path(__file__).resolve().parents[2]
PDFS = {
    "1° básico": "temario_basica_1deg_basico_UCE.pdf", "2° básico": "temario_basica_2deg_basico_UCE.pdf",
    "3° básico": "temario_basica_3deg_basico_UCE.pdf", "4° básico": "temario_basica_4deg_basico_uce.pdf",
    "5° básico": "temario_basica_5deg_basico_-UCE.pdf", "6° básico": "temario_basica_6deg_basico_UCE.pdf",
    "7° básico": "temario_basica_7deg_basico_uce.pdf", "8° básico": "temario_basica_8deg_basico_uce.pdf",
    "1° medio": "temario_media_1deg_medio_UCE.pdf", "2° medio": "temario_media_2deg_medio_UCE-1.pdf",
    "3° medio": "temario_media_3deg_medio_uce.pdf", "4° medio": "temario_media_4deg_medio_uce.pdf",
}
# Encabezado de sección de asignatura en el PDF (al inicio de línea) → clave común con la base.
ASIGNATURAS = [
    (r"lenguaje y comunicaci", "lenguaje"), (r"lengua y literatura", "lenguaje"),
    (r"matem[aá]tica", "matematica"), (r"ciencias naturales", "ciencias"),
    (r"ciencias? para la ciudadan", "ciencias"), (r"historia,? geograf", "historia"),
    (r"educaci[oó]n ciudadana", "ciudadana"), (r"filosof[ií]a", "filosofia"),
    (r"idioma extranjero|ingl[eé]s", "ingles"),
]
RE_OA = re.compile(r"Objetivo\s+de\s+Aprendizaje\s*(?:N\s*[°º]?\s*)?0?(\d{1,2})\b", re.I)


def clave_asignatura(nombre: str) -> str | None:
    n = unicodedata.normalize("NFC", nombre).lower()
    return next((k for patron, k in ASIGNATURAS if re.search(patron, n)), None)


def leer_pdf(nombre: str) -> str:
    return subprocess.run(["pdftotext", "-layout", str(RAIZ / "Temarios" / nombre), "-"],
                          capture_output=True, text=True, check=True).stdout


def oa_del_temario(texto: str) -> tuple[dict[str, list[int]], dict[str, str]]:
    """OA por asignatura, en el orden del PDF, y reglas generales (preguntas, duración)."""
    por_asig: dict[str, list[int]] = collections.defaultdict(list)
    actual = None
    for linea in texto.splitlines():
        # Título de sección: «Matemática», «Idioma Extranjero: Inglés», « Lengua y Literatura  ____».
        cabecera = re.match(r"^\s{0,10}([A-ZÁÉÍÓÚ][^\d•\-]{3,60}?)[\s_]*$", linea)
        if cabecera and (k := clave_asignatura(cabecera.group(1))):
            actual = k
            continue
        if actual:
            for m in RE_OA.finditer(linea):
                n = int(m.group(1))
                if n not in por_asig[actual]:
                    por_asig[actual].append(n)
    reglas = {}
    if m := re.search(r"consta de (\d+) preguntas", texto):
        reglas["preguntas"] = m.group(1)
    if m := re.search(r"duraci[oó]n de (\d+) minutos", texto):
        reglas["minutos"] = m.group(1)
    return dict(por_asig), reglas


def numero_oa(codigo: str) -> int | None:
    m = re.search(r"(\d+)", codigo or "")
    return int(m.group(1)) if m else None


def material(s: Session, nivel: Nivel):
    """{clave_asig: {oa_num: {'guia': n, 'prueba': n, 'simulacro': n}}} y el nombre de la asignatura."""
    tipo_de = {}
    for c in s.exec(select(ConjuntoEvaluacion)):
        for pid in c.pregunta_ids or []:
            tipo_de[pid] = "prueba" if c.tipo == "prueba_unidad" else "simulacro"
    datos, nombres = {}, {}
    for a in s.exec(select(Asignatura).where(Asignatura.nivel_id == nivel.id)):
        k = clave_asignatura(a.nombre) or a.nombre
        nombres[k] = a.nombre
        oas = {o.id: numero_oa(o.codigo_oficial) for o in s.exec(
            select(ObjetivoAprendizaje).where(ObjetivoAprendizaje.asignatura_id == a.id))}
        cuenta = {n: collections.Counter() for n in oas.values() if n is not None}
        for p in s.exec(select(Pregunta).where(Pregunta.asignatura_id == a.id)):
            n = oas.get(p.oa_id)
            if n is not None:
                cuenta.setdefault(n, collections.Counter())[tipo_de.get(p.id, "guia")] += 1
        datos[k] = cuenta
    return datos, nombres


def main() -> None:
    salida = Path(sys.argv[1]) if len(sys.argv) > 1 else None
    lineas = ["# Fase 1 — Cobertura de los temarios oficiales", "",
              "Generado por `backend/scripts/auditoria_cobertura_temarios.py` (solo lectura).", ""]
    resumen = []
    with Session(engine) as s:
        for nivel in s.exec(select(Nivel).order_by(Nivel.id)):
            pdf = PDFS.get(nivel.nombre)
            if not pdf:
                continue
            temario, reglas = oa_del_temario(leer_pdf(pdf))
            datos, nombres = material(s, nivel)
            lineas += [f"## {nivel.nombre}", "",
                       f"Temario: `{pdf}` · preguntas del examen: {reglas.get('preguntas', '—')} · "
                       f"duración: {reglas.get('minutos', '—')} min", "",
                       "| Asignatura | OA del temario | Sin material | En material sin estar en el temario | OA sin preguntas en simulacro |",
                       "|---|---|---|---|---|"]
            faltan_total = 0
            for k in sorted(set(temario) | set(datos)):
                t = temario.get(k, [])
                d = datos.get(k, {})
                sin_material = [n for n in t if not d.get(n)]
                extra = sorted(n for n in d if n not in t)
                sin_sim = [n for n in t if d.get(n) and not d[n].get("simulacro")]
                faltan_total += len(sin_material)
                lineas.append(f"| {nombres.get(k, k)} | {', '.join(map(str, t)) or '—'} | "
                              f"{', '.join(map(str, sin_material)) or '—'} | {', '.join(map(str, extra)) or '—'} | "
                              f"{', '.join(map(str, sin_sim)) or '—'} |")
            lineas += ["", "Preguntas por OA (guía / prueba / simulacro):", ""]
            for k in sorted(datos):
                partes = [f"OA {n}: {c['guia']}/{c['prueba']}/{c['simulacro']}" for n, c in sorted(datos[k].items())]
                lineas.append(f"- **{nombres.get(k, k)}:** " + " · ".join(partes))
            lineas.append("")
            resumen.append((nivel.nombre, sum(len(v) for v in temario.values()), faltan_total))
    lineas[4:4] = ["| Curso | OA en el temario | OA sin material |", "|---|---|---|",
                   *[f"| {n} | {t} | {f} |" for n, t, f in resumen], ""]
    texto = "\n".join(lineas) + "\n"
    if salida:
        salida.parent.mkdir(parents=True, exist_ok=True)
        salida.write_text(texto, encoding="utf-8")
    print(texto[:3000])


if __name__ == "__main__":
    main()
