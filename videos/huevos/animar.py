"""Versión animada del video de los 50 huevos.

Toma el guion y los dibujos de generar_escenas.py y les agrega movimiento cuadro a cuadro:
personaje animado, tarjetas que entran, números que cuentan, cámara con cortes,
efectos de sonido y música de fondo sintetizados.

Uso: python3 animar.py <carpeta_modelo_voz> <salida.mp4> [fps]
Requiere: rsvg-convert, ffmpeg, sherpa-onnx, numpy, soundfile.
"""
import importlib.util
import math
import os
import random
import re
import subprocess
import sys
from multiprocessing import Pool

import numpy as np
import soundfile as sf

AQUI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("huevos_esc", os.path.join(AQUI, "generar_escenas.py"))
G = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(G)

W, H, GY, INK = G.W, G.H, G.GY, G.INK
SR = 44100
FPS = 24


# ------------------------------------------------------------------ utilidades de tiempo
def c01(x):
    return max(0.0, min(1.0, x))


def prog(t, start, dur):
    return c01((t - start) / dur)


def ease_out(x):
    return 1 - (1 - x) ** 3


def ease_back(x, s=1.9):
    x -= 1
    return x * x * ((s + 1) * x + s) + 1


def lerp(a, b, p):
    return a + (b - a) * p


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def pop(svg, cx, cy, t, start, d=0.45):
    p = prog(t, start, d)
    if p <= 0:
        return ""
    sc = ease_back(p)
    return f'<g opacity="{f(min(1, p * 3))}" transform="translate({f(cx)} {f(cy)}) scale({f(sc)}) translate({f(-cx)} {f(-cy)})">{svg}</g>'


