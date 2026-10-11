"""Genera las fichas (SVG 1200x1200) de 5 personajes nuevos del universo de Rayo.

Uso: python3 generar_personajes.py <carpeta_salida>
"""
import os
import sys
from html import escape

INK = "#1A1A1A"
S = 1200


def ficha(bg, acento, etiqueta, nombre, frase, cuerpo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" width="{S}" height="{S}">'
            f'<rect width="{S}" height="{S}" fill="{bg}"/>'
            f'<circle cx="600" cy="560" r="440" fill="{acento}" opacity="0.28"/>'
            f'<ellipse cx="600" cy="975" rx="280" ry="30" fill="#000000" opacity="0.12"/>'
            f'{cuerpo}'
            f'<rect x="60" y="50" width="{len(etiqueta) * 21 + 60}" height="70" rx="35" fill="{INK}"/>'
            f'<text x="90" y="98" font-family="Arial, sans-serif" font-weight="bold" font-size="36" fill="#FFFFFF">{escape(etiqueta)}</text>'
            f'<rect x="90" y="1000" width="1020" height="160" rx="36" fill="{INK}"/>'
            f'<text x="600" y="1078" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="72" fill="#FFFFFF">{escape(nombre)}</text>'
            f'<text x="600" y="1132" text-anchor="middle" font-family="Arial, sans-serif" font-style="italic" font-weight="bold" font-size="36" fill="{acento}">“{escape(frase)}”</text>'
            '</svg>')


def palo(points, w=22, color=INK):
    return f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'


def mano(x, y, r=18):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{INK}"/>'


# ------------------------------------------------------------ 1. Byron, ajolote doble de riesgo
def byron():
    rosa, rosa_c, rojo = "#F8BBD0", "#FCE4EC", "#EC407A"
    s = []
    # cola
    s.append(f'<path d="M690 760 C 820 760 900 820 960 900 C 900 930 820 900 700 860 Z" fill="{rosa}" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
             f'<path d="M760 790 C 840 800 900 850 940 895" fill="none" stroke="{rojo}" stroke-width="8" opacity="0.6"/>')
    # piernas
    s.append(palo("550,850 520,968") + palo("650,850 690,968"))
    s.append(f'<ellipse cx="505" cy="972" rx="34" ry="14" fill="{INK}"/><ellipse cx="705" cy="972" rx="34" ry="14" fill="{INK}"/>')
    # cuerpo
    s.append(f'<ellipse cx="600" cy="700" rx="160" ry="175" fill="{rosa}" stroke="{INK}" stroke-width="10"/>'
             f'<ellipse cx="600" cy="720" rx="100" ry="125" fill="{rosa_c}"/>')
    # brazos: uno en la cintura, otro con pulgar arriba
    s.append(palo("455,640 380,700 440,760") + mano(440, 760))
    s.append(palo("745,640 830,600 850,500") + mano(850, 500, 22))
    s.append(f'<rect x="842" y="452" width="16" height="40" rx="8" fill="{INK}"/>')
    # branquias
    for lado in (-1, 1):
        for k, (dy, ang) in enumerate(((-90, -35), (0, 0), (90, 35))):
            cx = 600 + lado * 270
            cy = 430 + dy * 0.9
            s.append(f'<g transform="translate({cx} {cy}) rotate({ang * lado})">'
                     f'<ellipse cx="{lado * 40}" cy="0" rx="78" ry="28" fill="{rojo}" stroke="{INK}" stroke-width="8"/>'
                     + "".join(f'<line x1="{lado * (i * 22)}" y1="-22" x2="{lado * (i * 22 + 10)}" y2="-38" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>' for i in range(4))
                     + '</g>')
    # cabeza
    s.append(f'<ellipse cx="600" cy="430" rx="245" ry="190" fill="{rosa}" stroke="{INK}" stroke-width="10"/>')
    # casco de doble de riesgo
    s.append(f'<path d="M395 380 C 400 230 800 230 805 380 C 700 340 500 340 395 380 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
             f'<path d="M585 262 L 615 262 L 640 352 L 560 352 Z" fill="#E53935"/>'
             f'<polygon points="600,268 610,292 636,292 615,307 623,332 600,317 577,332 585,307 564,292 590,292" fill="#FFD54F" stroke="{INK}" stroke-width="4"/>')
    # cara
    s.append(f'<circle cx="515" cy="440" r="20" fill="{INK}"/><circle cx="685" cy="440" r="20" fill="{INK}"/>'
             '<circle cx="522" cy="432" r="7" fill="#FFFFFF"/><circle cx="692" cy="432" r="7" fill="#FFFFFF"/>'
             f'<path d="M520 500 Q 600 560 680 500" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
             '<ellipse cx="470" cy="495" rx="34" ry="18" fill="#F06292" opacity="0.5"/><ellipse cx="730" cy="495" rx="34" ry="18" fill="#F06292" opacity="0.5"/>')
    # curita
    s.append(f'<g transform="rotate(-25 735 410)"><rect x="700" y="395" width="70" height="28" rx="12" fill="#FFCC80" stroke="{INK}" stroke-width="5"/>'
             '<rect x="724" y="399" width="22" height="20" fill="#FFE0B2"/></g>')
    # brillo de "me vuelve a crecer"
    s.append('<g fill="#FFEB3B" stroke="#1A1A1A" stroke-width="4">'
             + "".join(f'<polygon transform="translate({x} {y}) scale({k})" points="0,-30 8,-8 30,0 8,8 0,30 -8,8 -30,0 -8,-8"/>' for x, y, k in ((910, 470, 1), (950, 560, 0.6), (880, 420, 0.5)))
             + '</g>')
    return ficha("#E0F7FA", "#EC407A", "AJOLOTE · DOBLE DE RIESGO", "BYRON", "¡Tranqui, me vuelve a crecer!", "".join(s))


