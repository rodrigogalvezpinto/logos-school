"""Importa el contenido ya escrito en contenido/{curso}/*.md a la base de datos:
guías + banco de autoevaluación, Pruebas de unidad y Exámenes simulacro.

Uso:
    python scripts/importar_contenido.py

Ver planificacion/11-especificacion-mvp-para-desarrollo.md (Paso 3 del plan de
desarrollo). Idempotente a nivel de Nivel: si el Nivel ya existe en la base, se omite
por completo (no duplica datos si se corre más de una vez).
"""

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select

from app.infrastructure.persistence.db import engine, crear_tablas
from app.infrastructure.persistence.orm_models import Asignatura, ConjuntoEvaluacion, Nivel, ObjetivoAprendizaje, Pregunta
from parser_contenido import parsear_guia
from parser_prueba_examen import parsear_prueba_o_examen

CONTENIDO_DIR = Path(__file__).parent.parent.parent / "contenido"

# Configuración de los cursos a importar — se agregan más a medida que el roadmap
# avance a más niveles (ver planificacion/03-roadmap-etapas.md).
def _curso_regimen_a(carpeta: str, nombre_nivel: str) -> dict:
    """1°-4° básico — prueba integrada única, 20 preguntas, decreto 439/2012."""
    return {
        "carpeta": carpeta,
        "nivel": {
            "nombre": nombre_nivel,
            "regimen": "A",
            "decreto": "439/2012",
            "formato_examen": "integrado",
            "num_preguntas_examen": 20,
            "duracion_examen_min": 90,
            "materiales_permitidos": "Ninguno",
        },
        "asignaturas": [
            ("lenguaje-y-comunicacion", "Lenguaje y Comunicación"),
            ("matematica", "Matemática"),
            ("ciencias-naturales", "Ciencias Naturales"),
            ("historia-geografia-y-cs-sociales", "Historia, Geografía y Cs. Sociales"),
        ],
    }


def _curso_regimen_b(carpeta: str, nombre_nivel: str, decreto: str, slug_lengua: str, nombre_lengua: str) -> dict:
    """5° básico - 2° medio — prueba separada por asignatura, 25 preguntas c/u, se agrega
    Inglés. Decreto 439/2012 hasta 6° básico, 614/2013 desde 7° básico (cambia también el
    nombre de la asignatura: "Lenguaje y Comunicación" -> "Lengua y Literatura")."""
    return {
        "carpeta": carpeta,
        "nivel": {
            "nombre": nombre_nivel,
            "regimen": "B",
            "decreto": decreto,
            "formato_examen": "separado_por_asignatura",
            "num_preguntas_examen": 25,
            "duracion_examen_min": 90,
            "materiales_permitidos": "Calculadora, diccionario de inglés",
        },
        "asignaturas": [
            (slug_lengua, nombre_lengua),
            ("matematica", "Matemática"),
            ("ciencias-naturales", "Ciencias Naturales"),
            ("historia-geografia-y-cs-sociales", "Historia, Geografía y Cs. Sociales"),
            ("ingles", "Inglés"),
        ],
    }


def _curso_regimen_c(carpeta: str, nombre_nivel: str) -> dict:
    """3°-4° medio — currículum de decreto 193/2019, asignaturas propias (Ciencias para la
    Ciudadanía, Filosofía, Educación Ciudadana en vez de Cs. Naturales e Historia)."""
    return {
        "carpeta": carpeta,
        "nivel": {
            "nombre": nombre_nivel,
            "regimen": "C",
            "decreto": "193/2019",
            "formato_examen": "separado_por_asignatura",
            "num_preguntas_examen": 25,
            "duracion_examen_min": 90,
            "materiales_permitidos": "Calculadora, diccionario de inglés",
        },
        "asignaturas": [
            ("lengua-y-literatura", "Lengua y Literatura"),
            ("matematica", "Matemática"),
            ("ciencias-para-la-ciudadania", "Ciencias para la Ciudadanía"),
            ("filosofia", "Filosofía"),
            ("ingles", "Inglés"),
            ("educacion-ciudadana", "Educación Ciudadana"),
        ],
    }


CURSOS = [
    _curso_regimen_a("01-basico", "1° básico"),
    _curso_regimen_a("02-basico", "2° básico"),
    _curso_regimen_a("03-basico", "3° básico"),
    _curso_regimen_a("04-basico", "4° básico"),
    _curso_regimen_b("05-basico", "5° básico", "439/2012", "lenguaje-y-comunicacion", "Lenguaje y Comunicación"),
    _curso_regimen_b("06-basico", "6° básico", "439/2012", "lenguaje-y-comunicacion", "Lenguaje y Comunicación"),
    _curso_regimen_b("07-basico", "7° básico", "614/2013", "lengua-y-literatura", "Lengua y Literatura"),
    _curso_regimen_b("08-basico", "8° básico", "614/2013", "lengua-y-literatura", "Lengua y Literatura"),
    _curso_regimen_b("01-medio", "1° medio", "614/2013", "lengua-y-literatura", "Lengua y Literatura"),
    _curso_regimen_b("02-medio", "2° medio", "614/2013", "lengua-y-literatura", "Lengua y Literatura"),
    _curso_regimen_c("03-medio", "3° medio"),
    _curso_regimen_c("04-medio", "4° medio"),
]


