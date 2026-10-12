"""Ilustraciones planas con sombreado para el documental: gente, dinero, calles, tiendas, fábricas.

Todas las funciones devuelven fragmentos SVG. Coordenadas en un lienzo de 1920x1080.
"""
import math
import random

W, H = 1920, 1080
FUENTE = "Inter, Liberation Sans, Arial"


def f(v):
    return f"{v:.1f}"


def c01(x):
    return max(0.0, min(1.0, x))


def ease_out(x):
    return 1 - (1 - x) ** 3


def mezclar(c1, c2, p):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{int(round(x + (y - x) * p)):02X}" for x, y in zip(a, b))


def oscurecer(c, p=0.25):
    return mezclar(c, "#000000", p)


def aclarar(c, p=0.25):
    return mezclar(c, "#FFFFFF", p)


# ---------------------------------------------------------------- paletas por época
ERAS = {
    "1920": dict(cielo=("#E8D5AE", "#C9A877"), sol="#F4E3B5", fachada=["#A08466", "#8C7158", "#B39B7C", "#7D6A57", "#9A8A74"],
                 ropa=["#3B3A36", "#5A4A3A", "#4A5560", "#6B4E3D", "#2F3B45", "#5E5548", "#7A6650"], suelo="#8D7A62", acera="#A8957A",
                 piel=["#E8C4A0", "#D9B08C", "#C99A76"], pelo=["#2B2018", "#4A3628", "#6B5040", "#1A1A1A"], sombrero=0.7, tinte=("#7A5A2E", 0.10)),
    "1940": dict(cielo=("#D9D2C0", "#A9A296"), sol="#EDE6D2", fachada=["#8E8A80", "#7A766C", "#9C978C", "#6E6A62"],
                 ropa=["#3A3D40", "#4F4A44", "#5C5248", "#2E3338", "#615A50"], suelo="#7A756B", acera="#99948A",
                 piel=["#E3C2A2", "#D4AE8C"], pelo=["#2B2018", "#4A3628", "#1A1A1A", "#6B5A4A"], sombrero=0.6, tinte=("#5A5040", 0.12)),
    "1980": dict(cielo=("#F7C98B", "#8EC3E6"), sol="#FFE8A8", fachada=["#E8A87C", "#C8D6AF", "#F2D388", "#A7C5EB", "#E57F84", "#F4F1DE"],
                 ropa=["#C0392B", "#2980B9", "#F39C12", "#16A085", "#8E44AD", "#D35400", "#2C3E50", "#E8DAEF"], suelo="#9C8A74", acera="#C7B79E",
                 piel=["#E8B98F", "#C68E62", "#A8724A", "#8A5A36"], pelo=["#1A1A1A", "#2B2018", "#4A3628"], sombrero=0.2, tinte=None),
    "2010": dict(cielo=("#9ED2F5", "#4FA3DB"), sol="#FFF4C2", fachada=["#F2E8CF", "#E0B080", "#7FB7BE", "#D3A588", "#EAEAEA", "#F7C59F"],
                 ropa=["#E63946", "#457B9D", "#F1C40F", "#2A9D8F", "#264653", "#F4A261", "#6D597A", "#FFFFFF"], suelo="#8F8F8F", acera="#BDBDBD",
                 piel=["#E8B98F", "#C68E62", "#8A5A36", "#5C3A22"], pelo=["#1A1A1A", "#2B2018", "#4A3628"], sombrero=0.15, tinte=None),
}


