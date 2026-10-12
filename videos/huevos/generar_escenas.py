"""Video: ¿Qué le pasa a tu cuerpo si comes 50 huevos en un día? (protagonista: Rayo).

Reutiliza los dibujos de ../rayo/generar_escenas.py.
Uso: python3 generar_escenas.py <carpeta_salida>
"""
import json
import math
import os
import sys
from html import escape

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "rayo"))
from generar_escenas import (  # noqa: E402
    BRAZOS, DEFS, GY, H, INK, PIERNAS, W, casco, cielo, corazon, envolver, fmt, montanas, persona, subtitulo,
)

# Valores por huevo grande (~50 g comestibles, USDA)
KCAL, PROT, GRASA, SAT, COL, COLINA = 72, 6.3, 4.8, 1.6, 186, 147

# ------------------------------------------------------------------ guion
E = []


def esc(narr, **spec):
    E.append((narr, spec))


esc("¿Qué le pasaría a tu cuerpo si te comieras cincuenta huevos en un solo día? Hoy, Rayo lo va a averiguar... por nosotros.",
    fondo="cocina", rayo=dict(pose="senala", x=420), mesa=50, titulo=("50 HUEVOS", "en un solo día"))
esc("Antes de empezar: esto es un experimento imaginario. Por favor, no lo intentes en casa.",
    fondo="plano", icono=("alerta", 1250, 470), rayo=dict(pose="normal", x=520))
esc("La idea no es nueva. En la película Cool Hand Luke, de mil novecientos sesenta y siete, el protagonista apuesta que puede comerse cincuenta huevos duros en una hora.",
    fondo="plano", icono=("claqueta", 1300, 450), rayo=dict(pose="piensa", x=520))
esc("Y en la vida real, la campeona de comida competitiva Sonya Thomas se comió sesenta y cinco huevos duros en seis minutos y cuarenta segundos.",
    fondo="plano", icono=("trofeo", 1080, 500), tarjeta=dict(titulo="Récord", numero="65", unidad="huevos en 6:40", x=1600, y=180, chica=True),
    rayo=dict(pose="celebra", x=520))
esc("Rayo tiene frente a él cincuenta huevos cocidos. Sin cáscara, son unos dos kilos y medio de comida.",
    fondo="cocina", rayo=dict(pose="normal", x=420), mesa=50,
    tarjeta=dict(titulo="Peso total", numero="2,5 kg", unidad="de huevo cocido"))
esc("Huevo número uno. Todo normal. Un huevo grande tiene unas setenta calorías y seis gramos de proteína de muy buena calidad.",
    fondo="cocina", rayo=dict(pose="come", x=420), mesa=49, contador=1,
    tarjeta=dict(titulo="1 huevo", filas=[("Calorías", "72"), ("Proteína", "6 g"), ("Grasa", "5 g")]))
esc("Hasta tres huevos al día, la gran mayoría de personas sanas no tiene ningún problema. Hasta aquí, Rayo va perfecto.",
    fondo="cocina", rayo=dict(pose="pulgar", x=420), mesa=47, contador=3, icono=("check", 1400, 430))
esc("Con cinco huevos, Rayo ya comió más proteína que en un almuerzo normal.",
    fondo="cocina", rayo=dict(pose="come", x=420, panza=10), mesa=45, contador=5,
    tarjeta=dict(titulo="Proteína", numero="32 g", unidad="≈ un almuerzo completo"))
esc("Huevo diez. Ya lleva unos sesenta gramos de proteína: más o menos lo que un adulto necesita en todo un día.",
    fondo="cocina", rayo=dict(pose="come", x=420, panza=25), mesa=40, contador=10,
    tarjeta=dict(titulo="Proteína", barras=[("Necesidad diaria", 60, 60, "#90A4AE"), ("Rayo", 63, 60, "#1E88E5")], unidad_barra="g"))
esc("La proteína y la grasa del huevo hacen que el estómago se vacíe más despacio. Por eso los huevos llenan tanto.",
    fondo="plano", icono=("estomago", 1300, 470, 0.25), rayo=dict(pose="normal", x=520, panza=25), contador=10)
esc("Huevo quince. La llenura empieza en serio. El estómago le manda al cerebro una señal muy clara: ¡ya basta!",
    fondo="cocina", rayo=dict(pose="come", x=420, panza=40, sudor=True), mesa=35, contador=15,
    burbuja=dict(texto="¡YA BASTA!", x=1250, y=340, de=(640, 360)))
esc("Huevo veinte. Mil cuatrocientas cuarenta calorías. Casi lo que muchas personas comen en todo un día.",
    fondo="cocina", rayo=dict(pose="come", x=420, panza=55, sudor=True), mesa=30, contador=20,
    tarjeta=dict(titulo="Calorías", barras=[("Un día normal", 2000, 2000, "#90A4AE"), ("Rayo", 20 * KCAL, 2000, "#FB8C00")], unidad_barra="kcal"))
esc("Y unos tres mil setecientos miligramos de colesterol. Durante años se recomendó no pasar de trescientos al día.",
    fondo="cocina", rayo=dict(pose="normal", x=420, panza=55), mesa=30, contador=20,
    tarjeta=dict(titulo="Colesterol", barras=[("Antiguo límite", 300, 3720, "#90A4AE"), ("Rayo", 20 * COL, 3720, "#E53935")], unidad_barra="mg"))
esc("Pero ojo: en la mayoría de personas, el colesterol de la comida sube poco el de la sangre, porque el hígado produce menos cuando comemos más.",
    fondo="plano", icono=("higado", 1300, 470), rayo=dict(pose="piensa", x=520, panza=55), contador=20)