# Algunos archivos de contenido/{curso}/pruebas/ usan un prefijo más corto que el
# slug real de la asignatura (descubierto al importar, no asumido de antemano) — ej.
# "historia-unidad-historia.md" en vez de "historia-geografia-y-cs-sociales-unidad-...".
ALIAS_SLUG = {
    "historia": "historia-geografia-y-cs-sociales",
}


def _titulo_desde_encabezado(ruta: Path) -> str | None:
    """El nombre de una prueba de unidad se toma del primer encabezado `# ...` del archivo
    (ya escrito con tildes y mayúsculas correctas) en vez de derivarlo del slug del nombre
    de archivo — `"matematica-unidad-geometria".title()` da "Matematica Unidad Geometria",
    sin tildes y con "Unidad" en mayúscula donde no corresponde."""
    for linea in ruta.read_text(encoding="utf-8").splitlines():
        linea = linea.strip()
        if linea.startswith("# "):
            return linea[2:].strip()
    return None


def _asignatura_por_archivo(nombre_archivo: str, slugs: list[str]) -> str | None:
    """Encuentra a qué asignatura pertenece un archivo de pruebas/examenes, por el
    slug más largo que calce al inicio del nombre (ej. "matematica-unidad-geometria"
    empieza con "matematica")."""
    candidatos = [s for s in slugs if nombre_archivo.startswith(s)]
    if candidatos:
        return max(candidatos, key=len)
    for alias, slug_real in ALIAS_SLUG.items():
        if nombre_archivo.startswith(alias) and slug_real in slugs:
            return slug_real
    return None


def _importar_conjunto(
    session: Session,
    ruta: Path,
    tipo: str,
    nombre: str,
    forma: str | None,
    asignatura_id: int | None,
    nivel_id: int | None,
    tiempo_sugerido_min: int | None,
    oas_por_codigo: dict[str, int],
) -> int:
    resultado = parsear_prueba_o_examen(ruta.read_text(encoding="utf-8"))
    if not resultado:
        return 0

    pregunta_ids = []
    for pregunta, pauta in resultado:
        oa_id = None
        if pauta and pauta.codigo_oa:
            oa_id = oas_por_codigo.get(pauta.codigo_oa)
        p = Pregunta(
            oa_id=oa_id,
            asignatura_id=asignatura_id,
            tipo=pregunta.tipo,
            enunciado=pregunta.enunciado,
            opciones=pregunta.opciones,
            respuesta_correcta=pauta.respuesta_correcta if pauta else "",
            retroalimentacion=pauta.retroalimentacion if pauta else "",
        )
        session.add(p)
        session.commit()
        session.refresh(p)
        pregunta_ids.append(p.id)

    conjunto = ConjuntoEvaluacion(
        tipo=tipo,
        asignatura_id=asignatura_id,
        nivel_id=nivel_id,
        nombre=nombre,
        forma=forma,
        pregunta_ids=pregunta_ids,
        tiempo_sugerido_min=tiempo_sugerido_min,
    )
    session.add(conjunto)
    session.commit()
    return len(pregunta_ids)


