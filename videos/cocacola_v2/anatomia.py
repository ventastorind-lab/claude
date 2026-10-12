"""Escenas "dentro del cuerpo" en estilo caricatura (contorno negro grueso) para el video de Byron.

Cada función recibe (fase, t, dur) y devuelve el SVG de un cuadro completo de 1920x1080.
Los órganos tienen carita para que reaccionen como personajes.
"""
import math
import random

W, H = 1920, 1080
INK = "#1A1A1A"
FUENTE = "Arial Black, Arial"


def f(v):
    return f"{v:.1f}"


def c01(x):
    return max(0.0, min(1.0, x))


def prog(t, a, d):
    return c01((t - a) / d) if d > 0 else float(t >= a)


def eo(x):
    return 1 - (1 - x) ** 3


def lerp(a, b, p):
    return a + (b - a) * p


def txt(x, y, s, fs, col=INK, anc="middle", extra=""):
    return f'<text x="{f(x)}" y="{f(y)}" text-anchor="{anc}" font-family="{FUENTE}" font-weight="900" font-size="{f(fs)}" fill="{col}" {extra}>{s}</text>'


def fondo_tejido(c1, c2, t, seed=1):
    r = random.Random(seed)
    s = [f'<defs><radialGradient id="tej{seed}" cx="0.5" cy="0.5" r="0.75"><stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></radialGradient></defs>',
         f'<rect width="1920" height="1080" fill="url(#tej{seed})"/>']
    for _ in range(26):
        x, y = r.uniform(0, 1920), r.uniform(0, 1080)
        rr = r.uniform(20, 70)
        dx = 10 * math.sin(t * 0.8 + x)
        s.append(f'<circle cx="{f(x + dx)}" cy="{f(y)}" r="{f(rr)}" fill="#FFFFFF" opacity="0.07"/>')
    return "".join(s)


