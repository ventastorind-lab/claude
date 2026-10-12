"""Render del documental de hiperinflación: motion graphics sin personajes.

Diseño: fondo azul noche con retícula de puntos, acentos dorado/rojo/turquesa/verde,
tipografía Inter, transición diagonal dorada, subtítulos karaoke y barra de progreso.

Uso: python3 render.py <carpeta_tts> <salida.mp4> [fps] [--muestra]
"""
import importlib.util
import math
import os
import random
import re
import subprocess
import sys
from html import escape
from multiprocessing import Pool

import numpy as np
import soundfile as sf

AQUI = os.path.dirname(os.path.abspath(__file__))


def _cargar(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CA = _cargar("cola_animar", os.path.join(AQUI, "..", "cocacola", "animar.py"))
GU = _cargar("hiper_guion", os.path.join(AQUI, "guion_v1.py"))
A = CA.A
SR = CA.SR
W, H = 1920, 1080

# ---------------------------------------------------------------- paleta
FONDO1, FONDO2 = "#0B1220", "#111B30"
PANEL = "#16223B"
LINEA = "#2A3A5C"
BLANCO = "#F5F7FA"
GRIS = "#9AA7BF"
ORO = "#F2B705"
ROJO = "#E63946"
TURQ = "#2EC4B6"
VERDE = "#3DDC97"
COLOR = {"rojo": ROJO, "dorado": ORO, "verde": VERDE, "turq": TURQ}
FUENTE = "Inter, Liberation Sans, Arial"
MONO = "DejaVu Sans Mono, Liberation Mono, monospace"

VOZ_SID, VOZ_VEL, VOZ_TONO = 29, 1.02, 0.97


def f(v):
    return f"{v:.1f}"


def c01(x):
    return max(0.0, min(1.0, x))


def prog(t, start, dur):
    return c01((t - start) / dur) if dur > 0 else float(t >= start)


def ease_out(x):
    return 1 - (1 - x) ** 3


def ease_io(x):
    return 3 * x * x - 2 * x * x * x


def ease_back(x, s=1.7):
    x -= 1
    return 1 + x * x * ((s + 1) * x + s)


def lerp(a, b, p):
    return a + (b - a) * p


def txt(x, y, s, fs, color=BLANCO, peso=800, ancla="middle", fam=FUENTE, extra=""):
    return (f'<text x="{f(x)}" y="{f(y)}" text-anchor="{ancla}" font-family="{fam}" font-weight="{peso}" '
            f'font-size="{f(fs)}" fill="{color}" {extra}>{escape(s)}</text>')


def aparece(svg, t, start, d=0.45, dy=40, cx=None, cy=None, escala=False):
    """Entrada: sube y aparece (o crece con rebote si escala=True)."""
    p = prog(t, start, d)
    if p <= 0:
        return ""
    if escala:
        k = ease_back(p)
        return f'<g opacity="{f(min(1, p * 2.5))}" transform="translate({f(cx)} {f(cy)}) scale({k:.3f}) translate({f(-cx)} {f(-cy)})">{svg}</g>'
    return f'<g opacity="{p:.3f}" transform="translate(0 {f(dy * (1 - ease_out(p)))})">{svg}</g>'


def ancho_txt(s, fs, peso=800):
    w = 0.0
    for ch in s:
        if ch.isupper():
            w += 0.74
        elif ch.isdigit():
            w += 0.64
        elif ch in " .,:;·'!¡|ijlíI()":
            w += 0.30
        else:
            w += 0.58
    return w * fs * (1.0 if peso >= 800 else 0.94)


def fmt_num(v):
    return f"{int(round(v)):,}".replace(",", ".")


def fmt_corto(v):
    if v >= 1e12:
        return f"{v / 1e12:.1f}".replace(".", ",").replace(",0", "") + " billones"
    if v >= 1e6:
        return f"{v / 1e6:.0f} mill."
    if v < 10 and v != int(v):
        return f"{v:.1f}".replace(".", ",")
    return fmt_num(v)


# ---------------------------------------------------------------- iconos (líneas)
def icono(nombre, cx, cy, color, k=1.0):
    st = f'fill="none" stroke="{BLANCO}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"'
    g = {
        "guerra": f'<path d="M-36 8 a36 32 0 0 1 72 0 Z" {st}/><path d="M-46 8 h92" {st}/><path d="M-10 -14 h20" {st}/>',
        "deuda": f'<rect x="-26" y="-36" width="52" height="72" rx="6" {st}/>' + txt(0, 14, "$", 40, BLANCO, 900) + f'<path d="M-14 26 h28" {st}/>',
        "fabrica": f'<path d="M-40 34 V-2 l22 -14 v14 l22 -14 v14 l22 -14 V34 Z" {st}/><path d="M24 -16 V-38 h10 V-10" {st}/>',
        "imprenta": f'<rect x="-38" y="-12" width="76" height="34" rx="6" {st}/><rect x="-22" y="-38" width="44" height="26" {st}/><rect x="-22" y="14" width="44" height="26" fill="{VERDE}" stroke="{BLANCO}" stroke-width="5"/>',
        "candado": f'<rect x="-30" y="-6" width="60" height="44" rx="8" {st}/><path d="M-18 -6 v-12 a18 18 0 0 1 36 0 v12" {st}/><circle cx="0" cy="14" r="5" fill="{BLANCO}"/>',
        "moneda": f'<circle r="36" {st}/><circle r="26" {st} stroke-dasharray="4 6"/>' + txt(0, 14, "$", 38, BLANCO, 900),
        "balanza": f'<path d="M0 -36 V34 M-24 34 h48 M-38 -24 h76" {st}/><path d="M-38 -24 l-14 28 h28 Z M38 -24 l-14 28 h28 Z" {st}/>',
        "banco": f'<path d="M-42 -12 L0 -38 L42 -12 Z M-42 34 h84 M-30 -6 v34 M-10 -6 v34 M10 -6 v34 M30 -6 v34" {st}/>',
        "grafica_baja": f'<path d="M-38 -36 V34 H40" {st}/><path d="M-30 -24 L-8 -2 L6 -14 L32 18" {st}/><path d="M18 18 h14 v-14" {st}/>',
        "tijera": f'<circle cx="-22" cy="22" r="12" {st}/><circle cx="22" cy="22" r="12" {st}/><path d="M-14 12 L28 -36 M14 12 L-28 -36" {st}/>',
        "etiqueta": f'<path d="M-36 -10 L-10 -36 H34 V8 L8 34 Z" {st} transform="rotate(0)"/><circle cx="18" cy="-20" r="6" {st}/>',
        "dolar": txt(0, 16, "US$", 40, BLANCO, 900),
        "ancla": f'<circle cx="0" cy="-28" r="8" {st}/><path d="M0 -20 V34 M-18 -6 h36 M-34 10 a34 26 0 0 0 68 0" {st}/>',
        "campo": f'<path d="M-40 32 H40 M0 32 V-8" {st}/><path d="M0 -4 C -6 -28 -30 -30 -34 -22 C -30 -4 -10 -2 0 -4 Z M0 -10 C 6 -34 30 -36 34 -28 C 30 -10 10 -8 0 -10 Z" {st}/>',
        "petroleo": f'<path d="M0 -38 C 14 -16 30 0 30 14 a30 30 0 0 1 -60 0 C -30 0 -14 -16 0 -38 Z" {st}/>',
        "confianza": f'<path d="M0 -38 L32 -26 V2 C32 22 16 32 0 40 C-16 32 -32 22 -32 2 V-26 Z" {st}/><path d="M2 -30 L-8 -6 L8 4 L-4 30" {st}/>',
    }.get(nombre, f'<circle r="30" {st}/>')
    return (f'<g transform="translate({f(cx)} {f(cy)}) scale({k:.3f})"><circle r="58" fill="{color}" opacity="0.18"/>'
            f'<circle r="58" fill="none" stroke="{color}" stroke-width="5"/>{g}</g>')


# ---------------------------------------------------------------- banderas
def bandera(tipo, x, y, w, h):
    franjas = {"alemania": ["#141414", "#DD0000", "#FFCE00"], "hungria": ["#CE2939", "#FFFFFF", "#477050"],
               "bolivia": ["#D52B1E", "#F9E300", "#007934"], "argentina": ["#74ACDF", "#FFFFFF", "#74ACDF"],
               "venezuela": ["#FCE300", "#0033A0", "#CF142B"],
               "zimbabue": ["#006400", "#FFD200", "#D40000", "#141414", "#D40000", "#FFD200", "#006400"],
               "brasil": ["#009C3B"]}[tipo]
    hh = h / len(franjas)
    s = "".join(f'<rect x="{f(x)}" y="{f(y + i * hh)}" width="{f(w)}" height="{f(hh + 0.6)}" fill="{c}"/>' for i, c in enumerate(franjas))
    cx, cy = x + w / 2, y + h / 2
    if tipo == "argentina":
        s += f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(h * 0.11)}" fill="#F6B40E"/>'
    elif tipo == "brasil":
        mx, my = w * 0.09, h * 0.12
        s += (f'<polygon points="{f(x + mx)},{f(cy)} {f(cx)},{f(y + my)} {f(x + w - mx)},{f(cy)} {f(cx)},{f(y + h - my)}" fill="#FFDF00"/>'
              f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(h * 0.25)}" fill="#002776"/>'
              f'<path d="M{f(cx - h * 0.25)} {f(cy - h * 0.03)} q {f(h * 0.25)} {f(-h * 0.08)} {f(h * 0.5)} {f(h * 0.06)}" stroke="#FFFFFF" stroke-width="{f(h * 0.04)}" fill="none"/>')
    elif tipo == "zimbabue":
        s += f'<polygon points="{f(x)},{f(y)} {f(x + h * 0.55)},{f(cy)} {f(x)},{f(y + h)}" fill="#FFFFFF"/>'
        s += f'<circle cx="{f(x + h * 0.18)}" cy="{f(cy)}" r="{f(h * 0.08)}" fill="#D40000"/>'
    elif tipo == "venezuela":
        s += "".join(f'<circle cx="{f(cx + h * 0.28 * math.cos(math.pi * (0.12 + i * 0.108)))}" cy="{f(cy + h * 0.1 - h * 0.22 * math.sin(math.pi * (0.12 + i * 0.108)))}" r="{f(h * 0.028)}" fill="#FFFFFF"/>' for i in range(8))
    return s + f'<rect x="{f(x)}" y="{f(y)}" width="{f(w)}" height="{f(h)}" fill="none" stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="3"/>'


