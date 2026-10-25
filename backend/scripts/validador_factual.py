#!/usr/bin/env python3
"""
Validador de precisión factual en contenido educativo.
Detecta afirmaciones científicamente imprecisas conocidas (ej. mito Amazonas 20% O₂).
Uso: python validador_factual.py [--fix] [ruta_archivo_o_directorio]
"""

import re
import sys
import argparse
from pathlib import Path
from typing import List, Dict, Tuple


# Base de conocimiento de imprecisiones factuaules detectadas + comunes
IMPRECISIONES_FACTUALES = [
    {
        'id': 'amazonas-oxigeno-20',
        'patron': r'amazonas?\s+(?:produce|genera|aporta|suministra)\s+(?:alrededor\s+de\s+|aproximadamente\s+|cerca\s+de\s+|~?\s*)?20%?\s+(?:del\s+)?ox[ií]geno\s+(?:mundial|atmosf[eé]rico|global|planetario)',
        'descripcion': 'Mito: "El Amazonas produce el 20% del oxígeno mundial"',
        'correccion': 'La contribución neta del Amazonas al O₂ atmosférico es cercana a cero (su ecosistema consume la mayor parte del que produce); la cifra bruta real es ~6-9% de la fotosíntesis global.',
        'fuente': 'Consenso científico: NASA, NOAA, estudios de biogeoquímica (ej. Malhi et al., 2008; Yadvinder Malhi)'
    },
    {
        'id': 'amazonas-pulmon-mundo',
        'patron': r'amazonas?\s+(?:es|funciona\s+como)\s+(?:el\s+)?pulm[oó]n\s+(?:del\s+mundo|del\s+planeta|mundial)',
        'descripcion': 'Mito: "El Amazonas es el pulmón del mundo"',
        'correccion': 'El Amazonas no es el "pulmón del mundo"; los océanos (fitoplancton) producen >50% del O₂. El Amazonas es vital por biodiversidad y captura de carbono, no por producción neta de oxígeno.',
        'fuente': 'NASA Earth Observatory, IPCC, estudios de ciclo del carbono'
    },
    {
        'id': 'doppler-luz-rojo-acercarse',
        'patron': r'(?:corrimiento|desplazamiento)\s+(?:al\s+rojo|hacia\s+el\s+rojo)\s+(?:al\s+acercarse|cuando\s+se\s+acerca|en\s+el\s+acercamiento)',
        'descripcion': 'Error: Corrimiento al rojo al acercarse (Doppler luz)',
        'correccion': 'Al acercarse una fuente de luz, el corrimiento es hacia el AZUL (blue shift). El corrimiento al rojo (redshift) ocurre al ALEJARSE.',
        'fuente': 'Física óptica: efecto Doppler relativista, corrimiento Doppler'
    },
    {
        'id': 'martenes-cambrian-explosion',
        'patron': r'explosi[oó]n\s+c[ae]mbrica\s+(?:fue\s+)?hace\s+540\s+millones\s+(?:de\s+años)?',
        'descripcion': 'Fecha imprecisa: Explosión cámbrica hace 540 millones de años',
        'correccion': 'La explosión cámbrica comenzó hace ~538-541 millones de años (inicio del Cámbrico), no exactamente 540.',
        'fuente': 'Escala temporal geológica ICS 2024, base Cámbrico 538.8±0.2 Ma'
    },
    {
        'id': 'dinosaurios-extincion-65',
        'patron': r'(?:extinci[oó]n\s+(?:de\s+los\s+)?dinosaurios|impacto\s+(?:de\s+)?chicxulub)\s+(?:fue\s+)?hace\s+65\s+millones\s+(?:de\s+años)?',
        'descripcion': 'Fecha imprecisa: Extinción dinosaurios hace 65 millones de años',
        'correccion': 'El impacto de Chicxulub y la extinción K-Pg ocurrieron hace 66 millones de años (66.043±0.011 Ma), no 65.',
        'fuente': 'Escala temporal geológica ICS 2024, límite K-Pg 66.043 Ma'
    },
    {
        'id': 'chile-territorio-756',
        'patron': r'chile\s+tiene\s+(?:un\s+)?territorio\s+de\s+756\s+(?:mil\s+)?km[²2]',
        'descripcion': 'Cifra imprecisa: Territorio Chile 756 mil km²',
        'correccion': 'Chile continental: 756.102 km²; incluyendo territorio antártico reclamado: 1.250.257,6 km². Preferir "aproximadamente 756 mil km²" o especificar.',
        'fuente': 'IGN Chile, decreto 1.554/2007 (territorio antártico)'
    },
    {
        'id': 'poblacion-chile-19',
        'patron': r'chile\s+tiene\s+(?:una\s+)?poblaci[oó]n\s+de\s+19\s+millones',
        'descripcion': 'Cifra desactualizada: Población Chile 19 millones',
        'correccion': 'Población estimada 2024: ~19,6-19,8 millones (INE). Usar "cerca de 20 millones" o citar año y fuente.',
        'fuente': 'INE Chile, proyecciones 2024'
    },
    {
        'id': 'velocidad-luz-300000',
        'patron': r'velocidad\s+(?:de\s+la\s+)?luz\s+(?:es|es\s+de)\s+300\.?000\s+km/s',
        'descripcion': 'Cifra redondeada imprecisa: Velocidad luz 300.000 km/s',
        'correccion': 'Velocidad de la luz en el vacío: 299.792,458 km/s (exacta por definición). 300.000 km/s es una aproximación grosera.',
        'fuente': 'SI (Sistema Internacional), CODATA 2018'
    },
    {
        'id': 'adn-doble-helice-watson-crick',
        'patron': r'(?:watson\s+y\s+crick|watson\s*[&y]\s*crick)\s+(?:descubrieron|determinaron)\s+la\s+(?:estructura\s+del\s+)?adn\s+(?:en\s+1953)?',
        'descripcion': 'Omisión: Estructura ADN - Rosalind Franklin',
        'correccion': 'Watson y Crick propusieron el modelo de doble hélice (1953) basándose en datos de difracción de rayos X de Rosalind Franklin y Maurice Wilkins. Franklin no recibió crédito pleno en vida.',
        'fuente': 'Historia de la ciencia molecular, Nobel 1962 (Watson, Crick, Wilkins)'
    },
    {
        'id': 'newton-manzana-gravedad',
        'patron': r'newton\s+(?:descubri[oó]|entendi[oó])\s+la\s+gravedad\s+(?:al\s+caerle\s+)?una\s+manzana',
        'descripcion': 'Mito: Newton descubrió la gravedad por una manzana',
        'correccion': 'Newton formuló la ley de gravitación universal; la anécdota de la manzana es posterior y probablemente apócrifa. La gravedad ya se conocía (caída de cuerpos, órbitas planetarias).',
        'fuente': 'Historia de la ciencia, Principia Mathematica 1687, correspondencia de Newton'
    },
    {
        'id': 'einstein-mal-estudiante',
        'patron': r'einstein\s+(?:fue\s+)?mal\s+estudiante\s+(?:en\s+matem[aá]ticas?)?',
        'descripcion': 'Mito: Einstein fue mal estudiante de matemáticas',
        'correccion': 'Einstein destacó en matemáticas y física desde joven; reprobó el examen de ingreso al Politécnico de Zúrich a los 16 años por no saber suficiente francés, no por matemáticas.',
        'fuente': 'Biografías de Einstein, documentos escolares (Notenbuch)'
    },
    {
        'id': 'colon-descubrio-america',
        'patron': r'col[oó]n\s+(?:descubri[oó]|lleg[oó]\s+a)\s+am[eé]rica\s+(?:en\s+1492)?',
        'descripcion': 'Mito/imprecisión: Colón "descubrió" América',
        'correccion': 'Colón llegó al Caribe en 1492; América ya estaba poblada hace >15.000 años por pueblos originarios. Los vikingos (Leif Erikson) llegaron a Terranova ~1000 d.C. No hubo "descubrimiento" sino encuentro europeo.',
        'fuente': 'Arqueología, genética poblacional, sagas nórdicas, historiografía crítica'
    },
    {
        'id': 'galileo-torre-pisa',
        'patron': r'galileo\s+(?:tir[oó]|lanz[oó])\s+(?:dos\s+)?esferas\s+(?:desde\s+la\s+)?torre\s+de\s+pisa',
        'descripcion': 'Mito: Galileo tiró esferas de la Torre de Pisa',
        'correccion': 'No hay evidencia histórica de que Galileo hiciera este experimento en la Torre de Pisa; es un experimento mental descrito por sus discípulos (Viviani). Galileo usó planos inclinados.',
        'fuente': 'Historia de la física, obras de Galileo, correspondencia de Viviani'
    },
    {
        'id': 'marie-curie-unica-mujer-nobel',
        'patron': r'marie\s+curie\s+(?:fue\s+)?la\s+(?:primera\s+|sola\s+|única\s+)?mujer\s+(?:en\s+ganar\s+el\s+)?nobel',
        'descripcion': 'Imprecisión: Marie Curie "única/primera mujer Nobel"',
        'correccion': 'Marie Curie: primera mujer en ganar Nobel (Física 1903, compartido), primera en ganar dos Nobel (Física 1903, Química 1911), única en dos ciencias distintas. No "única mujer" (hay >60 mujeres Nobel desde 1901).',
        'fuente': 'Fundación Nobel, lista oficial laureados'
    },
]