def carita(x, y, k=1.0, animo="feliz", t=0.0):
    """Ojos y boca caricatura. animo: feliz, susto, mareado, sufre, fiesta."""
    pest = 1 if (t % 3.2) > 0.12 else 0.1
    s = [f'<g transform="translate({f(x)} {f(y)}) scale({k:.3f})">']
    if animo == "mareado":
        for ex in (-38, 38):
            a = t * 400
            s.append(f'<g transform="translate({ex} 0) rotate({f(a)})"><path d="M0 0 m-14 0 a14 14 0 1 1 28 0 a10 10 0 1 1 -20 0 a6 6 0 1 1 12 0" fill="none" stroke="{INK}" stroke-width="5"/></g>')
    else:
        r = 22 if animo in ("susto", "fiesta") else 16
        for ex in (-38, 38):
            s.append(f'<ellipse cx="{ex}" cy="0" rx="{r}" ry="{f(r * 1.15 * pest)}" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
                     f'<circle cx="{ex + 4}" cy="3" r="{f(r * 0.5 * pest)}" fill="{INK}"/>')
    if animo == "feliz":
        s.append(f'<path d="M-26 34 Q 0 58 26 34" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>')
    elif animo == "fiesta":
        s.append(f'<path d="M-30 30 Q 0 76 30 30 Z" fill="#7A1F2B" stroke="{INK}" stroke-width="6"/>')
    elif animo == "susto":
        s.append(f'<ellipse cx="0" cy="46" rx="18" ry="24" fill="#7A1F2B" stroke="{INK}" stroke-width="6"/>')
        s.append(f'<path d="M-60 -50 l 20 10 M 60 -50 l -20 10" stroke="{INK}" stroke-width="6"/>')
    elif animo == "sufre":
        s.append(f'<path d="M-26 50 Q 0 28 26 50" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>')
        s.append(f'<path d="M-58 -36 l 30 -12 M 58 -36 l -30 -12" stroke="{INK}" stroke-width="6"/>')
        s.append(f'<path d="M64 -10 q 10 22 0 30 q -10 -8 0 -30" fill="#7EC8F2" stroke="{INK}" stroke-width="3"/>')
    else:
        s.append(f'<path d="M-24 44 h48" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
    s.append('</g>')
    return "".join(s)


def rotulo(texto, color, t, icono=""):
    p = eo(prog(t, 0.15, 0.45))
    w = len(texto) * 46 + 140
    x = 960 - w / 2
    return (f'<g transform="translate(0 {f(-120 * (1 - p))})"><rect x="{f(x)}" y="40" width="{f(w)}" height="100" rx="50" fill="{color}" stroke="{INK}" stroke-width="8"/>'
            + txt(960, 112, texto, 64, "#FFFFFF", extra=f'stroke="{INK}" stroke-width="3" paint-order="stroke"') + '</g>')


def medidor(x, y, valor, maximo, etiqueta, unidad, color, t, start=0.5):
    p = eo(prog(t, start, 1.2))
    v = valor * p
    frac = c01(v / maximo)
    s = [f'<g transform="translate({x} {y})"><rect x="0" y="0" width="420" height="150" rx="24" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>',
         txt(210, 46, etiqueta, 30),
         f'<rect x="30" y="70" width="360" height="34" rx="17" fill="#E0E0E0" stroke="{INK}" stroke-width="5"/>',
         f'<rect x="30" y="70" width="{f(360 * frac)}" height="34" rx="17" fill="{color}" stroke="{INK}" stroke-width="5"/>',
         txt(210, 138, f"{v:,.0f} {unidad}".replace(",", "."), 30, color), '</g>']
    return "".join(s)


def gota(x, y, k=1.0, col="#F4D03F"):
    return f'<path d="M{f(x)} {f(y - 30 * k)} C {f(x + 22 * k)} {f(y)} {f(x + 18 * k)} {f(y + 22 * k)} {f(x)} {f(y + 22 * k)} C {f(x - 18 * k)} {f(y + 22 * k)} {f(x - 22 * k)} {f(y)} {f(x)} {f(y - 30 * k)} Z" fill="{col}" stroke="{INK}" stroke-width="4"/>'


def burbujas(x0, x1, y0, y1, t, n=26, seed=3, vel=180, r0=8, r1=26, col="#FFFFFF"):
    r = random.Random(seed)
    s = []
    for _ in range(n):
        x = r.uniform(x0, x1)
        sp = r.uniform(0.6, 1.4) * vel
        y = y1 - ((r.uniform(0, y1 - y0) + t * sp) % (y1 - y0))
        rr = r.uniform(r0, r1)
        s.append(f'<circle cx="{f(x + 8 * math.sin(t * 3 + x))}" cy="{f(y)}" r="{f(rr)}" fill="{col}" fill-opacity="0.55" stroke="{INK}" stroke-width="3"/>')
    return "".join(s)


def hexagono(x, y, r=18, col="#FFFFFF"):
    pts = " ".join(f"{f(x + r * math.cos(math.radians(60 * i + 30)))},{f(y + r * math.sin(math.radians(60 * i + 30)))}" for i in range(6))
    return f'<polygon points="{pts}" fill="{col}" stroke="{INK}" stroke-width="4"/>'


def bacteria(x, y, k, t, col="#8BC34A", seed=0, come=False):
    a = 10 * math.sin(t * 4 + seed)
    boca = (f'<path d="M30 0 Q 48 {f(10 + 8 * math.sin(t * 12 + seed))} 30 20" fill="#7A1F2B" stroke="{INK}" stroke-width="4"/>' if come
            else f'<path d="M20 12 q 10 6 18 0" stroke="{INK}" stroke-width="4" fill="none"/>')
    pelos = "".join(f'<path d="M{f(-40 + i * 16)} -26 q 4 -14 -2 -22" stroke="{INK}" stroke-width="3" fill="none"/>' for i in range(5))
    return (f'<g transform="translate({f(x)} {f(y)}) rotate({f(a)}) scale({k:.2f})">{pelos}<ellipse rx="54" ry="30" fill="{col}" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="14" cy="-6" r="7" fill="#FFF" stroke="{INK}" stroke-width="3"/><circle cx="16" cy="-5" r="3" fill="{INK}"/>{boca}</g>')


def byron_cam(svg_byron, t):
    """Recuadro redondo con Byron reaccionando (imagen dentro de imagen)."""
    return (f'<g transform="translate(1770 740)"><circle r="140" fill="#FFF3E0" stroke="{INK}" stroke-width="8"/>'
            f'<clipPath id="bcam"><circle r="133"/></clipPath><g clip-path="url(#bcam)"><g transform="scale(0.27) translate(-960 -700)">{svg_byron}</g></g>'
            f'<rect x="-100" y="112" width="200" height="48" rx="24" fill="#E53935" stroke="{INK}" stroke-width="5"/>'
            + txt(0, 147, "BYRON CAM", 24, "#FFFFFF") + '</g>')


# ---------------------------------------------------------------- órganos
def dientes(fase, t, dur):
    s = [fondo_tejido("#F8BBD0", "#C2185B", t, 2), rotulo("DIENTES", "#E53935", t)]
    dano = c01(t / max(dur, 1)) if fase == "acido" else 0.6
    # muela en corte
    s.append('<g transform="translate(760 600)">')
    corona = "M-260 -120 Q -280 -300 -150 -320 Q -80 -340 0 -300 Q 80 -340 150 -320 Q 280 -300 260 -120 L 220 60 Q 180 300 120 330 Q 60 200 0 190 Q -60 200 -120 330 Q -180 300 -220 60 Z"
    s.append(f'<path d="{corona}" fill="#FFFDF7" stroke="{INK}" stroke-width="10"/>')
    s.append('<path d="M-200 -100 Q -210 -250 -120 -265 Q -60 -280 0 -245 Q 60 -280 120 -265 Q 210 -250 200 -100 L 170 60 Q 140 230 110 250 Q 50 150 0 140 Q -50 150 -110 250 Q -140 230 -170 60 Z" fill="#F7E3A8" stroke="#C9A54A" stroke-width="5"/>')
    s.append('<path d="M-90 -120 Q 0 -190 90 -120 L 70 60 Q 40 170 20 180 L 0 120 L -20 180 Q -40 170 -70 60 Z" fill="#F48FB1" stroke="#C2185B" stroke-width="5"/>')
    r = random.Random(5)
    for i in range(int(18 * dano)):
        a = r.uniform(-2.6, -0.5)
        x = 255 * math.cos(a) * 1.0
        y = -110 + 200 * math.sin(a)
        s.append(f'<ellipse cx="{f(x)}" cy="{f(y)}" rx="{f(r.uniform(8, 20))}" ry="{f(r.uniform(6, 12))}" fill="#C9A54A" opacity="0.8"/>')
    s.append(carita(0, -40, 1.1, "sufre" if dano > 0.35 else "susto", t))
    s.append('</g>')
    if fase == "acido":
        for i in range(10):
            q = (t * 0.7 + i * 0.1) % 1
            x = 520 + i * 52
            s.append(gota(x, 160 + q * 300, 1.0, "#8D2C1F"))
        s.append(f'<g transform="translate(1250 200)"><rect width="560" height="420" rx="30" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
                 + txt(280, 70, "ESCALA DE ACIDEZ (pH)", 34))
        barra = "".join(f'<rect x="{40 + i * 34}" y="110" width="34" height="60" fill="{c}"/>' for i, c in enumerate(
            ["#B71C1C", "#D84315", "#EF6C00", "#F9A825", "#C0CA33", "#7CB342", "#43A047", "#00897B", "#039BE5", "#3949AB", "#5E35B1", "#6A1B9A", "#4A148C", "#311B92"]))
        s.append(barra + f'<rect x="40" y="110" width="476" height="60" fill="none" stroke="{INK}" stroke-width="5"/>')
        for v, etq, y in ((2.0, "Limón ≈ 2", 230), (2.5, "COCA-COLA ≈ 2,5", 300), (7.0, "Agua = 7", 370)):
            x = 40 + v * 34
            p = prog(t, 0.6 + y / 400, 0.4)
            if p > 0:
                col = "#E53935" if "COCA" in etq else INK
                s.append(f'<g opacity="{f(p)}"><path d="M{f(x)} 175 V{y - 30}" stroke="{col}" stroke-width="5"/>' + txt(x if v > 3 else 60, y, etq, 32, col, "middle" if v > 3 else "start") + '</g>')
        s.append('</g>')
    else:
        r = random.Random(9)
        for i in range(6):
            x = 300 + i * 140 + 20 * math.sin(t * 2 + i)
            y = 230 + (i % 2) * 60
            s.append(bacteria(x, y, 0.9, t, ["#8BC34A", "#AED581", "#9CCC65"][i % 3], i, come=True))
            s.append(f'<rect x="{f(x - 80 - (t * 40) % 60)}" y="{f(y - 18)}" width="30" height="30" fill="#FFFFFF" stroke="{INK}" stroke-width="4"/>')
            for j in range(3):
                q = (t * 0.9 + j * 0.33 + i * 0.1) % 1
                s.append(gota(x + 20, y + 40 + q * 220, 0.6, "#8D2C1F"))
        s.append(f'<g transform="translate(1260 240)"><rect width="520" height="200" rx="30" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
                 + txt(260, 85, "AZÚCAR + BACTERIAS", 36) + txt(260, 150, "= MÁS ÁCIDO", 48, "#E53935") + '</g>')
    return "".join(s)


def estomago(fase, t, dur):
    s = [fondo_tejido("#FFCCBC", "#BF360C", t, 3), rotulo("ESTÓMAGO", "#FB8C00", t)]
    gas = fase in ("gas", "eructo")
    k = 1 + (0.18 + 0.03 * math.sin(t * 6) if gas else 0.0) * eo(prog(t, 0.4, 1.5))
    nivel = 0.35 if fase == "tamano" else 0.55
    s.append(f'<g transform="translate(900 600) scale({k:.3f})">')
    forma = "M-60 -400 L -60 -260 Q -280 -240 -300 0 Q -300 260 -60 300 Q 160 330 260 200 Q 320 120 300 40 L 360 40 L 360 -10 L 250 -20 Q 200 -180 80 -240 Q 40 -255 40 -260 L 40 -400 Z"
    s.append(f'<path d="{forma}" fill="#F48FB1" stroke="{INK}" stroke-width="12"/>')
    s.append('<clipPath id="estc"><path d="M-40 -250 Q -260 -230 -280 0 Q -280 240 -60 280 Q 150 310 240 190 Q 300 110 280 30 Q 230 -170 80 -225 Z"/></clipPath>')
    ly = lerp(300, -230, nivel * eo(prog(t, 0.3, 1.2)))
    ola = " ".join(f"L{f(-320 + i * 40)} {f(ly + 10 * math.sin(t * 3 + i * 0.7))}" for i in range(18))
    s.append(f'<g clip-path="url(#estc)"><path d="M-320 400 {ola} L 400 400 Z" fill="#5D2A12"/>'
             f'<path d="M-320 400 {ola} L 400 400 Z" fill="none" stroke="#8D4A22" stroke-width="10"/>'
             + burbujas(-260, 260, ly - 20, 280, t, 30 if gas else 14, 4, 160, 8, 22, "#FFFFFF") + '</g>')
    s.append(carita(-20, -120, 1.0, "susto" if gas else "feliz", t))
    s.append('</g>')
    if fase == "tamano":
        s.append(f'<g transform="translate(1420 300)"><rect width="420" height="330" rx="30" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
                 + txt(210, 70, "CAPACIDAD", 38) + f'<circle cx="110" cy="190" r="56" fill="#F48FB1" stroke="{INK}" stroke-width="6"/>' + txt(110, 290, "VACÍO", 28)
                 + f'<ellipse cx="300" cy="190" rx="92" ry="80" fill="#F48FB1" stroke="{INK}" stroke-width="6"/>' + txt(300, 290, "≈ 1 LITRO", 28) + '</g>')
    if gas:
        p = c01((t - 0.6) / 1.2)
        s.append(f'<g transform="translate(1500 240) rotate({f(-60 + 120 * p)} 0 120)"><circle cx="0" cy="120" r="150" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
                 f'<path d="M0 120 L 0 10" stroke="#E53935" stroke-width="12" stroke-linecap="round"/><circle cx="0" cy="120" r="16" fill="{INK}"/></g>'
                 + txt(1500, 560, "PRESIÓN", 44))
        s.append(burbujas(820, 900, 0, 260, t, 12, 8, 380, 10, 24))
        s.append(txt(1080, 240, "CO₂", 80, "#FFFFFF", extra=f'stroke="{INK}" stroke-width="6" paint-order="stroke"'))
    return "".join(s)


def vaso(t, celulas=12, glucosa=0, hipo=0.0, seed=4):
    s = ['<rect x="0" y="260" width="1920" height="560" fill="#C62828"/>',
         '<rect x="0" y="230" width="1920" height="60" fill="#E57373" stroke="#1A1A1A" stroke-width="8"/>',
         '<rect x="0" y="790" width="1920" height="60" fill="#E57373" stroke="#1A1A1A" stroke-width="8"/>',
         '<rect x="0" y="290" width="1920" height="500" fill="#B71C1C" opacity="0.5"/>']
    r = random.Random(seed)
    for i in range(celulas):
        y = r.uniform(340, 740)
        x = (r.uniform(0, 2200) + t * r.uniform(220, 320)) % 2300 - 200
        k = 1 + 0.6 * hipo
        s.append(f'<g transform="translate({f(x)} {f(y)}) rotate({f(r.uniform(-30, 30))}) scale({k:.2f})"><ellipse rx="62" ry="40" fill="#E53935" stroke="{INK}" stroke-width="6"/>'
                 f'<ellipse rx="30" ry="16" fill="#C62828"/></g>')
    for i in range(int(glucosa)):
        y = r.uniform(320, 760)
        x = (r.uniform(0, 2200) + t * r.uniform(150, 260)) % 2300 - 200
        s.append(hexagono(x, y, 16))
    return "".join(s)


def sangre(fase, t, dur):
    s = [fondo_tejido("#FFCDD2", "#8E0000", t, 5)]
    if fase == "normal":
        s.append(vaso(t, 14, 4))
        s.append(rotulo("TU SANGRE", "#C62828", t))
        s.append(f'<g transform="translate(60 640)"><rect width="680" height="170" rx="30" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
                 + hexagono(80, 85, 34) + txt(390, 75, "TODA tu sangre:", 36) + txt(390, 135, "≈ 4–5 g de azúcar", 52, "#C62828") + '</g>')
    elif fase == "azucar":
        n = 4 + 90 * eo(prog(t, 0.5, max(1, dur * 0.6)))
        s.append(vaso(t, 14, n))
        s.append(rotulo("¡AZÚCAR EN LA SANGRE!", "#C62828", t))
        s.append(f'<g transform="translate(60 640)"><rect width="680" height="170" rx="30" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
                 + txt(340, 75, "1 lata = 39 g", 44) + txt(340, 140, "≈ 9 veces la sangre", 48, "#C62828") + '</g>')
    else:  # hiponatremia
        h = eo(prog(t, 0.5, max(1, dur * 0.6)))
        s.append(vaso(t, 12, 0, h))
        for i in range(10):
            q = (t * 0.5 + i * 0.1) % 1
            s.append(gota(100 + i * 180, 280 + q * 500, 1.1, "#7EC8F2"))
        r = random.Random(2)
        for i in range(int(14 * (1 - h)) + 2):
            x = (r.uniform(0, 1920) + t * 200) % 1920
            y = r.uniform(330, 760)
            s.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="22" fill="#FFF59D" stroke="{INK}" stroke-width="4"/>' + txt(x, y + 9, "Na", 22))
        s.append(rotulo("SANGRE DILUIDA", "#1E88E5", t))
        s.append(f'<g transform="translate(60 640)"><rect width="760" height="170" rx="30" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
                 + txt(380, 75, "HIPONATREMIA", 48, "#1E88E5") + txt(380, 135, "el sodio baja · las células se hinchan", 30) + '</g>')
    return "".join(s)


def celula(x, y, r, abierta, t, col="#FFE082"):
    s = [f'<circle cx="{f(x)}" cy="{f(y)}" r="{r}" fill="{col}" stroke="{INK}" stroke-width="7"/>',
         f'<circle cx="{f(x - r * 0.25)}" cy="{f(y - r * 0.2)}" r="{r * 0.28}" fill="#FFB74D" stroke="{INK}" stroke-width="4"/>']
    px, py = x + r * 0.95, y
    if abierta:
        s.append(f'<rect x="{f(px - 18)}" y="{f(py - 30)}" width="36" height="60" fill="#5D4037" stroke="{INK}" stroke-width="5" transform="rotate(-50 {f(px - 18)} {f(py - 30)})"/>')
    else:
        s.append(f'<rect x="{f(px - 18)}" y="{f(py - 30)}" width="36" height="60" fill="#8D6E63" stroke="{INK}" stroke-width="5"/><circle cx="{f(px)}" cy="{f(py - 4)}" r="6" fill="{INK}"/>')
    return "".join(s)


def llave(x, y, k=1.0, rot=0):
    return (f'<g transform="translate({f(x)} {f(y)}) rotate({f(rot)}) scale({k:.2f})"><circle cx="-30" cy="0" r="22" fill="#FFD54F" stroke="{INK}" stroke-width="5"/>'
            f'<circle cx="-30" cy="0" r="8" fill="#FFF"/><path d="M-8 0 H 50 V 14 M 34 0 V 12" stroke="{INK}" stroke-width="16" fill="none"/>'
            f'<path d="M-8 0 H 50 V 14 M 34 0 V 12" stroke="#FFD54F" stroke-width="8" fill="none"/></g>')


def pancreas(fase, t, dur):
    s = [fondo_tejido("#FFF3E0", "#E65100", t, 6), rotulo("PÁNCREAS", "#F57C00", t)]
    s.append('<g transform="translate(420 560)">'
             f'<path d="M-260 40 Q -300 -80 -160 -100 Q 0 -120 120 -80 Q 250 -40 300 20 Q 260 90 120 80 Q -40 70 -140 120 Q -240 150 -260 40 Z" fill="#FFB74D" stroke="{INK}" stroke-width="10"/>'
             + "".join(f'<circle cx="{-200 + i * 60}" cy="{-30 + (i % 2) * 40}" r="14" fill="#FFA726" stroke="{INK}" stroke-width="3"/>' for i in range(8))
             + carita(0, -20, 0.9, "susto", t) + '</g>')
    s.append(txt(420, 380, "¡INSULINA!", 72, "#E53935", extra=f'stroke="{INK}" stroke-width="5" paint-order="stroke"'))
    for j, (cx, cy) in enumerate(((1250, 330), (1650, 420), (1300, 720), (1700, 800))):
        st = 0.8 + j * 0.45
        q = c01((t - st) / 0.9)
        s.append(celula(cx, cy, 120, q >= 1, t))
        if 0 < q < 1:
            s.append(llave(lerp(650, cx + 115, eo(q)), lerp(560, cy, eo(q)), 1.1, 360 * q))
        if q >= 1:
            for g in range(3):
                qq = ((t - st) * 0.8 + g * 0.33) % 1
                s.append(hexagono(cx + 220 - qq * 150, cy - 10 + g * 14, 13))
    return "".join(s)


def bodega(fase, t, dur):
    s = [fondo_tejido("#E8F5E9", "#2E7D32", t, 7), rotulo("¿DÓNDE SE GUARDA?", "#43A047", t)]
    for i, (nom, cap, x) in enumerate((("HÍGADO", "≈ 100 g", 160), ("MÚSCULOS", "≈ 400 g", 760))):
        w = 420 if i == 0 else 640
        lleno = eo(prog(t, 0.6 + i * 0.4, max(1.5, dur * 0.5)))
        s.append(f'<rect x="{x}" y="320" width="{w}" height="520" rx="20" fill="#FFFFFF" stroke="{INK}" stroke-width="9"/>')
        s.append(f'<rect x="{x + 14}" y="{f(826 - 492 * lleno)}" width="{w - 28}" height="{f(492 * lleno)}" fill="#FFE082"/>')
        r = random.Random(i)
        for k in range(int(30 * lleno * (w / 420))):
            s.append(hexagono(x + 40 + r.uniform(0, w - 80), 820 - r.uniform(0, 480 * lleno), 18))
        s.append(txt(x + w / 2, 300, nom, 50, "#FFFFFF", extra=f'stroke="{INK}" stroke-width="6" paint-order="stroke"'))
        s.append(txt(x + w / 2, 880, cap, 46, "#FFFFFF", extra=f'stroke="{INK}" stroke-width="6" paint-order="stroke"'))
        if lleno >= 1:
            s.append(f'<g transform="translate({x + w / 2} 580) rotate(-12)"><rect x="-150" y="-50" width="300" height="100" rx="14" fill="#E53935" stroke="{INK}" stroke-width="7"/>' + txt(0, 22, "LLENO", 60, "#FFFFFF") + '</g>')
    s.append(f'<g transform="translate(1700 300)"><rect x="-150" y="-60" width="300" height="230" rx="24" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
             + txt(0, 0, "BYRON:", 34) + txt(0, 80, "1.950 g", 60, "#E53935") + txt(0, 140, "de azúcar", 32) + '</g>')
    return "".join(s)


def cerebro(fase, t, dur):
    s = [fondo_tejido("#EDE7F6", "#4527A0", t, 8), rotulo("CEREBRO", "#7E57C2", t)]
    pulso = 1 + 0.03 * math.sin(t * 8)
    s.append(f'<g transform="translate(700 590) scale({pulso:.3f})">'
             '<path d="M-330 40 Q -380 -160 -220 -250 Q -120 -330 0 -290 Q 120 -340 230 -260 Q 380 -170 340 30 Q 320 180 160 220 Q 40 250 -40 220 Q -200 240 -290 160 Q -340 110 -330 40 Z" fill="#F8BBD0" stroke="#1A1A1A" stroke-width="12"/>'
             + "".join(f'<path d="M{-280 + i * 70} {-150 + (i % 3) * 60} q 30 -40 60 0 q 30 40 60 0" stroke="#C2185B" stroke-width="7" fill="none"/>' for i in range(8))
             + '<path d="M0 -290 Q -20 -40 10 220" stroke="#C2185B" stroke-width="7" fill="none"/>'
             + carita(0, 30, 1.2, "fiesta" if fase == "dopamina" else "mareado", t) + '</g>')
    if fase == "dopamina":
        r = random.Random(3)
        for i in range(10):
            q = ((t * 0.6) + i * 0.1) % 1
            cx, cy = 700 + r.uniform(-300, 300), 400 + r.uniform(-200, 120)
            for a in range(0, 360, 45):
                x2 = cx + math.cos(math.radians(a)) * 90 * q
                y2 = cy + math.sin(math.radians(a)) * 90 * q
                s.append(f'<circle cx="{f(x2)}" cy="{f(y2)}" r="{f(10 * (1 - q) + 2)}" fill="{["#FFD54F", "#FF4081", "#40C4FF", "#69F0AE"][i % 4]}" stroke="{INK}" stroke-width="2"/>')
        s.append(f'<g transform="translate(1460 420)"><rect x="-300" y="-110" width="600" height="230" rx="30" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
                 + txt(0, -20, "DOPAMINA", 70, "#FF4081") + txt(0, 70, "la química del \"¡qué rico!\"", 36) + '</g>')
    else:
        for i in range(4):
            x, y = 1250 + (i % 2) * 360, 300 + (i // 2) * 330
            s.append(f'<path d="M{x - 70} {y + 60} Q {x - 70} {y - 40} {x} {y - 40} Q {x + 70} {y - 40} {x + 70} {y + 60}" fill="#B39DDB" stroke="{INK}" stroke-width="8"/>')
            ent = prog(t, 0.6 + i * 0.35, 0.6)
            s.append(f'<g transform="translate({x} {f(lerp(y - 260, y - 10, eo(ent)))})"><polygon points="0,-46 40,-23 40,23 0,46 -40,23 -40,-23" fill="#6D4C41" stroke="{INK}" stroke-width="6"/>' + txt(0, 12, "CAF", 26, "#FFFFFF") + '</g>')
            if ent >= 1:
                rb = ((t * 1.3 + i * 0.3) % 1)
                s.append(f'<g transform="translate({f(x + 120 + rb * 60)} {f(y - 120 - rb * 80)})" opacity="{f(1 - rb)}"><circle r="32" fill="#90CAF9" stroke="{INK}" stroke-width="5"/>' + txt(0, 10, "zzz", 24) + '</g>')
    return "".join(s)


def corazon(fase, t, dur):
    s = [fondo_tejido("#FFEBEE", "#B71C1C", t, 9), rotulo("CORAZÓN Y VENAS", "#D32F2F", t)]
    bpm = lerp(70, 125, eo(prog(t, 0.5, max(1, dur * 0.6))))
    ph = (t * bpm / 60) % 1
    lat = 1 + 0.12 * math.exp(-((ph - 0.1) ** 2) / 0.004)
    s.append(f'<g transform="translate(620 580) scale({lat:.3f})">'
             '<path d="M-50 -200 V -330 M 50 -200 Q 50 -360 170 -360" stroke="#1A1A1A" stroke-width="60" fill="none" stroke-linecap="round"/><path d="M-50 -200 V -330 M 50 -200 Q 50 -360 170 -360" stroke="#C62828" stroke-width="44" fill="none" stroke-linecap="round"/>'
             + f'<path d="M0 230 C -320 30 -330 -230 -150 -250 C -60 -260 -10 -200 0 -150 C 10 -200 60 -260 150 -250 C 330 -230 320 30 0 230 Z" fill="#E53935" stroke="{INK}" stroke-width="12"/>'
             + carita(0, -40, 1.1, "sufre" if bpm > 100 else "susto", t) + '</g>')
    # electrocardiograma
    pts = []
    for i in range(160):
        x = 1100 + i * 4.8
        u = (i / 160 * 4 - t * bpm / 60) % 1
        y = 420 - (160 * math.exp(-((u - 0.5) ** 2) / 0.0006) - 40 * math.exp(-((u - 0.56) ** 2) / 0.0008)) + 18 * math.exp(-((u - 0.75) ** 2) / 0.004) * -1
        pts.append(f"{f(x)} {f(y)}")
    s.append(f'<rect x="1070" y="200" width="820" height="360" rx="24" fill="#102018" stroke="{INK}" stroke-width="8"/>')
    s.append('<path d="M' + " L".join(pts) + '" stroke="#69F0AE" stroke-width="7" fill="none"/>')
    s.append(txt(1400, 630, f"{bpm:.0f} pulsaciones / min", 54, "#FFFFFF", extra=f'stroke="{INK}" stroke-width="6" paint-order="stroke"'))
    # venas que laten
    for i in range(3):
        y = 800 + i * 70
        w = 26 + 10 * math.exp(-((ph - 0.12 - i * 0.05) ** 2) / 0.004)
        s.append(f'<path d="M1080 {y} Q 1300 {y - 40} 1500 {y} T 1900 {y}" stroke="#8E24AA" stroke-width="{f(w)}" fill="none" stroke-linecap="round"/>')
    return "".join(s)


def higado(fase, t, dur):
    s = [fondo_tejido("#FBE9E7", "#6D2E1E", t, 10), rotulo("HÍGADO", "#8D4A22", t)]
    grasa = eo(prog(t, 0.5, max(1.5, dur * 0.7))) if fase == "grasa" else 0
    col = "#A0442A" if grasa < 0.01 else ("#A0442A" if grasa < 0 else None)
    a = [int("A0442A"[i:i + 2], 16) for i in (0, 2, 4)]
    b = [int("D9A441"[i:i + 2], 16) for i in (0, 2, 4)]
    col = "#" + "".join(f"{int(x + (y - x) * grasa * 0.7):02X}" for x, y in zip(a, b))
    s.append(f'<g transform="translate(760 600)"><path d="M-420 -60 Q -400 -260 -100 -270 Q 200 -280 380 -180 Q 440 -140 400 -60 Q 300 120 40 200 Q -160 260 -300 150 Q -440 60 -420 -60 Z" fill="{col}" stroke="{INK}" stroke-width="12"/>')
    r = random.Random(4)
    for i in range(int(40 * grasa)):
        x, y = r.uniform(-340, 320), r.uniform(-220, 150)
        s.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r.uniform(12, 28))}" fill="#FFE082" stroke="{INK}" stroke-width="4"/>')
    s.append(carita(-40, -40, 1.2, "sufre" if grasa > 0.4 else "susto", t) + '</g>')
    if fase == "fructosa":
        for i in range(14):
            q = (t * 0.45 + i / 14) % 1
            x = lerp(1900, 1150, q)
            y = 300 + 400 * math.sin(i) * 0.5 + 300
            s.append(f'<g transform="translate({f(x)} {f(y)})"><polygon points="0,-24 23,-7 14,20 -14,20 -23,-7" fill="#FF8A65" stroke="{INK}" stroke-width="4"/></g>')
        s.append(f'<g transform="translate(1500 230)"><rect x="-330" y="-80" width="660" height="200" rx="30" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
                 + txt(0, 0, "AZÚCAR = 50 % GLUCOSA", 40) + txt(0, 80, "+ 50 % FRUCTOSA → HÍGADO", 40, "#E64A19") + '</g>')
    else:
        s.append(f'<g transform="translate(1500 260)"><rect x="-320" y="-90" width="640" height="220" rx="30" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
                 + txt(0, 0, "FRUCTOSA DE SOBRA", 44) + txt(0, 80, "= GOTITAS DE GRASA", 48, "#F9A825") + '</g>')
    return "".join(s)


