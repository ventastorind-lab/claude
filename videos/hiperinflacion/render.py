"""Render del documental de hiperinflación (versión ilustrada con mapas reales).

Uso: python3 render.py <carpeta_tts> <salida.mp4> [fps]
     python3 render.py --muestra <carpeta_salida> [indices separados por coma]
"""
import importlib.util
import math
import os
import random
import subprocess
import sys
from multiprocessing import Pool

import numpy as np
import soundfile as sf

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import ilustraciones as I  # noqa: E402
import mapas as M  # noqa: E402


def _cargar(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


V1 = _cargar("hiper_v1", os.path.join(AQUI, "render_v1.py"))
GU = _cargar("hiper_guion2", os.path.join(AQUI, "guion.py"))
A, CA = V1.A, V1.CA
SR = V1.SR
W, H = 1920, 1080
txt, aparece, prog, ease_out, ease_io, ease_back, lerp, c01, f = V1.txt, V1.aparece, V1.prog, V1.ease_out, V1.ease_io, V1.ease_back, V1.lerp, V1.c01, V1.f
ORO, ROJO, VERDE, TURQ, BLANCO, GRIS, FONDO1, PANEL = V1.ORO, V1.ROJO, V1.VERDE, V1.TURQ, V1.BLANCO, V1.GRIS, V1.FONDO1, V1.PANEL
COLOR = V1.COLOR
FUENTE = V1.FUENTE
BANDERA_DE = {"DEU": "alemania", "HUN": "hungria", "BOL": "bolivia", "ARG": "argentina", "BRA": "brasil", "ZWE": "zimbabue", "VEN": "venezuela"}
ANIO_DE = {"DEU": "1923", "HUN": "1946", "BOL": "1985", "ARG": "1989", "BRA": "1994", "ZWE": "2008", "VEN": "2017"}
NOMBRE_DE = {"DEU": "Alemania", "HUN": "Hungría", "BOL": "Bolivia", "ARG": "Argentina", "BRA": "Brasil", "ZWE": "Zimbabue", "VEN": "Venezuela"}
B = I.BILL


def bc(nombre):
    return B.get(nombre, nombre)


# ---------------------------------------------------------------- piezas comunes
def dato(d, t, start=0.6, pos="der"):
    valor, etiqueta, nota, col = d
    col = COLOR.get(col, ORO)
    p = ease_out(prog(t, start, 0.55))
    if p <= 0:
        return ""
    fs = min(96, 560 / max(1, len(valor) * 0.62))
    w = 640
    x = 1860 - w if pos == "der" else 60
    dx = (1 - p) * (120 if pos == "der" else -120)
    y = 120
    hgt = 250 if nota else 200
    s = (f'<g opacity="{f(p)}" transform="translate({f(dx)} 0)">'
         f'<rect x="{x + 10}" y="{y + 12}" width="{w}" height="{hgt}" rx="18" fill="#000" opacity="0.30"/>'
         f'<rect x="{x}" y="{y}" width="{w}" height="{hgt}" rx="18" fill="#0E1620" opacity="0.88"/>'
         f'<rect x="{x}" y="{y}" width="12" height="{hgt}" rx="6" fill="{col}"/>'
         + txt(x + 44, y + 30 + fs * 0.8, valor, fs, col, 900, "start")
         + txt(x + 46, y + 70 + fs * 0.9, etiqueta, 36, BLANCO, 800, "start"))
    if nota:
        s += txt(x + 46, y + 118 + fs * 0.9, nota, min(26, 560 / max(1, len(nota) * 0.5)), GRIS, 600, "start")
    return s + '</g>'


def rotulo(texto, x, y, t, start=0.3, fs=40, col=BLANCO, fondo="#0E1620", ancla="middle"):
    p = ease_out(prog(t, start, 0.4))
    if p <= 0:
        return ""
    return f'<g opacity="{f(p)}" transform="translate(0 {f(20 * (1 - p))})">' + I.caja_texto(x, y, texto, fs, fondo, col, 0.85, ancla) + '</g>'


def mesa(color="#6B4A2E"):
    s = [f'<rect width="1920" height="1080" fill="{color}"/>']
    r = random.Random(4)
    for i in range(40):
        y = r.uniform(0, 1080)
        s.append(f'<path d="M0 {f(y)} Q 960 {f(y + r.uniform(-30, 30))} 1920 {f(y + r.uniform(-20, 20))}" stroke="#000" stroke-opacity="{r.uniform(0.04, 0.12):.2f}" stroke-width="{r.uniform(2, 6):.1f}" fill="none"/>')
    s.append('<radialGradient id="lampara" cx="0.5" cy="0.4" r="0.6"><stop offset="0" stop-color="#FFE9B0" stop-opacity="0.35"/><stop offset="1" stop-color="#000" stop-opacity="0.45"/></radialGradient>'
             '<rect width="1920" height="1080" fill="url(#lampara)"/>')
    return "".join(s)


def pared(color, zocalo="#3A2E26", y=760):
    return (f'<rect width="1920" height="1080" fill="{color}"/><rect y="{y}" width="1920" height="{1080 - y}" fill="{zocalo}"/>'
            f'<rect y="{y}" width="1920" height="14" fill="#000" opacity="0.2"/>')


def vista(iso, relleno=0.55, dx=0.0):
    if iso == "mundo":
        return GU.MUNDO
    return M.vista_pais(iso, relleno, dx)


# ---------------------------------------------------------------- escenas: mapas
def esc_capitulo(v, t, dur, ctx):
    a = vista(v.get("desde", "mundo"), 0.5)
    b = vista(v["iso"], 0.5, -0.12)
    dv = min(2.6, dur * 0.65)
    p = ease_io(prog(t, 0.1, dv))
    cam = M.Camara(*M.interp_vista(a, b, p))
    cam.z *= 1 + 0.04 * prog(t, dv, dur)
    res = (v["iso"],) if p > 0.55 else ()
    s = [M.mapa(cam, t, resaltar=res)]
    for lon, lat, nom in v.get("pins", []):
        s.append(M.pin(cam, lon, lat, nom, t, dv + 0.2))
    # rótulo inferior
    q = ease_out(prog(t, dv * 0.55, 0.6))
    if q > 0:
        x0 = 60 - (1 - q) * 300
        s.append(f'<g opacity="{f(q)}"><rect x="{f(x0)}" y="600" width="700" height="250" rx="20" fill="#0E1620" opacity="0.9"/>'
                 f'<rect x="{f(x0)}" y="600" width="12" height="250" rx="6" fill="{ORO}"/>'
                 + V1.bandera(BANDERA_DE[v["iso"]], x0 + 50, 650, 180, 120)
                 + txt(x0 + 260, 680, f'CAPÍTULO {v["num"]}', 30, ORO, 800, "start", extra='letter-spacing="8"')
                 + txt(x0 + 258, 760, v["pais"], 74 if len(v["pais"]) < 9 else 64, BLANCO, 900, "start")
                 + txt(x0 + 260, 820, v["anio"], 44, ROJO, 800, "start")
                 + txt(x0 + 50, 830, "Fronteras actuales", 20, GRIS, 600, "start") + '</g>')
    return "".join(s)


def esc_mapa(v, t, dur, ctx):
    a = vista(v["iso"], v.get("relleno", 0.55), v.get("dx", 0))
    cam = M.Camara(a[0], a[1], a[2] * (1 + 0.05 * t / dur))
    s = [M.mapa(cam, t, resaltar=tuple(v.get("resaltar", ())), colores=v.get("colores"))]
    if v.get("region"):
        lon, lat, km, nom = v["region"]
        s.append(M.region(cam, lon, lat, km, nom, t, 0.5))
    for i, (a_, b_, nom) in enumerate(v.get("flechas", [])):
        s.append(M.flecha(cam, a_, b_, t, 1.0 + i * 0.6, 0.9, "#3D6FB6", 12, 0.22, nom))
    if v.get("billete_real"):
        p = ease_out(prog(t, 1.2, 0.7))
        if p > 0:
            s.append(f'<g opacity="{f(p)}">' + I.billete(1380, 720 + 40 * (1 - p), 620, "1", "REAL", bc("real"), rot=-6 + 2 * math.sin(t)) + '</g>')
    return "".join(s)


def esc_mapa_hiper(v, t, dur, ctx):
    cam = M.Camara(GU.MUNDO[0], GU.MUNDO[1], GU.MUNDO[2] * (1 + 0.04 * t / dur))
    lista = GU.HIPER
    paso = (dur * 0.7) / len(lista)
    n = int(c01((t - 0.3) / (dur * 0.7)) * len(lista))
    colores = {iso: ("#E4572E" if i < n else None) for i, iso in enumerate(lista)}
    colores = {k: c for k, c in colores.items() if c}
    s = [M.mapa(cam, t, colores=colores, etiquetas=False)]
    return "".join(s)


def esc_mapa_siete(v, t, dur, ctx):
    concl = v.get("conclusion")
    cam = M.Camara(-10, 10, 5.8 * (1 + 0.04 * t / dur))
    paso = 0.15 if concl else min(0.6, dur * 0.7 / 7)
    colores = {}
    s_pins = []
    pts = []
    for i, iso in enumerate(GU.SIETE):
        st = 0.3 + i * paso
        if t > st:
            colores[iso] = "#E4572E"
        p = M.D["paises"][iso]
        lado = 1 if iso in ("DEU", "HUN", "ZWE", "BRA") else -1
        s_pins.append(M.pin(cam, p["lx"], p["ly"], f"{NOMBRE_DE[iso]} {ANIO_DE[iso]}", t, st, "#FFFFFF", lado, 28))
        pts.append(cam.p(p["lx"], p["ly"]))
    s = [M.mapa(cam, t, colores=colores, etiquetas=False)]
    if concl:
        q = c01((t - 1.5) / max(1, dur - 2.5))
        n = q * (len(pts) - 1)
        k = int(n)
        vis = pts[:k + 1]
        if k < len(pts) - 1:
            fr = n - k
            vis.append((lerp(pts[k][0], pts[k + 1][0], fr), lerp(pts[k][1], pts[k + 1][1], fr)))
        if len(vis) > 1:
            s.append('<path d="M' + " L".join(f"{f(x)} {f(y)}" for x, y in vis) + f'" stroke="{ORO}" stroke-width="5" stroke-dasharray="14 10" fill="none"/>')
    s += s_pins
    return "".join(s)


def esc_migracion(v, t, dur, ctx):
    cam = M.Camara(-66, -12, 13.5 * (1 + 0.04 * t / dur))
    s = [M.mapa(cam, t, resaltar=("VEN",), colores={"COL": "#E8B04A", "PER": "#E8B04A", "BRA": "#E8B04A", "ECU": "#E8B04A", "CHL": "#E8B04A", "ARG": "#E8B04A"})]
    origen = (-66.9, 8.0)
    destinos = [((-74.07, 4.71), "Colombia"), ((-77.04, -12.05), "Perú"), ((-60.67, 2.82), "Brasil"), ((-78.47, -0.18), "Ecuador"),
                ((-70.66, -33.45), "Chile"), ((-58.4, -34.6), "Argentina")]
    for i, (dst, nom) in enumerate(destinos):
        s.append(M.flecha(cam, origen, dst, t, 0.6 + i * 0.45, 0.9, ORO, 9, 0.18 if i % 2 else -0.18))
        if t > 1.5 + i * 0.45:
            x, y = cam.p(*dst)
            s.append(f'<text x="{f(x)}" y="{f(y + 44)}" text-anchor="middle" font-family="{FUENTE}" font-weight="800" font-size="30" fill="#FFFFFF" stroke="#101820" stroke-width="6" paint-order="stroke">{nom}</text>')
    s.append(f'<g transform="translate(60 640)"><rect width="560" height="300" rx="18" fill="#0E1620" opacity="0.85"/>'
             + txt(30, 52, "1 figura ≈ 250.000 personas", 28, GRIS, 700, "start")
             + I.pictograma(50, 90, 10, 3, t, 1.0, 0.07, ORO, "#3A4552", 28, 48) + '</g>')
    return "".join(s)


def fondo_mapa_oscuro(iso, t, dur):
    if iso == "mundo":
        a = GU.MUNDO
    else:
        a = M.vista_pais(iso, 0.7)
    cam = M.Camara(a[0], a[1], a[2] * (1 + 0.03 * t / max(dur, 1)))
    return M.mapa(cam, t, resaltar=(() if iso == "mundo" else (iso,)), tinte=("#081018", 0.62), etiquetas=False)


def esc_grafica(v, t, dur, ctx):
    return fondo_mapa_oscuro(v["iso"], t, dur) + V1.grafica(v, t, dur)


def esc_barras(v, t, dur, ctx):
    items = [(lab, val, tx) for _, lab, val, tx in v["items"]]
    s = [fondo_mapa_oscuro("mundo", t, dur), V1.barras(dict(v, items=items), t, dur)]
    for i, (iso, *_r) in enumerate(v["items"]):
        y = 340 + i * 135
        st = 0.5 + i * min(1.3, dur * 0.6 / len(items))
        s.append(aparece(V1.bandera(BANDERA_DE[iso], 60, y + 20, 72, 48), t, st - 0.2, 0.4, 0))
    return "".join(s)


# ---------------------------------------------------------------- escenas: calle y comercio
def esc_panaderia(v, t, dur, ctx):
    era = v.get("era", "2010")
    dias = v.get("dias", 7)
    tt = c01((t - 0.6) / max(1, dur - 1.4))
    dia = 1 + int(tt * (dias - 1) + 1e-6)
    precio = v.get("de", 1000) * 2 ** (dia - 1)
    s = [I.calle(era, t), I.tienda(1020, 820, 800, 560, "PANADERÍA", "#B5651D", ("#B3261E", "#F4ECD8"), era,
                                    interior=I.pan(1170, 700, 0.9) + I.pan(1330, 700, 0.8))]
    s.append(I.multitud(40, 980, 965, 16, 7, t, era, filas=3, h=300, mira=1))
    # pizarra con precio
    sh = 4 * math.sin(t * 8) if (t - 0.6) % ((dur - 1.4) / max(1, dias - 1)) < 0.25 and t > 0.6 else 0
    s.append(f'<g transform="translate(1560 1010) rotate({f(sh)} 0 -200)"><path d="M-170 0 L -120 -420 M 170 0 L 120 -420" stroke="#5A4630" stroke-width="16"/>'
             '<rect x="-160" y="-430" width="320" height="300" rx="10" fill="#2B3A33" stroke="#6B4A2E" stroke-width="14"/>'
             + txt(0, -370, "PAN", 46, "#F4ECD8", 800, extra='letter-spacing="8"')
             + txt(0, -265, "$ " + V1.fmt_num(precio), 64 if precio < 100000 else 52, "#F2B705", 900)
             + txt(0, -175, f"DÍA {dia}", 40, "#F4ECD8", 700) + '</g>')
    # flecha de duplicación
    if dia > 1:
        s.append(rotulo("× 2 cada día", 1560, 520, t, 0.9, 40, ROJO))
    return "".join(s)


def esc_mercado(v, t, dur, ctx):
    era = v.get("era", "2010")
    sube = v.get("sube", 1.5)
    q = ease_io(c01((t - 0.8) / max(1, dur - 2)))
    fac = 1 + (sube - 1) * q
    if v.get("andino"):
        s = [I.calle(era, t, base=780, densidad=1.1)]
        cols = ["#E63946", "#2A9D8F", "#F4A261", "#457B9D"]
        prods = ["papas", "frutas", "verduras", "frutas"]
        for i in range(4):
            s.append(I.puesto_mercado(120 + i * 460, 840, 340, cols[i], i, prods[i]))
        s.append(I.multitud(0, 1920, 1000, 14, 12, t, era, filas=2, h=270, poses=["pie", "camina"]))
        precios = [2000, 3500, 1200, 5000]
        for i, pr in enumerate(precios):
            s.append(I.etiqueta_precio(170 + i * 460, 470 - 6 * math.sin(t * 2 + i), "$b " + V1.fmt_num(pr * fac), 0.9))
    else:
        s = [pared("#E9E4D8", "#BFB8AA", 900), '<rect y="0" width="1920" height="70" fill="#CFC9BC"/>']
        for x in range(120, 1920, 420):
            s.append(f'<rect x="{x}" y="70" width="220" height="16" fill="#FFFFFF"/><rect x="{x}" y="86" width="220" height="40" fill="#FFF9E0" opacity="0.4"/>')
        p_base = [["$ 2.500", "$ 4.900", "$ 1.200"], ["$ 8.300", "$ 3.100", "$ 6.700"], ["$ 950", "$ 12.400", "$ 5.200"]]
        p_now = [[f"$ {V1.fmt_num(int(x.split()[1].replace('.', '')) * fac)}" for x in fila] for fila in p_base]
        s.append(I.estante(80, 860, 820, 4, 3, 0.0, p_now))
        s.append(I.estante(1020, 860, 820, 4, 4, 0.0, p_now[::-1]))
        s.append(I.multitud(100, 1800, 1060, 6, 21, t, era, filas=1, h=380, poses=["pie", "camina"]))
        s.append(I.etiqueta_precio(700, 300 - 8 * math.sin(t * 2), "+" + str(int(round((fac - 1) * 100))) + " %", 1.3, "#FFF6D6", -8))
    return "".join(s)


def esc_pan_vs_billetes(v, t, dur, ctx):
    meses = v.get("meses", 12)
    q = c01((t - 0.5) / max(1, dur - 1.3))
    mes = max(1, int(q * meses + 0.999))
    fac = 1.5 ** (q * meses)
    s = [mesa("#7A5636")]
    s.append('<ellipse cx="480" cy="760" rx="260" ry="60" fill="#E8E2D4"/><ellipse cx="480" cy="750" rx="230" ry="48" fill="#F5F0E4"/>')
    s.append(I.pan(480, 740, 1.8))
    s.append(I.pila(1050, 900, 5, 3, 9, bc("dolar"), 120, visibles=min(135, fac * 135 / 130)))
    # calendario
    s.append(f'<g transform="translate(1600 250)"><rect x="-120" y="-110" width="240" height="230" rx="14" fill="#FFFFFF"/><rect x="-120" y="-110" width="240" height="60" rx="14" fill="{ROJO}"/>'
             + txt(0, -66, "MES", 34, "#FFFFFF", 800) + txt(0, 60, str(mes), 110, "#2B2B2B", 900) + '</g>')
    s.append(f'<g transform="translate(480 330)"><rect x="-260" y="-80" width="520" height="140" rx="20" fill="#0E1620" opacity="0.88"/>'
             + txt(0, 30, "× " + V1.fmt_num(fac), 96, ORO, 900) + '</g>')
    s.append(rotulo("El precio del mismo pan", 480, 200, t, 0.4, 34))
    return "".join(s)


def esc_carretilla(v, t, dur, ctx):
    era = v.get("era", "1920")
    s = [I.calle(era, t, seed=8), I.tienda(1100, 820, 760, 540, "BÄCKEREI", "#7A5A40", ("#6B2A20", "#E8D5AE"), era, interior=I.pan(1240, 700, 0.9))]
    s.append(I.multitud(30, 700, 960, 9, 31, t, era, filas=2, h=290, mira=1))
    q = ease_io(c01(t / max(1, dur * 0.8)))
    x = lerp(300, 820, q)
    s.append(I.carretilla(x, 1020, 1.25, bc("marco")))
    s.append(I.persona(x + 290, 1020, 330, 44, t, "empuja" if q < 1 else "pie", era, -1))
    s.append(I.etiqueta_precio(1200, 520, v.get("precio", "200.000.000.000"), 0.95, "#FFF6D6", -5))
    s.append(rotulo("1 pan", 1240, 610, t, 0.6, 30))
    return "".join(s)


def esc_bolsas(v, t, dur, ctx):
    era = v.get("era", "1980")
    s = [I.calle(era, t, base=780, densidad=1.1)]
    cols = ["#E63946", "#2A9D8F", "#F4A261"]
    for i in range(3):
        s.append(I.puesto_mercado(200 + i * 620, 840, 420, cols[i], i + 4, ["papas", "verduras", "frutas"][i]))
    for i in range(5):
        x = (200 + i * 380 + t * 60) % 2100 - 100
        saco = I.saco_dinero(30, -250, 0.6, "#C2A266", "$b")
        s.append(I.persona(x, 1010 - (i % 2) * 30, 300, 60 + i, t, "camina", era, 1, carga=saco))
    s.append(I.carretilla(1500, 1040, 0.9, bc(v.get("color", "peso_bo"))))
    return "".join(s)


def esc_remarcar(v, t, dur, ctx):
    s = [pared("#E9E4D8", "#BFB8AA", 900)]
    s.append(I.estante(60, 860, 1100, 4, 9))
    s.append(I.persona(1500, 1040, 420, 71, t, "carga", "1980", -1, ropa="#2980B9", carga=I.pistola_precios(-70, -250, 10, 0.55)))
    n = int(c01((t - 0.6) / max(1, dur - 1.2)) * 12)
    precio = 100
    for i in range(n + 1):
        precio = int(precio * 1.38)
        s.append(I.etiqueta_precio(560 - i * 6, 620 - i * 30, "₳ " + V1.fmt_num(precio), 1.0, "#FFF6D6", -6 + (i % 3) * 3))
    s.append(rotulo("Remarcando precios varias veces al día", 640, 160, t, 0.4, 36))
    return "".join(s)


def esc_saqueos(v, t, dur, ctx):
    era = "1980"
    s = [I.calle(era, t, base=800)]
    s.append(I.tienda(560, 800, 800, 520, "SUPERMERCADO", "#D9D2C0", ("#2980B9", "#FFFFFF"), era))
    s.append(f'<rect x="590" y="{f(800 - 520 * 0.62)}" width="{f(800 * 0.55)}" height="{f(520 * 0.42)}" fill="#8C959D"/>'
             + "".join(f'<path d="M590 {f(800 - 520 * 0.62 + i * 18)} h{f(800 * 0.55)}" stroke="#5E666E" stroke-width="3"/>' for i in range(12)))
    s.append(I.multitud(0, 1920, 1040, 24, 14, t, era, filas=3, h=300, poses=["brazos", "pie", "brazos", "camina"]))
    return "".join(s)


def esc_tienda_vacia(v, t, dur, ctx):
    s = [pared("#E6E2D6", "#B9B2A4", 900)]
    s.append(I.estante(60, 860, 860, 4, 5, 0.88))
    s.append(I.estante(1000, 860, 860, 4, 6, 0.92))
    canasta = '<path d="M30 -170 h80 l-10 60 h-60 Z" fill="none" stroke="#C0392B" stroke-width="7"/>'
    s.append(I.persona(900, 1040, 400, 81, t, "pie", "2010", -1, carga=canasta, triste=True))
    return "".join(s)


def esc_hielo(v, t, dur, ctx):
    s = [mesa("#3E5A6B")]
    g = c01((t - 0.8) / max(1, dur - 2.2))
    if t < dur - 1.0:
        s.append(I.hielo(960, 520 + 4 * math.sin(t * 2), I.etiqueta_precio(-180, 0, "$ 1.000", 1.4, "#FFF6D6", -4), g))
        s.append(rotulo("Precio congelado", 960, 860, t, 0.4, 40))
    else:
        q = c01((t - (dur - 1.0)) / 0.8)
        r = random.Random(7)
        for _ in range(16):
            ang = r.uniform(0, 6.28)
            d = 500 * q
            s.append(f'<rect x="{f(960 + math.cos(ang) * d - 40)}" y="{f(520 + math.sin(ang) * d - 40 + 300 * q * q)}" width="80" height="80" fill="#DFF4FB" opacity="{f(0.7 * (1 - q))}" transform="rotate({f(q * 200)} 960 520)"/>')
        s.append(I.etiqueta_precio(780, 520, "$ " + V1.fmt_num(1000 * (1 + 4 * q)), 1.4 + 0.2 * q, "#FFF6D6", -4, ROJO))
        s.append(rotulo("Se descongela... y salta", 960, 860, t, dur - 1.0, 40, ROJO))
    return "".join(s)


def esc_urv(v, t, dur, ctx):
    s = [pared("#EDE7DA", "#BDB4A3", 860)]
    s.append(I.estante(240, 820, 1440, 3, 13))
    paso = int(max(0, t - 0.5) / 0.55)
    viejo = 12000 * (1.012 ** (paso * 3))
    s.append(f'<g transform="translate(520 380)"><rect x="-300" y="-170" width="600" height="300" rx="20" fill="#FFFFFF" stroke="#B3261E" stroke-width="8"/>'
             + txt(0, -100, "CRUZEIROS REALES", 34, "#B3261E", 800)
             + txt(0, 30, "CR$ " + V1.fmt_num(viejo), 72, "#2B2B2B", 900) + txt(0, 100, "cambia todos los días", 28, GRIS, 600) + '</g>')
    s.append(f'<g transform="translate(1400 380)"><rect x="-300" y="-170" width="600" height="300" rx="20" fill="#FFFFFF" stroke="#2E9E5B" stroke-width="8"/>'
             + txt(0, -100, "URV (UNIDAD DE VALOR)", 34, "#2E9E5B", 800)
             + txt(0, 30, "URV 10,00", 72, "#2B2B2B", 900) + txt(0, 100, "1 URV ≈ 1 dólar · estable", 28, GRIS, 600) + '</g>')
    return "".join(s)


# ---------------------------------------------------------------- escenas: dinero
def esc_billete(v, t, dur, ctx):
    s = [mesa("#5E4128")]
    p = ease_out(prog(t, 0.1, 0.8))
    s.append(f'<g opacity="{f(p)}">' + I.billete(960, lerp(640, 430, p), 1400, v["valor"], v["moneda"], bc(v["color"]), rot=lerp(-12, -3, p) + math.sin(t), sello=v.get("sello")) + '</g>')
    nz = v["valor"].count("0")
    if v["valor"].startswith("1") and nz > 4:
        s.append(rotulo(f"un 1 con {nz} ceros", 960, 140, t, 1.0, 48, FONDO1, ORO))
    for i in range(4):
        cx, cy = 260 + i * 70, 930 - (i % 2) * 20
        s.append(f'<ellipse cx="{cx}" cy="{cy}" rx="44" ry="18" fill="#B08D57"/><ellipse cx="{cx}" cy="{cy - 6}" rx="44" ry="18" fill="#D4AF6A"/>')
    return "".join(s)


def esc_nuevo_billete(v, t, dur, ctx):
    s = [mesa("#5E4128")]
    s.append(I.pila(140, 980, 4, 3, 6, bc(v["viejo"]), 110))
    s.append(f'<rect width="1920" height="1080" fill="#000" opacity="{f(0.35 * ease_out(prog(t, 0.8, 1)))}"/>')
    p = ease_out(prog(t, 0.6, 1.0))
    if p > 0:
        s.append(f'<circle cx="1180" cy="500" r="{f(520 * p)}" fill="#FFE9B0" opacity="{f(0.25 * p)}"/>')
        s.append(f'<g opacity="{f(p)}">' + I.billete(1180, lerp(-300, 500, p), 1000, v["valor"], v["moneda"], bc(v["nuevo"]), rot=lerp(25, -4, p)) + '</g>')
    q = prog(t, 1.8, 0.4)
    if q > 0:
        k = 1.8 - 0.8 * ease_out(q)
        s.append(f'<g transform="translate(1450 760) rotate(-12) scale({f(k)})" opacity="{f(q)}"><rect x="-200" y="-55" width="400" height="110" rx="10" fill="none" stroke="#B3261E" stroke-width="8"/>'
                 + txt(0, 20, v["fecha"], 52, "#B3261E", 900) + '</g>')
    return "".join(s)


def esc_ceros(v, t, dur, ctx):
    num = v["numero"]
    quitar = v.get("quitar", 0)
    etapas = v.get("etapas")
    chars = list(num)
    quita = [False] * len(chars)
    orden = []
    cnt, i = 0, len(chars) - 1
    while i >= 0 and cnt < quitar:
        if chars[i] == "0":
            cnt += 1
        quita[i] = True
        orden.append(i)
        i -= 1
    if quitar and i >= 0 and chars[i] == ".":
        quita[i] = True
        orden.append(i)
    inicio, fin = 1.0, max(1.8, dur * 0.6)
    tiempos = {}
    if etapas:
        grupos, idx = [], 0
        for g in etapas:
            grp, z = [], 0
            while idx < len(orden) and z < g:
                if chars[orden[idx]] == "0":
                    z += 1
                grp.append(orden[idx])
                idx += 1
            grupos.append(grp)
        grupos[-1] += orden[idx:]
        tg = (fin - inicio) / len(grupos)
        for gi, grp in enumerate(grupos):
            for k, ci in enumerate(grp):
                tiempos[ci] = inicio + gi * tg + k * 0.06
    else:
        paso = (fin - inicio) / max(1, len(orden))
        for k, ci in enumerate(orden):
            tiempos[ci] = inicio + k * paso
    cambio = ease_out(prog(t, fin + 0.2, 0.6))
    col = I.mezclar(bc(v["color"]), bc(v.get("nuevo_color", v["color"])), cambio)
    moneda = v["moneda"] if cambio < 0.5 else v.get("nueva_moneda", v["moneda"])
    s = [mesa("#5E4128")]
    bw = 1500
    s.append(I.billete(960, 500, bw, "", moneda, col, rot=0, emblema=True))
    fs = min(150, bw * 0.82 / (len(chars) * 0.6))
    cw = fs * 0.6
    x0 = 960 - len(chars) * cw / 2
    yb = 500 + fs * 0.45
    restantes = [i for i in range(len(chars)) if not quita[i]]
    pc = ease_io(prog(t, fin, 0.6)) if quitar else 0
    for i, ch in enumerate(chars):
        x = x0 + i * cw + cw / 2
        if quita[i]:
            tc = tiempos.get(i, 99)
            q = c01((t - tc) / 0.9)
            if q >= 1:
                continue
            c = ROJO if t > tc - 0.2 else "#141414"
            s.append(f'<g opacity="{f(1 - q)}" transform="translate({f(x + 60 * q * (1 if i % 2 else -1))} {f(yb + 700 * q * q)}) rotate({f((40 if i % 2 else -30) * q)})">' + txt(0, 0, ch, fs, c, 900, fam=V1.MONO) + '</g>')
        else:
            k = restantes.index(i)
            xc = 960 + (k - (len(restantes) - 1) / 2) * cw
            esc = 1 + 0.6 * pc
            s.append(f'<g transform="translate({f(lerp(x, xc, pc))} {f(yb)}) scale({f(esc)})">' + txt(0, 0, ch, fs, "#141414", 900, fam=V1.MONO) + '</g>')
    if etapas:
        anios = ["2008", "2018", "2021"]
        tg = (fin - inicio) / len(etapas)
        for gi, g in enumerate(etapas):
            x = 960 + (gi - 1) * 400
            s.append(aparece(f'<rect x="{x - 170}" y="110" width="340" height="80" rx="40" fill="#0E1620" stroke="{ROJO}" stroke-width="4"/>'
                             + txt(x, 163, f"{anios[gi]}:  −{g} ceros", 38, BLANCO, 800), t, inicio + gi * tg, 0.4, cx=x, cy=150, escala=True))
    else:
        s.append(rotulo(f"−{quitar} ceros" if quitar else "conversión", 960, 170, t, inicio, 46, BLANCO, "#0E1620"))
    if v.get("extra"):
        s.append(rotulo(v["extra"], 960, 900, t, fin + 0.7, 56, FONDO1, VERDE))
    return "".join(s)


def esc_montana_vs(v, t, dur, ctx):
    s = [mesa("#4E3824")]
    q = c01((t - 0.3) / max(1, dur * 0.6))
    s.append(I.pila(60, 1000, 7, 4, 10, bc(v["color"]), 100, visibles=q * 280, seed=3))
    p = ease_out(prog(t, dur * 0.45, 0.7))
    if p > 0:
        s.append(f'<ellipse cx="1550" cy="860" rx="{f(260 * p)}" ry="40" fill="#FFE9B0" opacity="{f(0.3 * p)}"/>')
        s.append(f'<g opacity="{f(p)}">' + I.billete(1550, 720 - 30 * math.sin(t * 2), 520, "1", v["contra"].upper().replace("FORINTO", "FORINT"), bc(v["contra"]), rot=-5) + '</g>')
    s.append(rotulo("=", 1180, 760, t, dur * 0.45, 90, ORO))
    return "".join(s)


def esc_adopengo(v, t, dur, ctx):
    s = [mesa("#5E4128")]
    s.append(I.billete(560, 420, 760, "1.000.000", "PENGŐ", bc("pengo"), rot=-6))
    p = ease_out(prog(t, 0.4, 0.7))
    caida = c01((t - dur * 0.55) / 1.2)
    s.append(f'<g opacity="{f(p)}" transform="translate(0 {f(500 * caida * caida)}) rotate({f(20 * caida)} 1380 460)">' + I.billete(1380, 460, 760, "1", "ADÓPENGŐ", "#E8C39E", rot=5, sello="IMPUESTOS") + '</g>')
    pts = [(200, 220), (600, 280), (900, 420), (1200, 600), (1500, 820), (1800, 1000)]
    q = c01((t - dur * 0.4) / 1.5)
    n = int(q * (len(pts) - 1)) + 1
    if q > 0:
        s.append('<path d="M' + " L".join(f"{x} {y}" for x, y in pts[:n + 1]) + f'" stroke="{ROJO}" stroke-width="16" fill="none" stroke-linecap="round"/>')
    return "".join(s)


def esc_billetes_serie(v, t, dur, ctx):
    s = [mesa("#5E4128")]
    items = v["items"]
    paso = (dur * 0.75) / len(items)
    for i, (nom, anio, col) in enumerate(items):
        st = 0.3 + i * paso
        p = ease_out(prog(t, st, 0.6))
        if p <= 0:
            continue
        x, y = 420 + i * 360, 470 + (i % 2) * 90
        s.append(f'<g opacity="{f(p)}">' + I.billete(x, lerp(-200, y, p), 560, anio, nom, col, rot=-8 + i * 5) + '</g>')
        if t > st + paso and i < len(items) - 1:
            q = prog(t, st + paso, 0.3)
            s.append(f'<path d="M{x - 200} {y - 110} L{f(x - 200 + 400 * q)} {f(y - 110 + 220 * q)} M{x + 200} {y - 110} L{f(x + 200 - 400 * q)} {f(y - 110 + 220 * q)}" stroke="{ROJO}" stroke-width="18" stroke-linecap="round"/>')
    return "".join(s)


def esc_boveda(v, t, dur, ctx):
    s = [I.boveda(t)]
    izq = I.billete(0, -60, 300, "1", "PESO", bc("real"), rot=0, emblema=False)
    der = I.billete(0, -60, 300, "1", "US$", bc("dolar"), rot=0, emblema=False)
    s.append(f'<g transform="translate(0 40)">' + I.bascula(1340, 1060, t, izq, der, 0.08 * math.sin(t * 2) * c01(1 - t / 3)) + '</g>')
    s.append(rotulo("Cada peso, respaldado por un dólar en reservas", 960, 140, t, 0.4, 38))
    return "".join(s)


def esc_dolarizacion(v, t, dur, ctx):
    s = [mesa("#5E4128")]
    q = ease_io(c01((t - 0.6) / 1.4))
    s.append(f'<g transform="translate({f(-500 * q)} {f(200 * q)}) rotate({f(-15 * q)} 500 700)" opacity="{f(1 - 0.8 * q)}">' + I.pila(200, 900, 4, 3, 5, bc("zim"), 110) + '</g>')
    for i, (val, mon, col) in enumerate((("100", "US DOLLARS", bc("dolar")), ("20", "US DOLLARS", bc("dolar")), ("100", "RAND", "#D7B58A"), ("50", "PULA", "#A9CBE0"))):
        p = ease_out(prog(t, 1.2 + i * 0.35, 0.6))
        if p > 0:
            s.append(f'<g opacity="{f(p)}">' + I.billete(1250 + i * 80, lerp(1300, 380 + i * 110, p), 640, val, mon, col, rot=-14 + i * 9) + '</g>')
    return "".join(s)


def esc_pollo(v, t, dur, ctx):
    s = [I.calle("2010", t, base=860, densidad=1.2)]
    s.append(f'<rect x="300" y="840" width="1320" height="240" fill="#7A5636"/><rect x="300" y="840" width="1320" height="20" fill="#9A7650"/>')
    pila = I.pila(-170, 0, 3, 2, 4, bc("bolivar"), 90)
    s.append(I.bascula(960, 860, t, pila, I.pollo(0, 0, 0.95), 0.0))
    return "".join(s)


def esc_tijera_ceros(v, t, dur, ctx):
    s = [mesa("#5E4128")]
    s.append(I.billete(960, 520, 1500, "", "BILLETE NUEVO", bc("real")))
    texto = "1.000"
    ciclo = (t % 3.0) / 3.0
    fs = 170
    cw = fs * 0.6
    base = "1"
    if ciclo < 0.35:
        mostrar = "1.000"
    elif ciclo < 0.55:
        mostrar = "1"
    else:
        n = int((ciclo - 0.55) / 0.45 * 5)
        mostrar = ["1", "1.0", "1.00", "1.000", "1.000", "1.000"][min(5, n)]
    x0 = 960 - len(mostrar) * cw / 2
    for i, ch in enumerate(mostrar):
        col = ROJO if (ciclo >= 0.55 and i > 0) else "#141414"
        s.append(txt(x0 + i * cw + cw / 2, 520 + fs * 0.4, ch, fs, col, 900, fam=V1.MONO))
    tx = 960 + 160 if ciclo < 0.45 else 1500
    s.append(I.tijera(tx, 470, 90, 1.2, abs(math.sin(t * 6))))
    s.append(rotulo("Los ceros vuelven a crecer", 960, 170, t, 1.6, 44, ROJO))
    _ = (texto, base)
    return "".join(s)


# ---------------------------------------------------------------- escenas: lugares y gente
def esc_huelga_imprenta(v, t, dur, ctx):
    era = v.get("era", "1920")
    izq = I.calle(era, t, seed=12) + I.fabrica(80, 820, 900, t, apagada=True) + I.multitud(0, 980, 1000, 12, 41, t, era, filas=2, h=290, mira=1)
    izq += rotulo("Huelga en el Ruhr", 480, 140, t, 0.4, 40)
    der = (pared("#4A4038", "#3A322C", 860) + I.imprenta(1350, 900, t, 0.85, bc(v.get("color", "marco")))
           + rotulo("La impresora a toda marcha", 1400, 140, t, 0.9, 40))
    p = ease_out(prog(t, 0.2, 0.8))
    xc = lerp(1920, 960, p)
    return (izq + f'<clipPath id="cder"><polygon points="{f(xc + 120)},0 1920,0 1920,1080 {f(xc - 120)},1080"/></clipPath>'
            f'<g clip-path="url(#cder)">{der}</g><path d="M{f(xc + 120)} 0 L{f(xc - 120)} 1080" stroke="{ORO}" stroke-width="10"/>')


def esc_imprenta(v, t, dur, ctx):
    era = v.get("era", "1940")
    s = [pared("#5A4B40", "#3A322C", 860)]
    for x in (220, 860, 1500):
        s.append(f'<rect x="{x}" y="120" width="260" height="360" fill="#BFD7E3" opacity="0.25"/><path d="M{x + 130} 120 V480 M{x} 300 H{x + 260}" stroke="#3A322C" stroke-width="12"/>')
    s.append(I.imprenta(560, 920, t, 0.8, bc(v.get("color", "pengo"))))
    s.append(I.imprenta(1380, 940, t + 0.5, 0.75, bc(v.get("color", "pengo"))))
    s.append(I.persona(170, 1000, 320, 51, t, "pie", era, 1))
    s.append(I.lluvia_billetes(t, bc(v.get("color", "pengo")), 14, 5, -300, 160))
    return "".join(s)


def esc_ruinas(v, t, dur, ctx):
    s = [I.ruinas(t)]
    for i in range(5):
        x = (100 + i * 300 + t * 40) % 2000 - 60
        s.append(I.persona(x, 1050 - (i % 2) * 20, 260, 90 + i, t, "camina", "1940", 1, triste=True))
    return "".join(s)


def esc_reloj(v, t, dur, ctx):
    s = [pared("#CFC6B4", "#6B5A48", 820)]
    s.append(I.reloj(560, 470, 280, t, vel=2.2))
    horas = int(max(0, t - 0.5) * 2.2 * 12 / 15)
    s.append(f'<g transform="translate(1380 600)"><rect x="-330" y="-230" width="660" height="420" rx="24" fill="#0E1620" opacity="0.9"/>'
             + txt(0, -150, f"HORA {horas * 15}", 46, GRIS, 800)
             + txt(0, -20, "Precio × " + V1.fmt_num(2 ** horas), 76, ROJO, 900)
             + txt(0, 100, "se duplica cada 15 horas", 36, BLANCO, 700) + '</g>')
    return "".join(s)


def esc_ahorros(v, t, dur, ctx):
    return I.mesa_familia(t, v.get("era", "1920"))


def esc_mineros(v, t, dur, ctx):
    s = [I.mina(t)]
    for i in range(7):
        x = 520 + i * 170 + t * 35
        s.append(I.minero(x, 990 + (i % 2) * 30, 0.95, t, i, "camina"))
    return "".join(s)


def esc_decreto(v, t, dur, ctx):
    s = [mesa("#5E4128")]
    s.append(f'<g transform="translate(0 0)">' + V1.bandera(v.get("bandera", "bolivia"), 120, 120, 300, 200) + '</g>')
    s.append(I.documento(1000, 560, 900, 840, v["titulo"], v["lineas"], t, firma=prog(t, 1.0, 1.4), sello=prog(t, 2.6, 0.4)))
    return "".join(s)


def esc_petroleo(v, t, dur, ctx):
    s = [I.cielo("1980", t, sol=(1600, 640)), '<rect y="760" width="1920" height="320" fill="#8C6E4A"/>',
         '<path d="M0 760 Q 480 720 960 755 T 1920 750 V 800 H 0 Z" fill="#6E5638"/>']
    for i, (x, k) in enumerate(((300, 0.9), (900, 1.2), (1500, 0.8))):
        s.append(I.bomba_petroleo(x, 900 - (i % 2) * 40, t, k, i))
    pts = [(2014.4, 112), (2014.8, 85), (2015.0, 50), (2015.4, 62), (2015.8, 45), (2016.05, 30)]
    x0, x1, y0, y1 = 520, 1380, 520, 250
    xy = [(lerp(x0, x1, (a - 2014.4) / 1.65), lerp(y0, y1, b / 120)) for a, b in pts]
    q = c01((t - 0.6) / max(1, dur * 0.6))
    n = q * (len(xy) - 1)
    k = int(n)
    vis = xy[:k + 1]
    if k < len(xy) - 1:
        fr = n - k
        vis.append((lerp(xy[k][0], xy[k + 1][0], fr), lerp(xy[k][1], xy[k + 1][1], fr)))
    s.append(f'<rect x="{x0 - 60}" y="{y1 - 100}" width="{x1 - x0 + 140}" height="{y0 - y1 + 160}" rx="20" fill="#0E1620" opacity="0.55"/>')
    s.append(txt(x0, y1 - 40, "Precio del barril (US$)", 34, BLANCO, 800, "start"))
    if len(vis) > 1:
        s.append('<path d="M' + " L".join(f"{f(x)} {f(y)}" for x, y in vis) + f'" stroke="{ROJO}" stroke-width="10" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append(txt(xy[0][0] - 10, xy[0][1] - 20, "≈ 110 (2014)", 30, BLANCO, 800, "start"))
    if q >= 1:
        s.append(txt(xy[-1][0], xy[-1][1] + 50, "≈ 30 (2016)", 30, ROJO, 900))
    return "".join(s)


def esc_confianza(v, t, dur, ctx):
    s = ['<defs><linearGradient id="cf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#F2B705"/><stop offset="1" stop-color="#C2571A"/></linearGradient></defs>',
         '<rect width="1920" height="1080" fill="url(#cf)"/>']
    s.append(f'<g opacity="0.35">' + I.billete(960, 380, 1300, "", "CONFIANZA", "#FFF6D6") + '</g>')
    s.append(I.multitud(0, 1920, 1080, 30, 77, t, "2010", filas=3, h=260, fondo="#C2571A"))
    s.append(I.manos_apreton(960, 330, 0.9, t))
    return "".join(s)


def esc_suscribete(v, t, dur, ctx):
    s = [fondo_mapa_oscuro("mundo", t, dur), V1.suscribete(v, t, dur)]
    return "".join(s)


def esc_periodicos(v, t, dur, ctx):
    era = v.get("era", "1980")
    papel = {"1920": "#E8DDC4", "1940": "#E2DCCB", "1980": "#F1EBDD", "2010": "#F7F5F0"}[era]
    s = [mesa("#3E2C1E")]
    ev = v["eventos"]
    n = len(ev)
    paso = (dur * 0.7) / n
    w = min(520, 1700 / n - 30)
    pos = []
    for i, (fecha, titular, ico) in enumerate(ev):
        x = 960 + (i - (n - 1) / 2) * (w + 40)
        y = 500 + (i % 2) * 50 - 25
        pos.append((x, y - 250))
        st = 0.3 + i * paso
        p = ease_out(prog(t, st, 0.5))
        if p <= 0:
            continue
        rot = (-4, 3, -2, 4)[i % 4]
        k = 1.3 - 0.3 * p
        fig = {"billete": I.billete(0, 0, w * 0.7, "", "", "#C9C2B0", emblema=True),
               "banco": f'<g transform="scale({w / 1100:.3f})">' + I.banco_central(-420, 200, 840, 360, t, "#BDB6A6") + '</g>',
               "grafica": f'<path d="M{-w * 0.35} {-60} L {-w * 0.1} -10 L {w * 0.05} -40 L {w * 0.35} 80" stroke="#3A3A3A" stroke-width="12" fill="none"/>'}[ico]
        recorte = (f'<g transform="translate({f(x)} {f(y)}) rotate({rot}) scale({f(k)})" opacity="{f(p)}">'
                   f'<rect x="{f(-w / 2 + 10)}" y="-262" width="{f(w)}" height="560" fill="#000" opacity="0.3"/>'
                   f'<rect x="{f(-w / 2)}" y="-270" width="{f(w)}" height="560" fill="{papel}"/>'
                   f'<text x="0" y="-215" text-anchor="middle" font-family="Liberation Serif, serif" font-weight="700" font-size="38" fill="#2B2B2B">EL DIARIO</text>'
                   f'<path d="M{f(-w / 2 + 20)} -195 H{f(w / 2 - 20)} M{f(-w / 2 + 20)} -188 H{f(w / 2 - 20)}" stroke="#2B2B2B" stroke-width="2"/>'
                   + txt(0, -130, fecha, 52, "#B3261E", 900)
                   + "".join(txt(0, -70 + j * 44, ln, 36, "#1E1E1E", 900, fam="Liberation Serif, serif") for j, ln in enumerate(V1._envolver(titular, 18)))
                   + f'<rect x="{f(-w * 0.4)}" y="40" width="{f(w * 0.8)}" height="200" fill="#D8D2C2"/><g transform="translate(0 140)">{fig}</g>'
                   + '<circle cx="0" cy="-262" r="14" fill="#B3261E"/></g>')
        s.append(recorte)
    # hilo rojo
    vis = [pp for i, pp in enumerate(pos) if t > 0.6 + i * paso]
    if len(vis) > 1:
        s.append('<path d="M' + " L".join(f"{f(x)} {f(y - 12)}" for x, y in vis) + '" stroke="#B3261E" stroke-width="4" fill="none"/>')
    return "".join(s)


# ---------------------------------------------------------------- paneles (viñetas ilustradas)
def mini(clave, t, era):
    if clave == "guerra":
        s = I.ruinas(t, 900, "1940" if era != "1920" else "1940")
        for i in range(4):
            s += I.soldado(400 + i * 300, 1040, 1.1, t, i)
        return s
    if clave in ("deuda", "deuda_ext"):
        tit, ln = ("REPARACIONES", ["132.000.000.000", "marcos oro · 1921"]) if clave == "deuda" else ("DEUDA EXTERNA", ["Bolivia · 1982", "Pagos vencidos"])
        s = mesa("#5E4128") + I.documento(900, 540, 900, 900, tit, ln, t, 0, 1)
        s += "".join(f'<ellipse cx="{1420 + i * 46}" cy="{820 - i * 30}" rx="34" ry="20" fill="none" stroke="#7A7F84" stroke-width="12"/>' for i in range(6))
        return s + '<circle cx="1720" cy="560" r="130" fill="#2B2B2B"/>' + txt(1720, 580, "DEUDA", 50, "#FFFFFF", 900)
    if clave == "candado":
        return pared("#4A4038", "#3A322C", 860) + I.imprenta(980, 920, 0, 1.1, "#C9B98E", activa=False, cadena=1.0)
    if clave == "imprenta":
        return pared("#4A4038", "#3A322C", 860) + I.imprenta(980, 920, t, 1.1, "#B9D7A0") + I.lluvia_billetes(t, "#B9D7A0", 10, 2, -300, 180)
    if clave == "respaldo":
        return (I.cielo("1920", t) + '<path d="M0 640 Q 960 560 1920 640 V1080 H0 Z" fill="#9AAE6A"/>'
                + "".join(f'<path d="M0 {700 + i * 50} Q 960 {640 + i * 50} 1920 {700 + i * 50}" stroke="#7E9450" stroke-width="10" fill="none"/>' for i in range(8))
                + I.fabrica(1250, 640, 560, t) + I.billete(760, 520, 900, "1", "RENTENMARK", bc("rentenmark"), rot=-4))
    if clave == "balanza":
        izq = "".join(f'<ellipse cx="{-60 + i * 40}" cy="{-12 - (i % 2) * 18}" rx="40" ry="16" fill="#D4AF6A" stroke="#8A6A30" stroke-width="3"/>' for i in range(4))
        return mesa("#5E4128") + I.bascula(960, 1000, t, izq, izq, 0) + txt(620, 380, "INGRESOS", 50, BLANCO, 900) + txt(1300, 380, "GASTOS", 50, BLANCO, 900)
    if clave in ("forinto", "real", "moneda"):
        nom = {"forinto": ("FORINT", "forinto"), "real": ("REAL", "real"), "moneda": ("NUEVA MONEDA", "rentenmark")}[clave]
        return mesa("#5E4128") + f'<circle cx="960" cy="520" r="420" fill="#FFE9B0" opacity="0.25"/>' + I.billete(960, 520, 1200, "10", nom[0], bc(nom[1]), rot=-4 + math.sin(t))
    if clave in ("banco", "banco_cerrado"):
        s = I.calle("2010" if era == "2010" else "1980", t, base=900, lejos=True, densidad=1.3) + I.banco_central(360, 900, 1200, 600, t, bandera="#2A6FB6")
        if clave == "banco_cerrado":
            s += I.caja_texto(960, 560, "SIN CRÉDITO", 90, "#B3261E", "#FFFFFF", 0.95, "middle")
        return s
    if clave == "estano":
        s = I.mina(t)
        s += "".join(f'<path d="M{700 + (i % 4) * 130} {960 - (i // 4) * 50} l 120 0 l -20 -46 h -80 Z" fill="#B8BEC2" stroke="#6B7278" stroke-width="4"/>' for i in range(10))
        return s + f'<path d="M1300 300 L 1500 500 L 1600 450 L 1800 760" stroke="{ROJO}" stroke-width="26" fill="none"/><path d="M1760 700 l 60 80 l -100 10 Z" fill="{ROJO}"/>'
    if clave == "tijera":
        return mesa("#5E4128") + I.documento(900, 540, 900, 820, "PRESUPUESTO", ["Gasto público", "1985"], 0) + I.tijera(1300, 600, 160, 2.0, abs(math.sin(t * 5)))
    if clave in ("etiqueta", "etiqueta_control"):
        s = pared("#E9E4D8", "#BFB8AA", 900) + I.estante(200, 860, 1520, 4, 31, 0.6 if clave == "etiqueta_control" else 0.0)
        if clave == "etiqueta":
            for i in range(5):
                s += I.etiqueta_precio(300 + i * 280, 400 - 120 * ((t * 0.5 + i * 0.2) % 1), "$", 1.2, "#FFF6D6", -10 + i * 6)
        else:
            s += I.caja_texto(960, 300, "PRECIO REGULADO", 90, "#B3261E", "#FFFFFF", 0.95, "middle")
        return s
    if clave == "cambio":
        return (I.calle("1980", t, base=900) + I.tienda(460, 900, 1000, 640, "CASA DE CAMBIO", "#2E5E4E", ("#F2B705", "#2E5E4E"), "1980")
                + I.caja_texto(960, 640, "1 TASA ÚNICA", 80, "#0E1620", "#F2B705", 0.95, "middle"))
    if clave == "urv":
        return esc_urv({}, t, 6, {})
    if clave == "campo":
        return I.campo_seco(t)
    if clave == "exportaciones":
        s = I.cielo("2010", t) + '<rect y="760" width="1920" height="320" fill="#2E6E8E"/><rect y="700" width="760" height="70" fill="#8F8F8F"/>'
        s += '<path d="M900 760 h 760 l -80 120 h -600 Z" fill="#3A3A3A"/>' + "".join(f'<rect x="{960 + i * 120}" y="680" width="110" height="80" fill="{c}"/>' for i, c in enumerate(("#E63946", "#2A9D8F", "#F4A261")))
        return s + f'<path d="M300 200 L 700 500" stroke="{ROJO}" stroke-width="40"/><path d="M640 420 l 120 110 l -160 30 Z" fill="{ROJO}"/>'
    if clave == "petroleo_cae":
        s = I.cielo("2010", t, sol=(1600, 700)) + '<rect y="760" width="1920" height="320" fill="#8C6E4A"/>' + I.bomba_petroleo(900, 900, 0, 1.4)
        return s + f'<path d="M1300 260 L 1500 460 L 1600 420 L 1800 700" stroke="{ROJO}" stroke-width="26" fill="none"/><path d="M1760 640 l 60 80 l -100 10 Z" fill="{ROJO}"/>'
    if clave == "dolar":
        s = mesa("#5E4128")
        for i in range(5):
            s += I.billete(600 + i * 180, 560 - abs(i - 2) * 40, 700, "1" if i % 2 else "20", "US DOLLARS", bc("dolar"), rot=-24 + i * 12)
        return s
    if clave == "ancla":
        s = '<rect width="1920" height="1080" fill="#1F4E6B"/><rect y="560" width="1920" height="520" fill="#163A52"/>'
        s += f'<g transform="translate(960 {f(560 + 10 * math.sin(t * 2))})"><circle cx="0" cy="-300" r="50" fill="none" stroke="#C9D1D6" stroke-width="26"/><path d="M0 -250 V 300 M -160 -150 H 160 M -330 120 Q 0 460 330 120" stroke="#C9D1D6" stroke-width="40" fill="none" stroke-linecap="round"/></g>'
        return s
    if clave == "confianza":
        s = I.calle("1940", t, base=880, densidad=1.3) + I.banco_central(560, 880, 800, 460, t)
        return s + I.multitud(0, 1920, 1060, 22, 66, t, "1940", filas=3, h=300, poses=["camina", "brazos", "camina"])
    return pared("#333", "#222", 900)


def esc_paneles(v, t, dur, ctx):
    era = v.get("era", "1980")
    items = v["items"]
    ya = v.get("ya", 0)
    n = len(items)
    nuevos = n - ya
    oscuro = {"1920": "#2A2118", "1940": "#24231F", "1980": "#1E2430", "2010": "#14202B"}[era]
    s = [f'<rect width="1920" height="1080" fill="{oscuro}"/>',
         '<radialGradient id="pg" cx="0.5" cy="0.45" r="0.7"><stop offset="0" stop-color="#FFFFFF" stop-opacity="0.08"/><stop offset="1" stop-color="#000" stop-opacity="0.4"/></radialGradient>',
         '<rect width="1920" height="1080" fill="url(#pg)"/>']
    modo_rojo = any(k in ("guerra", "deuda", "deuda_ext", "banco_cerrado", "estano", "campo", "exportaciones", "imprenta", "etiqueta_control", "petroleo_cae", "confianza") for k, _ in items)
    col = ROJO if modo_rojo else VERDE
    if n == 1:
        pw, ph = 980, 551
    elif n == 2:
        pw, ph = 860, 484
    elif n == 3:
        pw, ph = 580, 326
    else:
        pw, ph = 430, 242
    gap = 30
    x0 = 960 - (n * pw + (n - 1) * gap) / 2
    y0 = min(520 - ph / 2 - (40 if n >= 3 else 20), 860 - ph - 106)
    y0 = max(y0, 200 if v.get("titulo") else 130)
    if v.get("titulo"):
        s.append(txt(960, 140, v["titulo"].upper(), 54, col, 900, extra='letter-spacing="10"'))
    paso = min(1.6, (dur * 0.75 - 0.3) / max(1, nuevos))
    for j, (clave, cap) in enumerate(items):
        st = -1 if j < ya else 0.3 + (j - ya) * paso
        p = 1.0 if j < ya else ease_out(prog(t, st, 0.55))
        if p <= 0:
            continue
        x = x0 + j * (pw + gap)
        k = pw / 1920
        dy = 60 * (1 - p)
        cid = f"pn{j}"
        contenido = mini(clave, t, era)
        s.append(f'<g opacity="{f(p)}" transform="translate(0 {f(dy)})">'
                 f'<rect x="{f(x + 10)}" y="{f(y0 + 14)}" width="{pw}" height="{f(ph + 110)}" rx="14" fill="#000" opacity="0.4"/>'
                 f'<clipPath id="{cid}"><rect x="{f(x)}" y="{f(y0)}" width="{pw}" height="{f(ph)}" rx="14"/></clipPath>'
                 f'<g clip-path="url(#{cid})"><g transform="translate({f(x)} {f(y0)}) scale({k:.4f})">{contenido}</g></g>'
                 f'<rect x="{f(x)}" y="{f(y0)}" width="{pw}" height="{f(ph)}" rx="14" fill="none" stroke="#FFFFFF" stroke-opacity="0.25" stroke-width="3"/>'
                 f'<rect x="{f(x)}" y="{f(y0 + ph + 14)}" width="{pw}" height="92" rx="14" fill="#0E1620"/>'
                 f'<rect x="{f(x)}" y="{f(y0 + ph + 14)}" width="10" height="92" rx="5" fill="{col}"/>')
        fs = min(40, (pw - 60) / max(1, len(cap) * 0.56))
        s.append(txt(x + pw / 2 + 5, y0 + ph + 14 + 46 + fs * 0.35, cap, fs, BLANCO, 800) + '</g>')
    return "".join(s)


ESC = {k[4:]: fn for k, fn in globals().items() if k.startswith("esc_") and callable(fn)}
ERA_PAIS = {"DEU": "1920", "HUN": "1940", "BOL": "1980", "ARG": "1980", "BRA": "1980", "ZWE": "2010", "VEN": "2010"}
SEPIA = {"1920": ("#8A6A3A", 0.13), "1940": ("#5A5040", 0.12)}


# ---------------------------------------------------------------- composición
def contenido(v, t, dur, ctx):
    return ESC[v["vis"]](v, t, dur, ctx)


def escena(idx, texto_n, v, t, dur, ctx):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', V1.DEFS]
    mapa_vis = v["vis"] in ("capitulo", "mapa", "mapa_hiper", "mapa_siete", "migracion")
    k = 1.0 if mapa_vis else 1 + 0.045 * (t / max(dur, 1))
    cuerpo = contenido(v, t, dur, ctx)
    if k != 1.0:
        cuerpo = f'<g transform="translate(960 500) scale({k:.4f}) translate(-960 -500)">{cuerpo}</g>'
    if ctx.get("prev") and t < 0.45:
        pv, pd = ctx["prev"]
        kp = 1.0 if pv["vis"] in ("capitulo", "mapa", "mapa_hiper", "mapa_siete", "migracion") else 1.045
        prev = contenido(pv, pd - 0.04, pd, ctx)
        if kp != 1.0:
            prev = f'<g transform="translate(960 500) scale({kp:.4f}) translate(-960 -500)">{prev}</g>'
        s.append(prev)
        s.append(f'<g opacity="{f(ease_io(t / 0.45))}">{cuerpo}</g>')
    else:
        s.append(cuerpo)
    sep = SEPIA.get(ctx.get("era"))
    if sep and not mapa_vis:
        s.append(f'<rect width="1920" height="1080" fill="{sep[0]}" opacity="{sep[1]}"/>')
    s.append('<rect width="1920" height="1080" fill="url(#vin)" opacity="0.7"/>')
    if v.get("dato"):
        s.append(dato(v["dato"], t, 0.7, "der"))
    s.append(capa(ctx))
    s.append(V1.subtitulos(texto_n, t, ctx["vdur"]))
    s.append('</svg>')
    return "".join(s)


def capa(ctx):
    s = [f'<rect x="0" y="0" width="1920" height="6" fill="#000" opacity="0.3"/><rect x="0" y="0" width="{f(1920 * ctx["tg"] / ctx["total"])}" height="6" fill="{ORO}"/>']
    lab = ctx["etiqueta"]
    w = V1.ancho_txt(lab, 24, 700) + len(lab) * 2 + 66
    s.append(f'<g transform="translate(50 36)"><rect width="{f(w)}" height="48" rx="24" fill="#0E1620" opacity="0.8"/>'
             f'<circle cx="26" cy="24" r="7" fill="{ORO}"/>' + txt(44, 33, lab, 24, BLANCO, 700, "start", extra='letter-spacing="2"') + '</g>')
    return "".join(s)


def contextos():
    out, lab, era = [], "INTRODUCCIÓN", "2010"
    prev = None
    for texto_n, v in GU.E:
        if v["vis"] == "capitulo":
            lab = f'CAP. {v["num"]:02d} · {v["pais"]} {v["anio"]}'
            era = ERA_PAIS[v["iso"]]
        if v["vis"] == "mapa_siete" and v.get("conclusion"):
            lab, era = "CONCLUSIÓN", "2010"
        out.append({"etiqueta": lab, "era": era, "prev_v": prev})
        prev = v
    return out


# ---------------------------------------------------------------- audio
def eventos(v, dur):
    vis = v["vis"]
    ev = [(0.0, "whoosh", 0.45)]
    if v.get("dato"):
        ev.append((0.7, "pop", 0.5))
    if vis == "capitulo":
        dv = min(2.6, dur * 0.65)
        ev += [(0.1, "swoosh", 0.6), (dv * 0.55, "boom", 0.8), (dv + 0.2, "pop", 0.5)]
    elif vis == "paneles":
        ya = v.get("ya", 0)
        nuevos = len(v["items"]) - ya
        paso = min(1.6, (dur * 0.75 - 0.3) / max(1, nuevos))
        ev += [(0.3 + j * paso, "swoosh", 0.5) for j in range(nuevos)]
    elif vis == "ceros":
        fin = max(1.8, dur * 0.6)
        n = v.get("quitar", 0)
        ev += [(1.0 + kk * (fin - 1.0) / max(1, n), "tick", 0.45) for kk in range(n)] + [(fin + 0.3, "ding", 0.6)]
    elif vis in ("billete", "nuevo_billete", "montana_vs"):
        ev += [(0.2, "swoosh", 0.5), (1.0, "ding", 0.4)]
        if vis == "nuevo_billete":
            ev.append((1.8, "boom", 0.6))
    elif vis == "periodicos":
        paso = (dur * 0.7) / len(v["eventos"])
        ev += [(0.3 + i * paso, "swoosh", 0.5) for i in range(len(v["eventos"]))]
    elif vis == "panaderia":
        paso = (dur - 1.4) / 6
        ev += [(0.6 + i * paso, "ding", 0.35) for i in range(7)]
    elif vis in ("imprenta", "huelga_imprenta"):
        ev += [(0.2 + kk * 0.5, "vibra", 0.25) for kk in range(int(dur / 0.5))]
    elif vis == "reloj":
        ev += [(0.5 + kk * 0.25, "tick", 0.35) for kk in range(int((dur - 0.5) / 0.25))]
    elif vis == "remarcar":
        ev += [(0.6 + kk * (dur - 1.2) / 12, "click", 0.4) for kk in range(12)]
    elif vis == "decreto":
        ev += [(2.6, "boom", 0.7)]
    elif vis == "hielo":
        ev += [(dur - 1.0, "boom", 0.7)]
    elif vis == "migracion":
        ev += [(0.6 + i * 0.45, "swoosh", 0.4) for i in range(6)]
    elif vis == "mapa_siete":
        paso = 0.15 if v.get("conclusion") else min(0.6, dur * 0.7 / 7)
        ev += [(0.3 + i * paso, "pop", 0.45) for i in range(7)]
    elif vis == "billetes_serie":
        paso = (dur * 0.75) / len(v["items"])
        ev += [(0.3 + i * paso, "swoosh", 0.5) for i in range(len(v["items"]))]
    elif vis == "suscribete":
        ev += [(0.3, "pop", 0.6), (1.75, "click", 0.8), (2.0, "campana", 0.7)]
    elif vis == "mapa":
        ev += [(1.0 + i * 0.6, "swoosh", 0.45) for i in range(len(v.get("flechas", [])))]
    return ev


# ---------------------------------------------------------------- render
def _cuadro(args):
    idx, texto_n, v, t, dur, ctx = args
    svg = escena(idx, texto_n, v, t, dur, ctx).encode("utf-8")
    return subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-f", "png"], input=svg, capture_output=True, check=True).stdout


def muestra(carpeta, indices=None, tiempos=(0.2, 3.5)):
    os.makedirs(carpeta, exist_ok=True)
    ctxs = contextos()
    for i, (texto_n, v) in enumerate(GU.E):
        if indices and i not in indices:
            continue
        for t in tiempos:
            ctx = dict(ctxs[i], tg=i * 7 + t, total=len(GU.E) * 7, vdur=6.5)
            ctx["prev"] = (ctxs[i]["prev_v"], 7.0) if ctxs[i]["prev_v"] else None
            png = _cuadro((i, texto_n, v, t, 7.0, ctx))
            with open(os.path.join(carpeta, f"{i:02d}_{v['vis']}_{t}.png"), "wb") as fh:
                fh.write(png)
    print("ok")


def main():
    if sys.argv[1] == "--muestra":
        idx = [int(x) for x in sys.argv[3].split(",")] if len(sys.argv) > 3 else None
        muestra(sys.argv[2], idx)
        return
    tts_dir, salida = sys.argv[1], sys.argv[2]
    fps = int(sys.argv[3]) if len(sys.argv) > 3 else 24
    escenas = GU.E
    tmp = salida + "_tmp"
    os.makedirs(tmp, exist_ok=True)
    voces = V1.generar_voces(tts_dir, [x for x, _ in escenas], tmp)
    durs = [max(len(vz) / SR, 3.2) for vz in voces]
    vdurs = [len(vz) / SR - 0.45 for vz in voces]
    total = sum(durs)
    print(f"{len(escenas)} escenas · {total:.1f} s", flush=True)
    A.cargar_sfx()
    A.SFX.update(vibra=CA.sfx_vibra(), riser=V1.sfx_riser())
    voz = np.zeros(int(SR * (total + 1)))
    efectos = np.zeros_like(voz)
    t0 = 0.0
    for (texto_n, v), vz, d in zip(escenas, voces, durs):
        i0 = int(SR * t0)
        voz[i0:i0 + len(vz)] += vz
        evs = eventos(v, d)
        if v["vis"] == "capitulo" and t0 > 1:
            evs.append((-0.9, "riser", 0.55))
        for ts, nombre, vol in evs:
            snd = A.SFX[nombre] * vol * 0.5
            j = i0 + int(SR * ts)
            if 0 <= j < len(efectos):
                efectos[j:j + len(snd)] += snd[:len(efectos) - j]
        t0 += d
    pista = voz + efectos
    pista[:int(SR * total)] += V1.musica_doc(total) * 0.11
    pista = pista[:int(SR * total)]
    pista /= max(1.0, np.abs(pista).max() / 0.95)
    wav = salida + ".wav"
    sf.write(wav, pista.astype(np.float32), SR)
    ctxs = contextos()
    tareas, tg = [], 0.0
    prev_d = None
    for kk, ((texto_n, v), d, vd) in enumerate(zip(escenas, durs, vdurs)):
        for fi in range(int(round(d * fps))):
            t = fi / fps
            ctx = dict(ctxs[kk], tg=tg + t, total=total, vdur=vd)
            ctx["prev"] = (ctxs[kk]["prev_v"], prev_d) if ctxs[kk]["prev_v"] else None
            tareas.append((kk, texto_n, v, t, d, ctx))
        tg += d
        prev_d = d
    print(f"{len(tareas)} cuadros", flush=True)
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(fps), "-i", "-", "-i", wav,
                           "-vf", "noise=c0s=5:c0f=t+u", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
                           "-c:a", "aac", "-b:a", "192k", "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-shortest", "-movflags", "+faststart", salida],
                          stdin=subprocess.PIPE)
    with Pool(4) as pool:
        for n, png in enumerate(pool.imap(_cuadro, tareas, chunksize=4)):
            ff.stdin.write(png)
            if n % 1200 == 0:
                print(f"cuadro {n}/{len(tareas)}", flush=True)
    ff.stdin.close()
    ff.wait()
    os.remove(wav)
    os.rmdir(tmp)
    print("listo", salida, flush=True)


if __name__ == "__main__":
    main()
