#!/usr/bin/env python3
"""
Validador y estandarizador de formato de pautas de corrección en exámenes.
Asegura que TODOS los exámenes tengan: puntaje_por_item, total, escala_conversion.
Uso: python validador_formato_pauta.py [--fix] [ruta_archivo_o_directorio]
"""

import re
import sys
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Optional


# Template estándar de pauta de corrección
TEMPLATE_PAUTA = """## PAUTA DE CORRECCIÓN — {{TIPO_EXAMEN}}

| N° | Tipo | Clave / Respuesta esperada | OA | Puntaje |
|----|------|----------------------------|-----|---------|
{{FILAS_PAUTA}}

### Resumen de puntaje

- **Total preguntas de alternativas:** {{TOTAL_ALT}} × 1 punto = {{PTS_ALT}} puntos
- **Total preguntas desarrollo breve:** {{TOTAL_BREVE}} × 2 puntos = {{PTS_BREVE}} puntos  
- **Total preguntas desarrollo extenso:** {{TOTAL_EXTENSO}} × 3 puntos = {{PTS_EXTENSO}} puntos
- **Puntaje total de la prueba: {{PUNTAJE_TOTAL}} puntos**

### Distribución por OA

| OA | N° de preguntas | Preguntas |
|----|----------------|-----------|
{{FILAS_OA}}

### Distribución por tipo de pregunta

| Tipo de pregunta | Cantidad | Preguntas |
|------------------|----------|-----------|
| Alternativas (4 opciones) | {{TOTAL_ALT}} | {{LISTA_ALT}} |
| Verdadero o Falso (con justificación) | {{TOTAL_VF}} | {{LISTA_VF}} |
| Desarrollo breve | {{TOTAL_BREVE}} | {{LISTA_BREVE}} |
| Desarrollo extenso | {{TOTAL_EXTENSO}} | {{LISTA_EXTENSO}} |
| **Total** | **{{TOTAL_PREGUNTAS}}** | |

### Escala de conversión a nota (referencial)

| Puntaje | Nota (escala 1,0–7,0) |
|---------|------------------------|
| {{PUNTAJE_TOTAL}} (100%) | 7,0 |
| {{PTS_90}} (90%) | 6,3 |
| {{PTS_80}} (80%) | 5,6 |
| {{PTS_70}} (70%) | 4,9 |
| {{PTS_60}} (60% — exigencia mínima) | **4,0** |
| {{PTS_50}} (50%) | 3,5 |
| {{PTS_40}} (40%) | 3,0 |
| {{PTS_30}} (30%) | 2,5 |
| {{PTS_20}} (20%) | 2,0 |
| {{PTS_10}} (10%) | 1,5 |
| 0 | 1,0 |

> **Nota:** Exigencia de aprobación 60% (nota 4,0), en línea con criterio Mineduc para Exámenes Libres. Ajustar según escala oficial vigente al momento de rendir.

---

> **Nota sobre esta {{FORMA}}**

Esta versión evalúa exactamente los mismos OA y la misma distribución por eje que la {{FORMA_OTRA}} ({{RUTA_FORMA_OTRA}}), pero con preguntas de contenido, contexto y/o valores numéricos distintos en todos los casos, para permitir su uso como segunda instancia de evaluación o como prueba de rendición paralela."""