def detectar_imprecisiones(contenido: str) -> List[Dict]:
    """Detecta imprecisiones factuaules en un texto."""
    hallazgos = []
    
    for regla in IMPRECISIONES_FACTUALES:
        patron = re.compile(regla['patron'], re.IGNORECASE | re.MULTILINE)
        for match in patron.finditer(contenido):
            # Obtener contexto (línea completa)
            inicio_linea = contenido.rfind('\n', 0, match.start()) + 1
            fin_linea = contenido.find('\n', match.end())
            if fin_linea == -1:
                fin_linea = len(contenido)
            linea = contenido[inicio_linea:fin_linea].strip()
            
            hallazgos.append({
                'id': regla['id'],
                'descripcion': regla['descripcion'],
                'correccion': regla['correccion'],
                'fuente': regla['fuente'],
                'texto_encontrado': match.group(),
                'linea': linea,
                'posicion': match.start()
            })
    
    return hallazgos


def analizar_archivo(ruta: Path) -> Dict:
    """Analiza un archivo buscando imprecisiones factuaules."""
    try:
        contenido = ruta.read_text(encoding='utf-8')
    except Exception as e:
        return {'archivo': str(ruta), 'error': str(e), 'hallazgos': []}
    
    hallazgos = detectar_imprecisiones(contenido)
    
    return {
        'archivo': str(ruta),
        'total': len(hallazgos),
        'hallazgos': hallazgos
    }


