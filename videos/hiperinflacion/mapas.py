"""Mapas animados con datos reales de Natural Earth (dominio público).

Proyección Mercator en grados; la cámara se define por (lon, lat, zoom) donde zoom = píxeles por grado.
"""
import json
import math
import os
import pickle

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
DATOS = os.path.join(AQUI, "datos")
W, H = 1920, 1080


def merc_y(lat):
    lat = max(-84.0, min(84.0, lat))
    return math.degrees(math.log(math.tan(math.pi / 4 + math.radians(lat) / 2)))


def _merc_np(lon, lat):
    lat = np.clip(lat, -84, 84)
    return lon, np.degrees(np.log(np.tan(np.pi / 4 + np.radians(lat) / 2)))


def _cargar():
    cache = os.path.join(DATOS, "cache_mapa.pkl")
    if os.path.exists(cache):
        with open(cache, "rb") as fh:
            return pickle.load(fh)
    paises = {}
    d = json.load(open(os.path.join(DATOS, "ne_50m_admin_0_countries.geojson")))
    for ft in d["features"]:
        p = ft["properties"]
        g = ft["geometry"]
        polys = g["coordinates"] if g["type"] == "MultiPolygon" else [g["coordinates"]]
        anillos = []
        for poly in polys:
            ring = np.array(poly[0], dtype=float)
            x, y = _merc_np(ring[:, 0], ring[:, 1])
            anillos.append(np.stack([x, y], 1))
        allp = np.concatenate(anillos)
        paises[p["ADM0_A3"]] = dict(nombre=p["NAME_ES"], lx=p["LABEL_X"], ly=p["LABEL_Y"], anillos=anillos,
                                    bbox=(allp[:, 0].min(), allp[:, 1].min(), allp[:, 0].max(), allp[:, 1].max()),
                                    rank=p.get("LABELRANK", 5))
    rios = []
    d = json.load(open(os.path.join(DATOS, "ne_50m_rivers_lake_centerlines.geojson")))
    for ft in d["features"]:
        g = ft["geometry"]
        if not g:
            continue
        lines = g["coordinates"] if g["type"] == "MultiLineString" else [g["coordinates"]]
        for ln in lines:
            a = np.array(ln, dtype=float)
            x, y = _merc_np(a[:, 0], a[:, 1])
            rios.append(np.stack([x, y], 1))
    ciudades = []
    d = json.load(open(os.path.join(DATOS, "ne_50m_populated_places_simple.geojson")))
    for ft in d["features"]:
        p = ft["properties"]
        ciudades.append(dict(nombre=p["name"], lon=p["longitude"], lat=p["latitude"], cap=p["adm0cap"] == 1,
                             pais=p["adm0_a3"], pop=p["pop_max"] or 0))
    datos = dict(paises=paises, rios=rios, ciudades=ciudades)
    with open(cache, "wb") as fh:
        pickle.dump(datos, fh)
    return datos


D = _cargar()


class Camara:
    def __init__(self, lon, lat, zoom):
        self.cx, self.cy, self.z = lon, merc_y(lat), zoom

    def p(self, lon, lat):
        return (W / 2 + (lon - self.cx) * self.z, H / 2 - (merc_y(lat) - self.cy) * self.z)

    def pm(self, arr):
        return np.stack([W / 2 + (arr[:, 0] - self.cx) * self.z, H / 2 - (arr[:, 1] - self.cy) * self.z], 1)

    def ve(self, bbox, margen=200):
        x0 = W / 2 + (bbox[0] - self.cx) * self.z
        x1 = W / 2 + (bbox[2] - self.cx) * self.z
        y0 = H / 2 - (bbox[3] - self.cy) * self.z
        y1 = H / 2 - (bbox[1] - self.cy) * self.z
        return x1 > -margen and x0 < W + margen and y1 > -margen and y0 < H + margen


def vista_pais(iso, relleno=0.55, dx=0.0):
    """Cámara (lon, lat, zoom) que encuadra el país principal (anillo más grande)."""
    p = D["paises"][iso]
    grande = max(p["anillos"], key=len)
    x0, y0 = grande.min(0)
    x1, y1 = grande.max(0)
    z = min(W * relleno / max(x1 - x0, 1e-3), H * relleno / max(y1 - y0, 1e-3))
    cy = (y0 + y1) / 2
    lat = math.degrees(2 * math.atan(math.exp(math.radians(cy))) - math.pi / 2)
    return ((x0 + x1) / 2 - dx * W / z, lat, z)