# ---------------------------------------------------------------- capa común
DEFS = (f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{FONDO1}"/><stop offset="1" stop-color="{FONDO2}"/></linearGradient>'
        '<radialGradient id="vin" cx="0.5" cy="0.5" r="0.75"><stop offset="0.55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.65"/></radialGradient>'
        '<radialGradient id="glow"><stop offset="0" stop-color="#FFF" stop-opacity="1"/><stop offset="1" stop-color="#FFF" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="gOro"><stop offset="0" stop-color="{ORO}" stop-opacity="0.35"/><stop offset="1" stop-color="{ORO}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="gRojo"><stop offset="0" stop-color="{ROJO}" stop-opacity="0.35"/><stop offset="1" stop-color="{ROJO}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="gVerde"><stop offset="0" stop-color="{VERDE}" stop-opacity="0.32"/><stop offset="1" stop-color="{VERDE}" stop-opacity="0"/></radialGradient>'
        f'<radialGradient id="gTurq"><stop offset="0" stop-color="{TURQ}" stop-opacity="0.30"/><stop offset="1" stop-color="{TURQ}" stop-opacity="0"/></radialGradient>'
        '<linearGradient id="areaR" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#E63946" stop-opacity="0.45"/><stop offset="1" stop-color="#E63946" stop-opacity="0"/></linearGradient>'
        '<linearGradient id="areaV" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3DDC97" stop-opacity="0.45"/><stop offset="1" stop-color="#3DDC97" stop-opacity="0"/></linearGradient>'
        '</defs>')
GLOW_DE = {ROJO: "gRojo", ORO: "gOro", VERDE: "gVerde", TURQ: "gTurq"}


def fondo(tg, acento):
    s = [DEFS, '<rect width="1920" height="1080" fill="url(#bg)"/>']
    # resplandores que derivan lentamente
    gid = GLOW_DE.get(acento, "gTurq")
    x1, y1 = 1500 + 160 * math.sin(tg * 0.13), 260 + 90 * math.cos(tg * 0.11)
    x2, y2 = 380 + 140 * math.cos(tg * 0.09), 820 + 80 * math.sin(tg * 0.12)
    s.append(f'<circle cx="{f(x1)}" cy="{f(y1)}" r="720" fill="url(#{gid})"/>')
    s.append(f'<circle cx="{f(x2)}" cy="{f(y2)}" r="620" fill="url(#gTurq)" opacity="0.6"/>')
    # retícula de puntos que se desplaza
    off = (tg * 12) % 60
    pts = []
    for gy in range(-1, 19):
        for gx in range(-1, 33):
            pts.append(f'M{f(gx * 60 + off)} {f(gy * 60 + off * 0.5)}h0.01')
    s.append(f'<path d="{" ".join(pts)}" stroke="#FFFFFF" stroke-opacity="0.07" stroke-width="4" stroke-linecap="round"/>')
    # líneas diagonales decorativas
    s.append(f'<path d="M{f(-200 + (tg * 20) % 400)} 1080 L{f(400 + (tg * 20) % 400)} 0" stroke="{acento}" stroke-opacity="0.06" stroke-width="80"/>')
    return "".join(s)


def capa_superior(ctx, t):
    s = ['<rect width="1920" height="1080" fill="url(#vin)"/>']
    # barra de progreso global
    s.append(f'<rect x="0" y="0" width="1920" height="6" fill="#FFFFFF" opacity="0.08"/>')
    s.append(f'<rect x="0" y="0" width="{f(1920 * ctx["tg"] / ctx["total"])}" height="6" fill="{ORO}"/>')
    # píldora de capítulo
    lab = ctx["etiqueta"]
    if lab:
        w = ancho_txt(lab, 26, 700) + len(lab) * 2 + 66
        s.append(f'<g transform="translate(60 44)"><rect width="{f(w)}" height="52" rx="26" fill="{PANEL}" stroke="{LINEA}" stroke-width="2" opacity="0.92"/>'
                 f'<circle cx="28" cy="26" r="7" fill="{ctx["acento"]}"/>'
                 + txt(46, 35, lab, 26, BLANCO, 700, "start", extra='letter-spacing="2"') + '</g>')
    s.append(txt(1860, 78, "HIPERINFLACIÓN", 22, GRIS, 700, "end", extra='letter-spacing="6" opacity="0.7"'))
    return "".join(s)