def corregir_archivo(ruta: Path, dry_run: bool = False) -> Tuple[int, str]:
    """Aplica correcciones automáticas donde sea posible (solo para casos con patrón claro)."""
    contenido = ruta.read_text(encoding='utf-8')
    original = contenido
    cambios = 0
    
    # Solo correcciones seguras y automáticas
    correcciones_automaticas = [
        # Amazonas 20% → nota correctiva
        (r'(amazonas?\s+(?:produce|genera|aporta|suministra)\s+(?:alrededor\s+de\s+|aproximadamente\s+|cerca\s+de\s+|~?\s*)?20%?\s+(?:del\s+)?ox[ií]geno\s+(?:mundial|atmosf[eé]rico|global|planetario))',
         lambda m: m.group(1) + ' [NOTA: La contribución neta del Amazonas al O₂ atmosférico es cercana a cero; la cifra bruta es ~6-9% de la fotosíntesis global.]'),
        
        # Doppler rojo al acercarse → corregir a azul
        (r'(corrimiento|desplazamiento)\s+(?:al\s+rojo|hacia\s+el\s+rojo)\s+(?:al\s+acercarse|cuando\s+se\s+acerca|en\s+el\s+acercamiento)',
         lambda m: m.group(0).replace('rojo', 'AZUL').replace('al acercarse', 'al ALEJARSE').replace('cuando se acerca', 'cuando se ALEJA').replace('en el acercamiento', 'en el ALEJAMIENTO')),
    ]
    
    for patron, reemplazo in correcciones_automaticas:
        def repl_func(match):
            nonlocal cambios
            cambios += 1
            return reemplazo(match)
        
        contenido = re.sub(patron, repl_func, contenido, flags=re.IGNORECASE)
    
    if not dry_run and contenido != original:
        ruta.write_text(contenido, encoding='utf-8')
    
    return cambios, contenido