# ------------------------------------------------------------ 2. Sócrates, calcetín filósofo
def socrates():
    contorno = ("M470 220 L710 220 L710 630 C710 690 770 710 830 728 C940 760 950 905 830 925 "
                "L560 925 C470 925 445 860 465 790 C480 730 470 690 470 630 Z")
    s = [f'<defs><clipPath id="calc"><path d="{contorno}"/></clipPath></defs>',
         f'<path d="{contorno}" fill="#FFFFFF"/>',
         '<g clip-path="url(#calc)">',
         '<rect x="400" y="300" width="600" height="38" fill="#E53935"/><rect x="400" y="345" width="600" height="18" fill="#1E88E5"/>',
         '<rect x="400" y="590" width="600" height="38" fill="#E53935"/><rect x="400" y="635" width="600" height="18" fill="#1E88E5"/>',
         '<ellipse cx="860" cy="830" rx="130" ry="130" fill="#FFCA28"/>',
         '<ellipse cx="520" cy="900" rx="110" ry="90" fill="#FFCA28"/>',
         '<rect x="400" y="220" width="600" height="62" fill="#ECEFF1"/>']
    s += [f'<line x1="{x}" y1="222" x2="{x}" y2="280" stroke="#B0BEC5" stroke-width="5"/>' for x in range(490, 710, 22)]
    s.append('</g>')
    s.append(f'<path d="{contorno}" fill="none" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>')
    # agujero con hilo
    s.append(f'<ellipse cx="905" cy="860" rx="20" ry="14" fill="#FFF8E1" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M915 855 C 960 840 975 880 1010 870" fill="none" stroke="#E53935" stroke-width="5" stroke-linecap="round"/>')
    # cara: ojos mirando arriba, monóculo
    s.append(f'<circle cx="550" cy="440" r="32" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/><circle cx="650" cy="440" r="32" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>'
             f'<circle cx="558" cy="426" r="13" fill="{INK}"/><circle cx="658" cy="426" r="13" fill="{INK}"/>'
             f'<path d="M510 395 Q 550 380 585 398 M615 398 Q 650 380 690 395" fill="none" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
             '<circle cx="650" cy="440" r="44" fill="none" stroke="#FFB300" stroke-width="8"/>'
             '<path d="M690 460 C 720 520 700 560 705 600" fill="none" stroke="#FFB300" stroke-width="4"/>')
    # barba de pelusa
    s.append('<g fill="#CFD8DC" stroke="#1A1A1A" stroke-width="5">'
             + "".join(f'<circle cx="{x}" cy="{y}" r="{r}"/>' for x, y, r in ((560, 520, 30), (600, 535, 34), (640, 520, 30), (585, 565, 26), (620, 568, 24), (602, 598, 20)))
             + '</g>'
             f'<ellipse cx="600" cy="505" rx="18" ry="12" fill="{INK}"/>')
    # brazos: uno sosteniendo el cartel, otro con el dedo "pensando"
    s.append(palo("470,560 400,620 370,580") + mano(370, 580))
    s.append(f'<g transform="rotate(-6 270 530)"><rect x="160" y="400" width="230" height="270" rx="8" fill="#FFF3E0" stroke="{INK}" stroke-width="7"/>'
             f'<text x="275" y="455" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="38" fill="#E53935">SE BUSCA</text>'
             f'<path d="M240 480 L290 480 L290 560 C290 580 310 585 330 590 C350 596 352 625 330 628 L255 628 C232 628 228 610 234 594 C238 580 240 570 240 560 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="5"/>'
             f'<rect x="240" y="500" width="50" height="12" fill="#E53935"/>'
             f'<text x="275" y="655" text-anchor="middle" font-family="Arial, sans-serif" font-weight="bold" font-size="22" fill="{INK}">¿Has visto a mi par?</text></g>')
    s.append(palo("710,560 800,520 815,440") + mano(815, 440))
    s.append(f'<line x1="815" y1="440" x2="822" y2="395" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>')
    return ficha("#FFF8E1", "#FFB300", "CALCETÍN · FILÓSOFO", "SÓCRATES", "Solo sé que perdí a mi par.", "".join(s))