esc("Hay un caso famoso: un señor de ochenta y ocho años que comía unos veinticinco huevos diarios y tenía el colesterol normal. Los médicos lo publicaron porque era algo excepcional.",
    fondo="plano", personas=[dict(tipo="abuelo", x=1000, pose="feliz", mira=-1)], mesa_x=1180, mesa=25, rayo=dict(pose="normal", x=480, panza=55),
    tarjeta=dict(titulo="Caso real · 1991", numero="25", unidad="huevos al día", x=1560, y=40, chica=True))
esc("Huevo veinticinco. Mitad del reto. El estómago se estira como un globo: puede pasar de un litro a varios litros de capacidad.",
    fondo="cocina", rayo=dict(pose="panza", x=420, panza=70, sudor=True), mesa=25, contador=25, icono=("estomago", 1400, 450, 0.5))
esc("Aparecen la pesadez, los eructos y las ganas de dormir. El cuerpo manda mucha sangre al sistema digestivo.",
    fondo="cocina", rayo=dict(pose="triste", x=420, panza=70, zzz=True), mesa=25, contador=25, onomatopeya=("¡BURP!", 1350, 380))
esc("Huevo treinta. Ya van casi cincuenta gramos de grasa saturada: más del doble del límite recomendado para todo un día.",
    fondo="cocina", rayo=dict(pose="come", x=420, panza=80, sudor=True), mesa=20, contador=30,
    tarjeta=dict(titulo="Grasa saturada", barras=[("Límite diario", 22, 48, "#90A4AE"), ("Rayo", 30 * SAT, 48, "#8E24AA")], unidad_barra="g"))
esc("Huevo treinta y cinco. Náuseas. El estómago está tan lleno que el cuerpo considera devolverlo todo.",
    fondo="cocina", rayo=dict(pose="panza", x=420, panza=90, nausea=True), mesa=15, contador=35)
esc("Huevo cuarenta. Aquí aparece un nutriente poco conocido: la colina. Cuarenta huevos tienen casi seis mil miligramos.",
    fondo="cocina", rayo=dict(pose="come", x=420, panza=100, sudor=True), mesa=10, contador=40,
    tarjeta=dict(titulo="Colina", barras=[("Límite máximo", 3500, 5880, "#90A4AE"), ("Rayo", 40 * COLINA, 5880, "#00897B")], unidad_barra="mg"))
esc("El límite máximo para adultos es de tres mil quinientos. Pasarse puede causar sudor, presión baja... y un olor corporal a pescado.",
    fondo="plano", icono=("pescado", 1300, 450), rayo=dict(pose="normal", x=520, panza=100, sudor=True), contador=40)
esc("Sí: Rayo podría empezar a oler a pescado. Y ni el casco lo salvaría.",
    fondo="cocina", rayo=dict(pose="triste", x=420, panza=100, olor=True), mesa=10, contador=40,
    personas=[dict(tipo="campesino", x=1500, pose="corre", mira=1)])
esc("Huevo cuarenta y cinco. También supera el límite diario de vitamina A y de selenio. Un solo día no suele ser grave, pero repetirlo sí puede serlo.",
    fondo="cocina", rayo=dict(pose="come", x=420, panza=110, sudor=True), mesa=5, contador=45,
    tarjeta=dict(titulo="Pasa el límite de:", filas=[("Vitamina A", "⚠"), ("Selenio", "⚠"), ("Colina", "⚠")]))
esc("¡Huevo cincuenta! Rayo lo logró. En total: tres mil seiscientas calorías, trescientos quince gramos de proteína y doscientos cuarenta de grasa.",
    fondo="cocina", rayo=dict(pose="celebra", x=420, panza=120), mesa=0, contador=50, confeti=True,
    tarjeta=dict(titulo="Total del día", filas=[("Calorías", "3.600"), ("Proteína", "315 g"), ("Grasa", "240 g"), ("Colesterol", "9.300 mg")]))
esc("Comparado con lo recomendado, es una locura: unas cinco veces la proteína que necesita y treinta veces el colesterol de la antigua recomendación.",
    fondo="plano", rayo=dict(pose="panza", x=420, panza=120),
    tarjeta=dict(titulo="Rayo vs. lo normal", grande=True, filas=[("Proteína", "×5"), ("Calorías", "×1,8"), ("Colesterol", "×31"), ("Colina", "×2")]))
esc("Una hora después. El estómago trabaja a toda máquina. Rayo se siente pesado y con muchísimo sueño.",
    fondo="cuarto", rayo=dict(pose="triste", x=520, panza=120, zzz=True), reloj="+1 HORA")
esc("Dos horas después. El huevo es rico en azufre, y las bacterias del intestino lo convierten en un gas con olor a... huevo podrido.",
    fondo="cuarto", rayo=dict(pose="triste", x=520, panza=110), reloj="+2 HORAS", icono=("gas", 900, 720))
esc("Cuatro horas después. Tanta proteína produce mucha urea, que los riñones tienen que eliminar. Rayo tiene sed y va al baño más seguido.",
    fondo="plano", icono=("rinones", 1300, 450), rayo=dict(pose="normal", x=520, panza=100, vaso=True), reloj="+4 HORAS")
esc("Digerir tanta proteína gasta energía y genera calor. Rayo puede sentirse acalorado y sudoroso.",
    fondo="plano", icono=("termometro", 1300, 450), rayo=dict(pose="normal", x=520, panza=95, sudor=True), reloj="+6 HORAS")
esc("En la noche, dormir es difícil: acidez, gases y un estómago que todavía no termina el trabajo.",
    fondo="noche", rayo=dict(pose="triste", x=700, panza=90), reloj="+10 HORAS", icono=("gas", 1050, 700))
