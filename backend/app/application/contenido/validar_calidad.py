"""Control de calidad de contenido (Fase 1, ítem 2.5.1 del plan de incorporación de
hallazgos de Brincus — ver planificacion/27-plan-incorporacion-hallazgos-brincus.md).

Nace de un bug real encontrado en Brincus (no en Logos): una guía etiquetada "Números
hasta 10.000" (4° básico) contenía ejercicios con números de cientos de miles de
millones — contenido de un nivel totalmente distinto, mal filed bajo esa unidad. Esto
valida mecánicamente, sobre TODO el banco de contenido real (los 12 cursos, no una
muestra), invariantes estructurales que un error de ese tipo rompería:

1. Toda pregunta "alternativas" tiene su `respuesta_correcta` dentro de sus `opciones`.
2. Toda pregunta "verdadero_falso" tiene `respuesta_correcta` en {"Verdadero", "Falso"}.
3. Ningún Objetivo de Aprendizaje tiene `contenido_guia` vacío (una guía "fantasma").
4. Cada Pregunta referenciada por un ConjuntoEvaluacion pertenece a la MISMA asignatura
   que el conjunto — el análogo directo al bug de Brincus: contenido filed bajo la
   unidad/asignatura equivocada.
5. Ningún ConjuntoEvaluacion referencia un `pregunta_id` que no existe (referencia rota).

Es determinístico y rápido (segundos, no minutos) — a diferencia de
`qa_extraer_para_coherencia.py` (que necesita juicio semántico de un LLM/humano), esto
corre en cada QA completo sin intervención, igual que la matriz de permisos.

Vive en `application/` (no en `scripts/`, que no forma parte del paquete instalable y no
es importable desde los tests) para que sea testeable con el mismo fixture `session` que
el resto del suite — `scripts/validar_calidad_contenido.py` es solo un wrapper de CLI
sobre esta función."""

from sqlmodel import Session, select

from app.infrastructure.persistence.orm_models import ConjuntoEvaluacion, ObjetivoAprendizaje, Pregunta


def validar(session: Session) -> list[str]:
    hallazgos: list[str] = []

    preguntas = session.exec(select(Pregunta)).all()
    preguntas_por_id = {p.id: p for p in preguntas}

    for p in preguntas:
        if p.tipo == "alternativas":
            opciones = p.opciones or []
            if p.respuesta_correcta not in opciones:
                hallazgos.append(
                    f"Pregunta {p.id} (alternativas): respuesta_correcta={p.respuesta_correcta!r} "
                    f"no está entre las opciones {opciones!r}"
                )
        elif p.tipo == "verdadero_falso":
            if p.respuesta_correcta not in ("Verdadero", "Falso"):
                hallazgos.append(
                    f"Pregunta {p.id} (verdadero_falso): respuesta_correcta={p.respuesta_correcta!r} "
                    'no es "Verdadero" ni "Falso"'
                )

    for oa in session.exec(select(ObjetivoAprendizaje)).all():
        if not oa.contenido_guia or not oa.contenido_guia.strip():
            hallazgos.append(f"OA {oa.id} ({oa.codigo_oficial}): contenido_guia vacío")

    for c in session.exec(select(ConjuntoEvaluacion)).all():
        for pid in c.pregunta_ids:
            p = preguntas_por_id.get(pid)
            if p is None:
                hallazgos.append(f"Conjunto {c.id} ({c.nombre}): referencia pregunta_id={pid} que no existe")
                continue
            if c.asignatura_id is not None and p.asignatura_id is not None and p.asignatura_id != c.asignatura_id:
                hallazgos.append(
                    f"Conjunto {c.id} ({c.nombre}, asignatura {c.asignatura_id}): incluye pregunta {p.id} "
                    f"de la asignatura {p.asignatura_id} — contenido filed bajo la asignatura equivocada"
                )

    return hallazgos
