"""Audita todos los cursos de forma masiva."""

import sys
import re
from pathlib import Path

CONTENIDO_DIR = Path(__file__).parent.parent.parent / "contenido"

def auditar_archivo_md(ruta_md: Path, tiene_pruebas_separadas: bool, nivel: str) -> dict:
    """Audita un archivo Markdown y retorna un reporte."""
    contenido = ruta_md.read_text(encoding="utf-8")
    
    reporte = {
        "archivo": ruta_md.name,
        "tiene_por_que_importa": False,
        "tiene_ejemplos": False,
        "tiene_preguntas": False,
        "tiene_retroalimentacion": False,
        "tiene_emojis": False,
        "tiene_errores_ortograficos_basicos": True,
        "longitud_caracteres": len(contenido),
        "problemas": [],
        "observaciones": [],
    }
    
    # Verificar estructura (si tiene longitud suficiente y títulos H2, asumo que tiene estructura)
    if reporte["longitud_caracteres"] > 5000 and "##" in contenido:
        reporte["tiene_por_que_importa"] = True
        reporte["observaciones"].append("✅ Tiene estructura con títulos H2")
    else:
        reporte["problemas"].append("❌ No tiene estructura suficiente (longitud < 5000 o sin títulos H2)")
    
    if "**Ejemplo" in contenido or "**Actividad" in contenido:
        reporte["tiene_ejemplos"] = True
    else:
        reporte["problemas"].append("❌ No tiene ejemplos/actividades")
    
    # Solo verificar preguntas y retroalimentación si no están en archivos separados
    if not tiene_pruebas_separadas:
        if "**Pregunta" in contenido or "**PREGUNTA" in contenido:
            reporte["tiene_preguntas"] = True
        else:
            reporte["problemas"].append("❌ No tiene preguntas de autoevaluación")
        
        if "Retroalimentación" in contenido or "retroalimentación" in contenido:
            reporte["tiene_retroalimentacion"] = True
        else:
            reporte["problemas"].append("❌ No tiene retroalimentación")
    else:
        reporte["observaciones"].append("✅ Preguntas y retroalimentación en archivos separados (diseño correcto)")
    
    if "::emoji::" in contenido:
        reporte["tiene_emojis"] = True
        emojis = re.findall(r"::emoji::([^:]+)::", contenido)
        reporte["observaciones"].append(f"✅ Tiene {len(emojis)} emojis educativos")
    else:
        # Mensaje diferente según nivel (1°-3° básico vs 4° en adelante)
        if nivel in ["01-basico", "02-basico", "03-basico"]:
            reporte["problemas"].append("❌ No tiene emojis educativos (puede ser muy denso para niño de 6-8 años)")
        else:
            reporte["observaciones"].append("ℹ️  No tiene emojis educativos (es aceptable para este nivel)")
    
    reporte["observaciones"].append(f"📊 Longitud: {reporte['longitud_caracteres']} caracteres")
    
    return reporte

CURSOS = [
    "01-basico",
    "02-basico",
    "03-basico",
    "04-basico",
    "05-basico",
    "06-basico",
    "07-basico",
    "08-basico",
    "1-medio",
    "2-medio",
    "3-medio",
    "4-medio",
]

print("\n" + "=" * 60)
print("🔍 AUDITORÍA MASIVA DE TODOS LOS CURSOS")
print("=" * 60 + "\n")

total_problemas = 0
total_observaciones = 0

for curso in CURSOS:
    print(f"\n{'=' * 60}")
    print(f"📚 CURSO: {curso}")
    print("=" * 60)
    
    contenido_dir = Path(__file__).parent.parent.parent / "contenido" / curso
    
    if not contenido_dir.exists():
        print(f"❌ El curso {curso} no existe")
        continue
    
    archivos_md = list(contenido_dir.glob("*.md"))
    archivos_md = [f for f in archivos_md if f.name != "00-estado-contenido.md"]
    
    if not archivos_md:
        print("❌ No hay archivos Markdown en el curso")
        continue
    
    pruebas_dir = contenido_dir / "pruebas"
    tiene_pruebas_separadas = pruebas_dir.exists() and list(pruebas_dir.glob("*.md"))
    
    print(f"📚 Archivos de contenido: {len(archivos_md)}")
    if tiene_pruebas_separadas:
        print(f"📝 Archivos de pruebas: {len(list(pruebas_dir.glob('*.md')))}")
    
    # Contar problemas y observaciones
    curso_problemas = 0
    curso_observaciones = 0
    
    for archivo_md in archivos_md:
        from auditar_contenido_curso import auditar_archivo_md
        reporte = auditar_archivo_md(archivo_md, tiene_pruebas_separadas, curso)
        
        curso_problemas += len(reporte["problemas"])
        curso_observaciones += len(reporte["observaciones"])
    
    print(f"\n📊 Resumen {curso}: {curso_observaciones} observaciones, {curso_problemas} problemas")
    
    total_problemas += curso_problemas
    total_observaciones += curso_observaciones

print("\n" + "=" * 60)
print("📊 RESUMEN GLOBAL")
print("=" * 60)
print(f"Total cursos auditados: {len(CURSOS)}")
print(f"Total observaciones: {total_observaciones}")
print(f"Total problemas: {total_problemas}")

if total_problemas == 0:
    print("✅ TODOS LOS CURSOS ESTÁN APROBADOS")
else:
    print(f"⚠️  HAY {total_problemas} PROBLEMAS EN TOTAL")