esc("Al día siguiente, la báscula marca más, pero casi todo es comida y agua. De grasa real, apenas unos doscientos gramos.",
    fondo="plano", icono=("bascula", 1150, 700), rayo=dict(pose="piensa", x=520, panza=40), reloj="+1 DÍA",
    tarjeta=dict(titulo="Grasa ganada", numero="0,2 kg", unidad="el resto es agua y comida", x=1560, y=120, chica=True))
esc("Y como el huevo no tiene nada de fibra, lo más probable es que Rayo pase un par de días... bastante estreñido.",
    fondo="plano", rayo=dict(pose="triste", x=520, panza=40), reloj="+2 DÍAS",
    tarjeta=dict(titulo="Fibra en 50 huevos", numero="0 g", unidad="necesitas 25 a 30 g al día"))
esc("¿Y si fueran crudos? Peor: aumenta el riesgo de salmonela, y la clara cruda bloquea la biotina, una vitamina del grupo B.",
    fondo="plano", icono=("alerta", 1500, 470), rayo=dict(pose="piensa", x=520), huevo_crudo=(1000, 700))
esc("Para personas con problemas de riñón, hígado, vesícula o del corazón, un reto así podría ser peligroso de verdad.",
    fondo="plano", personas=[dict(tipo="medico", x=1250, pose="normal", mira=-1)], rayo=dict(pose="normal", x=520),
    burbuja=dict(texto="¡Consulta a tu médico!", x=1250, y=170, de=(1230, 330)))
esc("¿Y si lo hiciera todos los días? Subiría de peso muy rápido, y el exceso de vitamina A y colina podría dañarle el hígado.",
    fondo="plano", icono=("calendario", 1300, 450), rayo=dict(pose="triste", x=520, panza=120))
esc("La buena noticia: para la mayoría de adultos sanos, comer de uno a tres huevos al día es una excelente opción.",
    fondo="cocina", rayo=dict(pose="pulgar", x=420), mesa=2, icono=("check", 1450, 430))
esc("El huevo tiene proteína de alta calidad, vitamina B doce y D, colina para el cerebro y luteína para los ojos.",
    fondo="plano", rayo=dict(pose="saluda", x=420),
    tarjeta=dict(titulo="Lo bueno del huevo", filas=[("Proteína", "✔"), ("Vitamina B12 y D", "✔"), ("Colina (cerebro)", "✔"), ("Luteína (ojos)", "✔")]))
esc("En resumen: el huevo es un gran alimento, pero hasta lo bueno, en exceso, hace daño.",
    fondo="plano", rayo=dict(pose="normal", x=520), icono=("balanza", 1300, 470))
esc("¿Y Rayo? No quiere ver un huevo en un mes. ¿Qué reto quieres que Rayo pruebe en el próximo video? Escríbelo en los comentarios.",
    fondo="cocina", rayo=dict(pose="saluda", x=420), mesa=0, titulo=("¿PRÓXIMO RETO?", "Escríbelo en los comentarios"))
esc("Y suscríbete, para no perderte la próxima locura de Rayo.",
    fondo="plano", rayo=dict(pose="celebra", x=520), suscribete=True)


