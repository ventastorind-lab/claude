"""Render del video de economía con varios personajes y voces.

Uso: python3 render.py <carpeta_tts> <salida.mp4> [fps] [--muestra]
"""
import importlib.util
import math
import os
import random
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
RY = _cargar("rayo_esc", os.path.join(AQUI, "..", "rayo", "generar_escenas.py"))
PJ = _cargar("pj_nuevos", os.path.join(AQUI, "..", "..", "personajes", "nuevos", "generar_personajes.py"))
GU = _cargar("eco_guion", os.path.join(AQUI, "guion.py"))
C, A, HV = CA.C, CA.A, CA.HV
W, H, GY, INK, SR = C.W, C.H, C.GY, C.INK, CA.SR
pop, prog, ease_out, ease_back, lerp, c01, f = A.pop, A.prog, A.ease_out, A.ease_back, A.lerp, A.c01, A.f

# ---------------------------------------------------------------- personajes de ficha (sin el marco de la ficha)
PJ.ficha = lambda bg, acento, etiqueta, nombre, frase, cuerpo: cuerpo
CUERPOS = {"gertrudis": PJ.gertrudis(), "tornillo": PJ.don_tornillo(), "tinto": PJ.tinto(), "socrates": PJ.socrates(), "buho": PJ.doctora_buho()}
ALTO = {"gertrudis": 760, "tornillo": 700, "tinto": 650, "socrates": 750, "byron": 760, "rayo": 740, "billetin": 680, "buho": 820}
NOMBRES = {"gertrudis": "Doña Gertrudis", "tornillo": "Don Tornillo", "tinto": "Tinto", "socrates": "Sócrates", "byron": "Byron", "rayo": "Rayo", "billetin": "Billetín", "buho": "Dra. Búho"}

VOCES = {  # motor, id, velocidad, tono, filtro
    "byron": ("kokoro", 53, 1.12, 1.19, ""),
    "gertrudis": ("kokoro", 28, 1.0, 0.95, ""),
    "tornillo": ("kokoro", 29, 0.95, 0.86, ""),
    "tinto": ("kokoro", 29, 1.05, 1.0, ",highpass=f=260,lowpass=f=3600"),
    "socrates": ("piper", "vits-piper-es_ES-sharvard-medium", 1.0, 1.0, ""),
    "billetin": ("piper", "vits-piper-es_MX-claude-high", 1.12, 1.25, ""),
    "buho": ("piper", "vits-piper-es_AR-daniela-high", 1.0, 1.0, ""),
}


def fmt_num(v):
    return f"{int(round(v)):,}".replace(",", ".")


# ---------------------------------------------------------------- personajes
def personaje(nombre, x, k, t, habla, spec, idx):
    if habla:
        dy = -16 * abs(math.sin(t * 7.5))
    elif spec.get("todos_felices"):
        dy = -30 * abs(math.sin(t * 5 + idx))
    else:
        dy = 3 * math.sin(t * 2 + idx)
    s = ""
    if nombre == "byron":
        boca = ("o" if int(t * 8) % 2 else "sonrisa") if habla else ("grande" if spec.get("todos_felices") else "sonrisa")
        ojos = spec.get("byron_ojos", "feliz" if spec.get("todos_felices") else "normal")
        pose = "saluda" if (habla and idx % 2 == 0 and not spec.get("tarjeta")) else ("senala" if habla else ("celebra" if spec.get("todos_felices") else "normal"))
        s = f'<g transform="translate(0 {f(dy * 0.5)})">' + C.byron(x, t=t, pose=pose, ojos=ojos, boca=boca, k=k * 1.0) + '</g>'
    elif nombre == "rayo":
        pose = "pulgar" if spec.get("rayo_pulgar") else "normal"
        s = f'<g transform="translate(0 {f(dy)})">' + RY.rayo(x, pose, -1 if x > 960 else 1, k) + '</g>'
    else:
        mira = -1 if (x > 960 and nombre in ("tinto",)) else 1
        sq = 1 + (0.03 * math.sin(t * 15) if habla else 0)
        if nombre == "billetin":
            v0, v1 = spec.get("billetin", (1.0, 1.0))
            cuerpo = PJ.billetin(lerp(v0, v1, ease_out(prog(t, 0.8, 2.2))))
        else:
            cuerpo = CUERPOS[nombre]
        s = (f'<g transform="translate({f(x)} {f(GY + dy)}) scale({f(k * mira)} {f(k / sq)}) translate(-600 -970)">'
             f'{cuerpo}</g>')
    if habla:
        hx, hy = x + 150 * k, GY - ALTO[nombre] * k + 40
        a = 0.5 + 0.5 * math.sin(t * 10)
        s += (f'<g stroke="#FFB300" stroke-width="8" stroke-linecap="round" fill="none" opacity="{f(a)}">'
              f'<path d="M{f(hx)} {f(hy)} q 18 20 0 40"/><path d="M{f(hx + 22)} {f(hy - 12)} q 28 32 0 64"/></g>')
    if spec.get("presentacion"):
        p = prog(t, 0.6 + idx * 0.9, 0.4)
        if p > 0:
            s += pop(f'<rect x="{f(x - 120)}" y="{GY + 12}" width="240" height="56" rx="20" fill="{INK}"/>'
                     f'<text x="{f(x)}" y="{GY + 51}" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="30" fill="#FFFFFF">{NOMBRES[nombre]}</text>',
                     x, GY + 40, t, 0.6 + idx * 0.9)
    return s


