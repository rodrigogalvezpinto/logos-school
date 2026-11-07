"""Identidad de marca compartida por todos los PDFs de Logos School (guía de estudio,
certificado de alumno regular): banda de encabezado con el logo + "Logos School", pie de
página con numeración, y una insignia de color reutilizable para chips tipo "OA 2" o
"4° básico" (ver la lista de útiles de Brincus como referencia de estilo — pill naranja
bajo el título).

Dibujado con las primitivas vectoriales de fpdf2 (rect/polygon/line), no con una imagen
embebida ni una fuente TTF nueva — a propósito, para no sumar dependencias externas (ver
la nota de "Fase 1 sin dependencias externas" en generador_guia.py). El logo es una
recreación simplificada, en formas rectas, del ícono real en
frontend/src/app/shared/logo/logo.ts (dos páginas de libro superpuestas + un trazo
ascendente) — fpdf2 core no soporta las curvas Bézier del SVG original.
"""

from fpdf import FPDF

from app.infrastructure.pdf.sanitizar_texto import sanitizar_para_pdf

INDIGO = (91, 79, 233)
INDIGO_OSCURO = (70, 56, 201)
INDIGO_SUAVE = (238, 236, 253)
CORAL = (255, 107, 74)
BLANCO = (255, 255, 255)
TEXTO_PRINCIPAL = (20, 19, 43)
TEXTO_SECUNDARIO = (110, 110, 125)

ALTO_ENCABEZADO_MM = 26
MARGEN_LATERAL_MM = 14
ANCHO_UTIL_MM = 210 - 2 * MARGEN_LATERAL_MM


class PDFConMarca(FPDF):
    """FPDF con el encabezado y pie de página de marca dibujados automáticamente en cada
    página — fpdf2 llama a `header()`/`footer()` en cada `add_page()` (incluyendo los
    saltos de página automáticos), así que no hay que invocarlos a mano."""

    def header(self) -> None:
        self.set_fill_color(*INDIGO)
        self.rect(0, 0, self.w, ALTO_ENCABEZADO_MM, style="F")

        x0, y0 = MARGEN_LATERAL_MM, 7
        # Dos "páginas" superpuestas de un libro abierto.
        self.set_fill_color(*BLANCO)
        self.polygon([(x0, y0 + 2), (x0 + 6, y0), (x0 + 6, y0 + 12), (x0, y0 + 10)], style="F")
        self.set_fill_color(*INDIGO_SUAVE)
        self.polygon([(x0 + 12, y0 + 2), (x0 + 6, y0), (x0 + 6, y0 + 12), (x0 + 12, y0 + 10)], style="F")
        # Trazo ascendente coral, como el "camino" del ícono original.
        self.set_draw_color(*CORAL)
        self.set_line_width(0.9)
        self.line(x0 + 2, y0 + 7.5, x0 + 5, y0 + 4)
        self.line(x0 + 5, y0 + 4, x0 + 8, y0 + 7)
        self.line(x0 + 8, y0 + 7, x0 + 10.5, y0 + 3)

        self.set_xy(x0 + 18, y0)
        self.set_font("Helvetica", "B", 15)
        self.set_text_color(*BLANCO)
        self.cell(0, 12, "Logos School", new_x="LMARGIN", new_y="TOP")

        self.set_y(ALTO_ENCABEZADO_MM + 8)
        self.set_text_color(*TEXTO_PRINCIPAL)

    def footer(self) -> None:
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.set_text_color(*TEXTO_SECUNDARIO)
        self.cell(
            0, 6,
            sanitizar_para_pdf(f"Logos School — material de estudio para Exámenes Libres · Página {self.page_no()}"),
            align="C",
        )


def dibujar_insignia(pdf: FPDF, texto: str, color: tuple[int, int, int] = CORAL, centrar: bool = False) -> None:
    """Chip de color con texto blanco en negrita (ej. "OA 2", "4° básico"), al estilo de
    la píldora naranja de la lista de útiles de Brincus. Deja el cursor debajo del chip,
    listo para el siguiente elemento."""
    texto = sanitizar_para_pdf(texto)
    pdf.set_font("Helvetica", "B", 10)
    ancho = pdf.get_string_width(texto) + 8
    x, y = pdf.get_x(), pdf.get_y()
    if centrar:
        x = (pdf.w - ancho) / 2
    pdf.set_fill_color(*color)
    pdf.rect(x, y, ancho, 7, style="F", round_corners=True, corner_radius=3.5)
    pdf.set_text_color(*BLANCO)
    pdf.set_xy(x, y)
    pdf.cell(ancho, 7, texto, align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*TEXTO_PRINCIPAL)
    pdf.set_x(MARGEN_LATERAL_MM)
