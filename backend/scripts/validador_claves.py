#!/usr/bin/env python3
"""
Validador de distribución de claves en exámenes de alternativas.
Regla: ninguna letra (a,b,c,d) debe superar 45% del total de preguntas de alternativas.
Uso: python validador_claves.py [--fix] [ruta_archivo_o_directorio]
"""

import re
import sys
import argparse
from pathlib import Path
from collections import Counter
from typing import List, Tuple, Dict


def extraer_claves_alternativas(contenido: str) -> List[str]:
    """Extrae las claves correctas de alternativas de la pauta de corrección."""
    claves = []
    
    # Buscar en la tabla de pauta de corrección
    # Patrón: | N | ... | **X)** ... | ... |
    patron_pauta = re.compile(r'\|\s*\d+\s*\|\s*[^|]*\|\s*\*\*([abcd])\)')
    
    # También buscar en texto: "Respuesta correcta: X)" o "Clave: X)"
    patron_inline = re.compile(r'(?:Respuesta correcta|Clave)[:\s]*\*\*?([abcd])\)?', re.IGNORECASE)
    
    for match in patron_pauta.finditer(contenido):
        claves.append(match.group(1).lower())
    
    for match in patron_inline.finditer(contenido):
        claves.append(match.group(1).lower())
    
    return claves


def analizar_archivo(ruta: Path) -> Dict:
    """Analiza un archivo y retorna estadísticas de claves."""
    contenido = ruta.read_text(encoding='utf-8')
    claves = extraer_claves_alternativas(contenido)
    
    if not claves:
        return {
            'archivo': str(ruta),
            'total': 0,
            'distribucion': {},
            'excede_45': False,
            'letra_max': None,
            'porcentaje_max': 0
        }
    
    total = len(claves)
    dist = Counter(claves)
    letra_max, count_max = dist.most_common(1)[0]
    pct_max = (count_max / total) * 100
    
    return {
        'archivo': str(ruta),
        'total': total,
        'distribucion': dict(dist),
        'excede_45': pct_max > 45,
        'letra_max': letra_max,
        'porcentaje_max': round(pct_max, 1)
    }


def rebalancear_claves(contenido: str) -> str:
    """
    Rebalancea las claves en la pauta de corrección para que ninguna letra > 45%.
    Estrategia: rotar claves sobrantes hacia letras deficitarias.
    """
    # Extraer todas las claves actuales con sus posiciones
    lineas = contenido.split('\n')
    claves_info = []  # (linea_idx, letra_original, match_obj)
    
    patron = re.compile(r'(\|\s*\d+\s*\|[^|]*\|\s*)\*\*([abcd])\)')
    
    for i, linea in enumerate(lineas):
        match = patron.search(linea)
        if match:
            claves_info.append((i, match.group(2).lower(), match))
    
    if not claves_info:
        return contenido
    
    total = len(claves_info)
    dist_actual = Counter(c[1] for c in claves_info)
    objetivo_max = int(total * 0.45)
    
    # Calcular cuántas de cada letra necesitamos mover
    letras = ['a', 'b', 'c', 'd']
    excesos = {}
    deficit = {}
    
    for letra in letras:
        count = dist_actual.get(letra, 0)
        if count > objetivo_max:
            excesos[letra] = count - objetivo_max
        elif count < objetivo_max:
            deficit[letra] = objetivo_max - count
    
    if not excesos:
        return contenido  # Ya está balanceado
    
    # Redistribuir: cambiar claves en exceso hacia letras en déficit
    letras_deficit = []
    for letra, cant in deficit.items():
        letras_deficit.extend([letra] * cant)
    
    idx_deficit = 0
    nuevas_lineas = lineas.copy()
    
    for linea_idx, letra_orig, match in claves_info:
        if letra_orig in excesos and excesos[letra_orig] > 0 and idx_deficit < len(letras_deficit):
            nueva_letra = letras_deficit[idx_deficit]
            idx_deficit += 1
            excesos[letra_orig] -= 1
            
            # Reemplazar en la línea
            inicio, fin = match.span(2)
            linea_original = lineas[linea_idx]
            nueva_linea = linea_original[:inicio] + nueva_letra + linea_original[fin:]
            nuevas_lineas[linea_idx] = nueva_linea
    
    return '\n'.join(nuevas_lineas)


def procesar_directorio(directorio: Path, fix: bool = False) -> List[Dict]:
    """Procesa todos los archivos de examen en un directorio."""
    resultados = []
    
    # Buscar archivos de examen Forma B e integrados
    patrones = [
        '*-forma-b.md',
        'examen-integrado-forma-*.md'
    ]
    
    archivos = set()
    for patron in patrones:
        archivos.update(directorio.rglob(patron))
    
    for archivo in sorted(archivos):
        resultado = analizar_archivo(archivo)
        resultados.append(resultado)
        
        if fix and resultado['excede_45']:
            print(f"[FIX] Rebalanceando: {archivo} (max: {resultado['letra_max']} {resultado['porcentaje_max']}%)")
            contenido = archivo.read_text(encoding='utf-8')
            nuevo_contenido = rebalancear_claves(contenido)
            archivo.write_text(nuevo_contenido, encoding='utf-8')
            
            # Verificar resultado
            nuevo_resultado = analizar_archivo(archivo)
            print(f"   -> Nuevo max: {nuevo_resultado['letra_max']} {nuevo_resultado['porcentaje_max']}%")
        elif resultado['excede_45']:
            print(f"[WARN] EXCEDE 45%: {archivo} — {resultado['letra_max']}={resultado['porcentaje_max']}% ({resultado['distribucion']})")
        elif resultado['total'] > 0:
            print(f"[OK] {archivo} — max {resultado['letra_max']} {resultado['porcentaje_max']}%")
    
    return resultados


def main():
    parser = argparse.ArgumentParser(description='Validador de distribución de claves (máx 45%)')
    parser.add_argument('ruta', nargs='?', default='contenido', help='Archivo o directorio a validar')
    parser.add_argument('--fix', action='store_true', help='Aplicar rebalanceo automático')
    args = parser.parse_args()
    
    ruta = Path(args.ruta)
    
    if not ruta.exists():
        print(f"❌ Ruta no existe: {ruta}")
        sys.exit(1)
    
    if ruta.is_file():
        resultado = analizar_archivo(ruta)
        print(f"Archivo: {resultado['archivo']}")
        print(f"Total alternativas: {resultado['total']}")
        print(f"Distribución: {resultado['distribucion']}")
        if resultado['excede_45']:
            print(f"⚠️ EXCEDE 45%: {resultado['letra_max']} = {resultado['porcentaje_max']}%")
            if args.fix:
                contenido = ruta.read_text(encoding='utf-8')
                nuevo = rebalancear_claves(contenido)
                ruta.write_text(nuevo, encoding='utf-8')
                print("✅ Rebalanceado aplicado")
        else:
            print("✅ Dentro de límites")
    else:
        print(f"Escaneando directorio: {ruta}")
        resultados = procesar_directorio(ruta, args.fix)
        
        total_archivos = len(resultados)
        con_exceso = sum(1 for r in resultados if r['excede_45'])
        print(f"[RESUMEN] {total_archivos} archivos, {con_exceso} exceden 45%")


if __name__ == '__main__':
    main()