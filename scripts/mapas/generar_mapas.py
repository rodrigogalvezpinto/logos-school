"""Genera frontend/src/app/shared/mapas-datos.ts: contornos SVG de América, Sudamérica y Chile.

Fuente: Natural Earth 1:50m (dominio público), redistribuido como TopoJSON en el paquete npm
`world-atlas@2.0.2` (licencia ISC). Para regenerar:
    npm pack world-atlas@2.0.2 && tar xzf world-atlas-2.0.2.tgz
    python3 scripts/mapas/generar_mapas.py package/countries-50m.json
Proyección equirectangular con corrección por coseno de la latitud central: simple y suficiente para
mapas escolares de ubicación (puntos cardinales, países vecinos, zonas).
"""
import json
import math
import sys
from pathlib import Path

SALIDA = Path(__file__).resolve().parents[2] / "frontend/src/app/shared/mapas-datos.ts"

ES = {
    "Argentina": "Argentina", "Bolivia": "Bolivia", "Brazil": "Brasil", "Chile": "Chile", "Colombia": "Colombia",
    "Ecuador": "Ecuador", "Guyana": "Guyana", "Paraguay": "Paraguay", "Peru": "Perú", "Suriname": "Surinam",
    "Uruguay": "Uruguay", "Venezuela": "Venezuela", "Falkland Is.": "_islas", "France": "_guayana",
    "Mexico": "México", "Guatemala": "Guatemala", "Belize": "Belice", "Honduras": "Honduras",
    "El Salvador": "El Salvador", "Nicaragua": "Nicaragua", "Costa Rica": "Costa Rica", "Panama": "Panamá",
    "Cuba": "Cuba", "Haiti": "Haití", "Dominican Rep.": "República Dominicana", "Jamaica": "Jamaica",
    "Puerto Rico": "Puerto Rico", "Bahamas": "Bahamas", "Trinidad and Tobago": "Trinidad y Tobago",
    "United States of America": "Estados Unidos", "Canada": "Canadá", "Greenland": "Groenlandia",
}

# Punto de etiqueta (lat, lon) donde el centroide no sirve: países alargados o con islas lejanas.
CENTROS_FIJOS = {"Chile": (-30.5, -70.8), "Estados Unidos": (39, -98), "Canadá": (58, -105), "Ecuador": (-1.5, -78.3),
                 "Argentina": (-35, -65), "Brasil": (-10, -52), "México": (23.5, -102.5), "Perú": (-9.5, -75)}


def centroide(r):
    """Centroide de un anillo en coordenadas lon/lat (fórmula del área de Gauss)."""
    a = cx = cy = 0.0
    for (x1, y1), (x2, y2) in zip(r, r[1:] + r[:1]):
        f = x1 * y2 - x2 * y1
        a += f
        cx += (x1 + x2) * f
        cy += (y1 + y2) * f
    return (cy / (3 * a), cx / (3 * a)) if a else (r[0][1], r[0][0])


# nombre: (lon_min, lon_max, lat_min, lat_max, alto en px, tolerancia de simplificación en px)
REGIONES = {
    "america": (-170, -30, -56, 75, 520, 0.7),
    "sudamerica": (-82, -34, -56, 13, 460, 0.5),
    "chile": (-77, -64, -56.5, -17, 520, 0.35),
}


def decodificar_arcos(topo):
    sx, sy = topo["transform"]["scale"]
    tx, ty = topo["transform"]["translate"]
    arcos = []
    for arco in topo["arcs"]:
        x = y = 0
        pts = []
        for dx, dy in arco:
            x += dx
            y += dy
            pts.append((x * sx + tx, y * sy + ty))
        arcos.append(pts)
    return arcos


def anillo(arcos, indices):
    pts = []
    for i in indices:
        a = arcos[i] if i >= 0 else list(reversed(arcos[~i]))
        pts.extend(a if not pts else a[1:])
    return pts


def poligonos(geom, arcos):
    if geom["type"] == "Polygon":
        return [[anillo(arcos, r) for r in geom["arcs"]]]
    if geom["type"] == "MultiPolygon":
        return [[anillo(arcos, r) for r in p] for p in geom["arcs"]]
    return []