def transicion(t, acento):
    if t > 0.5:
        return ""
    p = ease_io(prog(t, 0, 0.5))
    x = lerp(-700, 2300, p)
    return (f'<polygon points="{f(x - 520)},0 {f(x + 40)},0 {f(x - 260)},1080 {f(x - 820)},1080" fill="{FONDO1}"/>'
            f'<polygon points="{f(x)},0 {f(x + 140)},0 {f(x - 160)},1080 {f(x - 300)},1080" fill="{acento}"/>'
            f'<polygon points="{f(x + 170)},0 {f(x + 200)},0 {f(x - 100)},1080 {f(x - 130)},1080" fill="{BLANCO}" opacity="0.7"/>')


# ---------------------------------------------------------------- subtítulos karaoke
def trozos(texto, max_linea=46):
    palabras = texto.split()
    lineas, act = [], []
    for p in palabras:
        if act and len(" ".join(act + [p])) > max_linea:
            lineas.append(act)
            act = []
        act.append(p)
        if p[-1] in ".?!" and len(" ".join(act)) > 18:
            lineas.append(act)
            act = []
    if act:
        lineas.append(act)
    # agrupar de a 2 líneas, sin cruzar fin de frase en la segunda
    grupos, i = [], 0
    while i < len(lineas):
        g = [lineas[i]]
        if i + 1 < len(lineas) and lineas[i][-1][-1] not in ".?!":
            g.append(lineas[i + 1])
            i += 1
        grupos.append(g)
        i += 1
    return grupos


def subtitulos(texto, t, vdur):
    grupos = trozos(texto)
    palabras = [p for g in grupos for ln in g for p in ln]
    pesos = []
    for p in palabras:
        w = len(p) + 1
        if p.endswith((",", ";", ":")):
            w += 5
        if p.endswith((".", "?", "!")):
            w += 9
        pesos.append(w)
    tot = sum(pesos)
    habla = max(0.5, vdur - 0.42)
    pos = c01((t - 0.12) / habla) * tot
    acum, actual = 0, len(palabras) - 1
    for i, w in enumerate(pesos):
        if acum + w > pos:
            actual = i
            break
        acum += w
    # grupo que contiene la palabra actual
    idx = 0
    for g in grupos:
        n = sum(len(ln) for ln in g)
        if actual < idx + n:
            break
        idx += n
    fs, alto = 44, 60
    y0 = 1000 - (len(g) - 1) * alto
    ancho = max(ancho_txt(" ".join(ln), fs, 600) for ln in g) + 70
    s = [f'<rect x="{f(960 - ancho / 2)}" y="{f(y0 - 50)}" width="{f(ancho)}" height="{f(len(g) * alto + 28)}" rx="18" fill="#060B16" opacity="0.72"/>']
    j = idx
    for li, ln in enumerate(g):
        partes = []
        for p in ln:
            if j == actual:
                col = ORO
            elif j < actual:
                col = BLANCO
            else:
                col = "#8592AB"
            partes.append(f'<tspan fill="{col}">{escape(p)}</tspan>')
            j += 1
        s.append(f'<text x="960" y="{f(y0 + li * alto)}" text-anchor="middle" font-family="{FUENTE}" font-weight="600" font-size="{fs}">{" ".join(partes)}</text>')
    return "".join(s)


# ---------------------------------------------------------------- plantillas
def titulo_seccion(titulo, t, color):
    fs = min(60, 60 * 1500 / max(1, ancho_txt(titulo, 60)))
    w = ancho_txt(titulo, fs) + 20
    return aparece(f'<rect x="160" y="190" width="10" height="70" fill="{color}"/>' + txt(196, 248, titulo, fs, BLANCO, 900, "start")
                   + f'<rect x="196" y="272" width="{f(w * ease_out(prog(t, 0.2, 0.6)))}" height="4" fill="{color}" opacity="0.6"/>', t, 0.05, 0.4, 20)


def precio_ticker(v, t, dur):
    dias = v.get("dias", 7)
    de = v.get("de", 1000)
    tt = c01((t - 0.6) / max(1, dur - 1.6))
    dia_f = 1 + tt * (dias - 1)
    dia = int(dia_f)
    precio = de * 2 ** (dia - 1)
    s = [titulo_seccion("Precio del pan", t, ROJO)]
    # tarjeta de precio
    card = (f'<rect x="160" y="330" width="760" height="460" rx="34" fill="{PANEL}" stroke="{LINEA}" stroke-width="3"/>'
            + txt(220, 410, v.get("producto", "PAN"), 40, GRIS, 800, "start", extra='letter-spacing="8"')
            + txt(220, 470, f"DÍA {dia}", 48, ORO, 900, "start")
            + txt(540, 640, "$ " + fmt_num(precio), 120 if precio < 1e5 else 104, BLANCO, 900)
            + txt(540, 730, "× 2 cada día", 40, ROJO, 800))
    # pan dibujado
    pan = (f'<g transform="translate(820 420)"><ellipse rx="70" ry="44" fill="#D9A15B"/><ellipse rx="70" ry="44" fill="none" stroke="#7A4A1E" stroke-width="5"/>'
           '<path d="M-36 -20 q 10 18 0 36 M0 -26 q 10 22 0 50 M36 -20 q 10 18 0 36" stroke="#7A4A1E" stroke-width="5" fill="none"/></g>')
    s.append(aparece(card + pan, t, 0.15, 0.5, 60))
    # barras exponenciales
    bx, by, bw = 1040, 790, 90
    mx = de * 2 ** (dias - 1)
    s.append(aparece(f'<path d="M{bx - 20} {by} H{bx + dias * (bw + 22)}" stroke="{LINEA}" stroke-width="4"/>', t, 0.3))
    for d in range(1, dias + 1):
        p = c01(dia_f - d + 1)
        if p <= 0:
            continue
        val = de * 2 ** (d - 1)
        hgt = 520 * val / mx * ease_out(p)
        x = bx + (d - 1) * (bw + 22)
        col = ROJO if d == dia else "#7A2A35"
        s.append(f'<rect x="{x}" y="{f(by - max(hgt, 4))}" width="{bw}" height="{f(max(hgt, 4))}" rx="8" fill="{col}"/>')
        s.append(txt(x + bw / 2, by + 44, f"D{d}", 30, GRIS, 700))
        if d == dia:
            s.append(txt(x + bw / 2, by - hgt - 20, fmt_corto(val), 30, BLANCO, 800))
    return "".join(s)


def _partir_numero(valor):
    m = re.match(r"^([×]?)([\d.]+)(\s.*)?$", valor)
    if not m:
        return None
    return m.group(1), int(m.group(2).replace(".", "")), (m.group(3) or "")