def rinones(fase, t, dur):
    s = [fondo_tejido("#E3F2FD", "#0D47A1", t, 11), rotulo("RIÑONES Y VEJIGA", "#1E88E5", t)]
    for x, m in ((560, 1), (1060, -1)):
        s.append(f'<g transform="translate({x} 420) scale({m} 1)"><path d="M-110 -160 Q 60 -200 110 -60 Q 40 -20 60 40 Q 120 160 -40 200 Q -200 200 -170 0 Q -180 -130 -110 -160 Z" fill="#C2185B" stroke="{INK}" stroke-width="10"/>'
                 + carita(-40, 0, 0.7, "sufre", t) + '</g>')
    s.append(f'<path d="M640 560 Q 720 700 780 820 M 980 560 Q 900 700 840 820" stroke="#F8BBD0" stroke-width="22" fill="none"/><path d="M640 560 Q 720 700 780 820 M 980 560 Q 900 700 840 820" stroke="{INK}" stroke-width="4" fill="none" opacity="0.4"/>')
    llen = (t / 3.0) % 1
    s.append(f'<g transform="translate(810 840)"><ellipse rx="{f(110 + 40 * llen)}" ry="{f(80 + 30 * llen)}" fill="#F8BBD0" stroke="{INK}" stroke-width="9"/>'
             f'<clipPath id="vej"><ellipse rx="{f(100 + 40 * llen)}" ry="{f(70 + 30 * llen)}"/></clipPath><rect x="-160" y="{f(80 - 160 * llen)}" width="320" height="200" fill="#FFF176" clip-path="url(#vej)"/>'
             + txt(0, 14, "VEJIGA", 30) + '</g>')
    for i in range(6):
        q = (t * 1.2 + i / 6) % 1
        s.append(gota(lerp(640, 790, q), lerp(560, 820, q), 0.6, "#FFF176"))
    s.append(medidor(1360, 190, 1, 1, "LOS RIÑONES SACAN", "L / hora (máx.)", "#1E88E5", t, 0.5))
    s.append(medidor(1360, 370, 9, 9, "BYRON YA TOMÓ", "litros", "#E53935", t, 1.2))
    if prog(t, 2.2, 0.3) > 0:
        s.append(f'<g transform="translate(1500 545) rotate(-6)"><rect x="-230" y="-60" width="460" height="120" rx="20" fill="#E53935" stroke="{INK}" stroke-width="8"/>' + txt(0, 22, "¡NO ALCANZA!", 56, "#FFFFFF") + '</g>')
    return "".join(s)


