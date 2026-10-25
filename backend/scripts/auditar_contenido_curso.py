"""Audita el contenido de los archivos Markdown locales para verificar estructura y calidad.

Uso:
    python scripts/auditar_contenido_curso.py 01-basico
"""

import sys
from pathlib import Path
import re

sys.path.insert(0, str(Path(__file__).parent))

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


def auditar_curso(carpeta_curso: str):
    """Audita todos los archivos de un curso."""
    curso_dir = CONTENIDO_DIR / carpeta_curso
    
    if not curso_dir.exists():
        print(f"❌ El curso {carpeta_curso} no existe")
        return
    
    print(f"\n🔍 AUDITANDO CURSO: {carpeta_curso}")
    print("=" * 60)
    
    archivos_md = list(curso_dir.glob("*.md"))
    archivos_md = [f for f in archivos_md if f.name != "00-estado-contenido.md"]
    
    if not archivos_md:
        print("❌ No hay archivos Markdown en el curso")
        return
    
    # Verificar si hay carpeta de pruebas separada
    pruebas_dir = curso_dir / "pruebas"
    tiene_pruebas_separadas = pruebas_dir.exists() and list(pruebas_dir.glob("*.md"))
    
    print(f"📚 Encontrados {len(archivos_md)} archivos de contenido")
    if tiene_pruebas_separadas:
        print(f"📝 Encontrados {len(list(pruebas_dir.glob('*.md')))} archivos de pruebas separadas")
        print("   (Las preguntas de autoevaluación están en archivos separados - diseño correcto)")
    print()
    
    total_problemas = 0
    total_observaciones = 0
    
    for archivo_md in archivos_md:
        reporte = auditar_archivo_md(archivo_md, tiene_pruebas_separadas, carpeta_curso)
        
        print(f"\n📖 {reporte['archivo']}")
        print(f"   Longitud: {reporte['longitud_caracteres']} caracteres")
        
        for obs in reporte["observaciones"]:
            print(f"   {obs}")
            total_observaciones += 1
        
        for prob in reporte["problemas"]:
            print(f"   {prob}")
            total_problemas += 1
    
    print("\n" + "=" * 60)
    print(f"📊 RESUMEN:")
    print(f"   Archivos auditados: {len(archivos_md)}")
    print(f"   Observaciones: {total_observaciones}")
    print(f"   Problemas: {total_problemas}")
    
    if total_problemas == 0:
        print("   ✅ NO HAY PROBLEMAS CRÍTICOS")
    else:
        print(f"   ⚠️  HAY {total_problemas} PROBLEMAS QUE REQUIEREN ATENCIÓN")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        curso = sys.argv[1]
    else:
        curso = "01-basico"
    
    auditar_curso(curso)