# ------------------------------------------------------------ 3. Tinto, detective insomne
def tinto():
    s = []
    # plato
    s.append(f'<ellipse cx="600" cy="935" rx="270" ry="46" fill="#FFFFFF" stroke="{INK}" stroke-width="10"/>'
             f'<ellipse cx="600" cy="925" rx="170" ry="22" fill="#ECEFF1"/>')
    # vapor en forma de signo de pregunta
    s.append('<g fill="none" stroke="#BDBDBD" stroke-width="24" stroke-linecap="round">'
             '<path d="M690 470 C 650 420 720 380 690 330 C 660 280 720 240 760 250 C 830 265 830 340 780 360 C 750 372 745 395 748 420"/></g>'
             '<circle cx="748" cy="462" r="14" fill="#BDBDBD"/>'
             '<path d="M520 470 C 495 430 545 400 520 360" fill="none" stroke="#E0E0E0" stroke-width="16" stroke-linecap="round"/>')
    # asa
    s.append(f'<path d="M805 600 C 905 590 915 760 790 770" fill="none" stroke="{INK}" stroke-width="54" stroke-linecap="round"/>'
             f'<path d="M805 600 C 905 590 915 760 790 770" fill="none" stroke="#FFFFFF" stroke-width="34" stroke-linecap="round"/>')
    # pocillo
    s.append(f'<path d="M380 520 L820 520 L790 860 C785 900 760 915 720 915 L480 915 C440 915 415 900 410 860 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
             '<path d="M392 560 L808 560" stroke="#1565C0" stroke-width="12"/>'
             f'<ellipse cx="600" cy="520" rx="220" ry="40" fill="#FFFFFF" stroke="#1565C0" stroke-width="14"/>'
             f'<ellipse cx="600" cy="522" rx="190" ry="28" fill="#4E342E"/>'
             '<ellipse cx="560" cy="516" rx="60" ry="8" fill="#8D6E63" opacity="0.7"/>')
    # sombrero de detective sobre el borde
    s.append(f'<g transform="rotate(-9 560 470)"><ellipse cx="560" cy="478" rx="215" ry="34" fill="#5D4037" stroke="{INK}" stroke-width="9"/>'
             f'<path d="M430 470 C 430 360 470 330 560 330 C 650 330 690 360 690 470 Z" fill="#6D4C41" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>'
             '<path d="M520 340 Q 560 375 600 340" fill="none" stroke="#4E342E" stroke-width="8"/>'
             '<rect x="432" y="430" width="256" height="34" fill="#3E2723"/></g>')
    # cara con ojeras
    for cx in (530, 670):
        s.append(f'<ellipse cx="{cx}" cy="680" rx="40" ry="30" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>'
                 f'<circle cx="{cx + 6}" cy="688" r="13" fill="{INK}"/>'
                 f'<path d="M{cx - 42} 676 L {cx + 42} 676 L {cx + 40} 660 C {cx + 20} 645 {cx - 20} 645 {cx - 40} 660 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
                 f'<path d="M{cx - 34} 722 Q {cx} 740 {cx + 34} 722" fill="none" stroke="#A1887F" stroke-width="7" stroke-linecap="round"/>'
                 f'<path d="M{cx - 30} 732 Q {cx} 752 {cx + 30} 732" fill="none" stroke="#BCAAA4" stroke-width="5" stroke-linecap="round"/>')
    s.append(f'<path d="M560 790 Q 610 805 650 782" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>')
    # brazo con lupa
    s.append(palo("405,720 330,670 300,590") + mano(300, 590))
    s.append(f'<line x1="292" y1="575" x2="262" y2="520" stroke="#6D4C41" stroke-width="18" stroke-linecap="round"/>'
             f'<circle cx="235" cy="470" r="62" fill="#B3E5FC" fill-opacity="0.55" stroke="{INK}" stroke-width="12"/>'
             '<path d="M205 445 Q 220 425 245 422" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round"/>')
    return ficha("#EFEBE9", "#8D6E63", "TINTO · DETECTIVE INSOMNE", "TINTO", "No duermo… investigo.", "".join(s))