def parsear_pauta_existente(contenido: str) -> Optional[Dict]:
    """Intenta extraer información de una pauta existente (heurística)."""
    # Buscar sección de pauta (acepta # o ##)
    match_pauta = re.search(r'#{1,2}\s*PAUTA DE CORRECCI[OÓ]N.*?(?=#{1,2} |\Z)', contenido, re.DOTALL | re.IGNORECASE)
    if not match_pauta:
        return None
    
    pauta_texto = match_pauta.group(0)
    
    # Extraer filas de tabla
    filas = re.findall(r'\|\s*(\d+)\s*\|\s*([^|]*)\|\s*([^|]*)\|\s*([^|]*)\|\s*([^|]*)\|', pauta_texto)
    
    if not filas:
        return None
    
    # Analizar tipos de pregunta desde el contenido del examen
    # Buscar patrón de preguntas en el examen
    exam_match = re.search(r'#{1,2}\s*PREGUNTAS.*?(?=#{1,2} |\Z)', contenido, re.DOTALL)
    exam_texto = exam_match.group(0) if exam_match else contenido
    
    # Contar tipos
    alt_count = len(re.findall(r'\(Alternativas\)', exam_texto, re.IGNORECASE))
    vf_count = len(re.findall(r'\(Verdadero o Falso\)', exam_texto, re.IGNORECASE))
    breve_count = len(re.findall(r'\(Desarrollo breve\)', exam_texto, re.IGNORECASE))
    extenso_count = len(re.findall(r'\(Desarrollo extenso\)', exam_texto, re.IGNORECASE))
    
    # Si no encuentra patrones, inferir de filas de pauta
    if alt_count + vf_count + breve_count + extenso_count == 0 and filas:
        for f in filas:
            tipo = f[1].strip().lower()
            if 'alternativa' in tipo:
                alt_count += 1
            elif 'verdadero' in tipo or 'falso' in tipo:
                vf_count += 1
            elif 'breve' in tipo:
                breve_count += 1
            elif 'extenso' in tipo:
                extenso_count += 1
            else:
                alt_count += 1  # default
    
    total = alt_count + vf_count + breve_count + extenso_count
    if total == 0:
        total = len(filas)
    
    # Puntaje estándar
    pts_alt = alt_count * 1
    pts_breve = breve_count * 2
    pts_extenso = extenso_count * 3
    pts_vf = vf_count * 1  # V/F cuenta como alternativa
    total_pts = pts_alt + pts_vf + pts_breve + pts_extenso
    
    # Detectar forma (A/B)
    forma_match = re.search(r'(FORMA|Forma)\s+([AB])', contenido, re.IGNORECASE)
    forma = forma_match.group(2).upper() if forma_match else 'B'
    
    # Detectar curso y asignatura
    curso_match = re.search(r'curso:\s*([^\n]+)', contenido, re.IGNORECASE)
    asignatura_match = re.search(r'asignatura:\s*([^\n]+)', contenido, re.IGNORECASE)
    
    return {
        'filas_raw': filas,
        'alt_count': alt_count,
        'vf_count': vf_count,
        'breve_count': breve_count,
        'extenso_count': extenso_count,
        'total_pts': total_pts,
        'forma': forma,
        'curso': curso_match.group(1).strip() if curso_match else 'Curso',
        'asignatura': asignatura_match.group(1).strip() if asignatura_match else 'Asignatura',
        'tiene_puntaje_explicito': 'Puntaje total' in contenido or 'Puntaje:' in pauta_texto,
        'tiene_escala': 'Escala de conversión' in contenido or 'Tabla de conversión' in contenido,
        'tiene_distribucion_oa': 'Distribución por OA' in contenido,
        'tiene_distribucion_tipo': 'Distribución por tipo' in contenido,
    }