def numero(v, t, dur):
    col = COLOR.get(v.get("color", "dorado"), ORO)
    valor = v["valor"]
    partes = _partir_numero(valor) if v.get("contar", True) else None
    pc = ease_out(prog(t, 0.3, min(1.8, dur * 0.4)))
    if partes:
        pre, n, suf = partes
        mostrado = pre + fmt_num(n * pc) + suf
    else:
        mostrado = valor
    fs = min(250, 1650 / max(1, len(valor) * 0.62))
    s = [f'<circle cx="960" cy="470" r="{f(420 + 20 * math.sin(t * 2))}" fill="url(#{GLOW_DE.get(col, "gOro")})"/>']
    # anillos
    for i, r in enumerate((330, 380)):
        a = 360 * ease_out(prog(t, 0.1 + i * 0.15, 1.2))
        if a > 1:
            x2 = 960 + r * math.sin(math.radians(a))
            y2 = 470 - r * math.cos(math.radians(a))
            s.append(f'<path d="M960 {470 - r} A{r} {r} 0 {1 if a > 180 else 0} 1 {f(x2)} {f(y2)}" fill="none" stroke="{col}" stroke-opacity="{0.35 - i * 0.15:.2f}" stroke-width="{4 - i}"/>')
    num_svg = txt(960, 470 + fs * 0.36, mostrado, fs, col, 900)
    if partes:
        s.append(aparece(num_svg, t, 0.2, 0.3, 30))
    else:
        s.append(aparece(num_svg, t, 0.25, 0.55, cx=960, cy=470, escala=True))
    s.append(aparece(txt(960, 650, v.get("etiqueta", ""), 58, BLANCO, 800), t, 0.6, 0.45))
    if v.get("nota"):
        nota = v["nota"]
        w = ancho_txt(nota, 34, 600) + 70
        s.append(aparece(f'<rect x="{f(960 - w / 2)}" y="700" width="{f(w)}" height="64" rx="32" fill="{PANEL}" stroke="{col}" stroke-width="2"/>'
                         + txt(960, 744, nota, 34, GRIS, 600), t, 1.0, 0.45))
    return "".join(s)


def capitulo(v, t, dur, acento):
    s = []
    n = f'{v["num"]:02d}'
    p = ease_out(prog(t, 0.1, 0.8))
    s.append(f'<g opacity="{p:.3f}" transform="translate({f(lerp(-200, 0, p))} 0)">'
             + txt(520, 760, n, 560, "none", 900, extra=f'stroke="{acento}" stroke-width="6" stroke-opacity="0.9"') + '</g>')
    s.append(aparece(txt(980, 380, f"CAPÍTULO {v['num']}", 40, acento, 800, "start", extra='letter-spacing="10"'), t, 0.35, 0.4))
    s.append(aparece(txt(970, 530, v["pais"], 150 if len(v["pais"]) < 9 else 128, BLANCO, 900, "start"), t, 0.5, 0.5, 50))
    s.append(aparece(txt(980, 640, v["anio"], 90, ROJO if v["num"] != 7 else ORO, 800, "start"), t, 0.75, 0.45))
    # bandera con barrido
    pb = ease_out(prog(t, 0.9, 0.7))
    if pb > 0:
        s.append(f'<clipPath id="cb"><rect x="1300" y="580" width="{f(330 * pb)}" height="220"/></clipPath>'
                 f'<g clip-path="url(#cb)">{bandera(v["bandera"], 1300, 580, 330, 220)}</g>')
    # línea que corre
    s.append(f'<rect x="980" y="680" width="{f(260 * ease_out(prog(t, 1.0, 0.6)))}" height="6" fill="{acento}"/>')
    return "".join(s)


def lista(v, t, dur):
    causa = v.get("modo") == "causa"
    col = ROJO if causa else VERDE
    items = v["items"]
    ya = v.get("ya", 0)
    nuevos = len(items) - ya
    s = [titulo_seccion(v["titulo"], 0.6 if ya else t, col)]
    chip = "CAUSAS" if causa else "SALIDA"
    s.append(f'<g transform="translate(1600 200)"><rect width="180" height="56" rx="28" fill="{col}" opacity="0.2"/><rect width="180" height="56" rx="28" fill="none" stroke="{col}" stroke-width="3"/>'
             + txt(90, 38, chip, 28, col, 900, extra='letter-spacing="4"') + '</g>')
    paso = min(1.6, (dur * 0.75 - 0.4) / max(1, nuevos))
    alto = 140 if len(items) <= 3 else 124
    y0 = 330
    for j, (ic, texto) in enumerate(items):
        y = y0 + j * (alto + 16)
        if j < ya:
            st, viejo = -1.0, True
        else:
            st, viejo = 0.4 + (j - ya) * paso, False
        fila = (f'<rect x="160" y="{y}" width="1600" height="{alto}" rx="24" fill="{PANEL}" stroke="{LINEA}" stroke-width="2"/>'
                f'<rect x="160" y="{y}" width="10" height="{alto}" rx="5" fill="{col}"/>'
                + icono(ic, 270, y + alto / 2, col, 0.95 if alto == 140 else 0.85)
                + txt(370, y + alto / 2 + 20, texto, 56, BLANCO, 800, "start"))
        if not viejo and j == len(items) - 1 and nuevos >= 1:
            # brillo en la fila más reciente
            fila += f'<rect x="160" y="{y}" width="1600" height="{alto}" rx="24" fill="none" stroke="{col}" stroke-width="3" opacity="{0.4 + 0.3 * math.sin(t * 4):.2f}"/>'
        s.append(fila if viejo else _entra_lado(fila, t, st))
    return "".join(s)


def _entra_lado(svg, t, st):
    p = prog(t, st, 0.45)
    if p <= 0:
        return ""
    return f'<g opacity="{f(min(1, p * 2))}" transform="translate({f(-120 * (1 - ease_out(p)))} 0)">{svg}</g>'


def grafica(v, t, dur):
    col = COLOR.get(v.get("color", "rojo"), ROJO)
    vals, etq = v["valores"], v["etiquetas"]
    lg = v.get("log", False)
    x0, x1, y0, y1 = 300, 1600, 820, 420
    s = [titulo_seccion(v["titulo"], t, col)]
    s.append(f'<rect x="200" y="300" width="1540" height="580" rx="28" fill="{PANEL}" opacity="0.65"/>')
    for k in range(5):
        y = y0 - (y0 - y1) * k / 4
        s.append(f'<path d="M{x0} {f(y)} H{x1}" stroke="{LINEA}" stroke-width="2" stroke-dasharray="6 10"/>')
    tr = (lambda z: math.log10(z)) if lg else (lambda z: z)
    lo = min(0, min(tr(z) for z in vals)) if not lg else min(tr(z) for z in vals)
    hi = max(tr(z) for z in vals)
    pts = []
    n = len(vals)
    for i, z in enumerate(vals):
        x = x0 + (x1 - x0) * (i / (n - 1) if n > 1 else 0.5)
        y = y0 - (y0 - y1) * (tr(z) - lo) / ((hi - lo) or 1)
        pts.append((x, y))
    pd = ease_io(prog(t, 0.5, max(1.2, dur * 0.55)))
    seg = pd * (n - 1)
    k = int(seg)
    vis = pts[:k + 1]
    if k < n - 1:
        fr = seg - k
        vis.append((lerp(pts[k][0], pts[k + 1][0], fr), lerp(pts[k][1], pts[k + 1][1], fr)))
    for i, (x, _) in enumerate(pts):
        s.append(txt(x, 860, etq[i], 30, GRIS, 700))
    if len(vis) >= 2:
        d = " ".join(f"{'M' if i == 0 else 'L'}{f(x)} {f(y)}" for i, (x, y) in enumerate(vis))
        area = d + f" L{f(vis[-1][0])} {y0} L{f(vis[0][0])} {y0} Z"
        s.append(f'<path d="{area}" fill="url(#{"areaV" if col == VERDE else "areaR"})"/>')
        s.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round" stroke-linejoin="round"/>')
    for i, (x, y) in enumerate(pts):
        if seg + 1e-6 >= i:
            pp = c01((seg - i) * 3 + 0.34) if i else 1
            s.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(13 * ease_back(pp))}" fill="{FONDO1}" stroke="{col}" stroke-width="6"/>')
            lab = fmt_corto(vals[i]) + (" " + v["unidad"] if v.get("unidad") and i < n - 1 else "")
            if i < n - 1:
                s.append(f'<g opacity="{pp:.2f}">' + txt(x, y - 30, lab, 32, BLANCO, 800) + '</g>')
    if pd >= 1 and v.get("final"):
        x, y = pts[-1]
        fin = v["final"]
        w = ancho_txt(fin, 46) + 50
        bx, by = x - w - 40, y - 38
        s.append(aparece(f'<rect x="{f(bx)}" y="{f(by)}" width="{f(w)}" height="76" rx="18" fill="{col}"/>'
                         + txt(bx + w / 2, by + 53, fin, 46, FONDO1, 900), t, 0.5 + max(1.2, dur * 0.55), 0.4, cx=bx + w, cy=y, escala=True))
    if lg and "log" not in v["titulo"]:
        s.append(txt(1720, 290, "escala logarítmica", 24, GRIS, 600, "end", extra='font-style="italic"'))
    return "".join(s)