# ------------------------------------------------------------ 4. Doña Gertrudis, abuela pilota de drones
def gertrudis():
    s = []
    # dron con arepa
    s.append('<g stroke="#90CAF9" stroke-width="6" stroke-dasharray="4 16" stroke-linecap="round" fill="none">'
             '<path d="M690 650 Q 820 480 900 270"/></g>')
    s.append(f'<g transform="translate(930 220)">'
             f'<line x1="-120" y1="-20" x2="120" y2="-20" stroke="{INK}" stroke-width="12"/>'
             f'<line x1="-120" y1="-20" x2="-120" y2="-45" stroke="{INK}" stroke-width="10"/><line x1="120" y1="-20" x2="120" y2="-45" stroke="{INK}" stroke-width="10"/>'
             '<ellipse cx="-120" cy="-50" rx="70" ry="11" fill="#B0BEC5" opacity="0.85" stroke="#1A1A1A" stroke-width="4"/>'
             '<ellipse cx="120" cy="-50" rx="70" ry="11" fill="#B0BEC5" opacity="0.85" stroke="#1A1A1A" stroke-width="4"/>'
             f'<rect x="-70" y="-35" width="140" height="50" rx="20" fill="#424242" stroke="{INK}" stroke-width="7"/>'
             '<circle cx="0" cy="-10" r="10" fill="#E53935"/>'
             f'<line x1="0" y1="15" x2="0" y2="95" stroke="{INK}" stroke-width="4"/>'
             f'<circle cx="0" cy="135" r="45" fill="#FFE082" stroke="{INK}" stroke-width="7"/>'
             '<path d="M-25 115 L 25 155 M-30 140 L 10 165 M-10 100 L 35 132" stroke="#C8A15A" stroke-width="7" stroke-linecap="round"/>'
             '<g stroke="#1A1A1A" stroke-width="5" stroke-linecap="round" opacity="0.6"><line x1="-200" y1="-55" x2="-215" y2="-75"/><line x1="200" y1="-55" x2="215" y2="-75"/></g>'
             '</g>')
    # piernas y zapatos
    s.append(palo("555,900 545,965") + palo("645,900 655,965"))
    s.append(f'<ellipse cx="535" cy="970" rx="32" ry="14" fill="{INK}"/><ellipse cx="665" cy="970" rx="32" ry="14" fill="{INK}"/>')
    # vestido y chal
    s.append(f'<path d="M470 905 L730 905 L680 560 L520 560 Z" fill="#7E57C2" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
             '<path d="M520 560 L600 680 L680 560" fill="#B39DDB" stroke="#1A1A1A" stroke-width="8" stroke-linejoin="round"/>'
             + "".join(f'<circle cx="{x}" cy="{y}" r="7" fill="#FFFFFF" opacity="0.8"/>' for x, y in ((530, 760), (600, 820), (670, 770), (560, 860), (640, 870))))
    # brazos con control
    s.append(palo("525,600 480,690 555,740") + palo("675,600 720,690 645,740"))
    s.append(f'<rect x="510" y="712" width="180" height="62" rx="26" fill="#424242" stroke="{INK}" stroke-width="8"/>'
             '<circle cx="555" cy="743" r="14" fill="#90A4AE"/><circle cx="645" cy="743" r="14" fill="#90A4AE"/>'
             f'<line x1="672" y1="712" x2="695" y2="652" stroke="{INK}" stroke-width="7" stroke-linecap="round"/><circle cx="696" cy="648" r="9" fill="#E53935"/>')
    s.append(mano(555, 740) + mano(645, 740))
    # cabeza
    s.append(f'<circle cx="600" cy="300" r="58" fill="#CFD8DC" stroke="{INK}" stroke-width="8"/>'
             f'<line x1="570" y1="290" x2="640" y2="275" stroke="#FFB300" stroke-width="8" stroke-linecap="round"/>'
             f'<circle cx="600" cy="440" r="118" fill="#FFFFFF" stroke="{INK}" stroke-width="10"/>'
             f'<path d="M485 420 C 490 330 710 330 715 420 C 670 375 530 375 485 420 Z" fill="#CFD8DC" stroke="{INK}" stroke-width="8"/>')
    # gafas de aviador en la frente
    s.append(f'<path d="M482 395 C 540 380 660 380 718 395" fill="none" stroke="#6D4C41" stroke-width="16"/>'
             f'<circle cx="558" cy="385" r="30" fill="#81D4FA" stroke="{INK}" stroke-width="8"/><circle cx="642" cy="385" r="30" fill="#81D4FA" stroke="{INK}" stroke-width="8"/>'
             '<path d="M545 372 l 14 -8 M629 372 l 14 -8" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>')
    # cara: gafas redondas, guiño, sonrisa pícara
    s.append(f'<circle cx="560" cy="455" r="30" fill="none" stroke="{INK}" stroke-width="7"/><circle cx="645" cy="455" r="30" fill="none" stroke="{INK}" stroke-width="7"/>'
             f'<line x1="590" y1="455" x2="615" y2="455" stroke="{INK}" stroke-width="6"/>'
             f'<path d="M545 458 Q 560 448 575 458" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
             f'<circle cx="648" cy="456" r="11" fill="{INK}"/>'
             f'<path d="M555 505 Q 610 545 650 498" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>'
             '<ellipse cx="520" cy="500" rx="22" ry="12" fill="#F48FB1" opacity="0.55"/><ellipse cx="685" cy="500" rx="22" ry="12" fill="#F48FB1" opacity="0.55"/>')
    return ficha("#EDE7F6", "#7E57C2", "ABUELA · PILOTA DE DRONES", "DOÑA GERTRUDIS", "¡Mijo, ya lo vi desde el dron!", "".join(s))