# ------------------------------------------------------------------ Rayo animado
def rayo_a(x, pose, mira, panza, t, sudor=False, nausea=False, zzz=False, olor=False, vaso=False):
    casco = G.casco()
    dy = 5 * math.sin(2 * math.pi * 1.1 * t)
    rot_casco = 0.0
    brazo_der = None
    huevo_mano = ""
    if pose == "celebra":
        dy = -55 * abs(math.sin(math.pi * 1.6 * t))
    if pose == "triste":
        rot_casco = 14 + 3 * math.sin(2 * math.pi * 0.5 * t)
        dy = 3 * math.sin(2 * math.pi * 0.5 * t)
    hombro = (0, -385)
    if pose == "come":
        ph = (t * 0.95) % 1.0
        mesa_p, boca = (235, -330), (185, -505)
        if ph < 0.4:
            q = ease_out(ph / 0.4)
            mano = (lerp(mesa_p[0], boca[0], q), lerp(mesa_p[1], boca[1], q))
            esc_h = 1.0
        elif ph < 0.65:
            mano = boca
            esc_h = lerp(1.0, 0.0, (ph - 0.4) / 0.25)
            rot_casco = -6 * math.sin(math.pi * (ph - 0.4) / 0.25 * 3)
        else:
            q = ease_out((ph - 0.65) / 0.35)
            mano = (lerp(boca[0], mesa_p[0], q), lerp(boca[1], mesa_p[1], q))
            esc_h = 0.0
        codo = (lerp(150, 150, 0.5), lerp(-360, -420, c01((mesa_p[1] - mano[1]) / 175)))
        brazo_der = f"{hombro[0]},{hombro[1]} {f(codo[0])},{f(codo[1])} {f(mano[0])},{f(mano[1])}"
        if esc_h > 0.02:
            huevo_mano = G.huevo(mano[0] - 5, mano[1] - 32, 1.1 * max(esc_h, 0.25))
        manos_extra = mano
    if pose == "saluda":
        ang = math.radians(22 * math.sin(2 * math.pi * 2.2 * t))
        ex, ey, hx, hy = 160, -400, 245, -515
        rx = ex + (hx - ex) * math.cos(ang) - (hy - ey) * math.sin(ang)
        ry = ey + (hx - ex) * math.sin(ang) + (hy - ey) * math.cos(ang)
        brazo_der = f"0,-385 {ex},{ey} {f(rx)},{f(ry)}"
    if pose == "celebra":
        w = 18 * math.sin(2 * math.pi * 3 * t)
        br = [f"0,-380 -95,-470 {f(-120 + w)},-600", f"0,-380 95,-470 {f(120 - w)},-600"]
    elif pose == "panza":
        r = 40 + panza
        br = [f"0,-380 -40,-330 -10,-300", f"0,-380 {f(r*0.6)},-360 {f(r*0.9+20)},-300"]
    else:
        br = list(G.BRAZOS.get(pose, G.BRAZOS["normal"]))
        if pose == "come":
            br = ["0,-380 -45,-280 -55,-190", brazo_der]
        elif brazo_der:
            br[1] = brazo_der
    pi = G.PIERNAS.get(pose, G.PIERNAS["normal"])
    s = [f'<g transform="translate({f(x)} {f(GY)}) scale({mira} 1)"><g transform="translate(0 {f(min(dy, 0) if pose == "celebra" else dy * 0.4)})">',
         f'<g stroke="{INK}" stroke-width="20" stroke-linecap="round" stroke-linejoin="round" fill="none">']
    # piernas fijas al piso; cuerpo con leve respiración
    s.append(f'<line x1="0" y1="{f(-465 + dy * 0.6)}" x2="0" y2="-195"/>')
    for p in pi:
        s.append(f'<polyline points="{p}"/>')
    s.append('</g>')
    if panza:
        r = (40 + panza) * (1 + 0.025 * math.sin(2 * math.pi * 0.9 * t))
        s.append(f'<ellipse cx="{f(r*0.55)}" cy="-300" rx="{f(r)}" ry="{f(r*0.85)}" fill="#FFFFFF" stroke="{INK}" stroke-width="14"/>')
        if panza > 60:
            s.append(f'<path d="M{f(r*0.05)} -300 q {f(r*0.25)} 12 {f(r*0.5)} 0" stroke="#B0BEC5" stroke-width="6" fill="none"/>')
    s.append(f'<g transform="translate(0 {f(dy * 0.6)})">')
    s.append(f'<g stroke="{INK}" stroke-width="20" stroke-linecap="round" stroke-linejoin="round" fill="none">')
    for p in br:
        s.append(f'<polyline points="{p}"/>')
    s.append('</g>')
    for p in br:
        hx, hy = p.split()[-1].split(",")
        s.append(f'<circle cx="{hx}" cy="{hy}" r="17" fill="{INK}"/>')
    if vaso:
        s.append(f'<rect x="-90" y="-250" width="50" height="75" rx="6" fill="#B3E5FC" stroke="{INK}" stroke-width="5"/>')
    if pose == "saluda":
        o = 0.5 + 0.5 * math.sin(2 * math.pi * 2.2 * t)
        s.append(f'<g stroke="#2F8DEB" stroke-width="9" stroke-linecap="round" fill="none" opacity="{f(o)}">'
                 '<path d="M285 -560 Q305 -540 300 -510"/><path d="M315 -585 Q345 -545 335 -495"/></g>')
    s.append(f'<g transform="rotate({f(rot_casco)} 0 -460)">{casco}</g>')
    s.append(huevo_mano)
    if pose == "come":
        s.append(f'<circle cx="{f(manos_extra[0])}" cy="{f(manos_extra[1])}" r="17" fill="{INK}"/>')
    s.append('</g>')
    if sudor:
        gotas = []
        for k, (gx, gy0) in enumerate(((-170, -640), (200, -690), (215, -600))):
            fr = (t * 1.3 + k * 0.37) % 1.0
            gotas.append(f'<path transform="translate({gx} {f(gy0 + fr * 70)})" opacity="{f(1 - fr)}" d="M0 0 q -12 22 0 30 q 12 -8 0 -30 Z"/>')
        s.append(f'<g fill="#4FC3F7" stroke="#0277BD" stroke-width="3">{"".join(gotas)}</g>')
    if nausea:
        a = (t * 160) % 360
        s.append(f'<g stroke="#43A047" stroke-width="9" fill="none" stroke-linecap="round">'
                 f'<path transform="rotate({f(a)} 190 -700)" d="M190 -720 a 25 25 0 1 1 -10 40"/>'
                 f'<path transform="rotate({f(-a)} -200 -680)" d="M-200 -700 a 22 22 0 1 0 10 38"/></g>'
                 f'<ellipse cx="40" cy="-560" rx="200" ry="200" fill="#66BB6A" opacity="{f(0.12 + 0.08 * math.sin(t * 4))}"/>')
    if zzz:
        zs = []
        for k in range(3):
            fr = (t * 0.45 + k / 3) % 1.0
            zs.append(f'<text x="{f(-220 - fr * 150)}" y="{f(-620 - fr * 200)}" font-size="{f(45 + fr * 45)}" opacity="{f(1 - fr)}">Z</text>')
        s.append(f'<g font-family="Arial Black, Arial" font-weight="900" fill="#5C6BC0">{"".join(zs)}</g>')
    if olor:
        dx = 12 * math.sin(t * 3)
        s.append(f'<g transform="translate({f(dx)} {f(-((t * 40) % 40))})" stroke="#9CCC65" stroke-width="10" fill="none" stroke-linecap="round" opacity="0.9">'
                 '<path d="M-150 -500 q -30 -40 0 -80 q 30 -40 0 -80"/><path d="M230 -480 q -30 -40 0 -80 q 30 -40 0 -80"/>'
                 '<path d="M-220 -330 q -30 -40 0 -80 q 30 -40 0 -80"/></g>'
                 + G.pescado(330 + 15 * math.sin(t * 5), -330, 0.6))
    s.append('</g></g>')
    return "".join(s)