# ---------------------------------------------------------------- fondos
def fondo(tipo, spec, t):
    rnd = random.Random(7)
    if tipo in ("plano", "cuarto"):
        return HV.fondo(tipo)
    if tipo == "pueblo":
        return RY.cielo("dia", rnd) + RY.fondo("pueblo", "dia", rnd, {}) + RY.suelo("tierra", False)
    if tipo == "mercado":
        s = RY.cielo("dia", rnd) + RY.montanas(False) + RY.suelo("tierra", False)
        rayas = "".join(f'<path d="M{x} 260 h 120 v 90 q -60 40 -120 0 Z" fill="{c}" stroke="{INK}" stroke-width="6"/>'
                        for x, c in zip(range(700, 1900, 120), ["#E53935", "#FFFFFF"] * 6))
        return (s + f'<rect x="720" y="300" width="20" height="600" fill="#8D6E63"/><rect x="1860" y="300" width="20" height="600" fill="#8D6E63"/>'
                + rayas + f'<rect x="700" y="640" width="1200" height="260" fill="#A1887F" stroke="{INK}" stroke-width="8"/>'
                + "".join(arepa(x, 625, 0.9) for x in range(780, 1850, 110)))
    if tipo == "ferreteria":
        vacios = spec.get("estantes_vacios")
        s = [f'<rect width="{W}" height="{H}" fill="#FFE0B2"/>',
             f'<rect x="0" y="{GY}" width="{W}" height="{H - GY}" fill="#8D6E63"/>',
             f'<rect x="760" y="60" width="760" height="110" rx="16" fill="#FFC107" stroke="{INK}" stroke-width="8"/>',
             f'<text x="1140" y="138" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="54" fill="{INK}">FERRETERÍA DON TORNILLO</text>']
        for fila in range(3):
            y = 300 + fila * 170
            s.append(f'<rect x="780" y="{y}" width="1060" height="18" fill="#6D4C41" stroke="{INK}" stroke-width="5"/>')
            for c in range(7):
                if vacios and (c + fila) % 3:
                    continue
                s.append(f'<rect x="{800 + c * 148}" y="{y - 110}" width="130" height="110" rx="6" fill="#D9A066" stroke="{INK}" stroke-width="5"/>'
                         f'<text x="{865 + c * 148}" y="{y - 48}" text-anchor="middle" font-family="Arial" font-weight="bold" font-size="20" fill="{INK}">TORNILLOS</text>')
        s.append(f'<rect x="700" y="700" width="1220" height="200" fill="#A1887F" stroke="{INK}" stroke-width="8"/>')
        return "".join(s)
    if tipo == "banco":
        s = [HV.fondo("plano"),
             f'<polygon points="900,250 1410,130 1920,250" fill="#ECEFF1" stroke="{INK}" stroke-width="10"/>',
             f'<rect x="920" y="250" width="980" height="70" fill="#CFD8DC" stroke="{INK}" stroke-width="8"/>',
             f'<text x="1410" y="305" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="50" fill="{INK}">BANCO CENTRAL</text>']
        for i in range(6):
            s.append(f'<rect x="{960 + i * 165}" y="320" width="70" height="500" fill="#ECEFF1" stroke="{INK}" stroke-width="7"/>')
        s.append(f'<rect x="900" y="820" width="1020" height="40" fill="#B0BEC5" stroke="{INK}" stroke-width="7"/>'
                 f'<rect x="870" y="860" width="1080" height="40" fill="#90A4AE" stroke="{INK}" stroke-width="7"/>')
        return "".join(s)
    if tipo == "sotano":
        luz = 0.25 + 0.05 * math.sin(t * 9)
        return (f'<rect width="{W}" height="{H}" fill="#37474F"/>'
                + "".join(f'<rect x="{x}" y="{y}" width="150" height="70" fill="none" stroke="#2E3B42" stroke-width="5"/>' for x in range(0, W, 150) for y in range(0, GY, 70))
                + f'<polygon points="1250,40 900,{GY} 1600,{GY}" fill="#FFF59D" opacity="{f(luz)}"/>'
                f'<line x1="1250" y1="0" x2="1250" y2="40" stroke="{INK}" stroke-width="6"/><circle cx="1250" cy="50" r="22" fill="#FFF59D" stroke="{INK}" stroke-width="5"/>'
                f'<rect x="0" y="{GY}" width="{W}" height="{H - GY}" fill="#263238"/>')
    if tipo == "oficina":
        persiana = "".join(f'<rect x="1300" y="{120 + i * 34}" width="460" height="20" fill="#455A64"/>' for i in range(12))
        return (f'<rect width="{W}" height="{H}" fill="#1C2833"/>'
                f'<rect x="1300" y="120" width="460" height="410" fill="#0D1B2A" stroke="{INK}" stroke-width="10"/>'
                f'<circle cx="1640" cy="230" r="55" fill="#F5F3CE"/>' + persiana
                + f'<polygon points="1530,530 1100,{GY} 1960,{GY}" fill="#FFF59D" opacity="0.08"/>'
                f'<rect x="0" y="{GY}" width="{W}" height="{H - GY}" fill="#3E2723"/>'
                f'<rect x="900" y="700" width="900" height="40" fill="#5D4037" stroke="{INK}" stroke-width="7"/>'
                f'<path d="M1650 700 L 1690 600 L 1760 600" fill="none" stroke="{INK}" stroke-width="8"/><path d="M1720 560 L 1800 560 L 1780 610 L 1740 610 Z" fill="#FFC107" stroke="{INK}" stroke-width="6"/>')
    if tipo == "historia":
        s = f'<rect width="{W}" height="{H}" fill="#E8D5A9"/>'
        r = random.Random(3)
        s += "".join(f'<line x1="0" y1="{y}" x2="{W}" y2="{y + r.randint(-6, 6)}" stroke="#D7BF8C" stroke-width="2" opacity="0.6"/>' for y in range(20, H, 26))
        s += f'<rect x="0" y="{GY}" width="{W}" height="{H - GY}" fill="#C9A86A"/>'
        s += f'<rect width="{W}" height="{H}" fill="none" stroke="#8D6E3E" stroke-width="60" opacity="0.35"/>'
        return s
    return HV.fondo("plano")


# ---------------------------------------------------------------- utilería
def billete(x, y, k=1.0, rot=0, texto="$ 1.000.000", color="#81C784"):
    fs = min(30, int(140 / max(1, len(texto) * 0.6)))
    return (f'<g transform="translate({f(x)} {f(y)}) rotate({f(rot)}) scale({f(k)})">'
            f'<rect x="-120" y="-55" width="240" height="110" rx="8" fill="{color}" stroke="{INK}" stroke-width="5"/>'
            '<rect x="-108" y="-43" width="216" height="86" rx="6" fill="none" stroke="#2E7D32" stroke-width="3"/>'
            '<circle cx="-60" cy="0" r="28" fill="#A5D6A7" stroke="#2E7D32" stroke-width="3"/>'
            f'<text x="35" y="{fs * 0.35:.0f}" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="{fs}" fill="#1B5E20">{escape(texto)}</text></g>')