def main():
    parser = argparse.ArgumentParser(description='Validador de precisión factual en contenido educativo')
    parser.add_argument('ruta', nargs='?', default='contenido', help='Archivo o directorio a validar')
    parser.add_argument('--fix', action='store_true', help='Aplicar correcciones automáticas seguras')
    parser.add_argument('--dry-run', action='store_true', help='Simular correcciones sin guardar')
    parser.add_argument('--ext', nargs='*', default=['.md', '.txt'], help='Extensiones a procesar')
    args = parser.parse_args()
    
    ruta = Path(args.ruta)
    
    if not ruta.exists():
        print(f"[ERROR] Ruta no existe: {ruta}")
        sys.exit(1)
    
    extensiones = set(args.ext)
    
    if ruta.is_file():
        if ruta.suffix not in extensiones:
            print(f"⚠️ Extensión {ruta.suffix} no está en lista permitida")
        resultado = analizar_archivo(ruta)
        print(f"\n[FILE] {resultado['archivo']}")
        print(f"   Imprecisiones detectadas: {resultado['total']}")
        for h in resultado['hallazgos']:
            print(f"   - [{h['id']}] {h['descripcion']}")
            print(f"     Encontrado: \"{h['texto_encontrado']}\"")
            print(f"     Corrección: {h['correccion']}")
            print(f"     Fuente: {h['fuente']}")
        
        if args.fix or args.dry_run:
            cambios, _ = corregir_archivo(ruta, dry_run=args.dry_run)
            accion = "Simulados" if args.dry_run else "Aplicados"
            print(f"   {accion} {cambios} correcciones automáticas")
    else:
        archivos = []
        for ext in extensiones:
            archivos.extend(ruta.rglob(f'*{ext}'))
        
        print(f"[SCAN] Escaneando {len(archivos)} archivos en {ruta}...")
        
        total_archivos_con_hallazgos = 0
        total_hallazgos = 0
        total_cambios = 0
        
        for archivo in sorted(archivos):
            resultado = analizar_archivo(archivo)
            if resultado.get('total', 0) > 0:
                total_archivos_con_hallazgos += 1
                total_hallazgos += resultado['total']
                print(f"\n[FILE] {resultado['archivo']}")
                print(f"   {resultado['total']} imprecisiones detectadas")
                for h in resultado['hallazgos']:
                    print(f"   - [{h['id']}] {h['descripcion']}")
                    print(f"     Texto: \"{h['texto_encontrado'][:80]}...\"")
                    print(f"     Corrección: {h['correccion'][:100]}...")
                
                if args.fix or args.dry_run:
                    cambios, _ = corregir_archivo(archivo, dry_run=args.dry_run)
                    total_cambios += cambios
                    accion = "Simulados" if args.dry_run else "Aplicados"
                    print(f"   {accion} {cambios} correcciones")
        
        print(f"[RESUMEN]")
        print(f"   Archivos escaneados: {len(archivos)}")
        print(f"   Archivos con imprecisiones: {total_archivos_con_hallazgos}")
        print(f"   Total imprecisiones: {total_hallazgos}")
        if args.fix or args.dry_run:
            accion = "Simuladas" if args.dry_run else "Aplicadas"
            print(f"   Correcciones automáticas {accion}: {total_cambios}")


if __name__ == '__main__':
    main()