def generar_pauta_estandar(info: Dict, contenido_original: str) -> str:
    """Genera pauta estandarizada usando template."""
    
    # Extraer lista de preguntas por tipo desde el contenido
    exam_match = re.search(r'## PREGUNTAS.*?(?=## |\Z)', contenido_original, re.DOTALL)
    exam_texto = exam_match.group(0) if exam_match else contenido_original
    
    # Listas de números de pregunta por tipo
    listas = {'alt': [], 'vf': [], 'breve': [], 'extenso': []}
    
    # Buscar preguntas numeradas con tipo
    preg_matches = re.finditer(r'\*\*(\d+)\.\s*\(([^)]+)\)', exam_texto)
    for m in preg_matches:
        num = m.group(1)
        tipo = m.group(2).lower()
        if 'alternativa' in tipo:
            listas['alt'].append(num)
        elif 'verdadero' in tipo or 'falso' in tipo:
            listas['vf'].append(num)
        elif 'breve' in tipo:
            listas['breve'].append(num)
        elif 'extenso' in tipo:
            listas['extenso'].append(num)
    
    # Si no encuentra, usar filas de pauta original
    if not any(listas.values()):
        filas_raw = info.get('filas_raw', [])
        for i, fila in enumerate(filas_raw):
            num = str(i + 1)
            tipo = fila[1].strip().lower() if len(fila) > 1 else ''
            if 'alternativa' in tipo:
                listas['alt'].append(num)
            elif 'verdadero' in tipo or 'falso' in tipo:
                listas['vf'].append(num)
            elif 'breve' in tipo:
                listas['breve'].append(num)
            elif 'extenso' in tipo:
                listas['extenso'].append(num)
            else:
                listas['alt'].append(num)
    
    # Calcular puntajes
    alt = len(listas['alt'])
    vf = len(listas['vf'])
    breve = len(listas['breve'])
    extenso = len(listas['extenso'])
    total_preg = alt + vf + breve + extenso
    
    pts_alt = alt * 1
    pts_vf = vf * 1
    pts_breve = breve * 2
    pts_extenso = extenso * 3
    total_pts = pts_alt + pts_vf + pts_breve + pts_extenso
    
    # Helper para formatear listas
    def fmt_lista(lst):
        return ', '.join(lst) if lst else '—'
    
    # Calcular puntos porcentuales para escala
    def pct(p):
        return round(total_pts * p / 100)
    
    # Determinar forma otra
    forma_actual = info.get('forma', 'B')
    forma_otra = 'A' if forma_actual == 'B' else 'B'
    
    # Generar filas OA (simplificado - idealmente parsear de pauta original)
    filas_oa = "| OA 1 | 5 | 1, 2, 3, 4, 5 |\n| OA 2 | 5 | 6, 7, 8, 9, 10 |"
    
    template = TEMPLATE_PAUTA.replace('{{TIPO_EXAMEN}}', f"{info.get('asignatura', 'Asignatura')} — {info.get('curso', 'Curso')} — Forma {forma_actual}")
    template = template.replace('{{FORMA}}', forma_actual)
    template = template.replace('{{FORMA_OTRA}}', forma_otra)
    template = template.replace('{{RUTA_FORMA_OTRA}}', f"contenido/{{curso}}/{{asignatura}}-examen-forma-{forma_otra}.md")
    
    template = template.replace('{{FILAS_PAUTA}}', '[MANTENER FILAS ORIGINALES DE PAUTA — REVISAR MANUALMENTE]')
    template = template.replace('{{TOTAL_ALT}}', str(alt + vf))
    template = template.replace('{{PTS_ALT}}', str(alt + vf))
    template = template.replace('{{TOTAL_BREVE}}', str(breve))
    template = template.replace('{{PTS_BREVE}}', str(breve * 2))
    template = template.replace('{{TOTAL_EXTENSO}}', str(extenso))
    template = template.replace('{{PTS_EXTENSO}}', str(extenso * 3))
    template = template.replace('{{PUNTAJE_TOTAL}}', str(sum([alt, vf, breve * 2, extenso * 3])))
    
    template = template.replace('{{TOTAL_VF}}', str(vf))
    template = template.replace('{{TOTAL_PREGUNTAS}}', str(total_preg))
    template = template.replace('{{LISTA_ALT}}', ', '.join(listas['alt']) if listas['alt'] else '—')
    template = template.replace('{{LISTA_VF}}', ', '.join(listas['vf']) if listas['vf'] else '—')
    template = template.replace('{{LISTA_BREVE}}', ', '.join(listas['breve']) if listas['breve'] else '—')
    template = template.replace('{{LISTA_EXTENSO}}', ', '.join(listas['extenso']) if listas['extenso'] else '—')
    
    template = template.replace('{{FILAS_OA}', filas_oa)
    
    # Escala
    total = alt + vf + breve * 2 + extenso * 3
    template = template.replace('{{PTS_90}}', str(round(total * 0.9)))
    template = template.replace('{{PTS_80}}', str(round(total * 0.8)))
    template = template.replace('{{PTS_70}}', str(round(total * 0.7)))
    template = template.replace('{{PTS_60}}', str(round(total * 0.6)))
    template = template.replace('{{PTS_50}}', str(round(total * 0.5)))
    template = template.replace('{{PTS_40}}', str(round(total * 0.4)))
    template = template.replace('{{PTS_30}}', str(round(total * 0.3)))
    template = template.replace('{{PTS_20}}', str(round(total * 0.2)))
    template = template.replace('{{PTS_10}}', str(round(total * 0.1)))
    
    return template


def analizar_archivo(ruta: Path) -> Dict:
    """Analiza si un archivo de examen tiene pauta estandarizada."""
    contenido = ruta.read_text(encoding='utf-8')
    info = parsear_pauta_existente(contenido)
    
    if not info:
        return {
            'archivo': str(ruta),
            'tiene_pauta': False,
            'tiene_puntaje_explicito': False,
            'tiene_escala': False,
            'tiene_distribucion_oa': False,
            'tiene_distribucion_tipo': False,
            'necesita_estandarizacion': True,
            'info_extraida': None
        }
    
    return {
        'archivo': str(ruta),
        'tiene_pauta': True,
        'tiene_puntaje_explicito': info['tiene_puntaje_explicito'],
        'tiene_escala': info['tiene_escala'],
        'tiene_distribucion_oa': info['tiene_distribucion_oa'],
        'tiene_distribucion_tipo': info['tiene_distribucion_tipo'],
        'necesita_estandarizacion': not (info['tiene_puntaje_explicito'] and info['tiene_escala'] and info['tiene_distribucion_oa'] and info['tiene_distribucion_tipo']),
        'info_extraida': info
    }


