"""Descarga/impresión de guía en PDF (Fase 1, ítem 2.5 del plan de incorporación de
hallazgos de Brincus — ver planificacion/27-plan-incorporacion-hallazgos-brincus.md).

Usa `fpdf2` (puro Python, sin dependencias de sistema como Cairo/Pango que sí necesita
WeasyPrint) — deliberado: Fase 1 se acotó a ítems sin dependencias externas, y esto se
sirve directo desde el propio backend con el visor nativo del navegador, sin el Adobe
Document Cloud View SDK que usa Brincus para mostrar sus PDFs (ver el hallazgo de
seguridad en planificacion/25-analisis-competencia-brincus.md, Paso 11: Brincus expone sus
PDFs en una URL pública descargable sin sesión — acá el PDF se genera on-demand detrás del
mismo endpoint autenticado que ya protege el resto del contenido de estudio).

Conversión de Markdown deliberadamente simple (títulos, viñetas, párrafos, negrita quitada
de los asteriscos) — no un renderer de Markdown completo, cubre lo que realmente usa el
contenido de `contenido/` (ver `MarkdownPipe` del frontend para la versión con fidelidad
completa que sí se muestra en pantalla). Los dos realces especiales ("¿Por qué importa?" y
"Ejemplo N — Título") replican, con las primitivas de fpdf2, el mismo realce visual que ya
tiene la guía en pantalla (ver frontend/src/app/shared/markdown.pipe.ts) — para que el PDF
descargado no se vea plano en comparación.

Bug real corregido acá (reportado como "mal centrado"): `multi_cell()` deja el cursor X en
el borde derecho del bloque por defecto (`new_x="RIGHT"`), no en el margen izquierdo — sin
pasar `new_x="LMARGIN"` en cada llamada, cada línea nueva heredaba la X de la anterior y el
contenido derivaba hacia la derecha hasta salirse de la página."""

import re

from fpdf import FPDF

from app.infrastructure.pdf.pdf_marca import (
    ANCHO_UTIL_MM,
    CORAL,
    INDIGO_SUAVE,
    MARGEN_LATERAL_MM,
    PDFConMarca,
    TEXTO_PRINCIPAL,
    dibujar_insignia,
)
from app.infrastructure.pdf.sanitizar_texto import sanitizar_para_pdf

RE_POR_QUE_IMPORTA = re.compile(r"^\*\*¿Por qué importa\?\*\*\s*(.*)$")
RE_EJEMPLO = re.compile(r"^\*\*Ejemplo\s+(\d+)\s*—\s*(.*?)\*\*$")


def _quitar_enfasis(texto: str) -> str:
    texto = re.sub(r"\*\*(.+?)\*\*", r"\1", texto)
    texto = re.sub(r"\*(.+?)\*", r"\1", texto)
    return sanitizar_para_pdf(texto)