# ------------------------------------------------------------------ elementos animados
NUM = re.compile(r"^([^\d]*)(\d+(?:,\d+)?)(.*)$")


def contar(texto, p):
    m = NUM.match(texto)
    if not m:
        return texto
    pre, num, post = m.groups()
    dec = len(num.split(",")[1]) if "," in num else 0
    v = float(num.replace(",", ".")) * ease_out(p)
    s = f"{v:.{dec}f}".replace(".", ",")
    return pre + s + post


def tarjeta_a(spec, t, start=0.35):
    p = prog(t, start, 0.55)
    if p <= 0:
        return ""
    sp = dict(spec)
    q = prog(t, start + 0.5, 0.8)
    if sp.get("numero") is not None:
        sp["numero"] = contar(sp["numero"], q)
    if sp.get("barras"):
        sp["barras"] = [(k, v * ease_out(q), m, c) for k, v, m, c in sp["barras"]]
    if sp.get("filas"):
        n = len(sp["filas"])
        vis = int(c01((t - start - 0.45) / (0.28 * n)) * n + 0.999) if t > start + 0.45 else 0
        sp["filas"] = [fl if i < vis else ("", "") for i, fl in enumerate(sp["filas"])]
    dx = (1 - ease_back(p)) * 1100
    return f'<g transform="translate({f(dx)} 0)">{G.tarjeta(**sp)}</g>'


def icono_a(ic, t, prev_extra):
    nombre, x, y = ic[0], ic[1], ic[2]
    extra = ic[3] if len(ic) > 3 else None
    if nombre == "estomago":
        extra = lerp(prev_extra if prev_extra is not None else 0, extra, ease_out(prog(t, 0.3, 1.2)))
    svg = G.icono(nombre, x, y, extra)
    bob = 8 * math.sin(2 * math.pi * 0.7 * t)
    if nombre == "gas":
        svg = f'<g transform="translate({f(t * 25)} {f(-t * 12)}) scale(1)">{svg}</g>'
    elif nombre == "pescado":
        svg = f'<g transform="translate({f(25 * math.sin(t * 4))} 0)">{svg}</g>'
    elif nombre in ("alerta", "check"):
        k = 1 + 0.04 * math.sin(2 * math.pi * 1.5 * t)
        svg = f'<g transform="translate({x} {y}) scale({f(k)}) translate({-x} {-y})">{svg}</g>'
    else:
        svg = f'<g transform="translate(0 {f(bob)})">{svg}</g>'
    return pop(svg, x, y, t, 0.3, 0.5)