def colon(fase, t, dur):
    s = [fondo_tejido("#F3E5F5", "#4A148C", t, 12), rotulo("INTESTINO Y COLON", "#8E24AA", t)]
    # marco del colon
    d = "M360 900 V 330 Q 360 250 440 250 H 1420 Q 1500 250 1500 330 V 760 Q 1500 840 1420 840 H 1080 Q 1000 840 1000 920 V 1000"
    s.append(f'<path d="{d}" stroke="{INK}" stroke-width="190" fill="none" stroke-linejoin="round"/><path d="{d}" stroke="#CE93D8" stroke-width="170" fill="none" stroke-linejoin="round"/>')
    for i in range(18):
        s.append(f'<circle cx="{360 + (i % 6) * 228}" cy="{250 if i < 6 else (840 if i < 12 else 540)}" r="0" fill="none"/>')
    # fructosa que llega y bacterias
    r = random.Random(6)
    camino = [(360 + 0, 900 - q * 650) for q in (0.0,)]
    _ = camino
    for i in range(16):
        q = (t * 0.25 + i / 16) % 1
        L = 650 + 1060 + 510
        dpos = q * L
        if dpos < 650:
            x, y = 360, 900 - dpos
        elif dpos < 650 + 1060:
            x, y = 360 + (dpos - 650), 250
        else:
            x, y = 1500, 250 + (dpos - 1710)
        s.append(f'<g transform="translate({f(x + r.uniform(-40, 40))} {f(y + r.uniform(-30, 30))})"><polygon points="0,-20 19,-6 12,16 -12,16 -19,-6" fill="#FF8A65" stroke="{INK}" stroke-width="4"/></g>')
    for i in range(7):
        x = 560 + i * 130
        s.append(bacteria(x, 255 + 10 * math.sin(t * 3 + i), 0.75, t, ["#7CB342", "#26A69A", "#AB47BC"][i % 3], i, come=True))
    s.append(burbujas(300, 1550, 150, 900, t, 22, 9, 120, 10, 30, "#C5E1A5"))
    if fase == "diarrea":
        for i in range(8):
            q = (t * 0.8 + i / 8) % 1
            s.append(gota(560 + i * 120, lerp(120, 240, q), 0.8, "#7EC8F2"))
        s.append(f'<g transform="translate(940 560)"><rect x="-330" y="-90" width="660" height="200" rx="30" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
                 + txt(0, -10, "GAS + AGUA EN EL", 44) + txt(0, 70, "INTESTINO", 56, "#8E24AA") + '</g>')
    else:
        s.append(f'<g transform="translate(940 560)"><rect x="-330" y="-110" width="660" height="240" rx="30" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
                 + txt(0, -30, "Se absorbe bien: 25–50 g", 38) + txt(0, 40, "BYRON: ≈ 585 g", 58, "#E53935") + txt(0, 100, "de fructosa", 32) + '</g>')
    return "".join(s)


