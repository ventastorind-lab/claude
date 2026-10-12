"""Objetos (lo que Byron come o toma) e íconos extra para la serie "Byron vs. 50".

Cada objeto: fn(x, y, k=1.0, rot=0) -> SVG centrado en (x, y), de unos 70x120 px con k=1.
"""
import math

INK = "#1A1A1A"


def _g(x, y, k, rot, cuerpo):
    return f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot:.1f}) scale({k:.3f})">{cuerpo}</g>'


def banano(x, y, k=1.0, rot=0):
    return _g(x, y, k, rot - 25,
              f'<path d="M-20 -60 C 30 -40 45 20 10 62 C 0 70 -8 66 -4 58 C 20 20 10 -20 -28 -48 Z" fill="#FFE135" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
              f'<path d="M-20 -60 L -30 -66 L -24 -52 Z" fill="#6D4C41" stroke="{INK}" stroke-width="4"/>'
              f'<circle cx="2" cy="62" r="5" fill="#4E342E"/><path d="M-12 -40 C 15 -20 20 15 4 45" stroke="#F9A825" stroke-width="4" fill="none"/>')


def tinto(x, y, k=1.0, rot=0):
    return _g(x, y, k, rot,
              f'<path d="M-40 -30 L 40 -30 L 32 40 C 30 52 22 56 12 56 L -12 56 C -22 56 -30 52 -32 40 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
              f'<path d="M40 -10 C 62 -10 62 25 36 25" fill="none" stroke="{INK}" stroke-width="5"/>'
              f'<ellipse cx="0" cy="-30" rx="40" ry="9" fill="#4E342E" stroke="#1565C0" stroke-width="5"/>'
              '<path d="M-12 -45 q -8 -12 0 -24 q 8 -12 0 -24 M10 -45 q -8 -12 0 -24" stroke="#BDBDBD" stroke-width="5" fill="none" stroke-linecap="round"/>')


def chile(x, y, k=1.0, rot=0):
    return _g(x, y, k, rot + 15,
              f'<path d="M-14 -45 C 20 -50 30 -10 22 25 C 15 55 0 68 -6 60 C -2 40 -26 10 -24 -20 C -23 -36 -20 -43 -14 -45 Z" fill="#43A047" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
              f'<path d="M-8 -46 C -6 -60 0 -66 10 -70" fill="none" stroke="#2E7D32" stroke-width="8" stroke-linecap="round"/>'
              f'<path d="M-20 -48 C -10 -56 8 -54 14 -46" fill="#2E7D32" stroke="{INK}" stroke-width="4"/>'
              '<path d="M-10 -30 C -14 -10 -10 10 -4 30" stroke="#A5D6A7" stroke-width="5" fill="none" stroke-linecap="round"/>')


def dona(x, y, k=1.0, rot=0):
    granas = "".join(f'<rect x="{18 * math.cos(a) * 1.9 - 4:.1f}" y="{18 * math.sin(a) * 1.9 - 2:.1f}" width="9" height="4" rx="2" fill="{c}" '
                     f'transform="rotate({a * 57 + 30:.0f} {18 * math.cos(a) * 1.9:.1f} {18 * math.sin(a) * 1.9:.1f})"/>'
                     for a, c in zip([i * 0.7 for i in range(9)], ["#FFEB3B", "#42A5F5", "#FFFFFF", "#66BB6A", "#FF7043"] * 2))
    return _g(x, y, k, rot,
              f'<circle cx="0" cy="0" r="52" fill="#D7A86E" stroke="{INK}" stroke-width="5"/>'
              f'<path d="M-48 -8 C -50 -40 -20 -52 0 -50 C 30 -50 52 -30 48 -2 C 44 10 36 4 30 14 C 22 30 10 18 0 30 C -14 40 -20 22 -32 24 C -44 26 -46 10 -48 -8 Z" fill="#F48FB1"/>'
              + granas +
              f'<circle cx="0" cy="0" r="16" fill="#FFF3E0" stroke="{INK}" stroke-width="5"/>')


def energetica(x, y, k=1.0, rot=0):
    return _g(x, y, k, rot,
              f'<rect x="-28" y="-62" width="56" height="124" rx="9" fill="#1E3A8A" stroke="{INK}" stroke-width="5"/>'
              '<rect x="-28" y="-20" width="56" height="40" fill="#C0C7D1"/>'
              f'<polygon points="6,-55 -14,-2 2,-2 -8,50 16,-10 0,-10 14,-55" fill="#FFD600" stroke="{INK}" stroke-width="3"/>'
              f'<ellipse cx="0" cy="-62" rx="28" ry="8" fill="#CFD8DC" stroke="{INK}" stroke-width="4"/>')


