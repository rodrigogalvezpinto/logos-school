#!/usr/bin/env python3
"""
Validador de anglicismos en contenido educativo (texto en español).
Detecta palabras en inglés que no deben aparecer en material en español.
Uso: python validador_anglicismos.py [--fix] [ruta_archivo_o_directorio]
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple


# SOLO anglicismos REALMENTE detectados en auditoría + mitos factuaules
# NO incluir términos técnicos válidos en contexto educativo (persona, auto, pan, error, etc.)
ANGLICISMOS_PROHIBIDOS = {
    # Detectados en auditoría real (con evidencia)
    'population': 'población',           # 8° básico Historia: "cantidad de population"
    'information': 'información',        # 1° medio Lengua: "information implícita"; 1° medio Inglés
    'dimensions': 'dimensiones',         # 1° medio Ciencias: "tres dimensions"
    'welcome': 'vuelta atrás',           # 2° medio Lengua: "welcome de vuelta" (examen)
    
    # Mitos factuaules corregidos
    'amazon rainforest produces about 20% of the world\'s oxygen': 
        'la selva amazonica produce alrededor del 6-9% de la fotosintesis global (contribucion neta aprox 0%)',
    
    # Errores físicos detectados
    'red shift when approaching': 'corrimiento al azul al acercarse',
    'redshift when approaching': 'corrimiento al azul al acercarse',
    'doppler red shift when approaching': 'efecto Doppler: corrimiento al azul al acercarse',
}


def cargar_diccionario_anglicismos() -> Dict[str, str]:
    """Retorna diccionario {anglicismo: sugerencia_español}."""
    return ANGLICISMOS_PROHIBIDOS


DICCIONARIO = cargar_diccionario_anglicismos()


def detectar_anglicismos(texto: str) -> List[Tuple[str, int, str]]:
    """
    Detecta anglicismos en un texto.
    Retorna lista de (palabra_encontrada, posicion, sugerencia).
    """
    hallazgos = []
    
    for anglicismo, sugerencia in DICCIONARIO.items():
        # Patrón: palabra completa o frase, case-insensitive
        patron = re.compile(re.escape(anglicismo), re.IGNORECASE)
        for match in patron.finditer(texto):
            hallazgos.append((match.group(), match.start(), sugerencia))
    
    # Ordenar por posición
    hallazgos.sort(key=lambda x: x[1])
    return hallazgos


def analizar_archivo(ruta: Path) -> Dict:
    """Analiza un archivo buscando anglicismos."""
    try:
        contenido = ruta.read_text(encoding='utf-8')
    except Exception as e:
        return {'archivo': str(ruta), 'error': str(e), 'hallazgos': []}
    
    hallazgos = detectar_anglicismos(contenido)
    
    # Agrupar por palabra única
    unicos = {}
    for palabra, pos, sug in hallazgos:
        key = palabra.lower()
        if key not in unicos:
            unicos[key] = {'palabra_original': palabra, 'sugerencia': sug, 'ocurrencias': 0, 'posiciones': []}
        unicos[key]['ocurrencias'] += 1
        unicos[key]['posiciones'].append(pos)
    
    return {
        'archivo': str(ruta),
        'total_hallazgos': len(hallazgos),
        'palabras_unicas': len(unicos),
        'detalle': unicos
    }


def corregir_archivo(ruta: Path, dry_run: bool = False) -> Tuple[int, str]:
    """Corrige anglicismos en un archivo (reemplaza por sugerencia en español)."""
    contenido = ruta.read_text(encoding='utf-8')
    original = contenido
    cambios = 0
    
    # Ordenar por longitud descendente para evitar reemplazos parciales
    anglicismos_ordenados = sorted(DICCIONARIO.keys(), key=len, reverse=True)
    
    for anglicismo in anglicismos_ordenados:
        sugerencia = DICCIONARIO[anglicismo]
        # Reemplazar case-insensitive
        def reemplazo(match):
            nonlocal cambios
            cambios += 1
            return sugerencia
        
        patron = re.compile(re.escape(anglicismo), re.IGNORECASE)
        contenido = patron.sub(reemplazo, contenido)
    
    if not dry_run and contenido != original:
        ruta.write_text(contenido, encoding='utf-8')
    
    return cambios, contenido


def main():
    parser = argparse.ArgumentParser(description='Validador/Corrector de anglicismos en contenido español')
    parser.add_argument('ruta', nargs='?', default='contenido', help='Archivo o directorio a validar')
    parser.add_argument('--fix', action='store_true', help='Aplicar correcciones automáticas')
    parser.add_argument('--dry-run', action='store_true', help='Simular correcciones sin guardar')
    parser.add_argument('--ext', nargs='*', default=['.md', '.txt'], help='Extensiones de archivo a procesar')
    args = parser.parse_args()
    
    ruta = Path(args.ruta)
    
    if not ruta.exists():
        print(f"[ERROR] Ruta no existe: {ruta}")
        sys.exit(1)
    
    extensiones = set(args.ext)
    
    def es_archivo_ingles(ruta: Path) -> bool:
        """Detecta si el archivo pertenece a la asignatura Inglés (contenido en inglés esperado)."""
        partes = ruta.parts
        for parte in partes:
            if 'ingles' in parte.lower() or 'english' in parte.lower():
                return True
        return False


    if ruta.is_file():
        if ruta.suffix not in extensiones:
            print(f"[WARN] Extensión {ruta.suffix} no está en lista permitida")
        if es_archivo_ingles(ruta):
            print(f"[SKIP] Archivo de Inglés (contenido en inglés esperado): {ruta}")
            return
        resultado = analizar_archivo(ruta)
        print(f"\n[FILE] {resultado['archivo']}")
        print(f"   Total hallazgos: {resultado['total_hallazgos']}")
        print(f"   Palabras únicas: {resultado['palabras_unicas']}")
        for palabra, info in resultado['detalle'].items():
            print(f"   - '{info['palabra_original']}' -> '{info['sugerencia']}' ({info['ocurrencias']}x)")
        
        if args.fix or args.dry_run:
            cambios, _ = corregir_archivo(ruta, dry_run=args.dry_run)
            accion = "Simulados" if args.dry_run else "Aplicados"
            print(f"   {accion} {cambios} correcciones")
    else:
        archivos = []
        for ext in extensiones:
            archivos.extend(ruta.rglob(f'*{ext}'))
        
        print(f"[SCAN] Escaneando {len(archivos)} archivos en {ruta}...")
        
        total_archivos_con_hallazgos = 0
        total_hallazgos = 0
        total_cambios = 0
        
        for archivo in sorted(archivos):
            if es_archivo_ingles(archivo):
                continue
            resultado = analizar_archivo(archivo)
            if resultado.get('total_hallazgos', 0) > 0:
                total_archivos_con_hallazgos += 1
                total_hallazgos += resultado['total_hallazgos']
                print(f"\n[FILE] {resultado['archivo']}")
                print(f"   {resultado['total_hallazgos']} hallazgos ({resultado['palabras_unicas']} unicos)")
                for palabra, info in resultado['detalle'].items():
                    print(f"   - '{info['palabra_original']}' -> '{info['sugerencia']}' ({info['ocurrencias']}x)")
                
                if args.fix or args.dry_run:
                    cambios, _ = corregir_archivo(archivo, dry_run=args.dry_run)
                    total_cambios += cambios
                    accion = "Simulados" if args.dry_run else "Aplicados"
                    print(f"   {accion} {cambios} correcciones")
        
        print(f"\n[RESUMEN]")
        print(f"   Archivos escaneados: {len(archivos)}")
        print(f"   Archivos con anglicismos: {total_archivos_con_hallazgos}")
        print(f"   Total hallazgos: {total_hallazgos}")
        if args.fix or args.dry_run:
            accion = "Simuladas" if args.dry_run else "Aplicadas"
            print(f"   Correcciones {accion}: {total_cambios}")


if __name__ == '__main__':
    main()