def _caja_por_que_importa(pdf: FPDF, cuerpo: str) -> None:
    pdf.set_x(MARGEN_LATERAL_MM)
    pdf.set_fill_color(*INDIGO_SUAVE)
    pdf.set_text_color(*TEXTO_PRINCIPAL)
    pdf.set_font("Helvetica", "B", 11)
    pdf.multi_cell(ANCHO_UTIL_MM, 7, sanitizar_para_pdf("¿Por qué importa?"), fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(MARGEN_LATERAL_MM)
    pdf.set_font("Helvetica", "", 11)
    pdf.multi_cell(ANCHO_UTIL_MM, 6, _quitar_enfasis(cuerpo), fill=True, new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)


def _titulo_ejemplo(pdf: FPDF, numero: str, titulo: str) -> None:
    pdf.set_x(MARGEN_LATERAL_MM)
    pdf.set_draw_color(*INDIGO_SUAVE)
    pdf.set_line_width(0.4)
    pdf.line(MARGEN_LATERAL_MM, pdf.get_y(), MARGEN_LATERAL_MM + ANCHO_UTIL_MM, pdf.get_y())
    pdf.ln(3)
    y = pdf.get_y()
    pdf.set_fill_color(*CORAL)
    pdf.ellipse(MARGEN_LATERAL_MM, y, 6, 6, style="F")
    pdf.set_text_color(255, 255, 255)
    pdf.set_font("Helvetica", "B", 9)
    pdf.set_xy(MARGEN_LATERAL_MM, y + 0.6)
    pdf.cell(6, 5, numero, align="C")
    pdf.set_text_color(*TEXTO_PRINCIPAL)
    pdf.set_font("Helvetica", "B", 11)
    pdf.set_xy(MARGEN_LATERAL_MM + 8, y)
    pdf.cell(ANCHO_UTIL_MM - 8, 6, _quitar_enfasis(titulo), new_x="LMARGIN", new_y="NEXT")
    pdf.set_x(MARGEN_LATERAL_MM)
    pdf.set_y(y + 8)


def generar_pdf_guia(codigo_oficial: str, descripcion: str, contenido_markdown: str) -> bytes:
    pdf = PDFConMarca(format="A4")
    pdf.set_auto_page_break(auto=True, margin=22)
    pdf.add_page()
    pdf.set_left_margin(MARGEN_LATERAL_MM)
    pdf.set_right_margin(MARGEN_LATERAL_MM)

    dibujar_insignia(pdf, codigo_oficial)
    pdf.ln(2)

    pdf.set_font("Helvetica", "B", 16)
    pdf.set_text_color(*TEXTO_PRINCIPAL)
    pdf.multi_cell(ANCHO_UTIL_MM, 9, sanitizar_para_pdf(descripcion), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    for linea_cruda in contenido_markdown.splitlines():
        linea = linea_cruda.strip()
        if not linea:
            pdf.ln(2)
            continue
        pdf.set_x(MARGEN_LATERAL_MM)

        m_importa = RE_POR_QUE_IMPORTA.match(linea)
        m_ejemplo = RE_EJEMPLO.match(linea)

        if m_importa:
            _caja_por_que_importa(pdf, m_importa.group(1))
        elif m_ejemplo:
            _titulo_ejemplo(pdf, m_ejemplo.group(1), m_ejemplo.group(2))
        elif linea.startswith("#### "):
            # "Ejemplos resueltos" en algunos cursos usa #### en vez de ### (la misma
            # variación que ya se corrigió en el pipe de Markdown del frontend) — sin este
            # caso, el "####" literal se imprimía tal cual en el PDF.
            pdf.set_font("Helvetica", "B", 11)
            pdf.set_text_color(*CORAL)
            pdf.multi_cell(ANCHO_UTIL_MM, 7, _quitar_enfasis(linea[5:]), new_x="LMARGIN", new_y="NEXT")
        elif linea.startswith("### "):
            pdf.set_font("Helvetica", "B", 12)
            pdf.set_text_color(*TEXTO_PRINCIPAL)
            pdf.multi_cell(ANCHO_UTIL_MM, 7, _quitar_enfasis(linea[4:]), new_x="LMARGIN", new_y="NEXT")
        elif linea.startswith("## "):
            pdf.set_font("Helvetica", "B", 13)
            pdf.set_text_color(*TEXTO_PRINCIPAL)
            pdf.multi_cell(ANCHO_UTIL_MM, 8, _quitar_enfasis(linea[3:]), new_x="LMARGIN", new_y="NEXT")
        elif linea.startswith("# "):
            pdf.set_font("Helvetica", "B", 14)
            pdf.set_text_color(*TEXTO_PRINCIPAL)
            pdf.multi_cell(ANCHO_UTIL_MM, 8, _quitar_enfasis(linea[2:]), new_x="LMARGIN", new_y="NEXT")
        elif linea.startswith(("- ", "* ")):
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(*TEXTO_PRINCIPAL)
            # "-" en vez de "•": la fuente Helvetica core (sin Unicode embebido, para no
            # sumar dependencias) no soporta el carácter de viñeta. Se pinta de color coral
            # para que al menos destaque, ya que no puede ser un punto redondo real.
            pdf.set_text_color(*CORAL)
            pdf.set_font("Helvetica", "B", 11)
            pdf.cell(5, 6, "-")
            pdf.set_text_color(*TEXTO_PRINCIPAL)
            pdf.set_font("Helvetica", "", 11)
            pdf.multi_cell(ANCHO_UTIL_MM - 5, 6, _quitar_enfasis(linea[2:]), new_x="LMARGIN", new_y="NEXT")
        else:
            pdf.set_font("Helvetica", "", 11)
            pdf.set_text_color(*TEXTO_PRINCIPAL)
            pdf.multi_cell(ANCHO_UTIL_MM, 6, _quitar_enfasis(linea), new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())