def chocolatina(x, y, k=1.0, rot=0):
    cuadros = "".join(f'<rect x="{-26 + c * 18}" y="{-50 + r * 18}" width="15" height="15" rx="2" fill="#6D4C41" stroke="#3E2723" stroke-width="2"/>'
                      for r in range(3) for c in range(3))
    return _g(x, y, k, rot,
              f'<rect x="-32" y="-56" width="64" height="116" rx="6" fill="#5D4037" stroke="{INK}" stroke-width="5"/>' + cuadros +
              f'<path d="M-32 6 L 32 6 L 32 60 L -32 60 Z" fill="#C62828" stroke="{INK}" stroke-width="5"/>'
              f'<path d="M-32 6 l 8 -8 l 8 8 l 8 -8 l 8 8 l 8 -8 l 8 8 l 8 -8 l 8 8" fill="#C62828" stroke="{INK}" stroke-width="4"/>'
              '<text x="0" y="42" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="15" fill="#FFD54F">CHOCO</text>')


def naranja(x, y, k=1.0, rot=0):
    poros = "".join(f'<circle cx="{c1}" cy="{c2}" r="2.5" fill="#EF6C00"/>' for c1, c2 in ((-20, -10), (10, 15), (25, -20), (-10, 25), (5, -30), (-28, 12)))
    return _g(x, y, k, rot,
              f'<circle cx="0" cy="4" r="50" fill="#FB8C00" stroke="{INK}" stroke-width="5"/>' + poros +
              f'<path d="M0 -46 C 10 -66 34 -66 40 -56 C 30 -44 12 -42 0 -46 Z" fill="#43A047" stroke="{INK}" stroke-width="4"/>'
              '<path d="M-26 -18 q 10 -14 26 -16" stroke="#FFCC80" stroke-width="6" fill="none" stroke-linecap="round"/>')


def vaso_agua(x, y, k=1.0, rot=0):
    return _g(x, y, k, rot,
              f'<path d="M-36 -60 L 36 -60 L 28 60 L -28 60 Z" fill="#E1F5FE" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
              '<path d="M-33 -25 L 33 -25 L 28 56 L -28 56 Z" fill="#4FC3F7"/>'
              '<ellipse cx="0" cy="-25" rx="33" ry="6" fill="#81D4FA"/>'
              '<path d="M-22 -10 L -18 45" stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.7"/>')


def hamburguesa(x, y, k=1.0, rot=0):
    sem = "".join(f'<ellipse cx="{a}" cy="{b}" rx="4" ry="2.5" fill="#FFF8E1"/>' for a, b in ((-20, -38), (0, -46), (20, -38), (-8, -30), (12, -28)))
    return _g(x, y, k, rot,
              f'<path d="M-55 -18 C -55 -60 55 -60 55 -18 Z" fill="#E0A458" stroke="{INK}" stroke-width="5"/>' + sem +
              f'<path d="M-58 -18 q 10 12 20 0 q 10 12 20 0 q 10 12 20 0 q 10 12 20 0 q 10 12 20 0 q 10 12 18 0" fill="#7CB342" stroke="{INK}" stroke-width="4"/>'
              f'<path d="M-52 -4 L 52 -4 L 40 14 L -40 14 Z" fill="#FFCA28" stroke="{INK}" stroke-width="4"/>'
              f'<rect x="-56" y="4" width="112" height="24" rx="12" fill="#6D4C41" stroke="{INK}" stroke-width="5"/>'
              f'<path d="M-54 30 L 54 30 C 54 52 -54 52 -54 30 Z" fill="#E0A458" stroke="{INK}" stroke-width="5"/>')


def manzana(x, y, k=1.0, rot=0):
    return _g(x, y, k, rot,
              f'<path d="M0 -30 C -20 -48 -56 -40 -54 0 C -52 40 -24 62 0 50 C 24 62 52 40 54 0 C 56 -40 20 -48 0 -30 Z" fill="#E53935" stroke="{INK}" stroke-width="5"/>'
              f'<path d="M0 -30 C 2 -44 6 -54 10 -62" stroke="#6D4C41" stroke-width="7" fill="none" stroke-linecap="round"/>'
              f'<path d="M6 -48 C 18 -66 40 -64 42 -54 C 30 -44 16 -44 6 -48 Z" fill="#43A047" stroke="{INK}" stroke-width="4"/>'
              '<path d="M-36 -14 q 6 -18 22 -22" stroke="#FFCDD2" stroke-width="7" fill="none" stroke-linecap="round"/>')


OBJETOS = dict(banano=banano, tinto=tinto, chile=chile, dona=dona, energetica=energetica, chocolatina=chocolatina,
               naranja=naranja, vaso_agua=vaso_agua, hamburguesa=hamburguesa, manzana=manzana)