def lluvia_billetes(t, n=36):
    r = random.Random(11)
    s = []
    for _ in range(n):
        x0, v, y0 = r.randint(0, W), r.uniform(160, 300), r.randint(-900, 0)
        y = (y0 + v * t) % (H + 200) - 150
        s.append(billete(x0 + 40 * math.sin(t * 2 + x0), y, 0.5, (t * 90 + x0) % 360, "$"))
    return "".join(s)


def arepa(x, y, k=1.0):
    return (f'<g transform="translate({f(x)} {f(y)}) scale({f(k)})"><ellipse cx="0" cy="0" rx="48" ry="22" fill="#FFE082" stroke="{INK}" stroke-width="5"/>'
            '<path d="M-25 -8 L -5 8 M0 -10 L 20 6 M-40 0 L -28 10" stroke="#C8A15A" stroke-width="5" stroke-linecap="round"/></g>')


def impresora(x, y, t, activa=True):
    luz = "#76FF03" if activa and int(t * 4) % 2 else ("#33691E" if activa else "#B71C1C")
    temb = 3 * math.sin(t * 40) if activa else 0
    s = [f'<g transform="translate({f(x + temb)} {y})">',
         f'<rect x="-200" y="-260" width="400" height="300" rx="20" fill="#78909C" stroke="{INK}" stroke-width="10"/>',
         f'<rect x="-160" y="-220" width="320" height="80" rx="10" fill="#263238"/>',
         f'<text x="0" y="-165" text-anchor="middle" font-family="Courier New, monospace" font-weight="bold" font-size="36" fill="{"#76FF03" if activa else "#546E7A"}">IMPRIMIDORA 3000</text>',
         f'<circle cx="150" cy="-60" r="18" fill="{luz}" stroke="{INK}" stroke-width="5"/>',
         f'<rect x="200" y="-110" width="40" height="80" fill="#455A64" stroke="{INK}" stroke-width="6"/>']
    for i, cx in enumerate((-120, -40, 40)):
        a = (t * 400 + i * 40) % 360 if activa else 0
        s.append(f'<g transform="translate({cx} -60) rotate({f(a)})"><circle r="30" fill="#B0BEC5" stroke="{INK}" stroke-width="6"/><line x1="-30" y1="0" x2="30" y2="0" stroke="{INK}" stroke-width="5"/></g>')
    s.append(f'<rect x="-210" y="40" width="420" height="40" fill="#546E7A" stroke="{INK}" stroke-width="8"/>')
    if activa:
        for i in range(6):
            fr = (t * 1.6 + i / 6) % 1.0
            s.append(billete(240 + fr * 520, -70 - 260 * fr + 300 * fr * fr, 0.6, fr * 200, "$ 1.000.000"))
    s.append('</g>')
    return "".join(s)