def importar_curso(session: Session, curso: dict) -> None:
    nombre_nivel = curso["nivel"]["nombre"]
    existente = session.exec(select(Nivel).where(Nivel.nombre == nombre_nivel)).first()
    if existente:
        print(f"  {nombre_nivel}: ya estaba importado, se omite.")
        return

    # `orden` es la posición curricular real (1=1° básico...12=4° medio) — NUNCA el `id`
    # autoincremental, que depende del orden en que se haya importado cada curso, no del
    # orden en que se cursan (bug real: en Desarrollo, 4° básico se importó primero como
    # piloto y quedó con id=1). Ver Nivel.orden en orm_models.py.
    orden = [c["nivel"]["nombre"] for c in CURSOS].index(nombre_nivel) + 1
    nivel = Nivel(**curso["nivel"], orden=orden)
    session.add(nivel)
    session.commit()
    session.refresh(nivel)

    total_oa = 0
    total_preguntas = 0
    asignaturas_por_slug: dict[str, Asignatura] = {}
    oas_por_asignatura: dict[int, dict[str, int]] = {}  # asignatura_id -> {codigo_oficial: oa_id}

    # 1) Guías + banco de autoevaluación
    for archivo, nombre_asignatura in curso["asignaturas"]:
        ruta = CONTENIDO_DIR / curso["carpeta"] / f"{archivo}.md"
        if not ruta.exists():
            print(f"    ⚠️  No existe {ruta}, se omite esta asignatura.")
            continue

        asignatura = Asignatura(nivel_id=nivel.id, nombre=nombre_asignatura)
        session.add(asignatura)
        session.commit()
        session.refresh(asignatura)
        asignaturas_por_slug[archivo] = asignatura
        oas_por_asignatura[asignatura.id] = {}

        objetivos = parsear_guia(ruta.read_text(encoding="utf-8"))
        for oa_parseado in objetivos:
            oa = ObjetivoAprendizaje(
                asignatura_id=asignatura.id,
                codigo_oficial=oa_parseado.codigo_oficial,
                descripcion=oa_parseado.descripcion,
                eje_tematico=oa_parseado.eje_tematico,
                contenido_guia=oa_parseado.contenido_guia,
            )
            session.add(oa)
            session.commit()
            session.refresh(oa)
            total_oa += 1
            oas_por_asignatura[asignatura.id][oa_parseado.codigo_oficial] = oa.id

            for p in oa_parseado.preguntas:
                session.add(
                    Pregunta(
                        oa_id=oa.id,
                        asignatura_id=asignatura.id,
                        tipo=p.tipo,
                        enunciado=p.enunciado,
                        opciones=p.opciones,
                        respuesta_correcta=p.respuesta_correcta,
                        retroalimentacion=p.retroalimentacion,
                    )
                )
                total_preguntas += 1
        session.commit()
        print(f"    {nombre_asignatura}: {len(objetivos)} OA, {sum(len(o.preguntas) for o in objetivos)} preguntas")

    print(f"  {nombre_nivel}: TOTAL {total_oa} OA, {total_preguntas} preguntas de autoevaluación importadas.")

    slugs = list(asignaturas_por_slug.keys())

    # 2) Pruebas de unidad (sin cronómetro — ver planificacion/12-motor-de-evaluacion.md)
    dir_pruebas = CONTENIDO_DIR / curso["carpeta"] / "pruebas"
    total_pruebas = total_preguntas_pruebas = 0
    if dir_pruebas.exists():
        for ruta in sorted(dir_pruebas.glob("*.md")):
            slug = _asignatura_por_archivo(ruta.stem, slugs)
            if not slug:
                print(f"    ⚠️  No pude asociar {ruta.name} a ninguna asignatura, se omite.")
                continue
            asignatura = asignaturas_por_slug[slug]
            n = _importar_conjunto(
                session,
                ruta,
                tipo="prueba_unidad",
                nombre=_titulo_desde_encabezado(ruta) or ruta.stem.replace("-", " ").title(),
                forma=None,
                asignatura_id=asignatura.id,
                nivel_id=None,
                tiempo_sugerido_min=None,
                oas_por_codigo=oas_por_asignatura.get(asignatura.id, {}),
            )
            if n:
                total_pruebas += 1
                total_preguntas_pruebas += n
    print(f"  {nombre_nivel}: {total_pruebas} pruebas de unidad, {total_preguntas_pruebas} preguntas.")

    # 3) Exámenes simulacro (con cronómetro estricto — imita el examen real)
    dir_examenes = CONTENIDO_DIR / curso["carpeta"] / "examenes"
    total_examenes = total_preguntas_examenes = 0
    if dir_examenes.exists():
        for ruta in sorted(dir_examenes.glob("*.md")):
            forma_m = re.search(r"forma-([ab])", ruta.stem, re.IGNORECASE)
            forma = forma_m.group(1).upper() if forma_m else None

            if ruta.stem.startswith("examen-integrado"):
                # Régimen A: examen único, mezcla las asignaturas, no pertenece a una sola.
                n = _importar_conjunto(
                    session,
                    ruta,
                    tipo="examen_simulacro",
                    nombre=f"Examen integrado Forma {forma}",
                    forma=forma,
                    asignatura_id=None,
                    nivel_id=nivel.id,
                    tiempo_sugerido_min=nivel.duracion_examen_min,
                    oas_por_codigo={},  # OA de asignaturas mezcladas — no hay un único mapa
                )
            else:
                slug = _asignatura_por_archivo(ruta.stem, slugs)
                if not slug:
                    print(f"    ⚠️  No pude asociar {ruta.name} a ninguna asignatura, se omite.")
                    continue
                asignatura = asignaturas_por_slug[slug]
                n = _importar_conjunto(
                    session,
                    ruta,
                    tipo="examen_simulacro",
                    nombre=f"Examen {asignatura.nombre} Forma {forma}",
                    forma=forma,
                    asignatura_id=asignatura.id,
                    nivel_id=None,
                    tiempo_sugerido_min=nivel.duracion_examen_min,
                    oas_por_codigo=oas_por_asignatura.get(asignatura.id, {}),
                )
            if n:
                total_examenes += 1
                total_preguntas_examenes += n
    print(f"  {nombre_nivel}: {total_examenes} exámenes simulacro, {total_preguntas_examenes} preguntas.")


def main() -> None:
    crear_tablas()
    with Session(engine) as session:
        for curso in CURSOS:
            print(f"Importando {curso['nivel']['nombre']}...")
            importar_curso(session, curso)


if __name__ == "__main__":
    main()