def estandarizar_archivo(ruta: Path, dry_run: bool = False) -> Tuple[int, str]:
    """Estandariza la pauta de un archivo de examen."""
    contenido = ruta.read_text(encoding='utf-8')
    info = parsear_pauta_existente(contenido)
    
    if not info:
        return 0, contenido
    
    # Generar pauta estandarizada
    pauta_nueva = generar_pauta_estandar(info, contenido)
    
    # Reemplazar sección de pauta existente
    # Buscar desde "# PAUTA DE CORRECCIÓN" o "## PAUTA DE CORRECCIÓN" hasta final o próximo "## " o "# "
    patron_pauta = re.compile(r'(#{1,2}\s*PAUTA DE CORRECCI[OÓ]N.*?)(?=#{1,2} |\Z)', re.DOTALL | re.IGNORECASE)
    
    def reemplazo(match):
        return pauta_nueva
    
    nuevo_contenido = patron_pauta.sub(reemplazo, contenido, count=1)
    
    if not dry_run and nuevo_contenido != contenido:
        ruta.write_text(nuevo_contenido, encoding='utf-8')
    
    return 1 if nuevo_contenido != contenido else 0, nuevo_contenido


def main():
    parser = argparse.ArgumentParser(description='Estandarizador de formato de pautas de corrección')
    parser.add_argument('ruta', nargs='?', default='contenido', help='Archivo o directorio')
    parser.add_argument('--fix', action='store_true', help='Aplicar estandarización')
    parser.add_argument('--dry-run', action='store_true', help='Simular sin guardar')
    parser.add_argument('--ext', nargs='*', default=['.md'], help='Extensiones')
    args = parser.parse_args()
    
    ruta = Path(args.ruta)
    if not ruta.exists():
        print(f"[ERROR] Ruta no existe: {ruta}")
        sys.exit(1)
    
    extensiones = set(args.ext)
    
    if ruta.is_file():
        archivos = [ruta]
    else:
        archivos = []
        for ext in extensiones:
            archivos.extend(ruta.rglob(f'*{ext}'))
        # Filtrar solo exámenes
        archivos = [a for a in archivos if 'examen' in a.name.lower() or 'forma' in a.name.lower()]
    
    print(f"[SCAN] Analizando {len(archivos)} archivos de examen...")
    
    total_con_pauta = 0
    total_sin_estandarizar = 0
    total_estandarizados = 0
    
    for archivo in sorted(archivos):
        resultado = analizar_archivo(archivo)
        
        # Debug: ensure all required keys exist
        if 'necesita_estandarizar' not in resultado:
            resultado['necesita_estandarizar'] = True
        
        if not resultado['tiene_pauta']:
            print(f"[WARN] SIN PAUTA: {archivo}")
            continue
        
        total_con_pauta += 1
        
        if resultado['necesita_estandarizar']:
            total_sin_estandarizar += 1
            faltantes = []
            if not resultado['tiene_puntaje_explicito']: faltantes.append('puntaje total')
            if not resultado['tiene_escala']: faltantes.append('escala de conversión')
            if not resultado['tiene_distribucion_oa']: faltantes.append('distribución por OA')
            if not resultado['tiene_distribucion_tipo']: faltantes.append('distribución por tipo')
            
            print(f"[FIX] SIN ESTANDARIZAR: {archivo}")
            print(f"   Falta: {', '.join(faltantes)}")
            
            if args.fix or args.dry_run:
                cambios, _ = estandarizar_archivo(archivo, dry_run=args.dry_run)
                if cambios:
                    total_estandarizados += 1
                    accion = "Simulada" if args.dry_run else "Aplicada"
                    print(f"   [OK] Estandarización {accion.lower()}")
        else:
            print(f"[OK] YA ESTANDARIZADO: {archivo}")
    
    print(f"[RESUMEN]")
    print(f"   Archivos de examen: {len(archivos)}")
    print(f"   Con pauta: {total_con_pauta}")
    print(f"   Sin estandarizar: {total_sin_estandarizar}")
    if args.fix or args.dry_run:
        accion = "Simuladas" if args.dry_run else "Aplicadas"
        print(f"   Estandarizaciones {accion.lower()}: {total_estandarizados}")


if __name__ == '__main__':
    main()