def barras(v, t, dur):
    items = v["items"]
    s = [titulo_seccion(v["titulo"], t, ROJO)]
    mx = max(math.log10(z) for _, z, _ in items)
    for i, (lab, z, vt) in enumerate(items):
        y = 340 + i * 135
        st = 0.5 + i * min(1.3, dur * 0.6 / len(items))
        p = ease_out(prog(t, st, 0.9))
        w = 1000 * math.log10(z) / mx * p
        fila = (txt(160, y + 58, lab, 40, BLANCO, 800, "start")
                + f'<rect x="620" y="{y + 10}" width="1000" height="74" rx="14" fill="{PANEL}"/>'
                + f'<rect x="620" y="{y + 10}" width="{f(max(w, 0.1))}" height="74" rx="14" fill="{ROJO if i == 0 else "#B23A48"}"/>'
                + f'<g opacity="{c01(p * 2 - 1):.2f}">' + txt(620 + w + (20 if w < 640 else -20), y + 60, vt, 36, BLANCO if w < 640 else FONDO1, 900, "start" if w < 640 else "end") + '</g>')
        s.append(_entra_lado(fila, t, st - 0.2))
    return "".join(s)


def ceros(v, t, dur):
    num = v["numero"]
    quitar = v.get("quitar", 0)
    etapas = v.get("etapas")
    chars = list(num)
    quita = [False] * len(chars)
    orden = []  # índices quitados en orden de caída (derecha a izquierda)
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
    fs = min(190, 1560 / (len(chars) * 0.6))
    cw = fs * 0.6
    x0 = 960 - len(chars) * cw / 2
    yb = 520
    s = [txt(960, 260, "QUITANDO CEROS" if quitar else "LA CONVERSIÓN", 40, ORO, 800, extra='letter-spacing="10"')]
    # tiempos de caída
    inicio = 1.0
    fin_caida = max(inicio + 0.6, dur * 0.62)
    tiempos = {}
    if etapas:
        grupos, pos = [], 0
        ceros_orden = orden[:]
        # repartir por cantidad de ceros
        idx = 0
        for g in etapas:
            grp, z = [], 0
            while idx < len(ceros_orden) and z < g:
                if chars[ceros_orden[idx]] == "0":
                    z += 1
                grp.append(ceros_orden[idx])
                idx += 1
            grupos.append(grp)
        if idx < len(ceros_orden):
            grupos[-1] += ceros_orden[idx:]
        tg = (fin_caida - inicio) / len(grupos)
        for gi, grp in enumerate(grupos):
            for k, ci in enumerate(grp):
                tiempos[ci] = inicio + gi * tg + k * min(0.07, tg * 0.5 / max(1, len(grp)))
    else:
        paso = (fin_caida - inicio) / max(1, len(orden))
        for k, ci in enumerate(orden):
            tiempos[ci] = inicio + k * paso
    restantes = [i for i in range(len(chars)) if not quita[i]]
    p_centro = ease_io(prog(t, fin_caida + 0.3, 0.6)) if quitar else 0
    nr = len(restantes)
    for i, ch in enumerate(chars):
        x = x0 + i * cw + cw / 2
        if quita[i]:
            tc = tiempos.get(i, 99)
            q = c01((t - tc) / 0.9)
            if q >= 1:
                continue
            dy = 900 * q * q
            rot = (40 if i % 2 else -30) * q
            col = ROJO if t > tc - 0.25 else BLANCO
            s.append(f'<g opacity="{f(1 - q)}" transform="translate({f(x)} {f(yb + dy)}) rotate({f(rot)})">' + txt(0, 0, ch, fs, col, 800, fam=MONO) + '</g>')
        else:
            k = restantes.index(i)
            xc = 960 + (k - (nr - 1) / 2) * cw
            xx = lerp(x, xc, p_centro)
            esc = 1 + 0.5 * p_centro
            s.append(f'<g transform="translate({f(xx)} {f(yb)}) scale({esc:.3f})">' + txt(0, 0, ch, fs, BLANCO, 800, fam=MONO) + '</g>')
    if v.get("moneda"):
        op = 1 - prog(t, fin_caida, 0.4) if quitar else 1
        if op > 0:
            s.append(f'<g opacity="{op:.2f}">' + aparece(txt(960, yb + 90, v["moneda"], 44, GRIS, 700), t, 0.3, 0.4) + '</g>')
    if etapas:
        anios = ["2008", "2018", "2021"]
        tg = (fin_caida - inicio) / len(etapas)
        for gi, g in enumerate(etapas):
            x = 960 + (gi - 1) * 380
            s.append(aparece(f'<rect x="{x - 160}" y="630" width="320" height="76" rx="38" fill="{PANEL}" stroke="{ROJO}" stroke-width="3"/>'
                             + txt(x, 681, f"{anios[gi] if gi < 3 else ''}:  −{g} ceros", 36, BLANCO, 800), t, inicio + gi * tg, 0.4, cx=x, cy=668, escala=True))
    res = v.get("resultado", "")
    t_res = fin_caida + 0.6 if quitar else 1.2
    if res:
        w = ancho_txt(res, 64) + 90
        y = 812 if etapas else 720
        s.append(aparece(f'<rect x="{f(960 - w / 2)}" y="{y - 70}" width="{f(w)}" height="100" rx="50" fill="{VERDE}"/>'
                         + txt(960, y + 2, res, 64, FONDO1, 900), t, t_res, 0.5, cx=960, cy=y - 20, escala=True))
    return "".join(s)