def suscribete_a(t):
    cx, cy = 1340, 420
    p_click = prog(t, 1.75, 0.15)
    hecho = t > 1.85
    k = 1 - 0.08 * math.sin(math.pi * p_click)
    col = "#9E9E9E" if hecho else "#E53935"
    txt = "¡SUSCRITO! ✔" if hecho else "SUSCRÍBETE"
    fs = 92 if hecho else 110
    boton = (f'<g transform="translate({cx} {cy}) scale({f(k)})"><rect x="-380" y="-110" width="760" height="220" rx="40" fill="{col}" stroke="{INK}" stroke-width="10"/>'
             f'<text x="0" y="35" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="{fs}" fill="#FFFFFF">{txt}</text></g>')
    q = ease_out(prog(t, 0.8, 0.9))
    mx, my = lerp(1950, 1520, q), lerp(1000, 470, q)
    cursor = (f'<g transform="translate({f(mx)} {f(my)})"><path d="M0 0 L 0 120 L 30 90 L 55 140 L 75 130 L 50 82 L 90 80 Z" '
              f'fill="#FFFFFF" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/></g>')
    ang = 18 * math.sin(2 * math.pi * 4 * t) * c01(1 - (t - 2.0) / 1.2) if t > 2.0 else 0
    campana = (f'<g transform="translate({cx} {cy + 230}) rotate({f(ang)} 0 -50)"><path d="M-40 -40 q 40 -60 80 0 v 50 l 15 20 h -110 l 15 -20 Z" fill="#FFD54F" stroke="{INK}" stroke-width="7"/>'
               f'<circle cx="0" cy="45" r="14" fill="#FFD54F" stroke="{INK}" stroke-width="6"/></g>')
    return pop(boton + campana, cx, cy, t, 0.3, 0.5) + cursor


def confeti_a(t):
    r = random.Random(50)
    cols = ("#E53935", "#FB8C00", "#FDD835", "#43A047", "#1E88E5", "#8E24AA")
    s = []
    for _ in range(120):
        x0, y0, v = r.randint(0, W), r.randint(-900, 0), r.uniform(250, 480)
        y = y0 + v * t
        if y < -40 or y > H:
            continue
        x = x0 + 30 * math.sin(t * 3 + x0)
        s.append(f'<rect x="{f(x)}" y="{f(y)}" width="18" height="34" fill="{r.choice(cols)}" transform="rotate({f((t * 300 + x0) % 360)} {f(x + 9)} {f(y + 17)})"/>')
    return "".join(s)


# ------------------------------------------------------------------ escena animada
def foco(e):
    if "tarjeta" in e:
        tj = e["tarjeta"]
        if tj.get("chica") or tj.get("grande"):
            return tj.get("x", 1440), tj.get("y", 150) + 200
        return 1460, 330
    if "icono" in e:
        return e["icono"][1], e["icono"][2]
    r = e.get("rayo")
    if r:
        return r["x"] + 60, GY - 500
    return W / 2, H / 2


def camara(e, t, dur, sacudida_t):
    z, fx, fy = 1.0, W / 2, H / 2
    if dur > 5.0 and t >= dur * 0.5:
        tc = dur * 0.5
        z = lerp(1.24, 1.16, ease_out(prog(t, tc, 0.3)))
        fx, fy = foco(e)
    else:
        z = lerp(1.07, 1.0, ease_out(prog(t, 0, 0.4)))
    vw, vh = W / z, H / z
    left = min(max(fx - vw / 2, 0), W - vw)
    top = min(max(fy - vh / 2, 0), H - vh)
    sx = sy = 0.0
    if sacudida_t is not None and 0 <= t - sacudida_t < 0.45:
        a = 14 * (1 - (t - sacudida_t) / 0.45)
        sx, sy = a * math.sin(t * 90), a * math.cos(t * 77)
    return f'scale({f(z)}) translate({f(-left + sx)} {f(-top + sy)})'


