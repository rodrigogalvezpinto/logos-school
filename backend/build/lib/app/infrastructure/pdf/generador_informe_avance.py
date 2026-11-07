"""Informe de avance descargable en PDF para el Apoderado (Fase 1 del plan de
incorporación de hallazgos de Brincus — ver planificacion/27-plan-incorporacion-hallazgos-brincus.md,
gap detectado tras comparar en vivo: Brincus no ofrece esto tampoco, pero un apoderado que
paga por el estudio de su hijo/a espera poder guardar/imprimir un resumen fuera de la app,
igual que ya existe para el certificado de alumno regular).

Reutiliza exactamente los mismos datos que ya arma `ObtenerHistorialYNotas` (notas por
asignatura, guías revisadas) — no se recalcula nada nuevo, solo se presenta en PDF."""

from datetime import date

from app.application.progreso.consultas import ResultadoHistorial
from app.infrastructure.pdf.pdf_marca import (
    ANCHO_UTIL_MM,
    CORAL,
    INDIGO,
    INDIGO_SUAVE,
    MARGEN_LATERAL_MM,
    PDFConMarca,
    TEXTO_PRINCIPAL,
    TEXTO_SECUNDARIO,
    dibujar_insignia,
)
from app.infrastructure.pdf.sanitizar_texto import sanitizar_para_pdf


def _titulo_seccion(pdf: PDFConMarca, texto: str) -> None:
    pdf.set_x(MARGEN_LATERAL_MM)
    pdf.set_font("Helvetica", "B", 13)
    pdf.set_text_color(*TEXTO_PRINCIPAL)
    pdf.multi_cell(ANCHO_UTIL_MM, 8, sanitizar_para_pdf(texto), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(1)


def generar_pdf_informe_avance(
    nombre_completo: str,
    nivel_nombre: str,
    resultado: ResultadoHistorial,
    racha_dias_actual: int,
    logros_desbloqueados: int,
    logros_totales: int,
    fecha: date,
) -> bytes:
    pdf = PDFConMarca(format="A4")
    pdf.set_auto_page_break(auto=True, margin=22)
    pdf.add_page()
    pdf.set_left_margin(MARGEN_LATERAL_MM)
    pdf.set_right_margin(MARGEN_LATERAL_MM)

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*TEXTO_PRINCIPAL)
    pdf.multi_cell(ANCHO_UTIL_MM, 9, sanitizar_para_pdf(f"Informe de avance — {nombre_completo}"), new_x="LMARGIN", new_y="NEXT")
    dibujar_insignia(pdf, nivel_nombre)
    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*TEXTO_SECUNDARIO)
    pdf.set_x(MARGEN_LATERAL_MM)
    pdf.cell(ANCHO_UTIL_MM, 6, f"Generado el {fecha.strftime('%d-%m-%Y')}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    _titulo_seccion(pdf, "Resumen de hábito de estudio")
    pdf.set_x(MARGEN_LATERAL_MM)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(*TEXTO_PRINCIPAL)
    racha_texto = f"{racha_dias_actual} día(s) seguidos" if racha_dias_actual > 0 else "sin racha activa hoy"
    pdf.multi_cell(
        ANCHO_UTIL_MM, 6,
        sanitizar_para_pdf(
            f"Racha actual de estudio: {racha_texto}. Insignias desbloqueadas: "
            f"{logros_desbloqueados} de {logros_totales}. Guías revisadas: {len(resultado.guias_revisadas)}."
        ),
        new_x="LMARGIN", new_y="NEXT",
    )
    pdf.ln(4)

    _titulo_seccion(pdf, "Notas por asignatura")
    if not resultado.notas_por_asignatura:
        pdf.set_x(MARGEN_LATERAL_MM)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(*TEXTO_SECUNDARIO)
        pdf.multi_cell(ANCHO_UTIL_MM, 6, "Todavía no hay evaluaciones entregadas.", new_x="LMARGIN", new_y="NEXT")
    else:
        ancho_col = ANCHO_UTIL_MM / 3
        pdf.set_x(MARGEN_LATERAL_MM)
        pdf.set_font("Helvetica", "B", 10)
        pdf.set_fill_color(*INDIGO)
        pdf.set_text_color(255, 255, 255)
        for encabezado in ("Asignatura", "Práctica (prom.)", "Simulacro (última)"):
            pdf.cell(ancho_col, 8, sanitizar_para_pdf(encabezado), fill=True, align="C")
        pdf.ln(8)

        for i, n in enumerate(resultado.notas_por_asignatura):
            pdf.set_x(MARGEN_LATERAL_MM)
            pdf.set_font("Helvetica", "", 10)
            pdf.set_text_color(*TEXTO_PRINCIPAL)
            pdf.set_fill_color(*INDIGO_SUAVE) if i % 2 == 0 else pdf.set_fill_color(255, 255, 255)
            pdf.cell(ancho_col, 7, sanitizar_para_pdf(n.asignatura_nombre), fill=True, align="C")
            pdf.cell(ancho_col, 7, f"{n.nota_practica:.1f}" if n.nota_practica is not None else "-", fill=True, align="C")
            pdf.cell(ancho_col, 7, f"{n.nota_simulacro:.1f}" if n.nota_simulacro is not None else "-", fill=True, align="C")
            pdf.ln(7)
    pdf.ln(6)

    _titulo_seccion(pdf, "Últimas evaluaciones rendidas")
    ultimas = resultado.historial[:12]
    if not ultimas:
        pdf.set_x(MARGEN_LATERAL_MM)
        pdf.set_font("Helvetica", "", 11)
        pdf.set_text_color(*TEXTO_SECUNDARIO)
        pdf.multi_cell(ANCHO_UTIL_MM, 6, "Todavía no hay evaluaciones entregadas.", new_x="LMARGIN", new_y="NEXT")
    else:
        for item in ultimas:
            pdf.set_x(MARGEN_LATERAL_MM)
            pdf.set_font("Helvetica", "B", 10)
            pdf.set_text_color(*(CORAL if item.tipo == "examen_simulacro" else TEXTO_PRINCIPAL))
            etiqueta = "Examen simulacro" if item.tipo == "examen_simulacro" else "Prueba de unidad"
            pdf.cell(ANCHO_UTIL_MM * 0.65, 6, sanitizar_para_pdf(f"{item.nombre} ({etiqueta})"))
            pdf.set_text_color(*TEXTO_PRINCIPAL)
            pdf.set_font("Helvetica", "", 10)
            nota_texto = f"Nota: {item.nota:.1f}" if item.nota is not None else "Sin nota"
            pdf.cell(ANCHO_UTIL_MM * 0.35, 6, sanitizar_para_pdf(f"{item.fecha.strftime('%d-%m-%Y')} · {nota_texto}"), new_x="LMARGIN", new_y="NEXT")

    pdf.ln(8)
    pdf.set_x(MARGEN_LATERAL_MM)
    pdf.set_font("Helvetica", "I", 9)
    pdf.set_text_color(*TEXTO_SECUNDARIO)
    pdf.multi_cell(
        ANCHO_UTIL_MM, 5,
        "Este informe resume el avance dentro de Logos School y no reemplaza los resultados "
        "oficiales del Examen Libre, emitidos por el Ministerio de Educación o la entidad "
        "examinadora asignada.",
        new_x="LMARGIN", new_y="NEXT",
    )

    return bytes(pdf.output())