def resumen(fase, t, dur):
    s = [fondo_tejido("#FFF8E1", "#FF8F00", t, 13), rotulo("TODO LO QUE PASÓ", "#E53935", t)]
    # silueta humana caricatura
    s.append('<g transform="translate(960 560)">'
             f'<circle cx="0" cy="-330" r="95" fill="#FFE0B2" stroke="{INK}" stroke-width="10"/>'
             f'<path d="M-150 -220 Q 0 -250 150 -220 L 190 120 Q 0 160 -190 120 Z" fill="#FFE0B2" stroke="{INK}" stroke-width="10"/>'
             f'<path d="M-170 -200 L -290 120 M 170 -200 L 290 120 M -110 130 L -130 470 M 110 130 L 130 470" stroke="{INK}" stroke-width="64" stroke-linecap="round"/>'
             f'<path d="M-170 -200 L -290 120 M 170 -200 L 290 120 M -110 130 L -130 470 M 110 130 L 130 470" stroke="#FFE0B2" stroke-width="48" stroke-linecap="round"/>'
             '</g>')
    items = [("Cerebro", "sin sueño, ansiedad", 960, 230, 360, 200), ("Dientes", "esmalte atacado", 1010, 280, 1540, 260), ("Corazón", "pulso acelerado", 1000, 420, 1540, 420),
             ("Estómago", "inflado de gas", 930, 520, 360, 470), ("Hígado", "grasa nueva", 900, 470, 360, 650), ("Riñones", "sin descanso", 1020, 580, 1540, 590),
             ("Colon", "gases y diarrea", 960, 650, 1540, 760), ("Sangre", "azúcar y sodio alterados", 860, 720, 360, 830)]
    org = {"Cerebro": "#F8BBD0", "Dientes": "#FFFFFF", "Corazón": "#E53935", "Estómago": "#F48FB1", "Hígado": "#A0442A", "Riñones": "#C2185B", "Colon": "#CE93D8", "Sangre": "#B71C1C"}
    paso = max(0.35, (dur * 0.75) / len(items))
    for i, (nom, efecto, ox, oy, lx, ly) in enumerate(items):
        p = eo(prog(t, 0.4 + i * paso, 0.4))
        if p <= 0:
            continue
        s.append(f'<circle cx="{ox}" cy="{oy}" r="{f(26 * p)}" fill="{org[nom]}" stroke="{INK}" stroke-width="5"/>')
        s.append(f'<path d="M{ox} {oy} L{lx} {ly}" stroke="{INK}" stroke-width="4" stroke-dasharray="10 8" opacity="{f(p)}"/>')
        w = 380
        bx = lx - w / 2
        s.append(f'<g opacity="{f(p)}"><rect x="{f(bx)}" y="{ly - 50}" width="{w}" height="100" rx="20" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
                 + txt(lx, ly - 8, nom.upper(), 34, "#E53935") + txt(lx, ly + 34, efecto, 26) + '</g>')
    return "".join(s)


ORGANOS = {"dientes": dientes, "estomago": estomago, "sangre": sangre, "pancreas": pancreas, "bodega": bodega, "cerebro": cerebro,
           "corazon": corazon, "higado": higado, "rinones": rinones, "colon": colon, "resumen": resumen}