def escena_a(i, narr, e, prev, t, dur):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">', G.DEFS]
    sac = 0.5 if "onomatopeya" in e else (0.2 if "titulo" in e else None)
    s.append(f'<g transform="{camara(e, t, dur, sac)}">')
    s.append(G.fondo(e.get("fondo", "plano")))
    if "mesa" in e:
        n0 = prev.get("mesa", e["mesa"]) if prev else e["mesa"]
        n = round(lerp(n0, e["mesa"], ease_out(prog(t, 0.15, 0.9))))
        s.append(G.mesa(n, e.get("mesa_x", 560)))
    if "icono" in e:
        pe = prev.get("icono") if prev else None
        prev_extra = pe[3] if pe and pe[0] == "estomago" and len(pe) > 3 else None
        s.append(icono_a(e["icono"], t, prev_extra))
    if "huevo_crudo" in e:
        hx, hy = e["huevo_crudo"]
        s.append(pop(f'<g transform="rotate({f(4 * math.sin(t * 3))} {hx} {hy})">{G.huevo(hx, hy, k=2.2, crudo=True)}</g>', hx, hy, t, 0.5))
    for k, p in enumerate(e.get("personas", [])):
        bob = 4 * math.sin(2 * math.pi * 1.0 * t + k)
        px = p["x"]
        pose = p.get("pose", "normal")
        if pose == "corre":
            px += 260 * t * p.get("mira", 1)
            pose = "corre" if int(t * 6) % 2 == 0 else "normal"
        if pose == "feliz":
            bob = -30 * abs(math.sin(math.pi * 1.5 * t))
        if p["tipo"] == "medico":
            svg = G.medico(px)
        else:
            svg = G.persona(px, p["tipo"], pose, p.get("mira", 1))
        s.append(f'<g transform="translate(0 {f(bob)})">{svg}</g>')
    r = e.get("rayo")
    if r:
        pz0 = prev.get("rayo", {}).get("panza", r.get("panza", 0)) if prev and prev.get("rayo") else r.get("panza", 0)
        pz = lerp(pz0, r.get("panza", 0), ease_out(prog(t, 0.0, 1.0)))
        s.append(rayo_a(r["x"], r.get("pose", "normal"), r.get("mira", 1), pz, t, r.get("sudor", False),
                        r.get("nausea", False), r.get("zzz", False), r.get("olor", False), r.get("vaso", False)))
    if e.get("confeti"):
        s.append(confeti_a(t))
    if "tarjeta" in e:
        s.append(tarjeta_a(e["tarjeta"], t))
    if "burbuja" in e:
        b = e["burbuja"]
        s.append(pop(G.burbuja(**b), b["x"], b["y"], t, 0.6))
    if "onomatopeya" in e:
        tx, x, y = e["onomatopeya"]
        w = 6 * math.sin(t * 20) * c01(1 - (t - 0.5) / 1.0)
        s.append(pop(f'<g transform="rotate({f(w)} {x} {y})">{G.onomatopeya(tx, x, y)}</g>', x, y, t, 0.5, 0.35))
    s.append('</g>')
    # capa fija (no la mueve la cámara)
    if "contador" in e:
        c0 = prev.get("contador", 0) if prev else 0
        q = prog(t, 0.15, 0.75)
        n = round(lerp(c0, e["contador"], ease_out(q)))
        k = 1 + 0.07 * math.sin(math.pi * q) if c0 != e["contador"] else 1
        s.append(f'<g transform="translate(835 135) scale({f(k)}) translate(-835 -135)">{G.contador(n)}</g>')
    if "reloj" in e:
        dyr = (1 - ease_back(prog(t, 0.05, 0.45))) * -260
        s.append(f'<g transform="translate(0 {f(dyr)})">{G.reloj(e["reloj"])}</g>')
    if "titulo" in e:
        p = prog(t, 0.2, 0.55)
        if p > 0:
            dyt = (1 - ease_back(p)) * -500
            s.append(f'<g transform="translate(0 {f(dyt)})">{G.titulo(*e["titulo"])}</g>')
    if e.get("suscribete"):
        s.append(suscribete_a(t))
    s.append(G.subtitulo(narr))
    s.append('</svg>')
    return "".join(s)


