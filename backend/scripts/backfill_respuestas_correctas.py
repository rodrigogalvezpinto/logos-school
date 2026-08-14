"""Recalcula `Pregunta.respuesta_correcta` para todas las preguntas ya importadas (banco de
autoevaluación de las guías + pruebas de unidad + exámenes simulacro), usando los parsers ya
corregidos (parser_contenido.py y parser_prueba_examen.py — ver el bug real encontrado
2026-08-13 simulando un examen completo con las respuestas correctas reales: se guardaba solo
la letra de la pauta, o texto con basura de emoji/prefijo, que nunca calzaba con lo que el
alumno responde de verdad).

No borra ni recrea filas (evita tocar IDs referenciados por ConjuntoEvaluacion.pregunta_ids,
IntentoEvaluacion, ni las cuentas demo) — solo actualiza `respuesta_correcta` (y `opciones`,
por si acaso) de cada Pregunta ya existente, emparejando por `enunciado` exacto contra lo que
el parser corregido produce para el archivo fuente correspondiente.

Uso: python scripts/backfill_respuestas_correctas.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlmodel import Session, select

from app.infrastructure.persistence.db import engine
from app.infrastructure.persistence.orm_models import Asignatura, Nivel, ObjetivoAprendizaje, Pregunta
from importar_contenido import CONTENIDO_DIR, CURSOS
from parser_contenido import parsear_guia
from parser_prueba_examen import parsear_prueba_o_examen


def _actualizar(session: Session, fila: Pregunta, respuesta_correcta: str, opciones: list[str] | None) -> bool:
    cambios = False
    if fila.respuesta_correcta != respuesta_correcta:
        fila.respuesta_correcta = respuesta_correcta
        cambios = True
    if opciones is not None and fila.opciones != opciones:
        fila.opciones = opciones
        cambios = True
    if cambios:
        session.add(fila)
    return cambios


def main() -> None:
    total_actualizadas = 0
    with Session(engine) as session:
        for curso in CURSOS:
            nivel = session.exec(select(Nivel).where(Nivel.nombre == curso["nivel"]["nombre"])).first()
            if not nivel:
                continue

            # --- 1) Banco de autoevaluación (guías) ---
            for slug, nombre_asignatura in curso["asignaturas"]:
                asignatura = session.exec(
                    select(Asignatura).where(Asignatura.nivel_id == nivel.id, Asignatura.nombre == nombre_asignatura)
                ).first()
                if not asignatura:
                    continue
                ruta_guia = CONTENIDO_DIR / curso["carpeta"] / f"{slug}.md"
                if not ruta_guia.exists():
                    continue
                objetivos = parsear_guia(ruta_guia.read_text(encoding="utf-8"))
                por_enunciado = {}
                for oa in objetivos:
                    for p in oa.preguntas:
                        por_enunciado[p.enunciado] = p

                filas = session.exec(
                    select(Pregunta).where(Pregunta.asignatura_id == asignatura.id, Pregunta.oa_id.is_not(None))
                ).all()
                for fila in filas:
                    parseada = por_enunciado.get(fila.enunciado)
                    if not parseada:
                        continue
                    if _actualizar(session, fila, parseada.respuesta_correcta, parseada.opciones):
                        total_actualizadas += 1

            # --- 2) Pruebas de unidad y exámenes simulacro ---
            for subcarpeta in ("pruebas", "examenes"):
                directorio = CONTENIDO_DIR / curso["carpeta"] / subcarpeta
                if not directorio.exists():
                    continue
                por_enunciado = {}
                for ruta in directorio.glob("*.md"):
                    for p, pauta in parsear_prueba_o_examen(ruta.read_text(encoding="utf-8")):
                        if pauta:
                            por_enunciado[p.enunciado] = (pauta.respuesta_correcta, p.opciones)

                # Ojo: NO filtrar por oa_id acá — a diferencia del banco de autoevaluación,
                # una pregunta de prueba/examen SÍ puede tener oa_id asignado (cuando su
                # pauta referencia un código de OA), así que oa_id no sirve para distinguir
                # "es de examen" de "es del banco". Se distingue solo por el enunciado, que
                # es específico de cada pregunta.
                filas = session.exec(select(Pregunta)).all()
                for fila in filas:
                    if fila.enunciado not in por_enunciado:
                        continue
                    # Filtra por asignatura del curso actual cuando la pregunta tiene
                    # asignatura_id (exámenes integrados de Régimen A no tienen una sola).
                    if fila.asignatura_id is not None:
                        asign = session.get(Asignatura, fila.asignatura_id)
                        if not asign or asign.nivel_id != nivel.id:
                            continue
                    respuesta_correcta, opciones = por_enunciado[fila.enunciado]
                    if _actualizar(session, fila, respuesta_correcta, opciones):
                        total_actualizadas += 1

        session.commit()
    print(f"Preguntas actualizadas: {total_actualizadas}")


if __name__ == "__main__":
    main()
