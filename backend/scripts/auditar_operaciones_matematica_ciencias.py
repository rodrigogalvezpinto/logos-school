"""
Script de auditoría integral de Matemática y Ciencias (Física / Química / Ciencias Naturales)
para todos los cursos (1° Básico a 4° Medio).

Analiza:
1. Archivos de guías (matematica.md, ciencias-naturales.md, ciencias-para-la-ciudadania.md)
2. Archivos de pruebas por unidad (pruebas/*matematica*, pruebas/*ciencias*)
3. Archivos de exámenes semestrales/finales (examenes/*matematica*, examenes/*ciencias*, examenes/*integrado*)
4. Presencia de operaciones matemáticas, fracciones, potencias, raíces, ecuaciones y fórmulas científicas.
5. Identificación de texto plano ambiguo susceptible a mejora con KaTeX / Markdown interactivo.
"""

import os
import glob
import re
import json

CURSOS = [
    '01-basico', '02-basico', '03-basico', '04-basico',
    '05-basico', '06-basico', '07-basico', '08-basico',
    '01-medio', '02-medio', '03-medio', '04-medio'
]

PATRONES = {
    'fracciones_planas': re.compile(r'(?<![\w$])(\d+/\d+)(?![\w$])'),
    'divisiones_algebraicas': re.compile(r'(?<![\w$])([a-zA-Z]/[a-zA-Z0-9]+)(?![\w$])'),
    'potencias_planas': re.compile(r'([a-zA-Z0-9]+)\^(\d+)'),
    'raices_unicode': re.compile(r'(√\s*[\d\w\(\)]+)'),
    'formulas_fisica': re.compile(
        r'\b(v\s*=\s*d\s*/\s*t|a\s*=\s*\([^)]+\)\s*/\s*t|F\s*=\s*m\s*[\*·•x]\s*a|'
        r'P\s*=\s*m\s*[\*·•x]\s*g|W\s*=\s*F\s*[\*·•x]\s*d|E_?[kc]\s*=\s*1/2|'
        r'E_?p\s*=\s*m\s*[\*·•x]\s*g\s*[\*·•x]\s*h|V\s*=\s*I\s*[\*·•x]\s*R|'
        r'd\s*=\s*m\s*/\s*V|p\s*=\s*m\s*[\*·•x]\s*v)\b',
        re.IGNORECASE
    ),
    'formulas_quimica': re.compile(
        r'\b(pH\s*=\s*-\s*log|M\s*=\s*n\s*/\s*V|mol/L|g/mol|\d+\s*g/mol|\d+\s*mol\b|moles\s*=|concentración\s*molar)',
        re.IGNORECASE
    ),
    'unidades_compuestas': re.compile(r'\b(m/s\^2|km/h|m/s|g/cm\^3|kg/m\^3|N/m\^2|J/kg)\b'),
    'delimitadores_katex': re.compile(r'(\$\$|\\\[|\\\(|\[math\]|\[math:block\]|\[frac:)'),
    'widgets_svg_interactivos': re.compile(r'(\[recta:|\[fraccion:|\:\:emoji\:\:)'),
}

def auditar():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    contenido_dir = os.path.join(repo_root, 'contenido')

    resultados = {
        'resumen_general': {
            'total_cursos': len(CURSOS),
            'total_archivos_auditados': 0,
            'total_lineas': 0,
            'total_operaciones_detectadas': 0,
        },
        'cursos': {},
        'hallazgos_clave': []
    }

    for c in CURSOS:
        base_dir = os.path.join(contenido_dir, c)
        if not os.path.exists(base_dir):
            continue

        archivos_candidatos = []
        # Guías
        for g in ['matematica.md', 'ciencias-naturales.md', 'ciencias-para-la-ciudadania.md', 'fisica.md', 'quimica.md']:
            p = os.path.join(base_dir, g)
            if os.path.exists(p):
                archivos_candidatos.append(('guia', g, p))

        # Pruebas
        pruebas_dir = os.path.join(base_dir, 'pruebas')
        if os.path.exists(pruebas_dir):
            for archivo in os.listdir(pruebas_dir):
                if any(k in archivo for k in ['matematica', 'ciencias', 'fisica', 'quimica', 'algebra', 'geometria', 'probabilidad']):
                    archivos_candidatos.append(('prueba', f'pruebas/{archivo}', os.path.join(pruebas_dir, archivo)))

        # Exámenes
        examenes_dir = os.path.join(base_dir, 'examenes')
        if os.path.exists(examenes_dir):
            for archivo in os.listdir(examenes_dir):
                if any(k in archivo for k in ['matematica', 'ciencias', 'integrado', 'fisica', 'quimica']):
                    archivos_candidatos.append(('examen', f'examenes/{archivo}', os.path.join(examenes_dir, archivo)))

        curso_info = {
            'archivos': [],
            'totales': {k: 0 for k in PATRONES},
            'lineas_totales': 0
        }

        for tipo, rel_name, abs_path in archivos_candidatos:
            try:
                with open(abs_path, 'r', encoding='utf-8') as f:
                    texto = f.read()
            except Exception as e:
                print(f"Error leyendo {abs_path}: {e}")
                continue

            num_lineas = len(texto.splitlines())
            curso_info['lineas_totales'] += num_lineas
            resultados['resumen_general']['total_lineas'] += num_lineas
            resultados['resumen_general']['total_archivos_auditados'] += 1

            conteo_archivo = {}
            muestras_archivo = {}
            for clave, pat in PATRONES.items():
                coincidencias = pat.findall(texto)
                conteo_archivo[clave] = len(coincidencias)
                curso_info['totales'][clave] += len(coincidencias)
                if coincidencias:
                    # Guardar hasta 3 ejemplos
                    muestras_archivo[clave] = [str(m)[:60] for m in coincidencias[:3]]

            curso_info['archivos'].append({
                'nombre': rel_name,
                'tipo': tipo,
                'lineas': num_lineas,
                'conteos': conteo_archivo,
                'muestras': muestras_archivo
            })

        resultados['cursos'][c] = curso_info

    return resultados

if __name__ == '__main__':
    res = auditar()
    
    print("\n" + "="*80)
    print("REPORTE DE AUDITORÍA: MATEMÁTICA Y CIENCIAS CON OPERACIONES (12 CURSOS)")
    print("="*80)
    print(f"Total archivos analizados: {res['resumen_general']['total_archivos_auditados']}")
    print(f"Total líneas de contenido: {res['resumen_general']['total_lineas']:,}")
    print("-" * 80)
    print(f"{'Curso':12} | {'Archivos':8} | {'Líneas':7} | {'Frac':5} | {'Pot/Raíz':8} | {'Fís/Quím':8} | {'KaTeX':6} | {'SVG':5}")
    print("-" * 80)
    
    for c, data in res['cursos'].items():
        t = data['totales']
        pot_raiz = t['potencias_planas'] + t['raices_unicode']
        fis_quim = t['formulas_fisica'] + t['formulas_quimica'] + t['unidades_compuestas']
        print(f"{c:12} | {len(data['archivos']):8} | {data['lineas_totales']:7} | {t['fracciones_planas']:5} | "
              f"{pot_raiz:8} | {fis_quim:8} | {t['delimitadores_katex']:6} | {t['widgets_svg_interactivos']:5}")
    print("="*80)