# ------------------------------------------------------------------ sonido
def env_exp(n, tau):
    return np.exp(-np.arange(n) / (SR * tau))


def lowpass(x, a):
    y = np.zeros_like(x)
    acc = 0.0
    for i in range(len(x)):
        acc += a * (x[i] - acc)
        y[i] = acc
    return y


RNG = np.random.default_rng(7)


def sfx_pop():
    n = int(SR * 0.12)
    tt = np.arange(n) / SR
    fr = np.linspace(900, 260, n)
    return 0.55 * np.sin(2 * np.pi * np.cumsum(fr) / SR) * env_exp(n, 0.035)


def sfx_whoosh(d=0.32):
    n = int(SR * d)
    ruido = RNG.standard_normal(n)
    a = np.linspace(0.02, 0.25, n)
    y = np.zeros(n)
    acc = 0.0
    for i in range(n):
        acc += a[i] * (ruido[i] - acc)
        y[i] = acc
    env = np.sin(np.pi * np.arange(n) / n) ** 2
    return 0.5 * y * env / (np.abs(y).max() + 1e-9)


def sfx_ding(f0=1320, d=0.9, vol=0.35):
    n = int(SR * d)
    tt = np.arange(n) / SR
    y = sum(a * np.sin(2 * np.pi * f0 * h * tt) for h, a in ((1, 1), (2.01, 0.35), (3.02, 0.15)))
    return vol * y * env_exp(n, d / 4)


def sfx_tick():
    n = int(SR * 0.025)
    return 0.3 * RNG.standard_normal(n) * env_exp(n, 0.004)


def sfx_chomp():
    n = int(SR * 0.09)
    y = lowpass(RNG.standard_normal(n), 0.12) * env_exp(n, 0.02)
    out = np.zeros(int(SR * 0.22))
    out[:n] += y
    out[int(SR * 0.11):int(SR * 0.11) + n] += 0.8 * y
    return 1.4 * out / (np.abs(out).max() + 1e-9) * 0.5


def sfx_burp():
    d = 0.75
    n = int(SR * d)
    tt = np.arange(n) / SR
    f0 = 95 + 25 * np.sin(2 * np.pi * 7 * tt) - 20 * tt
    saw = 2 * ((np.cumsum(f0) / SR) % 1) - 1
    am = (0.6 + 0.4 * np.sin(2 * np.pi * 11 * tt)) * np.sin(np.pi * tt / d) ** 0.6
    y = lowpass(saw * am, 0.08)
    return 0.8 * y / (np.abs(y).max() + 1e-9)


def sfx_boom():
    n = int(SR * 0.7)
    tt = np.arange(n) / SR
    y = np.sin(2 * np.pi * (55 + 40 * np.exp(-tt * 20)) * tt) * env_exp(n, 0.18)
    y += 0.3 * lowpass(RNG.standard_normal(n), 0.05) * env_exp(n, 0.08)
    return 0.7 * y / (np.abs(y).max() + 1e-9)


def sfx_fanfarria():
    out = np.zeros(int(SR * 1.6))
    for k, fr in enumerate((523, 659, 784, 1047)):
        d = sfx_ding(fr, 1.0, 0.28)
        i0 = int(SR * 0.12 * k)
        out[i0:i0 + len(d)] += d[:len(out) - i0]
    return out


def sfx_alarma():
    out = np.zeros(int(SR * 0.6))
    for k, fr in enumerate((880, 660)):
        n = int(SR * 0.22)
        tt = np.arange(n) / SR
        y = 0.25 * np.sign(np.sin(2 * np.pi * fr * tt)) * np.minimum(1, (n - np.arange(n)) / 400)
        i0 = int(SR * 0.27 * k)
        out[i0:i0 + n] += lowpass(y, 0.3)
    return out