def billete(v, t, dur):
    valor = v["valor"]
    col = v.get("color", "#A5D6A7")
    p = ease_out(prog(t, 0.15, 0.8))
    rot = lerp(-14, -3, p) + 1.2 * math.sin(t * 1.3)
    y = lerp(780, 440, p) + 8 * math.sin(t * 1.7)
    bw, bh = 1300, 520
    gu = []
    for k in range(9):
        amp = 18 + k * 3
        d = "M-560 " + " ".join(f"L{f(-560 + j * 20)} {f(-200 + k * 48 + amp * math.sin(j * 0.45 + k))}" for j in range(57))
        gu.append(f'<path d="{d}" fill="none" stroke="#000" stroke-opacity="0.12" stroke-width="2"/>')
    fs = min(118, 1100 / (len(valor) * 0.62))
    ros = "".join(f'<ellipse rx="96" ry="34" fill="none" stroke="#000" stroke-opacity="0.22" stroke-width="3" transform="rotate({a})"/>' for a in range(0, 180, 30))
    nota = (f'<g transform="translate(960 {f(y)}) rotate({f(rot)})">'
            f'<rect x="{-bw / 2 + 14}" y="{-bh / 2 + 18}" width="{bw}" height="{bh}" rx="20" fill="#000" opacity="0.35"/>'
            f'<rect x="{-bw / 2}" y="{-bh / 2}" width="{bw}" height="{bh}" rx="20" fill="{col}"/>'
            f'<rect x="{-bw / 2 + 26}" y="{-bh / 2 + 26}" width="{bw - 52}" height="{bh - 52}" rx="12" fill="none" stroke="#000" stroke-opacity="0.45" stroke-width="5"/>'
            + "".join(gu)
            + f'<g transform="translate(-450 -110)">{ros}<circle r="40" fill="none" stroke="#000" stroke-opacity="0.3" stroke-width="4"/></g>'
            + txt(0, -150, v.get("moneda", ""), 46, "#1B1B1B", 900, extra='letter-spacing="8" opacity="0.8"')
            + txt(0, 40 + fs * 0.1, valor, fs, "#141414", 900)
            + txt(bw / 2 - 70, -bh / 2 + 100, "★", 70, "#000", 900, extra='opacity="0.4"')
            + txt(0, 200, "BANCO CENTRAL", 34, "#1B1B1B", 800, extra='letter-spacing="14" opacity="0.6"')
            + '</g>')
    s = [nota]
    nceros = valor.count("0")
    chip = f"un 1 con {nceros} ceros" if valor.startswith("1") and nceros > 4 else ""
    chips = [(c, col_c, st) for c, col_c, st in ((chip, ORO, 1.0), (v.get("nota", ""), TURQ, 1.4)) if c]
    ws = [ancho_txt(c, 44) + 70 for c, _, _ in chips]
    x = 960 - (sum(ws) + 30 * (len(ws) - 1)) / 2
    for (c, col_c, st), w in zip(chips, ws):
        s.append(aparece(f'<rect x="{f(x)}" y="770" width="{f(w)}" height="76" rx="38" fill="{col_c}"/>' + txt(x + w / 2, 822, c, 44, FONDO1, 900),
                         t, st, 0.45, cx=x + w / 2, cy=808, escala=True))
        x += w + 30
    return "".join(s)


def _envolver(s, n):
    pal, lin, act = s.split(), [], ""
    for p in pal:
        if act and len(act + " " + p) > n:
            lin.append(act)
            act = p
        else:
            act = (act + " " + p).strip()
    if act:
        lin.append(act)
    return lin


def tiempo(v, t, dur):
    ev = v["eventos"]
    n = len(ev)
    x0, x1, y = 220, 1700, 560
    pl = ease_io(prog(t, 0.2, max(1.0, dur * 0.65)))
    s = [txt(960, 260, "LÍNEA DE TIEMPO", 40, ORO, 800, extra='letter-spacing="10"')]
    s.append(f'<path d="M{x0} {y} H{x1}" stroke="{LINEA}" stroke-width="6" stroke-linecap="round"/>')
    s.append(f'<path d="M{x0} {y} H{f(lerp(x0, x1, pl))}" stroke="{ORO}" stroke-width="6" stroke-linecap="round"/>')
    for i, (fecha, texto) in enumerate(ev):
        x = lerp(x0 + 120, x1 - 120, i / (n - 1) if n > 1 else 0.5)
        frac = (x - x0) / (x1 - x0)
        st = 0.2 + frac * max(1.0, dur * 0.65) - 0.1
        arriba = i % 2 == 0
        col = ORO if i < n - 1 else (ROJO if any(w in texto.lower() for w in ("crisis", "hiper", "vuelve", "fin")) else VERDE)
        nodo = (f'<circle cx="{f(x)}" cy="{y}" r="22" fill="{FONDO1}" stroke="{col}" stroke-width="7"/><circle cx="{f(x)}" cy="{y}" r="9" fill="{col}"/>')
        lines = _envolver(texto, 16)
        if arriba:
            card_y = y - 70 - 60 * len(lines) - 70
        else:
            card_y = y + 70
        ch = 70 + 56 * len(lines)
        card = (f'<path d="M{f(x)} {y + (-26 if arriba else 26)} V{f(card_y + (ch if arriba else 0))}" stroke="{col}" stroke-width="3"/>'
                f'<rect x="{f(x - 190)}" y="{f(card_y)}" width="380" height="{f(ch)}" rx="20" fill="{PANEL}" stroke="{LINEA}" stroke-width="2"/>'
                + txt(x, card_y + 50, fecha, 38, col, 900)
                + "".join(txt(x, card_y + 104 + k * 50, ln, 38, BLANCO, 700) for k, ln in enumerate(lines)))
        s.append(aparece(nodo, t, st, 0.35, cx=x, cy=y, escala=True))
        s.append(aparece(card, t, st + 0.1, 0.4, 30 if arriba else -30))
    return "".join(s)


def texto(v, t, dur):
    frase = v["frase"]
    # tokens con resaltado *...*
    tokens = []
    resal = False
    for parte in re.split(r"(\*)", frase):
        if parte == "*":
            resal = not resal
            continue
        for p in parte.split():
            tokens.append((p, resal))
    fs = 104
    lineas, act, largo = [], [], 0
    for tok in tokens:
        if act and largo + len(tok[0]) + 1 > 20:
            lineas.append(act)
            act, largo = [], 0
        act.append(tok)
        largo += len(tok[0]) + 1
    if act:
        lineas.append(act)
    if max(sum(len(p) + 1 for p, _ in ln) for ln in lineas) > 18:
        fs = 92
    s = []
    y0 = 520 - (len(lineas) - 1) * fs * 0.62
    k = 0
    for li, ln in enumerate(lineas):
        anchos = [ancho_txt(p, fs, 900) for p, _ in ln]
        esp = fs * 0.3
        total = sum(anchos) + esp * (len(ln) - 1)
        x = 960 - total / 2
        y = y0 + li * fs * 1.25
        for (p, r), w in zip(ln, anchos):
            st = 0.25 + k * 0.12
            if r:
                pb = ease_out(prog(t, st + 0.25, 0.4))
                s.append(f'<rect x="{f(x - 12)}" y="{f(y - fs * 0.82)}" width="{f((w + 24) * pb)}" height="{f(fs * 1.05)}" rx="10" fill="{ORO}"/>')
                s.append(aparece(txt(x, y, p, fs, FONDO1 if pb > 0.5 else ORO, 900, "start"), t, st, 0.4, 50))
            else:
                s.append(aparece(txt(x, y, p, fs, BLANCO, 900, "start"), t, st, 0.4, 50))
            x += w + esp
            k += 1
    if v.get("sub"):
        yy = y0 + len(lineas) * fs * 1.25 + 30
        s.append(f'<rect x="{f(960 - 60 * ease_out(prog(t, 0.9, 0.5)))}" y="{f(yy - 60)}" width="{f(120 * ease_out(prog(t, 0.9, 0.5)))}" height="5" fill="{ORO}"/>')
        s.append(aparece(txt(960, yy + 10, v["sub"], 44, GRIS, 600), t, 1.0, 0.5))
    return "".join(s)