# --------------------------------------------------------------- dibujos
def fondo(tipo):
    s = []
    if tipo == "cocina":
        s.append(f'<rect width="{W}" height="{H}" fill="#FFF3E0"/>')
        for y in range(0, GY, 90):
            for x in range(0 if (y // 90) % 2 == 0 else -45, W, 90):
                s.append(f'<rect x="{x}" y="{y}" width="88" height="88" fill="#FFE0B2" opacity="0.55"/>')
        # ventana
        # estufa y olla
        s.append(f'<rect x="1550" y="{GY-330}" width="330" height="330" fill="#ECEFF1" stroke="{INK}" stroke-width="7"/>'
                 f'<rect x="1590" y="{GY-230}" width="250" height="180" rx="8" fill="#37474F"/>'
                 f'<path d="M1610 {GY-330} L1610 {GY-400} L1830 {GY-400} L1830 {GY-330}" fill="#B0BEC5" stroke="{INK}" stroke-width="7"/>'
                 f'<path d="M1650 {GY-430} q 15 -25 0 -50 M1720 {GY-430} q 15 -25 0 -50 M1790 {GY-430} q 15 -25 0 -50" stroke="#B0BEC5" stroke-width="7" fill="none" stroke-linecap="round"/>')
        s.append(f'<rect x="0" y="{GY}" width="{W}" height="{H-GY}" fill="#BCAAA4"/>'
                 f'<rect x="0" y="{GY}" width="{W}" height="10" fill="#8D6E63"/>')
    elif tipo == "cuarto":
        s.append(f'<rect width="{W}" height="{H}" fill="#E8EAF6"/>')
        s.append(f'<rect x="1350" y="140" width="320" height="230" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>'
                 f'<circle cx="1510" cy="255" r="70" fill="#FFD54F"/>')
        s.append(sofa(800))
        s.append(f'<rect x="0" y="{GY}" width="{W}" height="{H-GY}" fill="#A1887F"/>')
    elif tipo == "noche":
        s.append(cielo("noche", __import__("random").Random(5)))
        s.append(montanas(True))
        s.append(f'<rect x="0" y="{GY}" width="{W}" height="{H-GY}" fill="#3E2F5B"/>')
    else:  # plano tipo infografía
        s.append(f'<rect width="{W}" height="{H}" fill="#F4F7FB"/>')
        for x in range(0, W, 80):
            s.append(f'<line x1="{x}" y1="0" x2="{x}" y2="{GY}" stroke="#E3E9F2" stroke-width="2"/>')
        for y in range(0, GY, 80):
            s.append(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="#E3E9F2" stroke-width="2"/>')
        s.append(f'<rect x="0" y="{GY}" width="{W}" height="{H-GY}" fill="#CFD8DC"/>')
    return "".join(s)


def sofa(x):
    return (f'<g transform="translate({x} {GY})"><rect x="-260" y="-260" width="520" height="150" rx="40" fill="#7986CB" stroke="{INK}" stroke-width="7"/>'
            f'<rect x="-300" y="-150" width="600" height="110" rx="30" fill="#5C6BC0" stroke="{INK}" stroke-width="7"/>'
            f'<rect x="-280" y="-40" width="30" height="40" fill="{INK}"/><rect x="250" y="-40" width="30" height="40" fill="{INK}"/></g>')


def huevo(x, y, k=1.0, crudo=False):
    if crudo:
        return (f'<g transform="translate({x} {y}) scale({k})"><path d="M-90 10 C -110 -40 -40 -60 0 -45 C 50 -70 120 -30 95 15 C 80 50 -70 50 -90 10 Z" '
                f'fill="#FFFFFF" fill-opacity="0.85" stroke="{INK}" stroke-width="5"/><circle cx="0" cy="-5" r="32" fill="#FFB300" stroke="{INK}" stroke-width="5"/>'
                f'<circle cx="-10" cy="-15" r="9" fill="#FFE082"/></g>')
    return (f'<g transform="translate({x} {y}) scale({k})"><ellipse cx="0" cy="0" rx="22" ry="29" fill="#FFF8E7" stroke="{INK}" stroke-width="4"/>'
            f'<ellipse cx="-7" cy="-10" rx="6" ry="9" fill="#FFFFFF"/></g>')


def mesa(n, x0=560):
    """Mesa con n huevos apilados en pirámide."""
    top = GY - 260
    s = [f'<rect x="{x0}" y="{top}" width="560" height="26" rx="8" fill="#A1887F" stroke="{INK}" stroke-width="6"/>',
         f'<rect x="{x0+25}" y="{top+26}" width="22" height="234" fill="#8D6E63" stroke="{INK}" stroke-width="5"/>',
         f'<rect x="{x0+513}" y="{top+26}" width="22" height="234" fill="#8D6E63" stroke="{INK}" stroke-width="5"/>',
         f'<ellipse cx="{x0+280}" cy="{top}" rx="265" ry="16" fill="#ECEFF1" stroke="{INK}" stroke-width="5"/>']
    fila, restantes, y = 12, n, top - 26
    while restantes > 0 and fila > 0:
        k = min(fila, restantes)
        ancho = k * 42
        for i in range(k):
            s.append(huevo(x0 + 280 - ancho / 2 + 21 + i * 42, y, 0.9))
        restantes -= k
        fila -= 1
        y -= 46
    return "".join(s)


def rayo(x, pose="normal", mira=1, panza=0, sudor=False, nausea=False, zzz=False, olor=False, vaso=False):
    br = BRAZOS.get(pose)
    if pose == "come":
        br = ["0,-380 -45,-280 -55,-190", "0,-385 150,-420 185,-505"]
    elif pose == "panza":
        r = 40 + panza
        br = [f"0,-380 -40,-330 {fmt(-10)},-300", f"0,-380 {fmt(r*0.6)},-360 {fmt(r*0.9+20)},-300"]
    pi = PIERNAS.get(pose, PIERNAS["normal"])
    s = [f'<g transform="translate({x} {GY}) scale({mira} 1)">',
         f'<g stroke="{INK}" stroke-width="20" stroke-linecap="round" stroke-linejoin="round" fill="none">',
         '<line x1="0" y1="-465" x2="0" y2="-195"/>']
    for p in pi:
        s.append(f'<polyline points="{p}"/>')
    s.append('</g>')
    if panza:
        r = 40 + panza
        s.append(f'<ellipse cx="{fmt(r*0.55)}" cy="-300" rx="{fmt(r)}" ry="{fmt(r*0.85)}" fill="#FFFFFF" stroke="{INK}" stroke-width="14"/>')
        if panza > 60:
            s.append(f'<path d="M{fmt(r*0.55-r*0.5)} -300 q {fmt(r*0.25)} 12 {fmt(r*0.5)} 0" stroke="#B0BEC5" stroke-width="6" fill="none"/>')
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
        s.append('<g stroke="#2F8DEB" stroke-width="9" stroke-linecap="round" fill="none">'
                 '<path d="M285 -560 Q305 -540 300 -510"/><path d="M315 -585 Q345 -545 335 -495"/></g>')
    rot = ' transform="rotate(14 0 -460)"' if pose == "triste" else ""
    s.append(f'<g{rot}>{casco()}</g>')
    if pose == "come":
        s.append(huevo(178, -540, 1.1) + f'<circle cx="185" cy="-505" r="17" fill="{INK}"/>')
    if sudor:
        s.append('<g fill="#4FC3F7" stroke="#0277BD" stroke-width="3">'
                 '<path d="M-170 -640 q -12 22 0 30 q 12 -8 0 -30 Z"/><path d="M200 -690 q -12 22 0 30 q 12 -8 0 -30 Z"/>'
                 '<path d="M215 -600 q -10 18 0 25 q 10 -7 0 -25 Z"/></g>')
    if nausea:
        s.append('<g stroke="#43A047" stroke-width="9" fill="none" stroke-linecap="round">'
                 '<path d="M190 -720 a 25 25 0 1 1 -10 40"/><path d="M-200 -700 a 22 22 0 1 0 10 38"/></g>'
                 f'<ellipse cx="40" cy="-560" rx="200" ry="200" fill="#66BB6A" opacity="0.18"/>')
    if zzz:
        s.append(f'<g font-family="Arial Black, Arial" font-weight="900" fill="#5C6BC0"><text x="-230" y="-640" font-size="50">Z</text>'
                 '<text x="-290" y="-700" font-size="65">Z</text><text x="-370" y="-770" font-size="80">Z</text></g>')
    if olor:
        s.append('<g stroke="#9CCC65" stroke-width="10" fill="none" stroke-linecap="round" opacity="0.9">'
                 '<path d="M-150 -500 q -30 -40 0 -80 q 30 -40 0 -80"/><path d="M230 -480 q -30 -40 0 -80 q 30 -40 0 -80"/>'
                 '<path d="M-220 -330 q -30 -40 0 -80 q 30 -40 0 -80"/></g>' + pescado(330, -330, 0.6))
    s.append('</g>')
    return "".join(s)


# ----------------------------------------------------------------- iconos
def pescado(x, y, k=1.0):
    return (f'<g transform="translate({x} {y}) scale({k})"><path d="M-120 0 C -60 -80 70 -80 110 0 C 70 80 -60 80 -120 0 Z" fill="#4FC3F7" stroke="{INK}" stroke-width="7"/>'
            f'<path d="M110 0 L 180 -60 L 170 0 L 180 60 Z" fill="#29B6F6" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<circle cx="-70" cy="-12" r="12" fill="{INK}"/><path d="M-20 -40 q 25 40 0 80 M 20 -45 q 25 45 0 90" stroke="#0288D1" stroke-width="6" fill="none"/></g>')


def icono(nombre, x, y, extra=None):
    if nombre == "alerta":
        return (f'<g transform="translate({x} {y})"><polygon points="0,-230 230,170 -230,170" fill="#FFC107" stroke="{INK}" stroke-width="12" stroke-linejoin="round"/>'
                f'<rect x="-22" y="-110" width="44" height="170" rx="18" fill="{INK}"/><circle cx="0" cy="115" r="26" fill="{INK}"/></g>')
    if nombre == "claqueta":
        return (f'<g transform="translate({x} {y})"><rect x="-240" y="-110" width="480" height="300" rx="14" fill="#263238" stroke="{INK}" stroke-width="8"/>'
                f'<g transform="rotate(-12 -240 -110)"><rect x="-240" y="-200" width="480" height="80" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
                + "".join(f'<polygon points="{-220+i*95},-200 {-170+i*95},-200 {-210+i*95},-120 {-260+i*95},-120" fill="{INK}"/>' for i in range(5)) + '</g>'
                f'<text x="0" y="40" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="64" fill="#FFFFFF">1967</text>'
                f'<text x="0" y="130" text-anchor="middle" font-family="Arial" font-weight="bold" font-size="46" fill="#FFD54F">50 huevos / 1 hora</text></g>')
    if nombre == "trofeo":
        return (f'<g transform="translate({x} {y})"><path d="M-150 -200 L 150 -200 L 120 20 C 100 90 -100 90 -120 20 Z" fill="#FFC107" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
                f'<path d="M-150 -160 C -260 -160 -250 0 -120 0 M150 -160 C 260 -160 250 0 120 0" fill="none" stroke="{INK}" stroke-width="12"/>'
                f'<rect x="-30" y="80" width="60" height="90" fill="#FFB300" stroke="{INK}" stroke-width="8"/>'
                f'<rect x="-130" y="170" width="260" height="60" rx="10" fill="#8D6E63" stroke="{INK}" stroke-width="8"/>'
                + huevo(0, -80, 2.2) + '</g>')
    if nombre == "check":
        return (f'<g transform="translate({x} {y})"><circle r="170" fill="#43A047" stroke="{INK}" stroke-width="10"/>'
                f'<polyline points="-80,0 -20,65 90,-60" fill="none" stroke="#FFFFFF" stroke-width="36" stroke-linecap="round" stroke-linejoin="round"/></g>')
    if nombre == "estomago":
        lleno = extra if extra is not None else 0.5
        alto = 380
        return (f'<g transform="translate({x} {y})"><defs><clipPath id="clipest"><path d="M-60 -200 C -60 -140 -40 -120 -90 -60 C -190 60 -120 210 40 200 C 200 190 230 40 150 -40 '
                f'C 90 -100 40 -60 20 -200 Z"/></clipPath></defs>'
                f'<path d="M-60 -200 C -60 -140 -40 -120 -90 -60 C -190 60 -120 210 40 200 C 200 190 230 40 150 -40 C 90 -100 40 -60 20 -200 Z" fill="#F8BBD0"/>'
                f'<rect x="-250" y="{fmt(200 - alto*lleno)}" width="500" height="{fmt(alto*lleno)}" fill="#FFE082" clip-path="url(#clipest)"/>'
                + "".join(huevo(-60 + (i % 4) * 55, 170 - (i // 4) * 60, 0.7) for i in range(int(lleno * 14)))
                + f'<path d="M-60 -200 C -60 -140 -40 -120 -90 -60 C -190 60 -120 210 40 200 C 200 190 230 40 150 -40 C 90 -100 40 -60 20 -200 Z" fill="none" stroke="{INK}" stroke-width="10"/>'
                f'<text x="20" y="290" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="54" fill="{INK}">{int(lleno*100)}% lleno</text></g>')
    if nombre == "higado":
        return (f'<g transform="translate({x} {y})"><path d="M-230 -40 C -230 -160 120 -190 230 -110 C 270 -60 160 40 40 110 C -80 180 -230 120 -230 -40 Z" fill="#A1453A" stroke="{INK}" stroke-width="10"/>'
                f'<path d="M-30 -150 C -10 -60 -20 40 30 110" stroke="#7B2E26" stroke-width="8" fill="none"/>'
                f'<text x="0" y="230" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="52" fill="{INK}">HÍGADO</text>'
                f'<text x="0" y="290" text-anchor="middle" font-family="Arial" font-weight="bold" font-size="38" fill="#455A64">regula el colesterol</text></g>')
    if nombre == "rinones":
        rin = ('<path d="M0 -120 C 90 -120 110 -20 60 0 C 110 20 90 120 0 120 C -80 120 -90 -120 0 -120 Z" fill="#C62828" stroke="#1A1A1A" stroke-width="9"/>')
        return (f'<g transform="translate({x} {y})"><g transform="translate(-140 0) scale(-1 1)">{rin}</g><g transform="translate(140 0)">{rin}</g>'
                f'<path d="M-90 40 L -40 180 M90 40 L 40 180" stroke="#F48FB1" stroke-width="16" fill="none" stroke-linecap="round"/>'
                f'<text x="0" y="260" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="52" fill="{INK}">RIÑONES</text>'
                f'<text x="0" y="320" text-anchor="middle" font-family="Arial" font-weight="bold" font-size="38" fill="#455A64">eliminan la urea</text></g>')
    if nombre == "termometro":
        return (f'<g transform="translate({x} {y})"><rect x="-45" y="-260" width="90" height="360" rx="45" fill="#FFFFFF" stroke="{INK}" stroke-width="10"/>'
                f'<rect x="-20" y="-160" width="40" height="260" fill="#E53935"/><circle cx="0" cy="140" r="80" fill="#E53935" stroke="{INK}" stroke-width="10"/>'
                + "".join(f'<line x1="45" y1="{-220+i*50}" x2="80" y2="{-220+i*50}" stroke="{INK}" stroke-width="6"/>' for i in range(6))
                + f'<g stroke="#FF7043" stroke-width="10" fill="none" stroke-linecap="round"><path d="M150 -150 q 30 -30 0 -60"/><path d="M200 -100 q 30 -30 0 -60"/></g></g>')
    if nombre == "gas":
        return (f'<g transform="translate({x} {y})" opacity="0.85"><g fill="#AED581" stroke="#558B2F" stroke-width="6">'
                f'<circle cx="0" cy="0" r="70"/><circle cx="80" cy="-40" r="60"/><circle cx="150" cy="10" r="55"/><circle cx="60" cy="40" r="60"/></g>'
                f'<text x="70" y="25" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="60" fill="#33691E">S</text></g>')
    if nombre == "bascula":
        return (f'<g transform="translate({x} {y})"><rect x="-210" y="-60" width="420" height="120" rx="30" fill="#ECEFF1" stroke="{INK}" stroke-width="10"/>'
                f'<rect x="-90" y="-40" width="180" height="70" rx="10" fill="#263238"/>'
                f'<text x="0" y="15" text-anchor="middle" font-family="Courier New, monospace" font-weight="bold" font-size="48" fill="#76FF03">+2,8</text></g>')
    if nombre == "calendario":
        return (f'<g transform="translate({x} {y})"><rect x="-230" y="-200" width="460" height="420" rx="20" fill="#FFFFFF" stroke="{INK}" stroke-width="10"/>'
                f'<rect x="-230" y="-200" width="460" height="100" rx="20" fill="#E53935" stroke="{INK}" stroke-width="10"/>'
                f'<text x="0" y="-130" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="50" fill="#FFFFFF">TODOS LOS DÍAS</text>'
                + "".join(huevo(-170 + (i % 5) * 85, -40 + (i // 5) * 85, 1.0) for i in range(15)) + '</g>')
    if nombre == "balanza":
        return (f'<g transform="translate({x} {y})"><line x1="0" y1="-220" x2="0" y2="200" stroke="{INK}" stroke-width="16"/>'
                f'<rect x="-120" y="190" width="240" height="40" rx="10" fill="#8D6E63" stroke="{INK}" stroke-width="8"/>'
                f'<g transform="rotate(-10)"><line x1="-260" y1="-180" x2="260" y2="-180" stroke="{INK}" stroke-width="14"/>'
                f'<path d="M-330 -60 L -260 -180 L -190 -60 M190 -60 L 260 -180 L 330 -60" fill="none" stroke="{INK}" stroke-width="6"/>'
                f'<ellipse cx="-260" cy="-60" rx="80" ry="18" fill="#B0BEC5" stroke="{INK}" stroke-width="6"/><ellipse cx="260" cy="-60" rx="80" ry="18" fill="#B0BEC5" stroke="{INK}" stroke-width="6"/>'
                + huevo(-280, -100, 1.0) + huevo(-240, -100, 1.0)
                + f'<text x="260" y="-90" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="44" fill="#E53935">×50</text></g>'
                f'<text x="-260" y="320" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="44" fill="#43A047">BIEN</text>'
                f'<text x="260" y="320" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="44" fill="#E53935">EXCESO</text></g>')
    if nombre == "pescado":
        return pescado(x, y, 1.6)
    return ""


def tarjeta(titulo="", numero=None, unidad="", filas=None, barras=None, unidad_barra="", x=1440, y=150, chica=False, grande=False):
    w = 560 if chica else (820 if grande else 760)
    h_tit = 90
    if numero is not None:
        h = (330 if chica else 380) + 48 * (len(envolver(unidad, 40, w - 60)) - 1)
    elif filas:
        h = h_tit + 40 + len(filas) * 95
    else:
        h = h_tit + 60 + len(barras) * 130
    x0 = x - w / 2 if (chica or grande) else 1840 - w
    y0 = y if (chica or grande) else 110
    s = [f'<rect x="{fmt(x0+10)}" y="{y0+12}" width="{w}" height="{h}" rx="30" fill="#000000" opacity="0.15"/>',
         f'<rect x="{fmt(x0)}" y="{y0}" width="{w}" height="{h}" rx="30" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>',
         f'<path d="M{fmt(x0)} {y0+30} a 30 30 0 0 1 30 -30 h {w-60} a 30 30 0 0 1 30 30 v {h_tit-30} h {-w} Z" fill="#1E88E5" stroke="{INK}" stroke-width="8"/>',
         f'<text x="{fmt(x0+w/2)}" y="{y0+63}" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="48" fill="#FFFFFF">{escape(titulo)}</text>']
    cx = x0 + w / 2
    if numero is not None:
        fs = min(130 if chica else 170, int((w - 60) / (len(numero) * 0.64)))
        s.append(f'<text x="{fmt(cx)}" y="{y0+h_tit+(150 if chica else 190)}" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="{fs}" fill="{INK}">{escape(numero)}</text>')
        lineas = envolver(unidad, 40, w - 60)
        for i, l in enumerate(lineas):
            s.append(f'<text x="{fmt(cx)}" y="{y0+h-(len(lineas)-i)*48+20}" text-anchor="middle" font-family="Arial" font-weight="bold" font-size="40" fill="#455A64">{escape(l)}</text>')
    elif filas:
        for i, (k, v) in enumerate(filas):
            yy = y0 + h_tit + 75 + i * 95
            s.append(f'<text x="{fmt(x0+45)}" y="{yy}" font-family="Arial" font-weight="bold" font-size="52" fill="{INK}">{escape(k)}</text>')
            col = "#E53935" if v in ("⚠",) or v.startswith("×") else ("#43A047" if v == "✔" else "#1E88E5")
            s.append(f'<text x="{fmt(x0+w-45)}" y="{yy}" text-anchor="end" font-family="Arial Black, Arial" font-weight="900" font-size="60" fill="{col}">{escape(v)}</text>')
            if i < len(filas) - 1:
                s.append(f'<line x1="{fmt(x0+40)}" y1="{yy+30}" x2="{fmt(x0+w-40)}" y2="{yy+30}" stroke="#E0E0E0" stroke-width="4"/>')
    else:
        maxv = max(b[2] for b in barras)
        ancho = w - 90
        for i, (k, v, _m, col) in enumerate(barras):
            yy = y0 + h_tit + 50 + i * 130
            largo = ancho * min(v / maxv, 1.0)
            s.append(f'<text x="{fmt(x0+45)}" y="{yy}" font-family="Arial" font-weight="bold" font-size="40" fill="{INK}">{escape(k)}</text>')
            s.append(f'<rect x="{fmt(x0+45)}" y="{yy+15}" width="{fmt(max(largo, 14))}" height="56" rx="12" fill="{col}" stroke="{INK}" stroke-width="5"/>')
            etiqueta = f"{v:,.0f} {unidad_barra}".replace(",", ".")
            tx = x0 + 45 + largo - 15 if largo > 300 else x0 + 45 + largo + 15
            anchor = "end" if largo > 300 else "start"
            colt = "#FFFFFF" if largo > 300 else INK
            s.append(f'<text x="{fmt(tx)}" y="{yy+57}" text-anchor="{anchor}" font-family="Arial Black, Arial" font-weight="900" font-size="38" fill="{colt}">{escape(etiqueta)}</text>')
    return "".join(s)


def contador(n):
    p = n / 50
    return (f'<g transform="translate(620 36)"><rect width="430" height="150" rx="26" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
            + huevo(70, 70, 1.6)
            + f'<text x="140" y="68" font-family="Arial" font-weight="bold" font-size="38" fill="#455A64">HUEVO</text>'
            f'<text x="140" y="125" font-family="Arial Black, Arial" font-weight="900" font-size="64" fill="{INK}">{n}<tspan font-size="40" fill="#90A4AE"> / 50</tspan></text>'
            f'<rect x="0" y="170" width="430" height="26" rx="13" fill="#ECEFF1" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="0" y="170" width="{fmt(max(430*p, 26))}" height="26" rx="13" fill="#FFB300" stroke="{INK}" stroke-width="5"/></g>')


def reloj(texto):
    return (f'<g transform="translate(620 36)"><rect width="470" height="150" rx="26" fill="#263238" stroke="{INK}" stroke-width="8"/>'
            f'<g transform="translate(75 75)"><circle r="52" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
            f'<line x1="0" y1="0" x2="0" y2="-36" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>'
            f'<line x1="0" y1="0" x2="26" y2="10" stroke="#E53935" stroke-width="7" stroke-linecap="round"/></g>'
            f'<text x="150" y="98" font-family="Arial Black, Arial" font-weight="900" font-size="56" fill="#FFD54F">{escape(texto)}</text></g>')


def burbuja(texto, x, y, de):
    fs = 52
    w = len(texto) * fs * 0.6 + 80
    h = fs * 1.2 + 50
    tx, ty = de
    bx = x - w / 2
    return (f'<polygon points="{fmt(x-30)},{fmt(y+h/2-5)} {fmt(x+30)},{fmt(y+h/2-5)} {tx},{ty}" fill="#FFFFFF" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<rect x="{fmt(bx)}" y="{fmt(y-h/2)}" width="{fmt(w)}" height="{fmt(h)}" rx="34" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>'
            f'<rect x="{fmt(x-26)}" y="{fmt(y+h/2-16)}" width="52" height="14" fill="#FFFFFF"/>'
            f'<text x="{x}" y="{fmt(y+fs*0.35)}" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="{fs}" fill="{INK}">{escape(texto)}</text>')


def onomatopeya(texto, x, y):
    fs = 100
    pts = []
    for i in range(24):
        a = math.pi * 2 * i / 24
        r = (1.0 if i % 2 == 0 else 0.72) * (len(texto) * fs * 0.3 + 60)
        pts.append(f"{fmt(x + r * math.cos(a))},{fmt(y + r * 0.6 * math.sin(a))}")
    return (f'<polygon points="{" ".join(pts)}" fill="#FFEB3B" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<text x="{x}" y="{y + fs*0.35}" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="{fs}" fill="#E53935">{escape(texto)}</text>')


def titulo(t, sub):
    fs = min(150, int(1050 / (len(t) * 0.68)))
    return (f'<text x="1340" y="300" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="{fs}" fill="#FFB300" stroke="{INK}" stroke-width="12" paint-order="stroke">{escape(t)}</text>'
            f'<text x="1340" y="390" text-anchor="middle" font-family="Arial, sans-serif" font-weight="bold" font-size="64" fill="#FFFFFF" stroke="{INK}" stroke-width="8" paint-order="stroke">{escape(sub)}</text>')


def confeti():
    import random
    r = random.Random(50)
    cols = ("#E53935", "#FB8C00", "#FDD835", "#43A047", "#1E88E5", "#8E24AA")
    return "".join(f'<rect x="{r.randint(0, W)}" y="{r.randint(0, 760)}" width="18" height="34" fill="{r.choice(cols)}" transform="rotate({r.randint(0, 180)} {0} {0})" opacity="0.9"/>'
                   for _ in range(110))


def suscribete():
    return (f'<g transform="translate(1340 420)"><rect x="-380" y="-110" width="760" height="220" rx="40" fill="#E53935" stroke="{INK}" stroke-width="10"/>'
            f'<text x="0" y="35" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="110" fill="#FFFFFF">SUSCRÍBETE</text>'
            f'<g transform="translate(330 140)"><path d="M0 0 L 0 120 L 30 90 L 55 140 L 75 130 L 50 82 L 90 80 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/></g>'
            f'<g transform="translate(0 230)"><path d="M-40 -40 q 40 -60 80 0 v 50 l 15 20 h -110 l 15 -20 Z" fill="#FFD54F" stroke="{INK}" stroke-width="7"/>'
            f'<circle cx="0" cy="45" r="14" fill="#FFD54F" stroke="{INK}" stroke-width="6"/></g></g>')


def medico(x):
    return (persona(x, "medico_base", "normal", -1)
            + f'<g transform="translate({x} {GY}) scale(-0.9 0.9)"><path d="M-40 -440 C -60 -320 60 -320 40 -440" stroke="#455A64" stroke-width="10" fill="none"/>'
            f'<circle cx="0" cy="-330" r="20" fill="#B0BEC5" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M-50 -650 L 50 -650 L 40 -610 L -40 -610 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
            f'<path d="M-12 -640 h 24 v -8 h -24 Z M-4 -652 v 16 h 8 v -16 Z" fill="#E53935"/></g>')


def escena(i, narr, e):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">', DEFS, fondo(e.get("fondo", "plano"))]
    if "mesa" in e:
        s.append(mesa(e["mesa"], e.get("mesa_x", 560)))
    if "icono" in e:
        ic = e["icono"]
        s.append(icono(ic[0], ic[1], ic[2], ic[3] if len(ic) > 3 else None))
    if "huevo_crudo" in e:
        s.append(huevo(*e["huevo_crudo"], k=2.2, crudo=True))
    for p in e.get("personas", []):
        if p["tipo"] == "medico":
            s.append(medico(p["x"]))
        elif p["tipo"] == "abuelo":
            s.append(persona(p["x"], "abuelo", p.get("pose", "normal"), p.get("mira", 1)))
        else:
            s.append(persona(p["x"], p["tipo"], p.get("pose", "normal"), p.get("mira", 1)))
    r = e.get("rayo")
    if r:
        s.append(rayo(r["x"], r.get("pose", "normal"), r.get("mira", 1), r.get("panza", 0), r.get("sudor", False),
                      r.get("nausea", False), r.get("zzz", False), r.get("olor", False), r.get("vaso", False)))
    if e.get("confeti"):
        s.append(confeti())
    if "tarjeta" in e:
        s.append(tarjeta(**e["tarjeta"]))
    if "burbuja" in e:
        s.append(burbuja(**e["burbuja"]))
    if "onomatopeya" in e:
        s.append(onomatopeya(*e["onomatopeya"]))
    if "contador" in e:
        s.append(contador(e["contador"]))
    if "reloj" in e:
        s.append(reloj(e["reloj"]))
    if "titulo" in e:
        s.append(titulo(*e["titulo"]))
    if e.get("suscribete"):
        s.append(suscribete())
    s.append(subtitulo(narr))
    s.append('</svg>')
    return "".join(s)


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    guion = []
    for i, (narr, e) in enumerate(E, 1):
        with open(os.path.join(out, f"escena_{i:02d}.svg"), "w", encoding="utf-8") as f:
            f.write(escena(i, narr, e))
        guion.append({"n": i, "narracion": narr})
    with open(os.path.join(out, "guion.json"), "w", encoding="utf-8") as f:
        json.dump(guion, f, ensure_ascii=False, indent=1)
    print(len(E), "escenas")


if __name__ == "__main__":
    main()