SFX = {}


def cargar_sfx():
    SFX.update(pop=sfx_pop(), whoosh=sfx_whoosh(), ding=sfx_ding(), tick=sfx_tick(), chomp=sfx_chomp(), burp=sfx_burp(),
               boom=sfx_boom(), fanfarria=sfx_fanfarria(), alarma=sfx_alarma(), click=sfx_tick() * 1.5,
               campana=sfx_ding(1760, 1.2, 0.3), swoosh=sfx_whoosh(0.22))


def eventos_sfx(e, prev, dur):
    ev = [(0.0, "whoosh", 0.35)]
    if "tarjeta" in e:
        ev.append((0.35, "swoosh", 0.6))
        tj = e["tarjeta"]
        if tj.get("barras") or tj.get("numero"):
            ev += [(0.85 + k * 0.1, "tick", 0.5) for k in range(7)]
        if tj.get("filas"):
            ev += [(0.8 + k * 0.28, "pop", 0.45) for k in range(len(tj["filas"]))]
    if "icono" in e:
        nom = e["icono"][0]
        ev.append((0.3, "pop", 0.6))
        if nom == "alerta":
            ev.append((0.45, "alarma", 0.5))
        if nom == "check":
            ev.append((0.45, "ding", 0.7))
        if nom == "gas":
            ev.append((0.6, "burp", 0.35))
    if "contador" in e and (not prev or prev.get("contador") != e["contador"]):
        ev.append((0.9, "ding", 0.55))
    if "burbuja" in e:
        ev.append((0.6, "pop", 0.7))
    if "onomatopeya" in e:
        ev.append((0.5, "burp" if "BURP" in e["onomatopeya"][0] else "boom", 0.9))
    if "titulo" in e:
        ev.append((0.35, "boom", 0.6))
    if e.get("confeti"):
        ev.append((0.1, "fanfarria", 0.8))
    if e.get("suscribete"):
        ev += [(0.3, "pop", 0.6), (1.75, "click", 0.8), (2.0, "campana", 0.7)]
    if "reloj" in e:
        ev.append((0.1, "tick", 0.7))
    r = e.get("rayo")
    if r and r.get("pose") == "come":
        k = 0
        while True:
            tt = (k + 0.42) / 0.95
            if tt > dur - 0.2:
                break
            ev.append((tt, "chomp", 0.45))
            k += 1
    return ev


def pluck(fr, d, vol):
    n = int(SR * d)
    N = int(SR / fr)
    buf = RNG.uniform(-1, 1, N)
    out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % N]
        buf[i % N] = 0.996 * 0.5 * (buf[i % N] + buf[(i + 1) % N])
    return vol * out


def musica(total):
    bpm = 112
    beat = 60 / bpm
    acordes = [(261.6, 329.6, 392.0), (196.0, 246.9, 293.7), (220.0, 261.6, 329.6), (174.6, 220.0, 261.6)]
    bajos = [65.4, 49.0, 55.0, 43.7]
    compas = int(SR * beat * 4)
    loop = np.zeros(compas * 4)
    cache = {}
    for c, (ac, b) in enumerate(zip(acordes, bajos)):
        base = c * compas
        patron = [ac[0], ac[2], ac[1], ac[2], ac[0] * 2, ac[2], ac[1], ac[2]]
        for k, fr in enumerate(patron):
            key = round(fr, 1)
            if key not in cache:
                cache[key] = pluck(fr, 0.6, 0.18)
            nota = cache[key]
            i0 = base + int(SR * beat / 2 * k)
            loop[i0:i0 + len(nota)] += nota[:len(loop) - i0]
        for k in (0, 2):
            n = int(SR * beat * 0.9)
            tt = np.arange(n) / SR
            i0 = base + int(SR * beat * k)
            loop[i0:i0 + n] += 0.22 * np.sin(2 * np.pi * b * 2 * tt) * env_exp(n, 0.25)
        for k in range(4):
            n = int(SR * 0.03)
            i0 = base + int(SR * beat * (k + 0.5))
            loop[i0:i0 + n] += 0.05 * RNG.standard_normal(n) * env_exp(n, 0.006)
    reps = int(np.ceil(total * SR / len(loop)))
    m = np.tile(loop, reps)[:int(total * SR)]
    fade = int(SR * 3)
    m[-fade:] *= np.linspace(1, 0, fade)
    m[:int(SR * 0.5)] *= np.linspace(0, 1, int(SR * 0.5))
    return 0.35 * m / (np.abs(m).max() + 1e-9)