PAISES = [("alemania", "Alemania", "1923"), ("hungria", "Hungría", "1946"), ("bolivia", "Bolivia", "1985"), ("argentina", "Argentina", "1989"),
          ("brasil", "Brasil", "1994"), ("zimbabue", "Zimbabue", "2008"), ("venezuela", "Venezuela", "2017")]


def paises(v, t, dur):
    concl = v.get("conclusion")
    s = [aparece(txt(960, 250, "7 PAÍSES · 1 PATRÓN" if concl else "7 PAÍSES · 7 HIPERINFLACIONES", 64, BLANCO, 900, extra='letter-spacing="4"'), t, 0.1, 0.45)]
    paso = min(0.45, (dur * 0.6) / 7)
    for i, (b, nom, an) in enumerate(PAISES):
        fila = 0 if i < 4 else 1
        cols = 4 if fila == 0 else 3
        j = i if fila == 0 else i - 4
        cx = 960 + (j - (cols - 1) / 2) * 400
        cy = 430 + fila * 300
        card = (f'<rect x="{cx - 175}" y="{cy - 120}" width="350" height="260" rx="24" fill="{PANEL}" stroke="{LINEA}" stroke-width="2"/>'
                + bandera(b, cx - 110, cy - 90, 220, 140)
                + txt(cx, cy + 92, nom, 40, BLANCO, 800) + txt(cx + 0, cy + 128, an, 30, ORO, 800))
        s.append(aparece(card, t, 0.4 + i * paso, 0.45, cx=cx, cy=cy, escala=True))
    return "".join(s)


def suscribete(v, t, dur):
    s = [aparece(txt(500, 380, "¿Qué país", 84, BLANCO, 900), t, 0.2, 0.45),
         aparece(txt(500, 480, "analizamos", 84, BLANCO, 900), t, 0.35, 0.45),
         aparece(txt(500, 580, "a fondo?", 84, ORO, 900), t, 0.5, 0.45),
         aparece(txt(500, 680, "Déjalo en los comentarios", 40, GRIS, 600), t, 0.9, 0.45)]
    s.append(f'<g transform="translate(180 40) scale(0.9)">{A.suscribete_a(t)}</g>')
    return "".join(s)


# ---------------------------------------------------------------- escena
def acento_de(v):
    tipo = v["tipo"]
    if tipo == "capitulo":
        return ORO
    if tipo == "lista":
        return ROJO if v.get("modo") == "causa" else VERDE
    if tipo in ("numero", "grafica"):
        return COLOR.get(v.get("color", "dorado"), ORO)
    if tipo == "ceros":
        return VERDE
    return TURQ


def escena(idx, texto_narr, v, t, dur, ctx):
    acento = ctx["acento"]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">', fondo(ctx["tg"], acento)]
    tipo = v["tipo"]
    k = 1 + 0.035 * (t / max(dur, 1))
    cuerpo = {"precio_ticker": precio_ticker, "numero": numero, "lista": lista, "grafica": grafica, "barras": barras,
              "ceros": ceros, "billete": billete, "tiempo": tiempo, "texto": texto, "paises": paises, "suscribete": suscribete}
    if tipo == "capitulo":
        c = capitulo(v, t, dur, acento)
    else:
        c = cuerpo[tipo](v, t, dur)
    s.append(f'<g transform="translate(960 520) scale({k:.4f}) translate(-960 -520)">{c}</g>')
    s.append(capa_superior(ctx, t))
    s.append(subtitulos(texto_narr, t, ctx["vdur"]))
    s.append(transicion(t, ORO if tipo == "capitulo" else acento))
    s.append('</svg>')
    return "".join(s)


def contextos():
    """Etiqueta de capítulo y acento por escena."""
    out, lab = [], "INTRODUCCIÓN"
    for texto_n, v in GU.E:
        if v["tipo"] == "capitulo":
            lab = f'CAP. {v["num"]:02d} · {v["pais"]} {v["anio"]}'
        if v["tipo"] == "paises" and v.get("conclusion"):
            lab = "CONCLUSIÓN"
        out.append({"etiqueta": lab, "acento": acento_de(v)})
    return out


# ---------------------------------------------------------------- audio
def generar_voces(tts_dir, textos, tmp):
    import sherpa_onnx
    k = os.path.join(tts_dir, "kokoro-multi-lang-v1_0")
    kok = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
        model=f"{k}/model.onnx", voices=f"{k}/voices.bin", tokens=f"{k}/tokens.txt", data_dir=f"{k}/espeak-ng-data",
        dict_dir=f"{k}/dict", lexicon=f"{k}/lexicon-us-en.txt,{k}/lexicon-zh.txt", lang="es"), num_threads=4)))
    voces = []
    for n, texto_n in enumerate(textos):
        a = kok.generate(texto_n, sid=VOZ_SID, speed=VOZ_VEL)
        y = np.array(a.samples, dtype=np.float32)
        ruta = os.path.join(tmp, f"v{n}")
        sf.write(ruta + ".in.wav", y, a.sample_rate)
        filtros = (f"asetrate={int(a.sample_rate * VOZ_TONO)},aresample={SR},atempo={1 / VOZ_TONO:.5f},"
                   "highpass=f=70,equalizer=f=180:t=q:w=1:g=2,acompressor=threshold=-18dB:ratio=3:attack=5:release=80")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ruta + ".in.wav", "-af", filtros, "-ac", "1", ruta + ".out.wav"], check=True)
        z, _ = sf.read(ruta + ".out.wav")
        os.remove(ruta + ".in.wav")
        os.remove(ruta + ".out.wav")
        voces.append(np.concatenate([np.zeros(int(SR * 0.12)), z, np.zeros(int(SR * 0.45))]))
        if n % 10 == 0:
            print(f"voz {n}/{len(textos)}", flush=True)
    return voces


def musica_doc(total):
    """Colchón cinematográfico: pads lentos Am-F-C-G + pulso grave suave."""
    n = int(SR * total) + SR
    tt = np.arange(n) / SR
    acordes = [(220.0, 261.63, 329.63), (174.61, 220.0, 261.63), (130.81, 164.81, 196.0), (196.0, 246.94, 293.66)]
    bajos = [55.0, 43.65, 65.41, 49.0]
    dur_ac = 8.0
    out = np.zeros(n)
    rng = np.random.default_rng(7)
    for ci in range(int(total / dur_ac) + 2):
        a0 = int(ci * dur_ac * SR)
        a1 = min(n, a0 + int((dur_ac + 2.5) * SR))
        if a0 >= n:
            break
        seg = tt[a0:a1] - ci * dur_ac
        env = np.minimum(1, seg / 2.5) * np.minimum(1, np.maximum(0, (dur_ac + 2.5 - seg) / 2.5))
        notas, bajo = acordes[ci % 4], bajos[ci % 4]
        sig = np.zeros_like(seg)
        for fr in notas:
            for det in (-0.6, 0.0, 0.7):
                ph = rng.uniform(0, 2 * np.pi)
                sig += 0.5 * np.sin(2 * np.pi * (fr + det) * seg + ph) + 0.18 * np.sin(4 * np.pi * (fr + det) * seg + ph)
        sig += 1.2 * np.sin(2 * np.pi * bajo * seg)
        out[a0:a1] += sig * env * 0.06
    # pulso tipo latido cada 1 s
    pulso = np.zeros(n)
    golpe = np.sin(2 * np.pi * 52 * np.arange(int(0.25 * SR)) / SR) * np.exp(-np.arange(int(0.25 * SR)) / (0.06 * SR))
    for b in np.arange(0, total, 1.0):
        i0 = int(b * SR)
        g = golpe * (1.0 if int(b) % 2 == 0 else 0.6)
        pulso[i0:i0 + len(g)] += g[:n - i0]
    out += pulso * 0.12
    # brillo: arpegio suave de campanita cada 2 s
    for b in np.arange(0, total, 2.0):
        ci = int(b / dur_ac) % 4
        fr = acordes[ci][int(b / 2) % 3] * 2
        i0 = int(b * SR)
        m = min(int(1.6 * SR), n - i0)
        e = np.arange(m) / SR
        out[i0:i0 + m] += 0.035 * np.sin(2 * np.pi * fr * e) * np.exp(-e / 0.5)
    try:
        from scipy.signal import lfilter
        out = lfilter([0.25], [1, -0.75], out)
    except ImportError:
        pass
    return out[:int(SR * total)] / (np.abs(out).max() + 1e-9)