# ------------------------------------------------------------------ íconos extra
def icono_extra(nombre, x, y, t=0.0):
    if nombre == "fuego":
        k = 1 + 0.08 * math.sin(t * 14)
        return (f'<g transform="translate({x} {y}) scale({k:.3f} {2 - k:.3f})"><path d="M0 -240 C 60 -160 170 -110 150 30 C 140 130 60 190 0 190 C -60 190 -150 130 -150 30 C -150 -60 -80 -80 -60 -150 C -20 -100 -10 -170 0 -240 Z" '
                f'fill="#FF7043" stroke="{INK}" stroke-width="10"/><path d="M0 -60 C 40 0 90 40 70 110 C 60 150 30 170 0 170 C -30 170 -70 150 -70 100 C -70 50 -30 30 0 -60 Z" fill="#FFCA28"/></g>')
    if nombre == "radiacion":
        rot = (t * 40) % 360
        aspas = "".join(f'<path transform="rotate({a})" d="M0 0 L -80 -140 A 160 160 0 0 1 80 -140 Z" fill="{INK}"/>' for a in (0, 120, 240))
        return (f'<g transform="translate({x} {y})"><circle r="200" fill="#FFD600" stroke="{INK}" stroke-width="12"/>'
                f'<g transform="rotate({rot:.1f})">{aspas}</g><circle r="40" fill="{INK}" stroke="#FFD600" stroke-width="12"/></g>')
    if nombre == "salero":
        granos = "".join(f'<rect x="{-20 + (i * 37) % 60:.0f}" y="{120 + ((t * 300 + i * 53) % 160):.0f}" width="8" height="8" fill="#FFFFFF" stroke="{INK}" stroke-width="2"/>' for i in range(8))
        return (f'<g transform="translate({x} {y})"><g transform="rotate(160)"><path d="M-90 -150 L 90 -150 L 110 120 L -110 120 Z" fill="#FFFFFF" fill-opacity="0.85" stroke="{INK}" stroke-width="10"/>'
                f'<rect x="-100" y="-210" width="200" height="70" rx="20" fill="#B0BEC5" stroke="{INK}" stroke-width="10"/>'
                '<circle cx="-40" cy="-175" r="8" fill="#1A1A1A"/><circle cx="0" cy="-175" r="8" fill="#1A1A1A"/><circle cx="40" cy="-175" r="8" fill="#1A1A1A"/>'
                f'<text x="0" y="20" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="70" fill="#455A64" transform="rotate(180 0 0)">SAL</text></g>'
                + granos + '</g>')
    if nombre == "semilla":
        return (f'<g transform="translate({x} {y})">'
                + "".join(f'<g transform="translate({a} {b}) rotate({r})"><path d="M0 -60 C 40 -40 40 40 0 60 C -40 40 -40 -40 0 -60 Z" fill="#5D4037" stroke="{INK}" stroke-width="8"/>'
                          '<path d="M-10 -30 C -16 0 -12 20 -4 40" stroke="#8D6E63" stroke-width="6" fill="none"/></g>'
                          for a, b, r in ((-120, 20, -20), (0, -20, 10), (120, 30, 25)))
                + f'<text x="0" y="200" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="50" fill="#E53935">¡NO LAS MASTIQUES!</text></g>')
    if nombre == "pastilla":
        return (f'<g transform="translate({x} {y}) rotate({10 * math.sin(t * 2):.1f})"><rect x="-200" y="-80" width="400" height="160" rx="80" fill="#FFB300" stroke="{INK}" stroke-width="10"/>'
                f'<path d="M0 -80 L 0 80" stroke="{INK}" stroke-width="8"/><rect x="-200" y="-80" width="200" height="160" rx="80" fill="#FFF3E0" opacity="0.6"/>'
                f'<text x="100" y="25" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="80" fill="{INK}">C</text></g>')
    if nombre == "perro":
        return (f'<g transform="translate({x} {y})"><ellipse cx="0" cy="60" rx="170" ry="100" fill="#D7A86E" stroke="{INK}" stroke-width="10"/>'
                f'<circle cx="150" cy="-60" r="95" fill="#D7A86E" stroke="{INK}" stroke-width="10"/>'
                f'<path d="M90 -140 C 60 -220 120 -230 130 -150 Z M200 -140 C 240 -220 270 -170 220 -120 Z" fill="#8D6E63" stroke="{INK}" stroke-width="8"/>'
                f'<circle cx="130" cy="-70" r="14" fill="{INK}"/><circle cx="190" cy="-70" r="14" fill="{INK}"/><ellipse cx="170" cy="-25" rx="22" ry="16" fill="{INK}"/>'
                f'<path d="M-150 40 q -60 -60 -40 -120" stroke="{INK}" stroke-width="14" fill="none" stroke-linecap="round"/>'
                f'<circle cx="-40" cy="-170" r="70" fill="#FFFFFF" stroke="#E53935" stroke-width="14"/>'
                + chocolatina(-40, -170, 0.75, 0)
                + '<line x1="-90" y1="-120" x2="10" y2="-220" stroke="#E53935" stroke-width="16" stroke-linecap="round"/></g>')
    if nombre == "estomago_lleno":
        return None
    return None