# ------------------------------------------------------------------ voz
def generar_voz(modelo, textos):
    import sherpa_onnx
    nombre = [x for x in os.listdir(modelo) if x.endswith(".onnx")][0]
    cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
        vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=os.path.join(modelo, nombre), tokens=os.path.join(modelo, "tokens.txt"),
                                                   data_dir=os.path.join(modelo, "espeak-ng-data")), num_threads=4))
    tts = sherpa_onnx.OfflineTts(cfg)
    voces = []
    for tx in textos:
        a = tts.generate(tx, sid=0, speed=1.0)
        y = np.array(a.samples, dtype=np.float64)
        x_old = np.arange(len(y)) / a.sample_rate
        x_new = np.arange(int(len(y) * SR / a.sample_rate)) / SR
        y = np.interp(x_new, x_old, y)
        y = np.concatenate([np.zeros(int(SR * 0.12)), y, np.zeros(int(SR * 0.3))])
        voces.append(y)
    return voces


# ------------------------------------------------------------------ render
def _cuadro(args):
    i, narr, e, prev, t, dur = args
    svg = escena_a(i, narr, e, prev, t, dur).encode("utf-8")
    return subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-f", "png"], input=svg, capture_output=True, check=True).stdout


def main():
    modelo, salida = sys.argv[1], sys.argv[2]
    fps = int(sys.argv[3]) if len(sys.argv) > 3 else FPS
    escenas = G.E
    textos = [n for n, _ in escenas]
    print("voz...", flush=True)
    voces = generar_voz(modelo, textos)
    durs = [max(len(v) / SR, 2.5) for v in voces]
    total = sum(durs)
    print(f"duración total {total:.1f} s", flush=True)
    cargar_sfx()
    pista = np.zeros(int(SR * (total + 1)))
    t0 = 0.0
    for k, ((narr, e), v, d) in enumerate(zip(escenas, voces, durs)):
        prev = escenas[k - 1][1] if k else None
        i0 = int(SR * t0)
        pista[i0:i0 + len(v)] += v * 0.95
        for ts, nombre, vol in eventos_sfx(e, prev, d):
            snd = SFX[nombre] * vol * 0.6
            j = i0 + int(SR * ts)
            if j < len(pista):
                pista[j:j + len(snd)] += snd[:len(pista) - j]
        t0 += d
    pista[:int(SR * total)] += musica(total) * 0.32
    pista = pista[:int(SR * total)]
    pista /= max(1.0, np.abs(pista).max() / 0.95)
    wav = salida + ".wav"
    sf.write(wav, pista.astype(np.float32), SR)
    tareas = []
    for k, ((narr, e), d) in enumerate(zip(escenas, durs)):
        prev = escenas[k - 1][1] if k else None
        for fi in range(int(round(d * fps))):
            tareas.append((k + 1, narr, e, prev, fi / fps, d))
    print(f"{len(tareas)} cuadros", flush=True)
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(fps), "-i", "-", "-i", wav,
                           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-shortest", "-movflags", "+faststart", salida], stdin=subprocess.PIPE)
    with Pool(4) as pool:
        for n, png in enumerate(pool.imap(_cuadro, tareas, chunksize=4)):
            ff.stdin.write(png)
            if n % 240 == 0:
                print(f"cuadro {n}/{len(tareas)}", flush=True)
    ff.stdin.close()
    ff.wait()
    os.remove(wav)
    print("listo", salida, flush=True)


if __name__ == "__main__":
    main()