def interp_vista(a, b, p):
    """Vuelo: zoom en escala logarítmica, centro interpolado en coordenadas Mercator."""
    la, lb = math.log(a[2]), math.log(b[2])
    # pequeña salida hacia atrás en vuelos largos para dar sensación de altura
    dist = abs(a[0] - b[0]) + abs(merc_y(a[1]) - merc_y(b[1]))
    sube = min(1.2, dist / 60) * math.sin(math.pi * p)
    z = math.exp(la + (lb - la) * p - sube)
    ya, yb = merc_y(a[1]), merc_y(b[1])
    # el centro avanza más rápido cuando estamos lejos (zoom bajo)
    q = p
    lon = a[0] + (b[0] - a[0]) * q
    y = ya + (yb - ya) * q
    lat = math.degrees(2 * math.atan(math.exp(math.radians(y))) - math.pi / 2)
    return (lon, lat, z)


def _ruta(pts):
    r = np.round(pts).astype(int)
    keep = np.ones(len(r), bool)
    keep[1:] = np.any(np.abs(np.diff(r, axis=0)) > 1, axis=1)
    r = r[keep]
    if len(r) < 3:
        return ""
    return "M" + " L".join(f"{x} {y}" for x, y in r) + " Z"


def _linea(pts):
    r = np.round(pts).astype(int)
    keep = np.ones(len(r), bool)
    keep[1:] = np.any(np.abs(np.diff(r, axis=0)) > 2, axis=1)
    r = r[keep]
    if len(r) < 2:
        return ""
    return "M" + " L".join(f"{x} {y}" for x, y in r)


# paleta del mapa
OCEANO1, OCEANO2 = "#0E2A3B", "#081A26"
TIERRA = "#D9CBA8"
TIERRA_OSC = "#BFAE88"
BORDE = "#7D6E52"
RESALTE = "#E4572E"


def mapa(cam, t, resaltar=(), atenuar=False, rios=True, etiquetas=True, tinte=None, colores=None, fino=False):
    """Devuelve SVG del mapa base con la cámara dada."""
    s = [f'<defs><radialGradient id="oc" cx="0.5" cy="0.45" r="0.8"><stop offset="0" stop-color="{OCEANO1}"/><stop offset="1" stop-color="{OCEANO2}"/></radialGradient></defs>'
         '<rect width="1920" height="1080" fill="url(#oc)"/>']
    # retícula de meridianos/paralelos
    paso = 30 if cam.z < 12 else (10 if cam.z < 40 else 5)
    g = []
    lon0 = cam.cx - W / 2 / cam.z
    lon1 = cam.cx + W / 2 / cam.z
    for lon in range(int(math.floor(lon0 / paso) * paso), int(lon1) + paso, paso):
        x = W / 2 + (lon - cam.cx) * cam.z
        g.append(f"M{x:.0f} 0 V1080")
    for lat in range(-80, 81, paso):
        y = H / 2 - (merc_y(lat) - cam.cy) * cam.z
        if -10 < y < H + 10:
            g.append(f"M0 {y:.0f} H1920")
    s.append(f'<path d="{" ".join(g)}" stroke="#FFFFFF" stroke-opacity="0.06" stroke-width="1.5"/>')
    colores = colores or {}
    tierra, resal = [], []
    for iso, p in D["paises"].items():
        if not cam.ve(p["bbox"]):
            continue
        d = " ".join(_ruta(cam.pm(a)) for a in p["anillos"] if cam.ve((*a.min(0), *a.max(0)), 50))
        if not d.strip():
            continue
        if iso in resaltar or iso in colores:
            resal.append((iso, d))
        else:
            tierra.append(d)
    sw = 1.2 if cam.z < 10 else 2.0
    s.append(f'<path d="{" ".join(tierra)}" fill="{TIERRA_OSC if atenuar else TIERRA}" stroke="{BORDE}" stroke-width="{sw}" stroke-linejoin="round" fill-rule="evenodd"/>')
    for iso, d in resal:
        col = colores.get(iso, RESALTE)
        for w, op in ((26, 0.10), (14, 0.18), (6, 0.35)):
            s.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-opacity="{op}" stroke-width="{w}" stroke-linejoin="round"/>')
        s.append(f'<path d="{d}" fill="{col}" fill-opacity="0.85" stroke="#FFF4E0" stroke-width="2.5" stroke-linejoin="round" fill-rule="evenodd"/>')
    if rios and cam.z > 14:
        rs = []
        for r in D["rios"]:
            bb = (*r.min(0), *r.max(0))
            if cam.ve(bb, 0):
                rs.append(_linea(cam.pm(r)))
        s.append(f'<path d="{" ".join(x for x in rs if x)}" fill="none" stroke="#6FA8C7" stroke-opacity="0.7" stroke-width="2"/>')
    if etiquetas and cam.z > 6:
        fs = 22 if cam.z < 20 else 30
        for iso, p in D["paises"].items():
            if iso in resaltar or p["rank"] > (2 if cam.z < 10 else 5):
                continue
            x, y = cam.p(p["lx"], p["ly"])
            if 80 < x < W - 80 and 120 < y < H - 160:
                s.append(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="middle" font-family="Inter, Liberation Sans" font-weight="700" font-size="{fs}" '
                         f'fill="#5A4E38" fill-opacity="0.75" letter-spacing="3">{p["nombre"].upper()}</text>')
    if tinte:
        s.append(f'<rect width="1920" height="1080" fill="{tinte[0]}" opacity="{tinte[1]}"/>')
    return "".join(s)


