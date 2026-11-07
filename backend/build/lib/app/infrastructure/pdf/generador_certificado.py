"""Certificado de alumno regular (Fase 1, ítem 2.7 del plan de incorporación de
hallazgos de Brincus — ver planificacion/27-plan-incorporacion-hallazgos-brincus.md).

Verificado en Brincus: el tutorial se titula literalmente "¿Cómo descargar el
Certificado de Alumno Regular?" — un documento de conveniencia para trámites (subsidios,
seguros, etc.), NO un certificado oficial de aprobación del Examen Libre (eso lo emite
Mineduc/la entidad examinadora, no una plataforma de apoyo de estudio). Este documento se
limita a esa misma idea: una constancia simple de que el alumno está inscrito y
estudiando en Logos School, sin implicar ningún reconocimiento oficial."""

from datetime import date

from app.infrastructure.pdf.pdf_marca import (
    ANCHO_UTIL_MM,
    INDIGO,
    MARGEN_LATERAL_MM,
    PDFConMarca,
    TEXTO_PRINCIPAL,
    TEXTO_SECUNDARIO,
    dibujar_insignia,
)
from app.infrastructure.pdf.sanitizar_texto import sanitizar_para_pdf


def generar_pdf_certificado(nombre_completo: str, nivel_nombre: str, fecha: date) -> bytes:
    nombre_completo = sanitizar_para_pdf(nombre_completo)
    nivel_nombre = sanitizar_para_pdf(nivel_nombre)
    pdf = PDFConMarca(format="A4")
    pdf.add_page()
    pdf.set_left_margin(MARGEN_LATERAL_MM)
    pdf.set_right_margin(MARGEN_LATERAL_MM)

    pdf.ln(4)
    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*TEXTO_PRINCIPAL)
    pdf.set_x(MARGEN_LATERAL_MM)
    pdf.cell(ANCHO_UTIL_MM, 10, "Certificado de Alumno Regular", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)
    dibujar_insignia(pdf, nivel_nombre, color=INDIGO, centrar=True)

    pdf.ln(10)
    pdf.set_font("Helvetica", "", 12)
    pdf.set_text_color(*TEXTO_PRINCIPAL)
    pdf.set_x(MARGEN_LATERAL_MM)
    texto = (
        f"Se certifica que {nombre_completo} se encuentra actualmente inscrito/a y "
        f"estudiando en Logos School, en el nivel de {nivel_nombre}, como preparación "
        "para los Exámenes Libres de Validación de Estudios del Ministerio de "
        "Educación de Chile."
    )
    pdf.multi_cell(ANCHO_UTIL_MM, 8, texto, align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 10)
    pdf.set_text_color(*TEXTO_SECUNDARIO)
    pdf.set_x(MARGEN_LATERAL_MM)
    pdf.multi_cell(
        ANCHO_UTIL_MM,
        6,
        "Este documento es una constancia de inscripción emitida por Logos School. "
        "No reemplaza ni certifica la aprobación del Examen Libre, que es emitida "
        "únicamente por el Ministerio de Educación o la entidad examinadora asignada.",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.ln(14)
    pdf.set_font("Helvetica", "", 11)
    pdf.set_text_color(*TEXTO_PRINCIPAL)
    pdf.set_x(MARGEN_LATERAL_MM)
    pdf.cell(ANCHO_UTIL_MM, 8, f"Emitido el {fecha.strftime('%d-%m-%Y')}", align="C", new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())