def carretilla(x, y, k=1.0, t=0):
    bills = "".join(billete(-60 + (i % 4) * 50, -150 - (i // 4) * 35, 0.45, (i * 23) % 30 - 15, "$") for i in range(16))
    return (f'<g transform="translate({f(x)} {f(y)}) scale({f(k)})"><circle cx="-190" cy="-40" r="40" fill="#424242" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M-230 -110 L 120 -110 L 60 -40 L -170 -40 Z" fill="#F57C00" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>'
            f'<line x1="120" y1="-110" x2="260" y2="-60" stroke="{INK}" stroke-width="12" stroke-linecap="round"/>'
            f'<line x1="40" y1="-40" x2="60" y2="0" stroke="{INK}" stroke-width="10"/>' + bills + '</g>')


def precio(producto, de, a, t, x=1300, y=380):
    p = ease_out(prog(t, 0.9, 1.8))
    v = de + (a - de) * p
    txt = "$ " + fmt_num(v)
    fs = min(120, int(560 / (len(txt) * 0.62)))
    sube = a > de and p > 0
    col = "#E53935" if sube else INK
    sacude = 4 * math.sin(t * 30) if sube and p < 1 else 0
    return (f'<g transform="translate({f(x + sacude)} {y})"><rect x="-320" y="-200" width="640" height="360" rx="26" fill="#FFFFFF" stroke="{INK}" stroke-width="10"/>'
            f'<rect x="-320" y="-200" width="640" height="90" rx="26" fill="#FFC107" stroke="{INK}" stroke-width="10"/>'
            f'<text x="0" y="-138" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="52" fill="{INK}">{escape(producto)}</text>'
            f'<text x="0" y="{40 + fs * 0.35:.0f}" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="{fs}" fill="{col}">{txt}</text>'
            + (f'<polygon points="250,-90 290,-30 210,-30" fill="#E53935" stroke="{INK}" stroke-width="5"/><rect x="235" y="-30" width="30" height="60" fill="#E53935" stroke="{INK}" stroke-width="5"/>' if sube else '')
            + '</g>')


def grafica(spec, t):
    x, y = spec.get("x", 1100), spec.get("y", 150)
    w, h = 720, 460
    pts = spec["puntos"]
    col = spec.get("color", "#E53935")
    mx = max(pts) * 1.1
    p = prog(t, 0.6, 2.0)
    n = (len(pts) - 1) * p
    coords = []
    for i in range(len(pts)):
        if i <= n:
            coords.append((x + 60 + i * (w - 100) / (len(pts) - 1), y + h - 40 - pts[i] / mx * (h - 120)))
    if p > 0 and int(n) < len(pts) - 1:
        i = int(n)
        fr = n - i
        x1 = x + 60 + i * (w - 100) / (len(pts) - 1)
        x2 = x + 60 + (i + 1) * (w - 100) / (len(pts) - 1)
        y1 = y + h - 40 - pts[i] / mx * (h - 120)
        y2 = y + h - 40 - pts[i + 1] / mx * (h - 120)
        coords.append((lerp(x1, x2, fr), lerp(y1, y2, fr)))
    linea = " ".join(f"{f(a)},{f(b)}" for a, b in coords)
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="26" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
            f'<text x="{x + w / 2}" y="{y + 60}" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="46" fill="{INK}">{escape(spec["titulo"])}</text>'
            f'<line x1="{x + 50}" y1="{y + h - 40}" x2="{x + w - 30}" y2="{y + h - 40}" stroke="{INK}" stroke-width="6"/>'
            f'<line x1="{x + 50}" y1="{y + 80}" x2="{x + 50}" y2="{y + h - 40}" stroke="{INK}" stroke-width="6"/>'
            + (f'<polyline points="{linea}" fill="none" stroke="{col}" stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/>' if len(coords) > 1 else '')
            + (f'<circle cx="{f(coords[-1][0])}" cy="{f(coords[-1][1])}" r="14" fill="{col}" stroke="{INK}" stroke-width="5"/>' if coords else ''))


def balanza(t):
    ang = -12 * ease_out(prog(t, 0.6, 1.2)) + 1.5 * math.sin(t * 2)
    din = "".join(billete(-260 + (i % 3) * 35, -95 - (i // 3) * 28, 0.42, (i * 17) % 20 - 10, "$") for i in range(12))
    return (f'<g transform="translate(1300 520)"><line x1="0" y1="-260" x2="0" y2="260" stroke="{INK}" stroke-width="16"/>'
            f'<rect x="-130" y="250" width="260" height="40" rx="10" fill="#8D6E63" stroke="{INK}" stroke-width="8"/>'
            f'<g transform="rotate({f(ang)} 0 -240)"><line x1="-300" y1="-240" x2="300" y2="-240" stroke="{INK}" stroke-width="14"/>'
            f'<path d="M-370 -60 L -300 -240 L -230 -60 M230 -60 L 300 -240 L 370 -60" fill="none" stroke="{INK}" stroke-width="6"/>'
            f'<ellipse cx="-300" cy="-60" rx="95" ry="20" fill="#B0BEC5" stroke="{INK}" stroke-width="6"/><ellipse cx="300" cy="-60" rx="95" ry="20" fill="#B0BEC5" stroke="{INK}" stroke-width="6"/>'
            + din + arepa(290, -85, 0.8)
            + f'<text x="-300" y="20" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="44" fill="#2E7D32">DINERO ↑</text>'
            f'<text x="300" y="20" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="44" fill="#E65100">COSAS =</text></g></g>')


def bandera(tipo, x, y, w=180, h=120):
    franjas = {"alemania": ["#1A1A1A", "#DD0000", "#FFCE00"], "colombia": ["#FCD116", "#FCD116", "#003893", "#CE1126"],
               "venezuela": ["#FCE300", "#0033A0", "#CF142B"], "zimbabue": ["#006400", "#FFD200", "#D40000", "#1A1A1A", "#D40000", "#FFD200", "#006400"]}[tipo]
    hh = h / len(franjas)
    s = "".join(f'<rect x="{x}" y="{f(y + i * hh)}" width="{w}" height="{f(hh + 0.5)}" fill="{c}"/>' for i, c in enumerate(franjas))
    if tipo == "zimbabue":
        s += f'<polygon points="{x},{y} {x + 80},{y + h / 2} {x},{y + h}" fill="#FFFFFF" stroke="{INK}" stroke-width="3"/>'
    if tipo == "venezuela":
        s += "".join(f'<circle cx="{f(x + w / 2 + 50 * math.cos(math.pi * (0.15 + i * 0.1)))}" cy="{f(y + h / 2 + 10 - 30 * math.sin(math.pi * (0.15 + i * 0.1)))}" r="4" fill="#FFFFFF"/>' for i in range(8))
    return s + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="none" stroke="{INK}" stroke-width="6"/>'


def insignia_pais(nombre, anio, tipo):
    return (f'<g><rect x="50" y="40" width="560" height="170" rx="26" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>' + bandera(tipo, 80, 65)
            + f'<text x="290" y="120" font-family="Arial Black, Arial" font-weight="900" font-size="48" fill="{INK}">{escape(nombre)}</text>'
            f'<text x="290" y="182" font-family="Arial Black, Arial" font-weight="900" font-size="56" fill="#E53935">{escape(anio)}</text></g>')


def expediente(etq, valor, t):
    return pop(f'<g transform="translate(1300 460) rotate(-4)"><rect x="-330" y="-230" width="660" height="460" rx="14" fill="#E6C27A" stroke="{INK}" stroke-width="10"/>'
               f'<rect x="-330" y="-270" width="240" height="60" rx="12" fill="#E6C27A" stroke="{INK}" stroke-width="10"/>'
               f'<text x="0" y="-120" text-anchor="middle" font-family="Courier New, monospace" font-weight="bold" font-size="54" fill="{INK}">{escape(etq)}:</text>'
               f'<g transform="rotate(-8)"><rect x="-270" y="-40" width="540" height="140" rx="12" fill="none" stroke="#C62828" stroke-width="12"/>'
               f'<text x="0" y="60" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="90" fill="#C62828">{escape(valor)}</text></g></g>', 1300, 460, t, 0.5)


def canasta(x, y, t):
    items = [arepa(-110, -90, 0.9),
             f'<g transform="translate(20 -110)"><polygon points="-45,0 0,-40 45,0" fill="#E57373" stroke="{INK}" stroke-width="5"/><rect x="-35" y="0" width="70" height="50" fill="#FFF3E0" stroke="{INK}" stroke-width="5"/></g>',
             f'<g transform="translate(130 -90)"><rect x="-50" y="-30" width="100" height="55" rx="10" fill="#FFB300" stroke="{INK}" stroke-width="5"/><circle cx="-28" cy="28" r="12" fill="{INK}"/><circle cx="28" cy="28" r="12" fill="{INK}"/></g>',
             f'<g transform="translate(-40 -170)"><rect x="-30" y="-30" width="60" height="60" rx="8" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/><rect x="-8" y="-22" width="16" height="44" fill="#E53935"/><rect x="-22" y="-8" width="44" height="16" fill="#E53935"/></g>',
             f'<g transform="translate(80 -175)"><rect x="-38" y="-28" width="76" height="56" fill="#42A5F5" stroke="{INK}" stroke-width="5"/><line x1="0" y1="-28" x2="0" y2="28" stroke="{INK}" stroke-width="4"/></g>']
    shown = "".join(it for i, it in enumerate(items) if t > 0.5 + i * 0.35)
    return (f'<g transform="translate({x} {y})">{shown}<path d="M-230 -40 L 230 -40 L 180 180 L -180 180 Z" fill="#C8A15A" stroke="{INK}" stroke-width="10"/>'
            + "".join(f'<line x1="{-200 + i * 50}" y1="-40" x2="{-160 + i * 40}" y2="180" stroke="#8D6E3E" stroke-width="5"/>' for i in range(9))
            + f'<path d="M-200 -40 C -200 -300 200 -300 200 -40" fill="none" stroke="#8D6E3E" stroke-width="16"/>'
            f'<text x="0" y="270" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="52" fill="#FFFFFF" stroke="{INK}" stroke-width="5" paint-order="stroke">CANASTA · IPC</text></g>')


def poder_compra(t):
    lleno = "".join(arepa(-120 + (i % 4) * 80, 40 - (i // 4) * 45, 0.8) for i in range(12))
    poco = "".join(arepa(-120 + (i % 4) * 80, 40 - (i // 4) * 45, 0.8) for i in range(4))
    q = prog(t, 1.2, 0.5)
    return (f'<g transform="translate(1050 560)">{billete(0, -260, 0.9, 0, "$ 50.000")}<text x="0" y="200" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="44" fill="#FFFFFF">ANTES</text>{lleno}</g>'
            + (f'<g transform="translate(1550 560)" opacity="{f(q)}">{billete(0, -260, 0.9, 0, "$ 50.000")}<text x="0" y="200" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="44" fill="#FF8A80">AHORA</text>{poco}</g>' if q > 0 else ''))


def nota_pista(n, t):
    return pop(f'<g transform="translate(1680 140) rotate(6)"><rect x="-170" y="-90" width="340" height="180" fill="#FFF176" stroke="{INK}" stroke-width="6"/>'
               f'<text x="0" y="20" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="54" fill="{INK}">PISTA #{n}</text></g>', 1680, 140, t, 0.3)


def sello(txt, t):
    p = prog(t, 0.7, 0.25)
    if p <= 0:
        return ""
    k = lerp(2.4, 1.0, ease_out(p))
    return (f'<g transform="translate(1250 420) rotate(-12) scale({f(k)})" opacity="{f(min(1, p * 2))}"><rect x="-420" y="-100" width="840" height="200" rx="20" fill="none" stroke="#C62828" stroke-width="18"/>'
            f'<text x="0" y="38" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="100" fill="#C62828">{escape(txt)}</text></g>')


def riqueza(t):
    filas = [(arepa(0, 0, 1.3), "Comida"), ('<rect x="-30" y="-50" width="60" height="100" fill="#37474F" stroke="#1A1A1A" stroke-width="5"/><path d="M-30 -20 L 30 -40 M-30 10 L 30 -10 M-30 40 L 30 20" stroke="#90A4AE" stroke-width="6"/>', "Productos"),
             ('<polygon points="-50,0 0,-45 50,0" fill="#E57373" stroke="#1A1A1A" stroke-width="5"/><rect x="-40" y="0" width="80" height="55" fill="#FFF3E0" stroke="#1A1A1A" stroke-width="5"/>', "Casas"),
             ('<circle r="40" fill="#FFCC80" stroke="#1A1A1A" stroke-width="6"/><path d="M-20 -5 l 15 15 l 25 -30" stroke="#1A1A1A" stroke-width="8" fill="none"/>', "Trabajo")]
    s = [f'<rect x="1040" y="140" width="760" height="560" rx="30" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>',
         f'<text x="1420" y="215" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="54" fill="#2E7D32">RIQUEZA =</text>']
    for i, (ic, txt) in enumerate(filas):
        if t > 0.6 + i * 0.4:
            y = 300 + i * 100
            s.append(f'<g transform="translate(1160 {y})">{ic}</g><text x="1250" y="{y + 16}" font-family="Arial" font-weight="bold" font-size="48" fill="{INK}">{txt}</text>')
    return "".join(s)


def cometa(x, y, t):
    a = 8 * math.sin(t * 2)
    cola = " ".join(f"{f(x + 20 * math.sin(t * 3 + i))},{f(y + 140 + i * 40)}" for i in range(8))
    return (f'<polyline points="{cola}" fill="none" stroke="{INK}" stroke-width="5"/>'
            f'<g transform="translate({x} {y}) rotate({f(a)})"><polygon points="0,-150 110,0 0,150 -110,0" fill="#81C784" stroke="{INK}" stroke-width="8"/>'
            f'{billete(0, 0, 0.55, 45, "1.000.000")}<line x1="0" y1="-150" x2="0" y2="150" stroke="{INK}" stroke-width="4"/><line x1="-110" y1="0" x2="110" y2="0" stroke="{INK}" stroke-width="4"/></g>'
            f'<line x1="{x}" y1="{y + 150}" x2="600" y2="{GY - 300}" stroke="#5D4037" stroke-width="3"/>')


def maletas(x, y):
    return "".join(f'<g transform="translate({x + dx} {y})"><rect x="-80" y="-120" width="160" height="120" rx="14" fill="{c}" stroke="{INK}" stroke-width="7"/>'
                   f'<path d="M-30 -120 v -30 h 60 v 30" fill="none" stroke="{INK}" stroke-width="7"/></g>'
                   for dx, c in ((-120, "#8D6E63"), (60, "#5C6BC0"), (220, "#E57373")))


def colchon(x, y, t):
    asoman = "".join(billete(x - 180 + i * 90, y - 80 - 6 * math.sin(t * 3 + i), 0.4, -10 + i * 5, "$") for i in range(5))
    return (asoman + f'<rect x="{x - 300}" y="{y - 80}" width="600" height="110" rx="30" fill="#E1F5FE" stroke="{INK}" stroke-width="8"/>'
            + "".join(f'<line x1="{x - 260 + i * 80}" y1="{y - 70}" x2="{x - 260 + i * 80}" y2="{y + 20}" stroke="#B3E5FC" stroke-width="5"/>' for i in range(7)))


def alcancia(t):
    return (f'<g transform="translate(1430 760) scale({f(1 - 0.12 * ease_out(prog(t, 1.5, 2.0)))})"><ellipse cx="0" cy="0" rx="150" ry="110" fill="#F48FB1" stroke="{INK}" stroke-width="8"/>'
            f'<circle cx="130" cy="-20" r="45" fill="#F48FB1" stroke="{INK}" stroke-width="8"/><ellipse cx="160" cy="-15" rx="16" ry="12" fill="#EC407A"/>'
            f'<rect x="-50" y="-115" width="90" height="16" rx="8" fill="{INK}"/><circle cx="100" cy="-45" r="8" fill="{INK}"/>'
            f'<rect x="-90" y="90" width="30" height="50" fill="#F48FB1" stroke="{INK}" stroke-width="7"/><rect x="60" y="90" width="30" height="50" fill="#F48FB1" stroke="{INK}" stroke-width="7"/></g>')


def perilla(t):
    p = ease_out(prog(t, 1.0, 2.0))
    ang = -120 + 170 * p
    aguja = -60 + 100 * (1 - p)
    return (f'<g transform="translate(1150 500)"><circle r="170" fill="#ECEFF1" stroke="{INK}" stroke-width="10"/>'
            f'<g transform="rotate({f(ang)})"><circle r="120" fill="#78909C" stroke="{INK}" stroke-width="8"/><rect x="-12" y="-120" width="24" height="70" rx="8" fill="#E53935"/></g>'
            f'<text x="0" y="250" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="44" fill="{INK}">TASAS ↑</text></g>'
            f'<g transform="translate(1600 520)"><path d="M-170 0 A 170 170 0 0 1 170 0" fill="none" stroke="#E53935" stroke-width="40"/>'
            f'<path d="M-170 0 A 170 170 0 0 1 0 -170" fill="none" stroke="#43A047" stroke-width="40"/>'
            f'<g transform="rotate({f(aguja)})"><line x1="0" y1="0" x2="0" y2="-150" stroke="{INK}" stroke-width="12" stroke-linecap="round"/></g><circle r="20" fill="{INK}"/>'
            f'<text x="0" y="90" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="44" fill="{INK}">INFLACIÓN ↓</text></g>')


def consejo(n, texto, t):
    return pop(f'<g transform="translate(1320 460)"><rect x="-480" y="-260" width="960" height="520" rx="36" fill="#FFFFFF" stroke="{INK}" stroke-width="10"/>'
               f'<circle cx="0" cy="-130" r="90" fill="#43A047" stroke="{INK}" stroke-width="8"/>'
               f'<text x="0" y="-100" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="90" fill="#FFFFFF">{n}</text>'
               f'<text x="0" y="60" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="40" fill="#455A64">CONSEJO</text>'
               f'<text x="0" y="150" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="{min(60, int(880 / (len(texto) * 0.6)))}" fill="{INK}">{escape(texto)}</text></g>',
               1320, 460, t, 0.4)


def trueque(t):
    p = (math.sin(t * 2) + 1) / 2
    xa, xb = lerp(950, 1550, p), lerp(1550, 950, p)
    caja = (f'<g transform="translate({f(xb)} 520)"><rect x="-90" y="-70" width="180" height="140" rx="10" fill="#D9A066" stroke="{INK}" stroke-width="7"/>'
            f'<text x="0" y="10" text-anchor="middle" font-family="Arial" font-weight="bold" font-size="30" fill="{INK}">TORNILLOS</text></g>')
    return (caja + arepa(xa, 520, 2.0)
            + f'<g stroke="{INK}" stroke-width="10" fill="none" stroke-linecap="round"><path d="M1100 380 Q 1250 300 1400 380"/><path d="M1400 660 Q 1250 740 1100 660"/></g>'
            f'<polygon points="1400,380 1370,350 1365,392" fill="{INK}"/><polygon points="1100,660 1130,690 1135,648" fill="{INK}"/>'
            f'<text x="1250" y="250" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="64" fill="{INK}">TRUEQUE</text>')


# ---------------------------------------------------------------- escena
def foco(spec, hablante):
    for clave, fxy in (("tarjeta", (1460, 330)), ("precio", (1300, 380)), ("grafica", (1460, 380)), ("consejo", (1320, 460)),
                       ("expediente", (1300, 460)), ("billete_grande", None), ("impresora", None)):
        if clave in spec:
            if clave == "billete_grande":
                return spec["billete_grande"][0], spec["billete_grande"][1]
            if clave == "impresora":
                return spec["impresora"][0] + 150, spec["impresora"][1] - 150
            tj = spec.get("tarjeta") or {}
            if clave == "tarjeta" and (tj.get("chica") or tj.get("grande")):
                return tj.get("x", 1440), tj.get("y", 150) + 200
            return fxy
    for nombre, x in spec.get("reparto", []):
        if nombre == hablante:
            return x + 60, GY - ALTO[nombre] * spec.get("escala", 0.6) * 0.65
    return W / 2, H / 2


def camara(spec, hablante, t, dur):
    if dur > 5.0 and t >= dur * 0.5 and not spec.get("presentacion") and len(spec.get("reparto", [])) < 5:
        z = lerp(1.26, 1.18, ease_out(prog(t, dur * 0.5, 0.3)))
        fx, fy = foco(spec, hablante)
    else:
        z, fx, fy = lerp(1.08, 1.0, ease_out(prog(t, 0, 0.45))), W / 2, H / 2
    vw, vh = W / z, H / z
    left = min(max(fx - vw / 2, 0), W - vw)
    top = min(max(fy - vh / 2, 0), H - vh)
    sx = sy = 0.0
    if "onomatopeya" in spec and 0.5 <= t < 1.0:
        a = 14 * (1 - (t - 0.5) / 0.5)
        sx, sy = a * math.sin(t * 95), a * math.cos(t * 81)
    entrada = (1 - ease_out(prog(t, 0, 0.22))) * 220
    return f'translate({f(entrada)} 0) scale({f(z)}) translate({f(-left + sx)} {f(-top + sy)})'


def escena(i, hablante, texto, spec, t, dur):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">', HV.DEFS,
         f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>', f'<g transform="{camara(spec, hablante, t, dur)}">',
         fondo(spec.get("fondo", "plano"), spec, t)]
    if spec.get("rayo_moto"):
        s.append(RY.rayo_en_moto(-300 + t * 420, caja_atras=True, vel=True))
    if "carretilla" in spec:
        x, y = spec["carretilla"]
        s.append(pop(carretilla(x, y, 1.1, t), x, y - 100, t, 0.4))
    if "impresora" in spec:
        s.append(impresora(*spec["impresora"], t, not spec.get("impresora_apagada")))
    if spec.get("balanza"):
        s.append(pop(balanza(t), 1300, 520, t, 0.3))
    if spec.get("trueque"):
        s.append(pop(trueque(t), 1250, 520, t, 0.3))
    if "canasta" in spec:
        s.append(pop(canasta(*spec["canasta"], t), spec["canasta"][0], spec["canasta"][1], t, 0.3))
    if spec.get("poder_compra"):
        s.append(poder_compra(t))
    if "cometa" in spec:
        s.append(cometa(*spec["cometa"], t))
    if "maletas" in spec:
        s.append(pop(maletas(*spec["maletas"]), spec["maletas"][0], spec["maletas"][1], t, 0.4))
    if "colchon" in spec:
        s.append(colchon(*spec["colchon"], t))
    if spec.get("riqueza"):
        s.append(riqueza(t))
    if "billete_grande" in spec:
        x, y, tx = spec["billete_grande"]
        s.append(pop(billete(x, y + 10 * math.sin(t * 2), 2.4, 3 * math.sin(t * 1.5), tx), x, y, t, 0.4))
        if spec.get("tachado") and t > 1.5:
            s.append(f'<g stroke="#E53935" stroke-width="30" stroke-linecap="round"><line x1="{x - 260}" y1="{y - 140}" x2="{x + 260}" y2="{y + 140}"/>'
                     f'<line x1="{x + 260}" y1="{y - 140}" x2="{x - 260}" y2="{y + 140}"/></g>')
    if "icono" in spec:
        nom, x, y = spec["icono"]
        s.append(pop(HV.icono(nom, x, y), x, y, t, 0.3))
    for idx, (nombre, x) in enumerate(spec.get("reparto", [])):
        s.append(personaje(nombre, x, spec.get("escala", 0.6), t, nombre == hablante, spec, idx))
    if spec.get("rayo_moto") and hablante == "byron":
        pass
    if spec.get("lluvia_billetes"):
        s.append(lluvia_billetes(t))
    if spec.get("arepas_vuelan"):
        for k in range(6):
            fr = (t * 0.8 + k / 6) % 1
            s.append(arepa(1400 + 300 * fr, 600 - 400 * fr + 300 * fr * fr, 1.0))
    if "precio" in spec:
        s.append(pop(precio(*spec["precio"], t), 1300, 380, t, 0.3))
    if "grafica" in spec:
        g = spec["grafica"]
        s.append(pop(grafica(g, t), g.get("x", 1100) + 360, g.get("y", 150) + 230, t, 0.3))
    if spec.get("perilla"):
        s.append(pop(perilla(t), 1350, 500, t, 0.3))
    if spec.get("alcancia"):
        s.append(pop(alcancia(t), 1430, 760, t, 0.6))
    if "expediente" in spec:
        s.append(expediente(*spec["expediente"], t))
    if "consejo" in spec:
        s.append(consejo(*spec["consejo"], t))
    if "tarjeta" in spec:
        s.append(A.tarjeta_a(spec["tarjeta"], t))
    if "burbuja" in spec:
        b = spec["burbuja"]
        s.append(pop(HV.burbuja(**b), b["x"], b["y"], t, 0.6))
    if "burbuja_pensar" in spec:
        x, y = spec["burbuja_pensar"]
        s.append(pop(RY.burbuja("?", x, y, (x - 200, y + 200), pensamiento=True), x, y, t, 0.5))
    if "onomatopeya" in spec:
        tx, x, y = spec["onomatopeya"]
        s.append(pop(HV.onomatopeya(tx, x, y), x, y, t, 0.5, 0.35))
    if "sello" in spec:
        s.append(sello(spec["sello"], t))
    s.append('</g>')
    if "pais" in spec:
        s.append(f'<g transform="translate({f((1 - ease_back(prog(t, 0.05, 0.45))) * -700)} 0)">{insignia_pais(*spec["pais"])}</g>')
    if "pista" in spec:
        s.append(nota_pista(spec["pista"], t))
    if "titulo" in spec:
        p = prog(t, 0.2, 0.55)
        if p > 0:
            s.append(f'<g transform="translate(0 {f((1 - ease_back(p)) * -500)})">{HV.titulo(*spec["titulo"])}</g>')
    if spec.get("suscribete"):
        s.append(A.suscribete_a(t))
    s.append(HV.subtitulo(texto))
    s.append('</svg>')
    return "".join(s)


# ---------------------------------------------------------------- audio
def _piper_masculino(tts_dir):
    import sherpa_onnx
    m = os.path.join(tts_dir, "vits-piper-es_ES-sharvard-medium")
    onnx = [x for x in os.listdir(m) if x.endswith(".onnx")][0]
    cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(vits=sherpa_onnx.OfflineTtsVitsModelConfig(
        model=f"{m}/{onnx}", tokens=f"{m}/tokens.txt", data_dir=f"{m}/espeak-ng-data"), num_threads=4))
    tts = sherpa_onnx.OfflineTts(cfg)
    mejor, f0min = 0, 1e9
    for sid in range(tts.num_speakers):
        a = tts.generate("Hola, soy un filósofo.", sid=sid, speed=1.0)
        y = np.array(a.samples)
        fr = int(0.04 * a.sample_rate)
        f0s = []
        for i in range(0, len(y) - fr, fr // 2):
            seg = y[i:i + fr]
            if np.sqrt((seg ** 2).mean()) < 0.02:
                continue
            ac = np.correlate(seg, seg, "full")[fr - 1:]
            lo, hi = a.sample_rate // 400, a.sample_rate // 70
            j = lo + int(np.argmax(ac[lo:hi]))
            f0s.append(a.sample_rate / j)
        med = np.median(f0s) if f0s else 1e9
        if med < f0min:
            mejor, f0min = sid, med
    return tts, mejor


def generar_voces(tts_dir, lineas, tmp):
    import sherpa_onnx
    k = os.path.join(tts_dir, "kokoro-multi-lang-v1_0")
    kok = sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
        model=f"{k}/model.onnx", voices=f"{k}/voices.bin", tokens=f"{k}/tokens.txt", data_dir=f"{k}/espeak-ng-data",
        dict_dir=f"{k}/dict", lexicon=f"{k}/lexicon-us-en.txt,{k}/lexicon-zh.txt", lang="es"), num_threads=4)))
    piper_soc, sid_p = _piper_masculino(tts_dir)
    pipers = {"vits-piper-es_ES-sharvard-medium": (piper_soc, sid_p)}

    def _piper(nombre):
        if nombre not in pipers:
            m = os.path.join(tts_dir, nombre)
            onnx = [x for x in os.listdir(m) if x.endswith(".onnx")][0]
            pipers[nombre] = (sherpa_onnx.OfflineTts(sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
                vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=f"{m}/{onnx}", tokens=f"{m}/tokens.txt", data_dir=f"{m}/espeak-ng-data"), num_threads=4))), 0)
        return pipers[nombre]
    voces = []
    for n, (quien, texto, _) in enumerate(lineas):
        motor, sid, vel, tono, filtro = VOCES[quien]
        if motor == "kokoro":
            a = kok.generate(texto, sid=sid, speed=vel)
        else:
            tts_p, sp = _piper(sid)
            a = tts_p.generate(texto, sid=sp, speed=vel)
        y = np.array(a.samples, dtype=np.float32)
        ruta = os.path.join(tmp, f"v{n}")
        sf.write(ruta + ".in.wav", y, a.sample_rate)
        filtros = f"asetrate={int(a.sample_rate * tono)},aresample={SR},atempo={1 / tono:.5f}{filtro},acompressor=threshold=-18dB:ratio=3:attack=5:release=80"
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ruta + ".in.wav", "-af", filtros, "-ac", "1", ruta + ".out.wav"], check=True)
        z, _ = sf.read(ruta + ".out.wav")
        os.remove(ruta + ".in.wav")
        os.remove(ruta + ".out.wav")
        voces.append(np.concatenate([np.zeros(int(SR * 0.12)), z, np.zeros(int(SR * 0.3))]))
    return voces


def eventos(spec, dur):
    ev = [(0.0, "whoosh", 0.4)]
    for clave, snd, ts, vol in (("tarjeta", "swoosh", 0.35, 0.6), ("icono", "pop", 0.3, 0.6), ("burbuja", "pop", 0.6, 0.6),
                                ("billete_grande", "pop", 0.4, 0.6), ("expediente", "pop", 0.5, 0.6), ("consejo", "ding", 0.4, 0.6),
                                ("canasta", "pop", 0.3, 0.5), ("balanza", "pop", 0.3, 0.5), ("grafica", "swoosh", 0.3, 0.5),
                                ("pista", "pop", 0.3, 0.6), ("titulo", "boom", 0.35, 0.6), ("suscribete", "pop", 0.3, 0.6),
                                ("carretilla", "pop", 0.4, 0.5), ("perilla", "tick", 1.0, 0.6)):
        if spec.get(clave):
            ev.append((ts, snd, vol))
    if "precio" in spec:
        _, de, a = spec["precio"]
        ev.append((0.3, "pop", 0.5))
        if a > de:
            ev += [(0.9 + k * 0.12, "tick", 0.5) for k in range(14)] + [(2.75, "ding", 0.6)]
    if "impresora" in spec and not spec.get("impresora_apagada"):
        ev += [(0.1 + k * 0.5, "vibra", 0.35) for k in range(int(dur / 0.5))]
    if "onomatopeya" in spec:
        ev.append((0.5, "click" if "CLIC" in spec["onomatopeya"][0] else "boom", 0.9))
    if "sello" in spec:
        ev.append((0.75, "boom", 0.7))
    if spec.get("lluvia_billetes"):
        ev.append((0.2, "fanfarria", 0.6))
    if spec.get("suscribete"):
        ev += [(1.75, "click", 0.8), (2.0, "campana", 0.7)]
    if spec.get("presentacion"):
        ev += [(0.6 + k * 0.9, "pop", 0.5) for k in range(6)]
    return ev


# ---------------------------------------------------------------- render
def _cuadro(args):
    i, quien, texto, spec, t, dur = args
    svg = escena(i, quien, texto, spec, t, dur).encode("utf-8")
    return subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-f", "png"], input=svg, capture_output=True, check=True).stdout


def main():
    tts_dir, salida = sys.argv[1], sys.argv[2]
    fps = int(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].isdigit() else 24
    lineas = GU.L
    tmp = salida + "_tmp"
    os.makedirs(tmp, exist_ok=True)
    voces = generar_voces(tts_dir, lineas, tmp)
    durs = [max(len(v) / SR, 2.5) for v in voces]
    total = sum(durs)
    print(f"{len(lineas)} líneas · {total:.1f} s", flush=True)
    A.cargar_sfx()
    A.SFX.update(vibra=CA.sfx_vibra(), fizz=CA.sfx_fizz(), abrir=CA.sfx_abrir())
    voz = np.zeros(int(SR * (total + 1)))
    efectos = np.zeros_like(voz)
    t0 = 0.0
    for (quien, texto, spec), v, d in zip(lineas, voces, durs):
        i0 = int(SR * t0)
        voz[i0:i0 + len(v)] += v
        for ts, nombre, vol in eventos(spec, d):
            snd = A.SFX[nombre] * vol * 0.55
            j = i0 + int(SR * ts)
            if j < len(efectos):
                efectos[j:j + len(snd)] += snd[:len(efectos) - j]
        t0 += d
    pista = voz + efectos
    pista[:int(SR * total)] += CA.musica_fiesta(total) * 0.22
    pista = pista[:int(SR * total)]
    pista /= max(1.0, np.abs(pista).max() / 0.95)
    wav = salida + ".wav"
    sf.write(wav, pista.astype(np.float32), SR)
    tareas = []
    for k, ((quien, texto, spec), d) in enumerate(zip(lineas, durs)):
        for fi in range(int(round(d * fps))):
            tareas.append((k + 1, quien, texto, spec, fi / fps, d))
    print(f"{len(tareas)} cuadros", flush=True)
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(fps), "-i", "-", "-i", wav,
                           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
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