def ciudad(nombre_o_iso_cap):
    for c in D["ciudades"]:
        if c["nombre"] == nombre_o_iso_cap:
            return c
    for c in D["ciudades"]:
        if c["cap"] and c["pais"] == nombre_o_iso_cap:
            return c
    return None


def pin(cam, lon, lat, texto, t, start=0.0, color="#FFFFFF", lado=1, fs=34):
    p = max(0.0, min(1.0, (t - start) / 0.5))
    if p <= 0:
        return ""
    x, y = cam.p(lon, lat)
    r = 10 + 30 * ((t - start) % 1.6) / 1.6
    op = 0.6 * (1 - ((t - start) % 1.6) / 1.6)
    k = 1 - (1 - p) ** 3
    tx = x + lado * 28
    w = len(texto) * fs * 0.6 + 36
    bx = tx if lado > 0 else tx - w
    return (f'<g opacity="{p:.2f}"><circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="none" stroke="{color}" stroke-width="3" opacity="{op:.2f}"/>'
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{9 * k:.1f}" fill="{color}" stroke="#1A1A1A" stroke-width="3"/>'
            f'<rect x="{bx:.1f}" y="{y - fs * 0.85:.1f}" width="{w * k:.1f}" height="{fs * 1.4:.1f}" rx="8" fill="#101820" fill-opacity="0.82"/>'
            f'<text x="{bx + 18:.1f}" y="{y + fs * 0.32:.1f}" font-family="Inter, Liberation Sans" font-weight="800" font-size="{fs}" fill="#FFFFFF" opacity="{max(0, k * 2 - 1):.2f}">{texto}</text></g>')


def flecha(cam, a, b, t, start=0.0, dur=1.0, color="#E4572E", ancho=10, curva=0.25, texto=None):
    """Flecha curva animada entre dos (lon, lat)."""
    p = max(0.0, min(1.0, (t - start) / dur))
    if p <= 0:
        return ""
    x0, y0 = cam.p(*a)
    x1, y1 = cam.p(*b)
    mx, my = (x0 + x1) / 2, (y0 + y1) / 2
    nx, ny = -(y1 - y0), (x1 - x0)
    cx, cy = mx + nx * curva, my + ny * curva
    n = 40
    m = max(2, int(n * p))
    pts = []
    for i in range(m + 1):
        u = i / n
        pts.append(((1 - u) ** 2 * x0 + 2 * (1 - u) * u * cx + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * cy + u * u * y1))
    d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    ex, ey = pts[-1]
    px, py = pts[-2]
    ang = math.degrees(math.atan2(ey - py, ex - px))
    s = (f'<path d="{d}" fill="none" stroke="#000" stroke-opacity="0.25" stroke-width="{ancho + 6}" stroke-linecap="round"/>'
         f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{ancho}" stroke-linecap="round"/>'
         f'<g transform="translate({ex:.1f} {ey:.1f}) rotate({ang:.1f})"><path d="M8 0 L-26 -20 L-18 0 L-26 20 Z" fill="{color}" stroke="#1A1A1A" stroke-width="2"/></g>')
    if texto and p >= 1:
        s += (f'<text x="{x0:.1f}" y="{y0 - 22:.1f}" text-anchor="middle" font-family="Inter, Liberation Sans" font-weight="800" font-size="30" '
              f'fill="#FFFFFF" stroke="#101820" stroke-width="6" paint-order="stroke">{texto}</text>')
    return s


def region(cam, lon, lat, radio_km, texto, t, start=0.0, color="#F2B705"):
    p = max(0.0, min(1.0, (t - start) / 0.6))
    if p <= 0:
        return ""
    x, y = cam.p(lon, lat)
    r = radio_km / 111.0 / math.cos(math.radians(lat)) * cam.z * (1 - (1 - p) ** 3)
    puls = 1 + 0.05 * math.sin(t * 4)
    return (f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r * puls:.1f}" fill="{color}" fill-opacity="0.35" stroke="{color}" stroke-width="5" stroke-dasharray="14 10"/>'
            f'<text x="{x:.1f}" y="{y - r - 18:.1f}" text-anchor="middle" font-family="Inter, Liberation Sans" font-weight="900" font-size="40" '
            f'fill="#FFFFFF" stroke="#101820" stroke-width="7" paint-order="stroke" opacity="{p:.2f}">{texto}</text>')