def sfx_riser(d=0.9):
    m = int(d * SR)
    e = np.arange(m) / SR
    ruido = np.random.default_rng(3).normal(0, 1, m)
    fr = 200 + 1600 * (e / d) ** 2
    return (0.25 * ruido * (e / d) ** 2 + 0.3 * np.sin(2 * np.pi * np.cumsum(fr) / SR) * (e / d)) * 0.5


def eventos(v, dur):
    tipo = v["tipo"]
    ev = [(0.0, "whoosh", 0.55)]
    if tipo == "capitulo":
        ev += [(0.3, "boom", 0.9), (0.9, "swoosh", 0.5)]
    elif tipo == "numero":
        if v.get("contar", True) and _partir_numero(v["valor"]):
            d = min(1.8, dur * 0.4)
            ev += [(0.3 + k * d / 14, "tick", 0.45) for k in range(14)] + [(0.3 + d, "ding", 0.5)]
        else:
            ev.append((0.3, "boom", 0.6))
    elif tipo == "lista":
        ya = v.get("ya", 0)
        nuevos = len(v["items"]) - ya
        paso = min(1.6, (dur * 0.75 - 0.4) / max(1, nuevos))
        ev += [(0.4 + j * paso, "pop", 0.55) for j in range(nuevos)]
    elif tipo == "grafica":
        d = max(1.2, dur * 0.55)
        ev += [(0.5, "swoosh", 0.5), (0.5 + d, "ding", 0.5)]
    elif tipo == "barras":
        ev += [(0.5 + i * min(1.3, dur * 0.6 / len(v["items"])), "swoosh", 0.45) for i in range(len(v["items"]))]
    elif tipo == "ceros":
        fin = max(1.6, dur * 0.62)
        n = v.get("quitar", 0)
        if n:
            ev += [(1.0 + k * (fin - 1.0) / n, "tick", 0.5) for k in range(n)]
            ev.append((fin + 0.6, "ding", 0.6))
        else:
            ev.append((1.2, "ding", 0.6))
    elif tipo == "billete":
        ev += [(0.2, "swoosh", 0.6), (1.0, "pop", 0.5)]
    elif tipo == "tiempo":
        n = len(v["eventos"])
        for i in range(n):
            frac = (lerp(120, 1360, i / (n - 1) if n > 1 else 0.5)) / 1480
            ev.append((0.1 + frac * max(1.0, dur * 0.65), "pop", 0.5))
    elif tipo == "texto":
        ev.append((0.6, "pop", 0.45))
    elif tipo == "paises":
        paso = min(0.45, (dur * 0.6) / 7)
        ev += [(0.4 + i * paso, "pop", 0.45) for i in range(7)]
    elif tipo == "suscribete":
        ev += [(0.3, "pop", 0.6), (1.75, "click", 0.8), (2.0, "campana", 0.7)]
    return ev


# ---------------------------------------------------------------- render
def _cuadro(args):
    idx, texto_n, v, t, dur, ctx = args
    svg = escena(idx, texto_n, v, t, dur, ctx).encode("utf-8")
    return subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-f", "png"], input=svg, capture_output=True, check=True).stdout


def muestra(salida_dir):
    """Hoja de contacto: un cuadro representativo de cada tipo de escena."""
    os.makedirs(salida_dir, exist_ok=True)
    ctxs = contextos()
    vistos = {}
    for i, (texto_n, v) in enumerate(GU.E):
        clave = v["tipo"] + ("_e" if v.get("etapas") else "") + ("_y" if v.get("ya") else "")
        if clave in vistos:
            continue
        vistos[clave] = i
        dur = 7.0
        for t in (0.25, 5.5):
            ctx = dict(ctxs[i], tg=i * 7 + t, total=len(GU.E) * 7, vdur=6.5)
            png = _cuadro((i, texto_n, v, t, dur, ctx))
            with open(os.path.join(salida_dir, f"{i:02d}_{clave}_{t}.png"), "wb") as fh:
                fh.write(png)
    print("muestras:", len(vistos))


def main():
    if "--muestra" in sys.argv:
        muestra(sys.argv[2])
        return
    tts_dir, salida = sys.argv[1], sys.argv[2]
    fps = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 24
    escenas = GU.E
    tmp = salida + "_tmp"
    os.makedirs(tmp, exist_ok=True)
    voces = generar_voces(tts_dir, [x for x, _ in escenas], tmp)
    durs = [max(len(v) / SR, 3.0) for v in voces]
    vdurs = [len(v) / SR - 0.45 for v in voces]
    total = sum(durs)
    print(f"{len(escenas)} escenas · {total:.1f} s", flush=True)
    A.cargar_sfx()
    A.SFX["riser"] = sfx_riser()
    voz = np.zeros(int(SR * (total + 1)))
    efectos = np.zeros_like(voz)
    t0 = 0.0
    for (texto_n, v), vz, d in zip(escenas, voces, durs):
        i0 = int(SR * t0)
        voz[i0:i0 + len(vz)] += vz
        evs = eventos(v, d)
        if v["tipo"] == "capitulo" and t0 > 1:
            evs.append((-0.9, "riser", 0.6))
        for ts, nombre, vol in evs:
            snd = A.SFX[nombre] * vol * 0.5
            j = i0 + int(SR * ts)
            if 0 <= j < len(efectos):
                efectos[j:j + len(snd)] += snd[:len(efectos) - j]
        t0 += d
    pista = voz + efectos
    pista[:int(SR * total)] += musica_doc(total) * 0.11
    pista = pista[:int(SR * total)]
    pista /= max(1.0, np.abs(pista).max() / 0.95)
    wav = salida + ".wav"
    sf.write(wav, pista.astype(np.float32), SR)
    ctxs = contextos()
    tareas, tg = [], 0.0
    for k, ((texto_n, v), d, vd) in enumerate(zip(escenas, durs, vdurs)):
        for fi in range(int(round(d * fps))):
            t = fi / fps
            tareas.append((k, texto_n, v, t, d, dict(ctxs[k], tg=tg + t, total=total, vdur=vd)))
        tg += d
    print(f"{len(tareas)} cuadros", flush=True)
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(fps), "-i", "-", "-i", wav,
                           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-shortest", "-movflags", "+faststart", salida], stdin=subprocess.PIPE)
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