# ------------------------------------------------------------ 5. Don Tornillo, drywall jubilado
def don_tornillo():
    s = []
    # bastón: un clavo
    s.append(f'<line x1="405" y1="640" x2="392" y2="962" stroke="#B0BEC5" stroke-width="18" stroke-linecap="round"/>'
             f'<line x1="405" y1="640" x2="392" y2="962" stroke="{INK}" stroke-width="18" stroke-opacity="0.15"/>'
             f'<ellipse cx="406" cy="634" rx="36" ry="12" fill="#B0BEC5" stroke="{INK}" stroke-width="6"/>'
             f'<polygon points="384,950 400,950 392,978" fill="#B0BEC5" stroke="{INK}" stroke-width="5"/>')
    # cuerpo (vástago) y punta
    s.append(f'<rect x="522" y="415" width="156" height="430" fill="#37474F" stroke="{INK}" stroke-width="10"/>'
             f'<polygon points="522,840 678,840 600,972" fill="#37474F" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>')
    # rosca
    for y in range(600, 930, 44):
        x1, x2 = 505, 695
        if y > 840:
            k = (y - 840) / 132
            x1, x2 = 505 + 78 * k, 695 - 78 * k
        s.append(f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y - 30}" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
                 f'<line x1="{x1 + 4}" y1="{y - 3}" x2="{x2 - 4}" y2="{y - 33}" stroke="#78909C" stroke-width="7" stroke-linecap="round"/>')
    s.append('<line x1="540" y1="430" x2="540" y2="590" stroke="#78909C" stroke-width="8" stroke-linecap="round" opacity="0.8"/>')
    # cabeza trompeta con ranura Phillips
    s.append(f'<path d="M430 300 C 445 370 525 385 528 425 L 672 425 C 675 385 755 370 770 300 Z" fill="#263238" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
             f'<ellipse cx="600" cy="298" rx="172" ry="40" fill="#455A64" stroke="{INK}" stroke-width="10"/>'
             f'<path d="M540 298 L 660 298 M600 278 L 600 318" stroke="{INK}" stroke-width="16" stroke-linecap="round"/>'
             '<path d="M470 290 Q 520 272 570 270" fill="none" stroke="#90A4AE" stroke-width="6" stroke-linecap="round"/>')
    # cara: cejas pobladas, bigote enorme
    s.append(f'<circle cx="570" cy="478" r="22" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/><circle cx="630" cy="478" r="22" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
             f'<circle cx="573" cy="483" r="9" fill="{INK}"/><circle cx="627" cy="483" r="9" fill="{INK}"/>'
             '<path d="M535 455 Q 560 432 595 452 M605 452 Q 640 432 665 455" fill="none" stroke="#FFFFFF" stroke-width="14" stroke-linecap="round"/>'
             f'<path d="M600 518 C 570 500 540 505 520 520 C 500 535 485 530 478 512 C 470 545 520 560 560 545 C 580 538 595 530 600 528 '
             f'C 605 530 620 538 640 545 C 680 560 730 545 722 512 C 715 530 700 535 680 520 C 660 505 630 500 600 518 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    # medalla
    s.append(f'<path d="M640 585 L 655 625 L 670 585" fill="#E53935" stroke="{INK}" stroke-width="4"/>'
             f'<circle cx="655" cy="645" r="28" fill="#FFC107" stroke="{INK}" stroke-width="6"/>'
             f'<text x="655" y="655" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="22" fill="{INK}">40</text>')
    # brazos: uno en el bastón, otro con el dedo dando lección
    s.append(palo("522,580 450,650 410,740") + mano(410, 740))
    s.append(palo("678,580 770,560 795,470") + mano(795, 470))
    s.append(f'<line x1="795" y1="470" x2="800" y2="425" stroke="{INK}" stroke-width="14" stroke-linecap="round"/>')
    return ficha("#ECEFF1", "#90A4AE", "TORNILLO · JUBILADO", "DON TORNILLO", "En mis tiempos, los muebles duraban 40 años.", "".join(s))


PERSONAJES = [("01_byron", byron), ("02_socrates", socrates), ("03_tinto", tinto), ("04_dona_gertrudis", gertrudis), ("05_don_tornillo", don_tornillo)]


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for nombre, fn in PERSONAJES:
        with open(os.path.join(out, nombre + ".svg"), "w", encoding="utf-8") as fh:
            fh.write(fn())
    print("ok")


if __name__ == "__main__":
    main()