# ---------------------------------------------------------------- personas
def persona(x, y, h=300, seed=0, t=0.0, pose="pie", era="1980", mira=1, ropa=None, carga=None, triste=False, opac=1.0, niebla=None):
    """Figura plana sin rostro. (x, y) = pies. pose: pie, camina, carga, empuja, brazos, sentado."""
    r = random.Random(seed)
    E = ERAS[era]
    piel = r.choice(E["piel"])
    pelo = r.choice(E["pelo"])
    abrigo = ropa or r.choice(E["ropa"])
    pant = oscurecer(r.choice(E["ropa"]), 0.35)
    mujer = r.random() < 0.45
    sombrero = r.random() < E["sombrero"]
    if niebla:
        piel, pelo, abrigo, pant = (mezclar(c, niebla[0], niebla[1]) for c in (piel, pelo, abrigo, pant))
    k = h / 300.0
    fase = t * 3.2 + r.random() * 6.28
    sw = math.sin(fase) if pose == "camina" else 0.0
    resp = 1.5 * math.sin(t * 1.7 + seed) if pose in ("pie", "carga", "brazos") else 0
    lean = {"empuja": 14, "carga": 3}.get(pose, 0) * mira
    s = [f'<g transform="translate({f(x)} {f(y)}) scale({k:.3f})" opacity="{opac:.2f}">']
    s.append('<ellipse cx="0" cy="2" rx="46" ry="9" fill="#000" opacity="0.18"/>')
    # piernas
    lw = 17
    for lado, ph in ((-1, 0), (1, math.pi)):
        a = 22 * math.sin(fase + ph) if pose == "camina" else (10 * lado if pose == "empuja" else 3 * lado)
        hx, hy = lado * 9, -150
        kx = hx + math.sin(math.radians(a)) * 72
        ky = hy + math.cos(math.radians(a)) * 72
        fx = kx + math.sin(math.radians(a * 0.4)) * 76
        fy = -4
        s.append(f'<path d="M{hx} {hy} L{f(kx)} {f(ky)} L{f(fx)} {f(fy)}" stroke="{pant}" stroke-width="{lw}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        s.append(f'<ellipse cx="{f(fx + 8 * mira)}" cy="-3" rx="15" ry="7" fill="#1E1A16"/>')
    # torso (abrigo)
    g = f'<g transform="rotate({lean} 0 -150)">'
    largo = -95 if era in ("1920", "1940") else -140
    if mujer and era in ("1920", "1940"):
        largo = -80
    torso = (f'<path d="M-30 -258 Q -40 -250 -38 -220 L -34 {largo} Q 0 {largo + 6} 34 {largo} L 38 -220 Q 40 -250 30 -258 Q 0 -266 -30 -258 Z" '
             f'fill="{abrigo}"/>'
             f'<path d="M10 -258 Q 40 -250 38 -220 L 34 {largo} Q 22 {largo + 3} 12 {largo + 2} Z" fill="#000" opacity="0.14"/>')
    if mujer and era not in ("1920", "1940"):
        torso += f'<path d="M-34 -160 L -46 -112 L 46 -112 L 34 -160 Z" fill="{oscurecer(abrigo, 0.15)}"/>'
    g += torso
    # cabeza
    hy = -292 + resp * 0.3
    g += f'<rect x="-8" y="-272" width="16" height="16" fill="{oscurecer(piel, 0.15)}"/>'
    cab_inc = 14 if triste else 0
    g += f'<g transform="rotate({cab_inc * mira} 0 -262)">'
    g += f'<ellipse cx="{3 * mira}" cy="{f(hy)}" rx="25" ry="29" fill="{piel}"/>'
    g += f'<path d="M{3 * mira + 6} {f(hy - 26)} A25 29 0 0 1 {3 * mira + 25} {f(hy)} Q {3 * mira + 18} {f(hy + 16)} {3 * mira + 8} {f(hy + 28)} Z" fill="#000" opacity="0.10"/>'
    if mujer:
        g += f'<path d="M{3 * mira - 27} {f(hy + 18)} Q {3 * mira - 32} {f(hy - 36)} {3 * mira} {f(hy - 32)} Q {3 * mira + 32} {f(hy - 36)} {3 * mira + 26} {f(hy + 6)} Q {3 * mira + 20} {f(hy - 18)} {3 * mira} {f(hy - 20)} Q {3 * mira - 16} {f(hy - 16)} {3 * mira - 18} {f(hy + 22)} Z" fill="{pelo}"/>'
    else:
        g += f'<path d="M{3 * mira - 26} {f(hy - 2)} Q {3 * mira - 26} {f(hy - 34)} {3 * mira} {f(hy - 31)} Q {3 * mira + 26} {f(hy - 32)} {3 * mira + 25} {f(hy - 6)} Q {3 * mira + 8} {f(hy - 20)} {3 * mira - 26} {f(hy - 2)} Z" fill="{pelo}"/>'
    if sombrero:
        sc = oscurecer(abrigo, 0.4)
        if era in ("1920", "1940"):
            g += (f'<ellipse cx="{3 * mira}" cy="{f(hy - 18)}" rx="40" ry="8" fill="{sc}"/>'
                  f'<path d="M{3 * mira - 24} {f(hy - 18)} Q {3 * mira - 24} {f(hy - 50)} {3 * mira} {f(hy - 50)} Q {3 * mira + 24} {f(hy - 50)} {3 * mira + 24} {f(hy - 18)} Z" fill="{sc}"/>'
                  f'<rect x="{3 * mira - 24}" y="{f(hy - 26)}" width="48" height="6" fill="#000" opacity="0.3"/>')
        else:
            g += f'<path d="M{3 * mira - 26} {f(hy - 12)} Q {3 * mira} {f(hy - 52)} {3 * mira + 26} {f(hy - 12)} Z M{3 * mira} {f(hy - 14)} h{32 * mira} v6 h{-32 * mira} Z" fill="{sc}"/>'
    g += '</g>'
    # brazos
    aw = 15
    hombro_y = -248
    brazos = []
    for lado in (-1, 1):
        sx = lado * 30
        if pose == "camina":
            a1 = -24 * math.sin(fase + (0 if lado < 0 else math.pi))
            a2 = a1 - 15
        elif pose in ("carga", "empuja"):
            a1, a2 = -70 * mira, -85 * mira
        elif pose == "brazos":
            a1, a2 = 160 * lado + 8 * math.sin(t * 5 + lado), 170 * lado
        elif triste:
            a1, a2 = 4 * lado, 2 * lado
        else:
            a1, a2 = 8 * lado + resp, 6 * lado
        ex = sx + math.sin(math.radians(a1)) * 58
        ey = hombro_y + math.cos(math.radians(a1)) * 58
        wx = ex + math.sin(math.radians(a2)) * 54
        wy = ey + math.cos(math.radians(a2)) * 54
        brazos.append(f'<path d="M{sx} {hombro_y} L{f(ex)} {f(ey)} L{f(wx)} {f(wy)}" stroke="{oscurecer(abrigo, 0.12 if lado == mira else 0.25)}" stroke-width="{aw}" fill="none" stroke-linecap="round" stroke-linejoin="round"/>'
                      f'<circle cx="{f(wx)}" cy="{f(wy)}" r="8" fill="{piel}"/>')
    g += "".join(brazos)
    if carga:
        g += carga
    g += '</g>'
    s.append(g)
    s.append('</g>')
    return "".join(s)


def multitud(x0, x1, y, n, seed, t, era="1980", filas=3, h=260, pose="pie", fondo="#000000", mira=None, triste=False, poses=None):
    r = random.Random(seed)
    out = []
    for fila in range(filas - 1, -1, -1):
        prof = fila / max(1, filas - 1)
        hh = h * (1 - 0.18 * fila)
        yy = y - fila * h * 0.16
        m = int(n * (1 + 0.25 * fila) / filas)
        for i in range(m):
            xx = x0 + (x1 - x0) * (i + 0.5 + r.uniform(-0.35, 0.35)) / m
            ps = r.choice(poses) if poses else pose
            out.append((yy, persona(xx, yy, hh * r.uniform(0.9, 1.06), seed * 100 + fila * 37 + i, t, ps, era,
                                    mira if mira is not None else r.choice((-1, 1)), triste=triste,
                                    niebla=(fondo, 0.45 * prof) if fila else None)))
    out.sort(key=lambda z: z[0])
    return "".join(o for _, o in out)


# ---------------------------------------------------------------- dinero
BILL = {"marco": "#C9B98E", "pengo": "#B7A3D3", "peso_bo": "#9CCFC0", "austral": "#9DB4D8", "cruzeiro": "#C7D99A", "zim": "#B9D7A0",
        "bolivar": "#E3B9C6", "dolar": "#A9C79A", "real": "#B9D3E8", "rentenmark": "#D8C08A", "forinto": "#E2C49A"}


def fajo(x, y, w=120, color="#A9C79A", k=1.0):
    """Fajo de billetes isométrico; (x, y) = esquina frontal inferior izquierda."""
    w *= k
    d = w * 0.42
    hgt = w * 0.18
    top = f'M{f(x)} {f(y - hgt)} L{f(x + w)} {f(y - hgt)} L{f(x + w + d * 0.6)} {f(y - hgt - d * 0.45)} L{f(x + d * 0.6)} {f(y - hgt - d * 0.45)} Z'
    fr = f'M{f(x)} {f(y)} L{f(x + w)} {f(y)} L{f(x + w)} {f(y - hgt)} L{f(x)} {f(y - hgt)} Z'
    sd = f'M{f(x + w)} {f(y)} L{f(x + w + d * 0.6)} {f(y - d * 0.45)} L{f(x + w + d * 0.6)} {f(y - hgt - d * 0.45)} L{f(x + w)} {f(y - hgt)} Z'
    banda = f'M{f(x + w * 0.42)} {f(y)} L{f(x + w * 0.58)} {f(y)} L{f(x + w * 0.58 + d * 0.6)} {f(y - hgt - d * 0.45)} L{f(x + w * 0.42 + d * 0.6)} {f(y - hgt - d * 0.45)} Z'
    lineas = "".join(f'<path d="M{f(x)} {f(y - hgt * j / 5)} H{f(x + w)}" stroke="{oscurecer(color, 0.3)}" stroke-width="1"/>' for j in range(1, 5))
    return (f'<path d="{fr}" fill="{oscurecer(color, 0.12)}"/>{lineas}<path d="{sd}" fill="{oscurecer(color, 0.28)}"/>'
            f'<path d="{top}" fill="{aclarar(color, 0.15)}"/>'
            f'<ellipse cx="{f(x + w / 2 + d * 0.3)}" cy="{f(y - hgt - d * 0.22)}" rx="{f(w * 0.12)}" ry="{f(d * 0.12)}" fill="none" stroke="{oscurecer(color, 0.3)}" stroke-width="2"/>'
            f'<path d="{banda}" fill="#F4ECD8" opacity="0.9"/>')


def pila(x, y, cols, filas, capas, color, w=110, visibles=None, seed=1):
    """Pila de fajos (cols × filas × capas). visibles limita cuántos se dibujan (para animar)."""
    r = random.Random(seed)
    d = w * 0.42
    out = []
    n = 0
    tot = cols * filas * capas
    vis = tot if visibles is None else int(visibles)
    for c in range(capas):
        for fi in range(filas - 1, -1, -1):
            for co in range(cols):
                if n >= vis:
                    return "".join(out)
                xx = x + co * (w + 2) + fi * d * 0.6 + r.uniform(-3, 3)
                yy = y - c * w * 0.185 - fi * d * 0.45
                out.append(fajo(xx, yy, w, color))
                n += 1
    return "".join(out)


def billete(x, y, w, valor, moneda, color, rot=0.0, sello=None, k_texto=1.0, emblema=True):
    h = w * 0.46
    gu = []
    for j in range(7):
        amp = h * 0.035 + j * 1.5
        pts = " ".join(f"L{f(-w * 0.42 + i * w * 0.84 / 40)} {f(-h * 0.3 + j * h * 0.1 + amp * math.sin(i * 0.5 + j))}" for i in range(41))
        gu.append(f'<path d="M{f(-w * 0.42)} {f(-h * 0.3 + j * h * 0.1)} {pts}" fill="none" stroke="#000" stroke-opacity="0.10" stroke-width="1.5"/>')
    fs = min(h * 0.26, w * 0.85 / max(1, len(valor) * 0.6)) * k_texto
    ros = "".join(f'<ellipse rx="{f(h * 0.2)}" ry="{f(h * 0.07)}" fill="none" stroke="#000" stroke-opacity="0.25" stroke-width="2" transform="rotate({a})"/>' for a in range(0, 180, 30))
    s = (f'<g transform="translate({f(x)} {f(y)}) rotate({f(rot)})">'
         f'<rect x="{f(-w / 2 + 8)}" y="{f(-h / 2 + 10)}" width="{f(w)}" height="{f(h)}" rx="8" fill="#000" opacity="0.30"/>'
         f'<rect x="{f(-w / 2)}" y="{f(-h / 2)}" width="{f(w)}" height="{f(h)}" rx="8" fill="{color}"/>'
         f'<rect x="{f(-w / 2 + w * 0.025)}" y="{f(-h / 2 + w * 0.025)}" width="{f(w * 0.95)}" height="{f(h - w * 0.05)}" rx="5" fill="none" stroke="#000" stroke-opacity="0.4" stroke-width="3"/>'
         + "".join(gu))
    if emblema:
        s += f'<g transform="translate({f(-w * 0.3)} {f(-h * 0.05)})">{ros}</g>'
        s += f'<circle cx="{f(w * 0.3)}" cy="{f(-h * 0.05)}" r="{f(h * 0.24)}" fill="#FFFFFF" opacity="0.35"/><circle cx="{f(w * 0.3)}" cy="{f(-h * 0.05)}" r="{f(h * 0.24)}" fill="none" stroke="#000" stroke-opacity="0.25" stroke-width="2"/>'
    s += (f'<text x="0" y="{f(-h * 0.3)}" text-anchor="middle" font-family="{FUENTE}" font-weight="900" font-size="{f(min(h * 0.1, w * 0.8 / max(1, len(moneda) * 0.8)))}" fill="#1B1B1B" opacity="0.8" letter-spacing="{f(h * 0.02)}">{moneda}</text>'
          f'<text x="0" y="{f(h * 0.12 + fs * 0.35)}" text-anchor="middle" font-family="{FUENTE}" font-weight="900" font-size="{f(fs)}" fill="#141414">{valor}</text>')
    if sello:
        s += (f'<g transform="translate({f(w * 0.22)} {f(h * 0.22)}) rotate(-14)"><rect x="{f(-w * 0.2)}" y="{f(-h * 0.1)}" width="{f(w * 0.4)}" height="{f(h * 0.2)}" rx="6" fill="none" stroke="#B3261E" stroke-width="5"/>'
              f'<text x="0" y="{f(h * 0.045)}" text-anchor="middle" font-family="{FUENTE}" font-weight="900" font-size="{f(h * 0.11)}" fill="#B3261E">{sello}</text></g>')
    return s + '</g>'


def lluvia_billetes(t, color, n=40, seed=3, y0=-200, vel=260):
    r = random.Random(seed)
    s = []
    for _ in range(n):
        x = r.uniform(-50, 1970)
        sp = r.uniform(0.7, 1.3) * vel
        y = (r.uniform(-1200, 0) + t * sp) % 1400 + y0
        rot = r.uniform(0, 360) + t * r.uniform(-90, 90)
        sk = 1 + 0.6 * math.sin(t * 3 + x)
        s.append(f'<g transform="translate({f(x)} {f(y)}) rotate({f(rot)}) scale({sk:.2f} 1)"><rect x="-55" y="-25" width="110" height="50" rx="4" fill="{color}" stroke="{oscurecer(color, 0.35)}" stroke-width="2"/>'
                 f'<circle r="12" fill="none" stroke="{oscurecer(color, 0.35)}" stroke-width="2"/></g>')
    return "".join(s)


def carretilla(x, y, k=1.0, color="#C9B98E", lleno=1.0):
    s = [f'<g transform="translate({f(x)} {f(y)}) scale({k:.3f})">']
    s.append('<ellipse cx="0" cy="4" rx="150" ry="14" fill="#000" opacity="0.2"/>')
    s.append('<circle cx="-110" cy="-38" r="38" fill="#2B2B2B"/><circle cx="-110" cy="-38" r="16" fill="#777"/>')
    s.append('<path d="M-170 -150 L 120 -150 L 70 -60 L -140 -60 Z" fill="#5B6B73"/><path d="M-170 -150 L 120 -150 L 112 -136 L -165 -136 Z" fill="#7C8E96"/>')
    s.append('<path d="M60 -80 L 180 -30 M 70 -100 L 190 -50" stroke="#6B4A2E" stroke-width="12" stroke-linecap="round"/>')
    s.append('<path d="M-60 -60 L -40 0 M 30 -60 L 20 0" stroke="#4A4A4A" stroke-width="10"/>')
    if lleno > 0:
        n = int(14 * lleno)
        r = random.Random(4)
        for i in range(n):
            fx = -160 + (i % 5) * 52 + r.uniform(-6, 6)
            fy = -150 - (i // 5) * 20 - r.uniform(0, 8)
            s.append(fajo(fx, fy, 62, color))
    s.append('</g>')
    return "".join(s)


def saco_dinero(x, y, k=1.0, color="#C2A266", simbolo="$"):
    return (f'<g transform="translate({f(x)} {f(y)}) scale({k:.3f})"><ellipse cx="0" cy="2" rx="70" ry="10" fill="#000" opacity="0.2"/>'
            f'<path d="M-60 0 Q -80 -90 -30 -120 L -22 -140 Q 0 -150 22 -140 L 30 -120 Q 80 -90 60 0 Z" fill="{color}"/>'
            f'<path d="M20 -125 Q 78 -88 60 0 L 30 0 Q 50 -70 10 -120 Z" fill="#000" opacity="0.15"/>'
            f'<path d="M-30 -126 Q 0 -112 30 -126" stroke="{oscurecer(color, 0.4)}" stroke-width="7" fill="none"/>'
            f'<text x="0" y="-38" text-anchor="middle" font-family="{FUENTE}" font-weight="900" font-size="58" fill="{oscurecer(color, 0.45)}">{simbolo}</text></g>')


def pan(x, y, k=1.0):
    return (f'<g transform="translate({f(x)} {f(y)}) scale({k:.3f})"><ellipse cx="0" cy="6" rx="78" ry="12" fill="#000" opacity="0.2"/>'
            '<path d="M-80 0 Q -84 -60 0 -62 Q 84 -60 80 0 Z" fill="#D69A4E"/><path d="M-80 0 Q -84 -60 0 -62 Q 30 -60 50 -50 Q 0 -40 -40 0 Z" fill="#E8B46A"/>'
            '<path d="M-40 -48 q 12 18 2 36 M0 -56 q 12 22 2 44 M40 -48 q 12 18 2 36" stroke="#9C6428" stroke-width="7" fill="none" stroke-linecap="round"/></g>')


def etiqueta_precio(x, y, texto, k=1.0, color="#FFF6D6", rot=-6, tinta="#B3261E"):
    w = max(150, len(texto) * 30 + 60)
    return (f'<g transform="translate({f(x)} {f(y)}) rotate({rot}) scale({k:.3f})">'
            f'<path d="M0 0 L 34 -40 H{w} V40 H34 Z" fill="{color}" stroke="#3A3A3A" stroke-width="4"/>'
            f'<circle cx="34" cy="0" r="9" fill="#3A3A3A"/>'
            f'<text x="{f(34 + (w - 34) / 2 + 8)}" y="16" text-anchor="middle" font-family="{FUENTE}" font-weight="900" font-size="44" fill="{tinta}">{texto}</text></g>')


# ---------------------------------------------------------------- escenarios
def cielo(era, t=0.0, nubes=True, sol=(1500, 260)):
    E = ERAS[era]
    s = [f'<defs><linearGradient id="cielo_{era}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{E["cielo"][1]}"/><stop offset="1" stop-color="{E["cielo"][0]}"/></linearGradient></defs>',
         f'<rect width="1920" height="1080" fill="url(#cielo_{era})"/>']
    if sol:
        s.append(f'<circle cx="{sol[0]}" cy="{sol[1]}" r="190" fill="{E["sol"]}" opacity="0.25"/><circle cx="{sol[0]}" cy="{sol[1]}" r="90" fill="{E["sol"]}" opacity="0.9"/>')
    if nubes:
        r = random.Random(11)
        for i in range(5):
            x = (r.uniform(0, 2200) + t * r.uniform(8, 18)) % 2300 - 200
            y = r.uniform(90, 330)
            k = r.uniform(0.7, 1.4)
            s.append(f'<g transform="translate({f(x)} {f(y)}) scale({k:.2f})" fill="#FFFFFF" opacity="0.55"><ellipse rx="110" ry="34"/><ellipse cx="-50" cy="-20" rx="60" ry="40"/><ellipse cx="40" cy="-28" rx="70" ry="48"/></g>')
    return "".join(s)


def edificio(x, base, w, h, color, seed, era, ventanas_luz=0.2):
    r = random.Random(seed)
    s = [f'<rect x="{f(x)}" y="{f(base - h)}" width="{f(w)}" height="{f(h)}" fill="{color}"/>',
         f'<rect x="{f(x + w * 0.75)}" y="{f(base - h)}" width="{f(w * 0.25)}" height="{f(h)}" fill="#000" opacity="0.10"/>']
    if era in ("1920", "1940"):
        s.append(f'<rect x="{f(x - 8)}" y="{f(base - h - 14)}" width="{f(w + 16)}" height="18" fill="{oscurecer(color, 0.25)}"/>')
        s.append(f'<path d="M{f(x - 4)} {f(base - h - 14)} L{f(x + w / 2)} {f(base - h - 14 - w * 0.18)} L{f(x + w + 4)} {f(base - h - 14)} Z" fill="{oscurecer(color, 0.35)}"/>' if r.random() < 0.4 else "")
    else:
        s.append(f'<rect x="{f(x - 4)}" y="{f(base - h - 8)}" width="{f(w + 8)}" height="10" fill="{oscurecer(color, 0.2)}"/>')
    cols = max(2, int(w / 70))
    filas = max(2, int((h - 120) / 90))
    vw = w / cols * 0.5
    for fi in range(filas):
        for co in range(cols):
            vx = x + (co + 0.25) * w / cols
            vy = base - h + 40 + fi * 90
            luz = r.random() < ventanas_luz
            s.append(f'<rect x="{f(vx)}" y="{f(vy)}" width="{f(vw)}" height="56" fill="{"#F6D98B" if luz else "#2F3A44"}" opacity="{0.95 if luz else 0.75}"/>'
                     f'<rect x="{f(vx - 4)}" y="{f(vy + 56)}" width="{f(vw + 8)}" height="6" fill="{oscurecer(color, 0.3)}"/>')
    return "".join(s)


def calle(era, t=0.0, base=820, seed=5, densidad=1.0, lejos=True):
    E = ERAS[era]
    r = random.Random(seed)
    s = [cielo(era, t)]
    if lejos:
        x = -40
        while x < 1960:
            w = r.uniform(140, 260)
            h = r.uniform(380, 620)
            s.append(f'<rect x="{f(x)}" y="{f(base - 80 - h)}" width="{f(w)}" height="{f(h)}" fill="{mezclar(r.choice(E["fachada"]), E["cielo"][0], 0.55)}"/>')
            x += w + r.uniform(-10, 10)
    x = -60
    while x < 1980:
        w = r.uniform(230, 360) * densidad
        h = r.uniform(330, 520)
        s.append(edificio(x, base, w, h, r.choice(E["fachada"]), r.randint(0, 999), era))
        x += w
    s.append(f'<rect x="0" y="{base}" width="1920" height="{1080 - base}" fill="{E["suelo"]}"/>')
    s.append(f'<rect x="0" y="{base}" width="1920" height="40" fill="{E["acera"]}"/><rect x="0" y="{base + 40}" width="1920" height="8" fill="#000" opacity="0.15"/>')
    if era in ("1920", "1940"):
        for lx in (300, 1000, 1700):
            s.append(f'<path d="M{lx} {base} V{base - 330}" stroke="#2A2A2A" stroke-width="10"/><path d="M{lx - 26} {base - 330} h52 l-10 -40 h-32 Z" fill="#2A2A2A"/><circle cx="{lx}" cy="{base - 352}" r="12" fill="#F6D98B"/>')
    return "".join(s)


def tienda(x, base, w, h, nombre, color, toldo=("#C0392B", "#F4ECD8"), era="1980", interior=None):
    s = [f'<rect x="{f(x)}" y="{f(base - h)}" width="{f(w)}" height="{f(h)}" fill="{color}"/>',
         f'<rect x="{f(x + 30)}" y="{f(base - h * 0.62)}" width="{f(w * 0.55)}" height="{f(h * 0.5)}" fill="#3B4A55"/>',
         f'<rect x="{f(x + 30)}" y="{f(base - h * 0.62)}" width="{f(w * 0.55)}" height="{f(h * 0.5)}" fill="#BFD7E3" opacity="0.25"/>',
         f'<rect x="{f(x + w * 0.66)}" y="{f(base - h * 0.62)}" width="{f(w * 0.26)}" height="{f(h * 0.62)}" fill="{oscurecer(color, 0.5)}"/>']
    if interior:
        s.append(interior)
    n = 9
    tw = w / n
    for i in range(n):
        s.append(f'<path d="M{f(x + i * tw)} {f(base - h * 0.72)} h{f(tw)} l{f(-tw * 0.1)} 60 h{f(-tw * 0.8)} Z" fill="{toldo[i % 2]}"/>')
        s.append(f'<path d="M{f(x + i * tw + tw * 0.1)} {f(base - h * 0.72 + 60)} a{f(tw * 0.4)} 16 0 0 0 {f(tw * 0.8)} 0" fill="{toldo[i % 2]}"/>')
    s.append(f'<rect x="{f(x + w * 0.1)}" y="{f(base - h + 20)}" width="{f(w * 0.8)}" height="{f(h * 0.18)}" rx="8" fill="#2B2420"/>')
    s.append(f'<text x="{f(x + w / 2)}" y="{f(base - h + 20 + h * 0.13)}" text-anchor="middle" font-family="{FUENTE}" font-weight="900" font-size="{f(h * 0.1)}" fill="#F6D98B" letter-spacing="6">{nombre}</text>')
    return "".join(s)


def estante(x, y, w, filas, seed, vacio=0.0, precios=None):
    """Estantería de supermercado con productos genéricos."""
    r = random.Random(seed)
    cols = ["#E63946", "#F1C40F", "#2A9D8F", "#F4A261", "#457B9D", "#8E44AD", "#FFFFFF", "#E76F51"]
    s = [f'<rect x="{f(x)}" y="{f(y - filas * 150 - 30)}" width="{f(w)}" height="{f(filas * 150 + 30)}" fill="#D7DCE0"/>',
         f'<rect x="{f(x)}" y="{f(y - filas * 150 - 30)}" width="{f(w)}" height="{f(filas * 150 + 30)}" fill="none" stroke="#9AA3AA" stroke-width="8"/>']
    for fi in range(filas):
        yy = y - fi * 150
        s.append(f'<rect x="{f(x)}" y="{f(yy - 14)}" width="{f(w)}" height="16" fill="#8F99A1"/>')
        xx = x + 16
        while xx < x + w - 60:
            pw = r.uniform(40, 70)
            ph = r.uniform(70, 120)
            if r.random() > vacio:
                c = r.choice(cols)
                if r.random() < 0.5:
                    s.append(f'<rect x="{f(xx)}" y="{f(yy - 14 - ph)}" width="{f(pw)}" height="{f(ph)}" rx="4" fill="{c}"/><rect x="{f(xx)}" y="{f(yy - 14 - ph * 0.6)}" width="{f(pw)}" height="{f(ph * 0.25)}" fill="#FFFFFF" opacity="0.6"/>')
                else:
                    s.append(f'<rect x="{f(xx)}" y="{f(yy - 14 - ph * 0.8)}" width="{f(pw * 0.8)}" height="{f(ph * 0.8)}" rx="10" fill="{c}"/><rect x="{f(xx)}" y="{f(yy - 14 - ph * 0.8)}" width="{f(pw * 0.8)}" height="10" rx="4" fill="#BBB"/>')
            xx += pw + 6
        if precios:
            for j, p in enumerate(precios[fi % len(precios)]):
                px = x + 40 + j * (w - 80) / max(1, len(precios[fi % len(precios)]))
                s.append(f'<rect x="{f(px)}" y="{f(yy - 12)}" width="120" height="34" fill="#FFF7C2" stroke="#555" stroke-width="2"/>'
                         f'<text x="{f(px + 60)}" y="{f(yy + 14)}" text-anchor="middle" font-family="{FUENTE}" font-weight="900" font-size="22" fill="#B3261E">{p}</text>')
    return "".join(s)


def puesto_mercado(x, base, w, color_toldo, seed, productos="papas"):
    r = random.Random(seed)
    s = [f'<path d="M{f(x)} {f(base)} V{f(base - 330)} M{f(x + w)} {f(base)} V{f(base - 330)}" stroke="#5A4630" stroke-width="12"/>',
         f'<path d="M{f(x - 30)} {f(base - 330)} L{f(x + w + 30)} {f(base - 330)} L{f(x + w)} {f(base - 400)} L{f(x)} {f(base - 400)} Z" fill="{color_toldo}"/>',
         f'<path d="M{f(x - 30)} {f(base - 330)} L{f(x + w + 30)} {f(base - 330)} L{f(x + w + 30)} {f(base - 316)} L{f(x - 30)} {f(base - 316)} Z" fill="{oscurecer(color_toldo, 0.3)}"/>',
         f'<rect x="{f(x - 10)}" y="{f(base - 150)}" width="{f(w + 20)}" height="150" fill="#8A6A48"/><rect x="{f(x - 10)}" y="{f(base - 150)}" width="{f(w + 20)}" height="14" fill="#A8845C"/>']
    pal = {"papas": ["#B08850", "#C49A60", "#9A7440"], "frutas": ["#E63946", "#F4A261", "#F1C40F", "#2A9D8F"], "verduras": ["#4C9A2A", "#76B041", "#E76F51"]}[productos]
    for i in range(int(w / 26) * 3):
        px = x + r.uniform(0, w)
        py = base - 152 - abs(r.gauss(0, 18)) * (1 - abs(px - x - w / 2) / (w / 2 + 1)) * 2
        s.append(f'<circle cx="{f(px)}" cy="{f(py)}" r="{f(r.uniform(12, 18))}" fill="{r.choice(pal)}"/>')
    return "".join(s)


def imprenta(x, y, t, k=1.0, color_billete="#C9B98E", activa=True, cadena=0.0):
    """Rotativa industrial con pliego de billetes saliendo."""
    s = [f'<g transform="translate({f(x)} {f(y)}) scale({k:.3f})">']
    s.append('<ellipse cx="0" cy="6" rx="420" ry="26" fill="#000" opacity="0.25"/>')
    s.append('<rect x="-380" y="-360" width="520" height="360" rx="20" fill="#3E4A52"/><rect x="-380" y="-360" width="520" height="40" rx="12" fill="#56646D"/>')
    s.append('<rect x="-360" y="-300" width="140" height="220" rx="10" fill="#2F3940"/><rect x="-200" y="-300" width="320" height="120" rx="10" fill="#2F3940"/>')
    vel = t * (240 if activa else 0)
    for i, (cx, cy, r) in enumerate(((-290, -190, 58), (-60, -240, 46), (60, -240, 46), (-60, -120, 30), (60, -120, 30))):
        s.append(f'<g transform="translate({cx} {cy}) rotate({f(vel * (1 if i % 2 else -1))})"><circle r="{r}" fill="#8C9AA3"/><circle r="{r * 0.35}" fill="#3E4A52"/>'
                 + "".join(f'<rect x="-4" y="{-r}" width="8" height="{r * 0.5}" fill="#3E4A52" transform="rotate({a})"/>' for a in range(0, 360, 60)) + '</g>')
    s.append('<rect x="140" y="-150" width="60" height="150" fill="#56646D"/>')
    # pliego de billetes que sale
    off = (t * (260 if activa else 0)) % 120
    hoja = [f'<path d="M180 -110 Q 300 -110 330 -40 L 600 -40" stroke="{color_billete}" stroke-width="64" fill="none"/>']
    for i in range(-1, 4):
        bx = 340 + i * 120 + off
        if bx < 600:
            hoja.append(f'<rect x="{f(bx)}" y="-66" width="100" height="52" rx="3" fill="none" stroke="{oscurecer(color_billete, 0.35)}" stroke-width="3"/><circle cx="{f(bx + 50)}" cy="-40" r="12" fill="none" stroke="{oscurecer(color_billete, 0.35)}" stroke-width="2"/>')
    s.append("".join(hoja))
    s.append('<rect x="560" y="-40" width="160" height="40" fill="#56646D"/>')
    altura = int(min(12, (t * 2.5 if activa else 6)))
    for j in range(altura):
        s.append(fajo(575, -40 - j * 21, 120, color_billete))
    if activa:
        for j in range(3):
            fy = -380 - ((t * 60 + j * 40) % 120)
            s.append(f'<circle cx="{-300 + j * 30}" cy="{f(fy)}" r="{f(18 + j * 6)}" fill="#C8CDD0" opacity="{0.5 - j * 0.12:.2f}"/>')
    if cadena > 0:
        p = c01(cadena)
        s.append(f'<g opacity="{p:.2f}">' + "".join(f'<ellipse cx="{-380 + i * 40}" cy="{-200 + 50 * math.sin(i / 13 * math.pi)}" rx="22" ry="12" fill="none" stroke="#B0B6BA" stroke-width="8" transform="rotate({20 if i % 2 else -20} {-380 + i * 40} {-200 + 50 * math.sin(i / 13 * math.pi)})"/>' for i in range(14))
                 + f'<g transform="translate(-120 {f(-130 - 30 * (1 - ease_out(p)))})"><rect x="-60" y="-10" width="120" height="100" rx="14" fill="#E0A100"/><path d="M-36 -10 v-30 a36 36 0 0 1 72 0 v30" stroke="#B0B6BA" stroke-width="16" fill="none"/><circle cx="0" cy="34" r="12" fill="#5A4300"/><rect x="-5" y="34" width="10" height="30" fill="#5A4300"/></g></g>')
    s.append('</g>')
    return "".join(s)


def fabrica(x, base, w, t, color="#8C6B55", humo=True, apagada=False):
    s = [f'<rect x="{f(x)}" y="{f(base - 300)}" width="{f(w)}" height="300" fill="{color}"/>']
    n = 4
    for i in range(n):
        sx = x + i * w / n
        s.append(f'<path d="M{f(sx)} {f(base - 300)} l{f(w / n)} -90 v90 Z" fill="{oscurecer(color, 0.2)}"/>')
    for i, cx in enumerate((x + w * 0.15, x + w * 0.45, x + w * 0.8)):
        s.append(f'<rect x="{f(cx - 22)}" y="{f(base - 560)}" width="44" height="260" fill="{oscurecer(color, 0.35)}"/><rect x="{f(cx - 26)}" y="{f(base - 570)}" width="52" height="16" fill="{oscurecer(color, 0.5)}"/>')
        if humo and not apagada:
            for j in range(5):
                q = ((t * 0.35 + j * 0.2 + i * 0.13) % 1)
                s.append(f'<circle cx="{f(cx + q * 120)}" cy="{f(base - 590 - q * 260)}" r="{f(24 + q * 60)}" fill="#9A9A9A" opacity="{0.55 * (1 - q):.2f}"/>')
    for i in range(int(w / 90)):
        s.append(f'<rect x="{f(x + 30 + i * 90)}" y="{f(base - 200)}" width="50" height="70" fill="{"#3A4048" if apagada else "#F6D98B"}" opacity="0.85"/>')
    return "".join(s)


def soldado(x, y, k=1.0, t=0.0, seed=0, color="#5B6146"):
    casco = (f'<path d="M-28 -298 Q 0 -340 28 -298 Z" fill="{oscurecer(color, 0.25)}"/><rect x="-34" y="-300" width="68" height="8" rx="3" fill="{oscurecer(color, 0.35)}"/>')
    fusil = '<path d="M30 -250 L 60 -330" stroke="#3A2A1A" stroke-width="8" stroke-linecap="round"/>'
    return persona(x, y, 300 * k, seed, t, "pie", "1920", 1, ropa=color, carga=casco + fusil)


def ruinas(t, base=860, era="1940"):
    r = random.Random(9)
    s = [cielo(era, t, nubes=False, sol=(1500, 300))]
    x = -40
    while x < 1960:
        w = r.uniform(160, 300)
        h = r.uniform(260, 520)
        c = mezclar(r.choice(ERAS[era]["fachada"]), "#3A3A3A", 0.25)
        pts = [(x, base), (x, base - h)]
        for j in range(5):
            pts.append((x + w * (j + 1) / 6, base - h + r.uniform(-20, 160)))
        pts += [(x + w, base - h * r.uniform(0.3, 0.8)), (x + w, base)]
        s.append(f'<path d="M' + " L".join(f"{f(a)} {f(b)}" for a, b in pts) + f' Z" fill="{c}"/>')
        for j in range(int(w / 60)):
            for i in range(int(h / 110)):
                vy = base - h + 60 + i * 100
                if vy < base - 40:
                    s.append(f'<rect x="{f(x + 20 + j * 60)}" y="{f(vy)}" width="30" height="46" fill="#1E1E1E" opacity="0.8"/>')
        x += w + r.uniform(20, 60)
    # río y puente roto
    s.append(f'<rect x="0" y="{base}" width="1920" height="{1080 - base}" fill="#5E6E78"/>')
    s.append(f'<path d="M0 {base + 30} H1920" stroke="#8FA3AE" stroke-width="4" opacity="0.5"/>')
    s.append(f'<path d="M200 {base - 40} L 820 {base - 40} L 860 {base + 30} M 1080 {base + 40} L 1120 {base - 40} L 1720 {base - 40}" stroke="#3E3A36" stroke-width="30" fill="none"/>')
    for px in (420, 640, 1300, 1500):
        s.append(f'<rect x="{px - 20}" y="{base - 40}" width="40" height="{1080 - base + 40}" fill="#3E3A36"/>')
    for i in range(4):
        q = (t * 0.2 + i * 0.25) % 1
        cx = 300 + i * 420
        s.append(f'<circle cx="{f(cx + q * 80)}" cy="{f(base - 380 - q * 300)}" r="{f(50 + q * 100)}" fill="#4A4A4A" opacity="{0.5 * (1 - q):.2f}"/>')
    return "".join(s)


def mina(t, base=860):
    s = [cielo("1980", t, sol=(1600, 220))]
    s.append(f'<path d="M-50 {base} L 300 360 L 520 520 L 820 260 L 1180 {base} Z" fill="#8C6E58"/><path d="M820 260 L 1180 {base} L 900 {base} Z" fill="#000" opacity="0.15"/>')
    s.append(f'<path d="M900 {base} L 1300 300 L 1600 480 L 1980 380 L 1980 {base} Z" fill="#7A604C"/>')
    s.append(f'<path d="M380 {base} V {base - 200} Q 470 {base - 300} 560 {base - 200} V {base} Z" fill="#2A1E16"/><path d="M370 {base} V {base - 210} Q 470 {base - 320} 570 {base - 210} V {base}" stroke="#6B4A2E" stroke-width="24" fill="none"/>')
    s.append(f'<rect x="0" y="{base}" width="1920" height="{1080 - base}" fill="#A68B6E"/>')
    s.append(f'<path d="M470 {base} L 1300 1080 M 520 {base} L 1420 1080" stroke="#555" stroke-width="8"/>')
    for i in range(8):
        yy = base + i * 28
        s.append(f'<path d="M{f(480 + i * 105)} {f(yy)} h 80" stroke="#6B4A2E" stroke-width="10"/>')
    s.append(f'<g transform="translate(800 {base + 70})"><path d="M-80 0 L -100 -90 H 100 L 80 0 Z" fill="#6E7B83"/><circle cx="-50" cy="6" r="18" fill="#333"/><circle cx="50" cy="6" r="18" fill="#333"/>'
             '<path d="M-90 -90 Q -40 -130 0 -96 Q 40 -140 90 -90 Z" fill="#8F8F8F"/></g>')
    return "".join(s)


def minero(x, y, k, t, seed, pose="camina", triste=True):
    casco = '<path d="M-30 -312 Q 3 -356 34 -312 Z" fill="#F1C40F"/><rect x="-36" y="-316" width="74" height="8" rx="3" fill="#C9A20C"/><circle cx="18" cy="-330" r="7" fill="#FFF7C2"/>'
    return persona(x, y, 300 * k, seed, t, pose, "1980", 1, ropa=random.Random(seed).choice(["#3D5A80", "#5C677D", "#6B4F3A", "#4A4E69"]), carga=casco, triste=triste)


def bomba_petroleo(x, base, t, k=1.0, fase=0.0):
    a = 18 * math.sin(t * 2.2 + fase)
    return (f'<g transform="translate({f(x)} {f(base)}) scale({k:.3f})"><rect x="-120" y="-20" width="300" height="20" fill="#2B2B2B"/>'
            f'<path d="M-40 -20 L 0 -230 L 40 -20 Z" fill="none" stroke="#2B2B2B" stroke-width="16"/>'
            f'<g transform="translate(0 -230) rotate({f(a)})"><rect x="-190" y="-16" width="330" height="32" rx="6" fill="#E0A100"/>'
            f'<path d="M140 -16 Q 200 0 140 50 Z" fill="#2B2B2B"/><rect x="-200" y="-10" width="40" height="70" fill="#2B2B2B"/></g>'
            f'<path d="M150 -20 V {f(-180 + 30 * math.sin(t * 2.2 + fase))}" stroke="#555" stroke-width="6"/></g>')


def campo_seco(t, base=760):
    s = [cielo("2010", t, sol=(1550, 230))]
    s.append(f'<path d="M0 {base - 60} Q 500 {base - 120} 1000 {base - 70} T 1920 {base - 90} V 1080 H 0 Z" fill="#C9A86A"/>')
    for i in range(16):
        y = base - 40 + i * 22
        s.append(f'<path d="M0 {y} Q 960 {y - 10} 1920 {y + 6}" stroke="#A88A50" stroke-width="5" fill="none"/>')
    r = random.Random(8)
    for i in range(40):
        x = r.uniform(0, 1920)
        y = r.uniform(base, 1060)
        s.append(f'<path d="M{f(x)} {f(y)} q -6 -26 -14 -34 M{f(x)} {f(y)} q 4 -30 12 -36" stroke="#8A7A3A" stroke-width="4" fill="none"/>')
    s.append(f'<path d="M500 {base + 120} l 40 -60 l 30 50 l 50 -30" stroke="#6B5A30" stroke-width="5" fill="none"/>')
    # tractor parado
    s.append(f'<g transform="translate(1300 {base + 150})"><rect x="-120" y="-150" width="200" height="90" rx="10" fill="#B3261E"/><rect x="-60" y="-240" width="110" height="100" fill="#8C1E18"/>'
             '<rect x="-48" y="-228" width="86" height="60" fill="#BFD7E3" opacity="0.6"/><circle cx="-70" cy="-40" r="60" fill="#2B2B2B"/><circle cx="-70" cy="-40" r="26" fill="#777"/>'
             '<circle cx="60" cy="-30" r="38" fill="#2B2B2B"/><circle cx="60" cy="-30" r="15" fill="#777"/></g>')
    return "".join(s)


def banco_central(x, base, w, h, t, color="#E8E0CC", bandera=None):
    s = [f'<rect x="{f(x)}" y="{f(base - 40)}" width="{f(w)}" height="40" fill="{oscurecer(color, 0.2)}"/>',
         f'<rect x="{f(x + 20)}" y="{f(base - h)}" width="{f(w - 40)}" height="{f(h - 40)}" fill="{color}"/>',
         f'<path d="M{f(x)} {f(base - h)} L{f(x + w / 2)} {f(base - h - h * 0.3)} L{f(x + w)} {f(base - h)} Z" fill="{oscurecer(color, 0.08)}"/>',
         f'<path d="M{f(x + 40)} {f(base - h - 10)} L{f(x + w / 2)} {f(base - h - h * 0.24)} L{f(x + w - 40)} {f(base - h - 10)} Z" fill="{oscurecer(color, 0.18)}"/>',
         f'<rect x="{f(x)}" y="{f(base - h - 10)}" width="{f(w)}" height="26" fill="{oscurecer(color, 0.12)}"/>']
    n = 6
    for i in range(n):
        cx = x + 60 + i * (w - 120) / (n - 1)
        s.append(f'<rect x="{f(cx - 22)}" y="{f(base - h + 20)}" width="44" height="{f(h - 60)}" fill="{aclarar(color, 0.3)}"/><rect x="{f(cx + 6)}" y="{f(base - h + 20)}" width="16" height="{f(h - 60)}" fill="#000" opacity="0.08"/>')
    s.append(f'<text x="{f(x + w / 2)}" y="{f(base - h + 8)}" text-anchor="middle" font-family="Liberation Serif, serif" font-weight="700" font-size="{f(h * 0.06)}" fill="{oscurecer(color, 0.6)}" letter-spacing="8">BANCO CENTRAL</text>')
    if bandera:
        fx, fy = x + w / 2, base - h - h * 0.3
        s.append(f'<path d="M{f(fx)} {f(fy)} V{f(fy - 160)}" stroke="#555" stroke-width="6"/>')
        ond = "".join(f"L{f(fx + i * 12)} {f(fy - 160 + 6 * math.sin(t * 4 + i * 0.6))} " for i in range(13))
        s.append(f'<path d="M{f(fx)} {f(fy - 160)} {ond} L{f(fx + 144)} {f(fy - 80 + 6 * math.sin(t * 4 + 7.2))} L{f(fx)} {f(fy - 80)} Z" fill="{bandera}"/>')
    return "".join(s)


def reloj(x, y, r, t, vel=1.0, color="#F4ECD8"):
    s = [f'<circle cx="{f(x)}" cy="{f(y)}" r="{f(r + 18)}" fill="#5A3E28"/><circle cx="{f(x)}" cy="{f(y)}" r="{f(r)}" fill="{color}"/>']
    for i in range(12):
        a = math.radians(i * 30)
        s.append(f'<path d="M{f(x + math.sin(a) * r * 0.82)} {f(y - math.cos(a) * r * 0.82)} L{f(x + math.sin(a) * r * 0.94)} {f(y - math.cos(a) * r * 0.94)}" stroke="#2B2B2B" stroke-width="{8 if i % 3 == 0 else 4}"/>')
    am = t * 360 * vel
    ah = am / 12
    for a, l, wd in ((ah, 0.5, 14), (am, 0.78, 8)):
        ra = math.radians(a)
        s.append(f'<path d="M{f(x)} {f(y)} L{f(x + math.sin(ra) * r * l)} {f(y - math.cos(ra) * r * l)}" stroke="#2B2B2B" stroke-width="{wd}" stroke-linecap="round"/>')
    s.append(f'<circle cx="{f(x)}" cy="{f(y)}" r="12" fill="#B3261E"/>')
    return "".join(s)


def bascula(x, base, t, izq, der, inclina=0.0):
    a = inclina * 12
    s = [f'<path d="M{f(x)} {f(base)} V{f(base - 380)}" stroke="#5A4630" stroke-width="22"/><path d="M{f(x - 120)} {f(base)} h240" stroke="#5A4630" stroke-width="26" stroke-linecap="round"/>']
    s.append(f'<g transform="rotate({f(a)} {f(x)} {f(base - 380)})"><path d="M{f(x - 360)} {f(base - 380)} H{f(x + 360)}" stroke="#7A5E40" stroke-width="18" stroke-linecap="round"/>')
    for lado, cont in ((-1, izq), (1, der)):
        px = x + lado * 340
        s.append(f'<g transform="rotate({f(-a)} {f(px)} {f(base - 380)})"><path d="M{f(px)} {f(base - 380)} L{f(px - 120)} {f(base - 220)} M{f(px)} {f(base - 380)} L{f(px + 120)} {f(base - 220)}" stroke="#555" stroke-width="4"/>'
                 f'<path d="M{f(px - 150)} {f(base - 220)} Q {f(px)} {f(base - 160)} {f(px + 150)} {f(base - 220)} Z" fill="#B08D57"/>'
                 f'<g transform="translate({f(px)} {f(base - 220)})">{cont}</g></g>')
    s.append(f'</g><circle cx="{f(x)}" cy="{f(base - 380)}" r="18" fill="#3A2A1A"/>')
    return "".join(s)


def pollo(x, y, k=1.0):
    return (f'<g transform="translate({f(x)} {f(y)}) scale({k:.3f})"><ellipse cx="0" cy="-50" rx="95" ry="58" fill="#F2C49B"/><ellipse cx="-20" cy="-70" rx="60" ry="26" fill="#F8D9BC"/>'
            '<path d="M70 -60 q 50 -20 60 10 q -10 20 -40 14 Z M -80 -50 q -50 -30 -60 0 q 10 22 40 16 Z" fill="#E8B48A"/>'
            '<circle cx="134" cy="-46" r="12" fill="#FFF"/><circle cx="-144" cy="-38" r="12" fill="#FFF"/></g>')


def documento(x, y, w, h, titulo, lineas, t, firma=0.0, sello=0.0, rot=-3):
    s = [f'<g transform="translate({f(x)} {f(y)}) rotate({rot})"><rect x="{f(-w / 2 + 12)}" y="{f(-h / 2 + 14)}" width="{f(w)}" height="{f(h)}" fill="#000" opacity="0.25"/>'
         f'<rect x="{f(-w / 2)}" y="{f(-h / 2)}" width="{f(w)}" height="{f(h)}" fill="#F5EEDC"/>',
         f'<text x="0" y="{f(-h / 2 + 90)}" text-anchor="middle" font-family="Liberation Serif, serif" font-weight="700" font-size="52" fill="#2B2B2B">{titulo}</text>']
    for i, ln in enumerate(lineas):
        s.append(f'<text x="{f(-w / 2 + 60)}" y="{f(-h / 2 + 170 + i * 52)}" font-family="Liberation Serif, serif" font-size="34" fill="#3A3A3A">{ln}</text>')
    for i in range(6):
        yy = -h / 2 + 170 + len(lineas) * 52 + i * 34
        if yy < h / 2 - 150:
            s.append(f'<path d="M{f(-w / 2 + 60)} {f(yy)} H{f(w / 2 - 60 - (i % 3) * 60)}" stroke="#9A9080" stroke-width="5"/>')
    if firma > 0:
        n = int(30 * c01(firma))
        pts = " ".join(f"L{f(-w * 0.32 + i * 9)} {f(h / 2 - 110 + 18 * math.sin(i * 0.9) - i * 0.6)}" for i in range(n))
        s.append(f'<path d="M{f(-w * 0.32)} {f(h / 2 - 110)} {pts}" stroke="#1A3A8A" stroke-width="5" fill="none"/>')
    if sello > 0:
        p = c01(sello)
        k = 1.6 - 0.6 * ease_out(p)
        s.append(f'<g transform="translate({f(w * 0.25)} {f(h / 2 - 120)}) scale({k:.2f}) rotate(-12)" opacity="{p:.2f}"><circle r="70" fill="none" stroke="#B3261E" stroke-width="8"/>'
                 f'<circle r="54" fill="none" stroke="#B3261E" stroke-width="3"/><text y="12" text-anchor="middle" font-family="{FUENTE}" font-weight="900" font-size="30" fill="#B3261E">OFICIAL</text></g>')
    s.append('</g>')
    return "".join(s)


def alcancia(x, y, k=1.0, rota=False):
    s = (f'<g transform="translate({f(x)} {f(y)}) scale({k:.3f})"><ellipse cx="0" cy="4" rx="120" ry="14" fill="#000" opacity="0.2"/>'
         '<ellipse cx="0" cy="-90" rx="130" ry="90" fill="#E89AAE"/><circle cx="110" cy="-100" r="40" fill="#E89AAE"/><ellipse cx="140" cy="-96" rx="18" ry="22" fill="#D0788E"/>'
         '<path d="M-60 -10 v20 M -20 -10 v20 M 40 -10 v20 M 80 -10 v20" stroke="#D0788E" stroke-width="22" stroke-linecap="round"/>'
         '<rect x="-30" y="-182" width="60" height="10" rx="4" fill="#9A4A5E"/><circle cx="100" cy="-118" r="7" fill="#2B2B2B"/>')
    if rota:
        s += '<path d="M-60 -170 L -30 -110 L -70 -80 L -20 -20" stroke="#5A2A36" stroke-width="7" fill="none"/>'
    return s + '</g>'


def mesa_familia(t, era="1920"):
    s = [f'<rect width="1920" height="1080" fill="#5A4636"/><rect width="1920" height="700" fill="#7A6450"/>']
    s.append('<rect x="760" y="140" width="400" height="300" fill="#3E5060"/><rect x="760" y="140" width="400" height="300" fill="none" stroke="#4A3626" stroke-width="22"/><path d="M960 140 V440 M760 290 H1160" stroke="#4A3626" stroke-width="12"/>')
    s.append('<path d="M920 0 V 230" stroke="#2B2B2B" stroke-width="4"/><path d="M880 230 h80 l -20 40 h-40 Z" fill="#2B2B2B"/><circle cx="920" cy="282" r="14" fill="#F6D98B"/>')
    s.append('<ellipse cx="960" cy="290" rx="300" ry="200" fill="#F6D98B" opacity="0.08"/>')
    s.append(persona(600, 930, 380, 21, t, "pie", era, 1, triste=True))
    s.append(persona(1320, 930, 360, 22, t, "pie", era, -1, triste=True))
    s.append(persona(1060, 930, 240, 23, t, "pie", era, -1, triste=True))
    s.append('<rect x="440" y="740" width="1040" height="34" fill="#6B4A2E"/><rect x="440" y="774" width="1040" height="20" fill="#4A3220"/><rect x="480" y="794" width="30" height="260" fill="#4A3220"/><rect x="1410" y="794" width="30" height="260" fill="#4A3220"/>')
    s.append(alcancia(760, 740, 0.9, rota=True))
    # libreta de ahorros
    s.append('<g transform="translate(1110 720) rotate(-8)"><rect x="-110" y="-70" width="220" height="140" fill="#2E5E4E"/><rect x="-100" y="-60" width="200" height="120" fill="#F5EEDC"/>'
             f'<text x="0" y="-18" text-anchor="middle" font-family="{FUENTE}" font-weight="800" font-size="22" fill="#2B2B2B">AHORROS</text>'
             f'<text x="0" y="34" text-anchor="middle" font-family="{FUENTE}" font-weight="900" font-size="44" fill="#B3261E">0,00</text></g>')
    return "".join(s)


def hielo(x, y, contenido, grietas=0.0):
    s = [f'<g transform="translate({f(x)} {f(y)})"><rect x="-260" y="-200" width="520" height="400" rx="30" fill="#BFE6F5" opacity="0.55"/>{contenido}'
         '<rect x="-260" y="-200" width="520" height="400" rx="30" fill="#DFF4FB" opacity="0.45"/><rect x="-260" y="-200" width="520" height="400" rx="30" fill="none" stroke="#FFFFFF" stroke-width="6" opacity="0.8"/>'
         '<path d="M-220 -160 L -120 -170 M -230 -120 L -190 -40" stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity="0.8"/>']
    if grietas > 0:
        n = int(6 * c01(grietas)) + 1
        r = random.Random(2)
        for i in range(n):
            x0, y0 = r.uniform(-200, 200), r.uniform(-160, 160)
            pts = [(x0, y0)]
            for _ in range(4):
                pts.append((pts[-1][0] + r.uniform(-70, 70), pts[-1][1] + r.uniform(-70, 70)))
            s.append('<path d="M' + " L".join(f"{f(a)} {f(b)}" for a, b in pts) + '" stroke="#FFFFFF" stroke-width="5" fill="none"/>')
    s.append('</g>')
    return "".join(s)


def manos_apreton(x, y, k=1.0, t=0.0):
    b = 6 * math.sin(t * 6)
    return (f'<g transform="translate({f(x)} {f(y + b)}) scale({k:.3f})">'
            '<path d="M-700 120 L -160 20 L -60 40 L -40 110 L -680 260 Z" fill="#2F3B45"/>'
            '<path d="M700 120 L 160 20 L 60 40 L 40 110 L 680 260 Z" fill="#6B4E3D"/>'
            '<path d="M-180 10 Q -60 -60 60 0 Q 110 30 60 80 Q -40 140 -140 90 Z" fill="#E8B98F"/>'
            '<path d="M180 10 Q 80 -40 -10 10 Q -60 50 -10 90 Q 60 130 150 90 Z" fill="#C68E62"/>'
            '<path d="M-10 30 q 30 -10 60 0 M -20 55 q 35 -10 70 0 M -10 80 q 30 -8 55 0" stroke="#8A5A36" stroke-width="5" fill="none"/></g>')


def tijera(x, y, ang, k=1.0, abre=0.0):
    a = 10 + 18 * abre
    return (f'<g transform="translate({f(x)} {f(y)}) rotate({f(ang)}) scale({k:.3f})">'
            f'<g transform="rotate({f(-a)})"><path d="M0 -10 L 220 -6 L 220 6 L 0 10 Z" fill="#C9D1D6" stroke="#5A646B" stroke-width="3"/><circle cx="-60" cy="0" r="38" fill="none" stroke="#B3261E" stroke-width="16"/></g>'
            f'<g transform="rotate({f(a)})"><path d="M0 -10 L 220 -6 L 220 6 L 0 10 Z" fill="#DDE3E7" stroke="#5A646B" stroke-width="3"/><circle cx="-60" cy="0" r="38" fill="none" stroke="#B3261E" stroke-width="16"/></g>'
            '<circle r="9" fill="#5A646B"/></g>')


def pistola_precios(x, y, ang=0.0, k=1.0):
    return (f'<g transform="translate({f(x)} {f(y)}) rotate({f(ang)}) scale({k:.3f})"><path d="M-120 -40 H 90 Q 120 -40 120 -10 V 30 H -120 Z" fill="#E67E22"/>'
            '<path d="M-60 30 L -40 140 H 10 L 0 30 Z" fill="#2B2B2B"/><rect x="-110" y="-30" width="120" height="46" rx="4" fill="#FFF7C2"/>'
            f'<text x="-50" y="2" text-anchor="middle" font-family="{FUENTE}" font-weight="900" font-size="26" fill="#B3261E">$$$</text>'
            '<path d="M-20 34 Q -10 70 20 60" stroke="#2B2B2B" stroke-width="10" fill="none"/></g>')


def pictograma(x, y, cols, filas, t, start, paso, color="#F2B705", gris="#5A6470", n_color=None, tam=44):
    """Rejilla de personitas; se van coloreando de una en una."""
    s = []
    total = cols * filas
    n_color = total if n_color is None else n_color
    for i in range(total):
        cx = x + (i % cols) * tam
        cy = y + (i // cols) * tam * 1.5
        on = i < n_color and t > start + i * paso
        c = color if on else gris
        s.append(f'<circle cx="{f(cx)}" cy="{f(cy)}" r="{f(tam * 0.2)}" fill="{c}"/><path d="M{f(cx - tam * 0.28)} {f(cy + tam * 0.75)} V{f(cy + tam * 0.45)} Q {f(cx)} {f(cy + tam * 0.18)} {f(cx + tam * 0.28)} {f(cy + tam * 0.45)} V{f(cy + tam * 0.75)} Z" fill="{c}"/>')
    return "".join(s)


def boveda(t, abre=1.0):
    s = ['<rect width="1920" height="1080" fill="#3A4046"/><rect y="860" width="1920" height="220" fill="#2A2E33"/>']
    for i in range(4):
        y = 300 + i * 150
        s.append(f'<rect x="80" y="{y}" width="700" height="16" fill="#6B7178"/>')
        s.append(pila(110, y - 2, 5, 1, 1, "#A9C79A", 110))
    s.append(f'<g transform="translate(1340 520)"><circle r="330" fill="#5E666E"/><circle r="300" fill="#8C959D"/>'
             f'<g transform="rotate({f(t * 30)})">' + "".join(f'<rect x="-10" y="-260" width="20" height="90" rx="8" fill="#5E666E" transform="rotate({a})"/>' for a in range(0, 360, 45)) +
             '<circle r="80" fill="#5E666E"/><circle r="40" fill="#C9D1D6"/></g></g>')
    return "".join(s)


def caja_texto(x, y, texto, fs=40, fondo="#101820", color="#FFFFFF", op=0.85, ancla="start", padding=24):
    w = len(texto) * fs * 0.58 + padding * 2
    bx = x if ancla == "start" else (x - w / 2 if ancla == "middle" else x - w)
    return (f'<rect x="{f(bx)}" y="{f(y - fs * 1.05)}" width="{f(w)}" height="{f(fs * 1.5)}" rx="10" fill="{fondo}" opacity="{op}"/>'
            f'<text x="{f(bx + w / 2)}" y="{f(y)}" text-anchor="middle" font-family="{FUENTE}" font-weight="800" font-size="{fs}" fill="{color}">{texto}</text>')