def simplificar(pts, tol):
    if len(pts) < 4:
        return pts
    def dist(p, a, b):
        (x, y), (x1, y1), (x2, y2) = p, a, b
        dx, dy = x2 - x1, y2 - y1
        if dx == dy == 0:
            return math.hypot(x - x1, y - y1)
        t = max(0, min(1, ((x - x1) * dx + (y - y1) * dy) / (dx * dx + dy * dy)))
        return math.hypot(x - x1 - t * dx, y - y1 - t * dy)
    pila, guardar = [(0, len(pts) - 1)], {0, len(pts) - 1}
    while pila:
        i, j = pila.pop()
        dmax, k = 0, None
        for m in range(i + 1, j):
            d = dist(pts[m], pts[i], pts[j])
            if d > dmax:
                dmax, k = d, m
        if k is not None and dmax > tol:
            guardar.add(k)
            pila += [(i, k), (k, j)]
    return [pts[i] for i in sorted(guardar)]


def main() -> None:
    topo = json.loads(Path(sys.argv[1]).read_text())
    arcos = decodificar_arcos(topo)
    geoms = topo["objects"]["countries"]["geometries"]
    centros = {}
    for g in geoms:
        es = ES.get(g["properties"]["name"])
        if es and not es.startswith("_"):
            mayor = max((pol[0] for pol in poligonos(g, arcos)), key=lambda r: abs(sum(
                x1 * y2 - x2 * y1 for (x1, y1), (x2, y2) in zip(r, r[1:] + r[:1]))))
            lat, lon = CENTROS_FIJOS.get(es, centroide(mayor))
            centros[es] = [round(lat, 2), round(lon, 2)]
    salida = {}
    for nombre, (lo0, lo1, la0, la1, alto, tol) in REGIONES.items():
        k = alto / (la1 - la0)
        c = math.cos(math.radians((la0 + la1) / 2))
        ancho = round((lo1 - lo0) * k * c)
        proy = lambda lon, lat: ((lon - lo0) * k * c, (la1 - lat) * k)
        paises = {}
        for g in geoms:
            es = ES.get(g["properties"]["name"])
            if not es:
                continue
            partes = []
            for pol in poligonos(g, arcos):
                for r in pol:
                    if es == "_guayana":  # de Francia solo interesa la Guayana Francesa
                        r = [p for p in r if -55 < p[0] < -51 and 2 < p[1] < 6.5]
                    if not r or all(not (lo0 - 2 < x < lo1 + 2 and la0 - 2 < y < la1 + 2) for x, y in r):
                        continue
                    pp = simplificar([proy(x, y) for x, y in r], tol)
                    if len(pp) < 3:
                        continue
                    xs, ys = [p[0] for p in pp], [p[1] for p in pp]
                    if max(xs) - min(xs) < 1.2 and max(ys) - min(ys) < 1.2:
                        continue  # islotes que no se verían
                    partes.append("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pp) + "Z")
            if partes:
                paises[es] = paises.get(es, "") + "".join(partes)
        salida[nombre] = {"ancho": ancho, "alto": alto, "lonMin": lo0, "latMax": la1, "k": round(k, 4), "c": round(c, 5), "paises": paises}
    ts = ("// Generado por scripts/mapas/generar_mapas.py a partir de Natural Earth 1:50m (dominio público).\n"
          "// No editar a mano.\n/* eslint-disable */\n"
          "export interface DatosMapa { ancho: number; alto: number; lonMin: number; latMax: number; k: number; c: number; paises: Record<string, string> }\n"
          f"export const MAPAS: Record<string, DatosMapa> = {json.dumps(salida, ensure_ascii=False)};\n"
          "/** Punto de etiqueta de cada país: [latitud, longitud]. */\n"
          f"export const CENTROS: Record<string, [number, number]> = {json.dumps(centros, ensure_ascii=False)};\n")
    SALIDA.write_text(ts, encoding="utf-8")
    print(f"{SALIDA.name}: {len(ts) // 1024} KB; " + ", ".join(f"{n} {len(v['paises'])} países" for n, v in salida.items()))


if __name__ == "__main__":
    main()
