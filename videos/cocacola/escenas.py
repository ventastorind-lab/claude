"""Guion y dibujos: ¿Qué pasa si te tomas 50 Coca-Colas en un día? (protagonista: Byron el ajolote).

Las funciones de dibujo reciben t (segundos dentro de la escena) para poder animarse.
"""
import importlib.util
import math
import os
import random
from html import escape

AQUI = os.path.dirname(os.path.abspath(__file__))
_spec = importlib.util.spec_from_file_location("huevos_esc", os.path.join(AQUI, "..", "huevos", "generar_escenas.py"))
HV = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(HV)

W, H, GY, INK = HV.W, HV.H, HV.GY, HV.INK

# Valores por lata de 355 ml (etiqueta Coca-Cola Original)
KCAL, AZUCAR, CAFEINA, ML = 140, 39, 34, 355

E = []


def esc(narr, **spec):
    E.append((narr, spec))


# ------------------------------------------------------------------ guion
esc("¡Hola, hola! Soy Byron, el ajolote que lo prueba todo... para que tú no tengas que hacerlo. Hoy: ¿qué pasa si te tomas cincuenta Coca-Colas en un solo día?",
    fondo="cocina", byron=dict(pose="saluda", x=420, ojos="feliz"), latas=50, titulo=("50 COCA-COLAS", "en un solo día"))
esc("Tranqui, a mí todo me vuelve a crecer. A ti no. Así que no lo intentes en casa, ¿listo?",
    fondo="plano", byron=dict(pose="pulgar", x=520), icono=("alerta", 1300, 470))
esc("Cincuenta latas son casi dieciocho litros de gaseosa. ¡Eso es más que un garrafón de agua!",
    fondo="plano", byron=dict(pose="senala", x=440, boca="o", ojos="grandes"), icono=("garrafon", 1050, 600),
    tarjeta=dict(titulo="Líquido total", numero="17,7 L", unidad="de gaseosa", x=1560, y=150, chica=True))
esc("Y traen casi dos kilos de azúcar. ¡Dos kilos! Como cuatrocientos ochenta cubitos.",
    fondo="plano", byron=dict(pose="celebra", x=440, boca="o", ojos="grandes"), icono=("azucar", 1080, 640),
    tarjeta=dict(titulo="Azúcar total", numero="1,95 kg", unidad="≈ 487 cubitos", x=1560, y=150, chica=True))
esc("Lata número uno. ¡Ahhh, deliciosa! Treinta y nueve gramos de azúcar y ciento cuarenta calorías.",
    fondo="cocina", byron=dict(pose="toma", x=420), latas=49, contador=1,
    tarjeta=dict(titulo="1 lata (355 ml)", filas=[("Calorías", "140"), ("Azúcar", "39 g"), ("Cafeína", "34 mg")]))
esc("Ojo: la OMS recomienda no pasar de cincuenta gramos de azúcar al día, e idealmente menos de veinticinco. ¡Con una sola lata ya pasé el ideal!",
    fondo="cocina", byron=dict(pose="piensa", x=420, ojos="grandes"), latas=49, contador=1,
    tarjeta=dict(titulo="Azúcar", barras=[("Ideal (OMS)", 25, 50, "#90A4AE"), ("Límite (OMS)", 50, 50, "#78909C"), ("Byron", 39, 50, "#E53935")], unidad_barra="g"))
esc("Lata dos. Ya pasé el límite de azúcar del día entero. ¡Y apenas son las nueve de la mañana!",
    fondo="cocina", byron=dict(pose="toma", x=420), latas=48, contador=2, reloj_pared="9:00")
esc("El azúcar entra rapidísimo a la sangre, y el páncreas sale a gritar: ¡insulina, insulina!",
    fondo="plano", byron=dict(pose="normal", x=440), icono=("pancreas", 1250, 520),
    burbuja=dict(texto="¡INSULINA!", x=1250, y=200, de=(1250, 380)))
esc("Lata cinco. ¡Me siento invencible! Es la cafeína y el azúcar haciendo fiesta en mi cerebro.",
    fondo="cocina", byron=dict(pose="celebra", x=420, ojos="feliz", boca="grande"), latas=45, contador=5, icono=("cerebro", 1350, 420))
esc("Lata diez. Trescientos cuarenta miligramos de cafeína. Ya casi llego a los cuatrocientos que la FDA considera seguros para un adulto.",
    fondo="cocina", byron=dict(pose="toma", x=420, panza=15), latas=40, contador=10,
    tarjeta=dict(titulo="Cafeína", barras=[("Seguro (FDA)", 400, 400, "#90A4AE"), ("Byron", 10 * CAFEINA, 400, "#6D4C41")], unidad_barra="mg"))
esc("¡Y el gas! Cada lata trae dióxido de carbono que tiene que salir por algún lado... ¡BUUURP!",
    fondo="cocina", byron=dict(pose="panza", x=420, panza=20, boca="grande"), latas=40, contador=10,
    onomatopeya=("¡BUUURP!", 1250, 380), burbujas_gas=True)
esc("Lata doce. Pasé los cuatrocientos miligramos de cafeína. Me tiemblan las patitas... y no es de la emoción.",
    fondo="cocina", byron=dict(pose="normal", x=420, panza=25, tiembla=True, ojos="grandes", sudor=True), latas=38, contador=12)
esc("Lata quince. Corazón acelerado: ¡tum, tum, tum, tum! La cafeína pone el corazón a mil.",
    fondo="plano", byron=dict(pose="panza", x=440, panza=30, ojos="grandes", sudor=True), icono=("corazon", 1250, 470), contador=15)
esc("Y el baño... ¡voy cada veinte minutos! La cafeína y tanto líquido no perdonan.",
    fondo="plano", byron=dict(pose="corre", x=300, panza=30), icono=("bano", 1450, 520), contador=15)
esc("Lata veinte. Dos mil ochocientas calorías. Más de lo que necesito en todo un día... solo en gaseosa.",
    fondo="cocina", byron=dict(pose="toma", x=420, panza=45, sudor=True), latas=30, contador=20,
    tarjeta=dict(titulo="Calorías", barras=[("Un día normal", 2000, 2800, "#90A4AE"), ("Byron", 20 * KCAL, 2800, "#FB8C00")], unidad_barra="kcal"))
esc("Y setecientos ochenta gramos de azúcar. El hígado ya no sabe dónde guardar tanta fructosa, y empieza a convertirla en grasa.",
    fondo="plano", byron=dict(pose="piensa", x=440, panza=45), icono=("higado", 1300, 470), contador=20)
esc("¡Mitad del reto! Llevo casi nueve litros adentro. Mi barriga parece un globo de agua.",
    fondo="cocina", byron=dict(pose="panza", x=420, panza=75, ojos="grandes", boca="o"), latas=25, contador=25, onomatopeya=("¡GLUP!", 1300, 330))
esc("Peligro real: los riñones solo pueden sacar alrededor de un litro por hora. Si tomas muchísimo líquido muy rápido, la sangre se diluye. Eso se llama hiponatremia, y puede ser grave.",
    fondo="plano", byron=dict(pose="piensa", x=440, panza=75), icono=("rinones", 1300, 450), contador=25)
esc("Lata treinta. Mil veinte miligramos de cafeína. Sudor, ansiedad, náuseas... ¡estoy vibrando como celular en silencio!",
    fondo="cocina", byron=dict(pose="normal", x=420, panza=85, tiembla=True, sudor=True, ojos="espiral"), latas=20, contador=30,
    burbuja=dict(texto="¡BZZZ!", x=1100, y=260, de=(640, 330)))
esc("Lata treinta y cinco. La FDA advierte que unos mil doscientos miligramos de cafeína tomados de golpe pueden causar convulsiones. ¡Y yo ya voy por ahí!",
    fondo="cocina", byron=dict(pose="panza", x=420, panza=95, tiembla=True, sudor=True, ojos="grandes", boca="o"), latas=15, contador=35,
    tarjeta=dict(titulo="Cafeína", barras=[("Seguro (FDA)", 400, 1200, "#90A4AE"), ("Riesgo de golpe", 1200, 1200, "#E53935"), ("Byron", 35 * CAFEINA, 1200, "#6D4C41")], unidad_barra="mg"))
esc("Por eso, en la vida real, esto podría terminar en urgencias. ¡Yo soy un ajolote profesional, no lo copies!",
    fondo="plano", byron=dict(pose="pulgar", x=440, panza=95), icono=("hospital", 1300, 470))
esc("Lata cuarenta. Mil quinientos sesenta gramos de azúcar. ¡Mis dientes piden auxilio! El ácido fosfórico de la gaseosa ataca el esmalte.",
    fondo="cocina", byron=dict(pose="toma", x=420, panza=105, sudor=True), latas=10, contador=40, icono=("diente", 1400, 430))
esc("Lata cuarenta y cinco. Ya no siento la lengua, solo burbujas. ¡Me falta poquito!",
    fondo="cocina", byron=dict(pose="panza", x=420, panza=115, ojos="espiral", boca="ondas", sudor=True), latas=5, contador=45, burbujas_gas=True)
esc("¡LATA CINCUENTA! ¡Lo logré! Siete mil calorías, casi dos kilos de azúcar y mil setecientos miligramos de cafeína.",
    fondo="cocina", byron=dict(pose="celebra", x=420, panza=125, ojos="feliz", boca="grande"), latas=0, contador=50, confeti=True,
    tarjeta=dict(titulo="Total del día", filas=[("Calorías", "7.000"), ("Azúcar", "1,95 kg"), ("Cafeína", "1.700 mg"), ("Líquido", "17,7 L")]))
esc("Comparado con lo recomendado: treinta y nueve veces el azúcar, más de cuatro veces la cafeína y tres veces y media las calorías.",
    fondo="plano", byron=dict(pose="panza", x=420, panza=125, ojos="grandes"),
    tarjeta=dict(titulo="Byron vs. lo normal", grande=True, filas=[("Azúcar", "×39"), ("Cafeína", "×4"), ("Calorías", "×3,5")]))
esc("Una hora después llega el famoso bajón de azúcar. Estoy agotado... pero la cafeína no me deja dormir.",
    fondo="cuarto", byron=dict(pose="triste", x=520, panza=110, ojos="cansado"), reloj="+1 HORA")
esc("Tres horas después: gases, inflamación y eructos que suenan a trompeta.",
    fondo="cuarto", byron=dict(pose="panza", x=520, panza=100, boca="grande"), reloj="+3 HORAS", icono=("gas", 950, 700),
    onomatopeya=("¡PRRR!", 1350, 360))
esc("En la noche: cero sueño. La cafeína dura horas en el cuerpo; la mitad sigue ahí unas cinco horas después.",
    fondo="noche", byron=dict(pose="normal", x=700, panza=90, ojos="grandes"), reloj="3:00 A.M.")
esc("Al día siguiente: dolor de cabeza, cansancio y mucha sed. Mi cuerpo pide agua... ¡agua de verdad!",
    fondo="plano", byron=dict(pose="triste", x=520, panza=40, ojos="cansado"), reloj="+1 DÍA", icono=("botella", 1300, 520))
esc("Y esto no es solo un chiste. Hay casos médicos reales de personas que tomaban entre cuatro y seis litros de cola al día.",
    fondo="plano", byron=dict(pose="senala", x=440),
    tarjeta=dict(titulo="Casos reales", numero="4 a 6 L", unidad="de cola al día", x=1500, y=150, chica=True))
esc("Terminaron con el potasio muy bajo, debilidad muscular e incluso daño en los músculos.",
    fondo="plano", byron=dict(pose="triste", x=440), icono=("musculo", 1300, 470))
esc("Si lo hiciera todos los días: diabetes tipo dos, hígado graso, caries y muchos kilos de más.",
    fondo="plano", byron=dict(pose="panza", x=440, panza=125, ojos="grandes"), icono=("calendario_latas", 1300, 450))
esc("La buena noticia: una gaseosa de vez en cuando no te va a hacer daño. El problema es el exceso.",
    fondo="cocina", byron=dict(pose="pulgar", x=420, ojos="feliz"), latas=1, icono=("check", 1450, 420))
esc("Mi consejo de ajolote: si tienes sed, toma agua. Es gratis, no tiene azúcar, y tus riñones te lo van a agradecer.",
    fondo="plano", byron=dict(pose="toma_agua", x=520, ojos="feliz"), icono=("botella", 1300, 520))
esc("¿Qué quieres que pruebe la próxima vez? Escríbelo en los comentarios... ¡yo me arriesgo por ti!",
    fondo="cocina", byron=dict(pose="saluda", x=420, ojos="feliz"), latas=0, titulo=("¿PRÓXIMO RETO?", "Escríbelo en los comentarios"))
esc("¡Y suscríbete! Que a mí me vuelve a crecer la cola... pero los suscriptores no.",
    fondo="plano", byron=dict(pose="celebra", x=480, ojos="feliz", boca="grande"), suscribete=True)


# ------------------------------------------------------------------ Byron
ROSA, ROSA_C, ROJO = "#F8BBD0", "#FCE4EC", "#EC407A"


def f(v):
    return f"{v:.2f}".rstrip("0").rstrip(".")


def lata(x, y, k=1.0, rot=0, abierta=True):
    return (f'<g transform="translate({f(x)} {f(y)}) rotate({f(rot)}) scale({f(k)})">'
            f'<rect x="-32" y="-58" width="64" height="116" rx="10" fill="#E53935" stroke="{INK}" stroke-width="5"/>'
            '<path d="M-32 -5 C -10 -25 10 15 32 -5 L 32 8 C 10 28 -10 -12 -32 8 Z" fill="#FFFFFF"/>'
            f'<text x="0" y="40" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="20" fill="#FFFFFF">COLA</text>'
            f'<ellipse cx="0" cy="-58" rx="32" ry="9" fill="#CFD8DC" stroke="{INK}" stroke-width="4"/>'
            + (f'<ellipse cx="6" cy="-58" rx="9" ry="4" fill="#78909C"/>' if abierta else '')
            + '<rect x="-24" y="-48" width="8" height="90" rx="4" fill="#FFFFFF" opacity="0.35"/></g>')


def brazos_pose(pose, t):
    L0, R0 = (-145, -330), (145, -330)
    p = {
        "normal": [(-210, -230), (-215, -140), (210, -230), (215, -140)],
        "saluda": [(-220, -270), (-160, -210), (250, -400), (300 + 40 * math.sin(t * 13), -520)],
        "pulgar": [(-220, -270), (-160, -210), (230, -370), (250, -470)],
        "celebra": [(-230, -430), (-250 - 20 * math.sin(t * 18), -560), (230, -430), (250 + 20 * math.sin(t * 18), -560)],
        "senala": [(-220, -270), (-160, -210), (270, -370), (390, -400)],
        "panza": [(-185, -260), (-95, -250), (185, -260), (95, -250)],
        "piensa": [(-220, -270), (-160, -210), (230, -390), (120, -445)],
        "triste": [(-170, -230), (-175, -130), (170, -230), (175, -130)],
        "corre": [(-230, -300 + 40 * math.sin(t * 16)), (-280, -240), (230, -300 - 40 * math.sin(t * 16)), (280, -380)],
    }
    if pose in ("toma", "toma_agua"):
        ph = (t * 0.8) % 1.0
        q = math.sin(math.pi * min(ph / 0.6, 1.0)) if ph < 0.6 else 0.0
        mano = (230 - 140 * q, -260 - 210 * q)
        codo = (250 - 20 * q, -330 - 60 * q)
        return [L0, (-220, -270), (-160, -210)], [R0, codo, mano], mano, 60 + 70 * q
    a = p.get(pose, p["normal"])
    return [L0, a[0], a[1]], [R0, a[2], a[3]], a[3], None


def byron(x, gy=GY, t=0.0, pose="normal", panza=0, ojos="normal", boca="sonrisa", sudor=False, tiembla=False, mira=1, k=0.95):
    dy = 6 * math.sin(2 * math.pi * 1.2 * t)
    dx = 0.0
    if pose == "celebra":
        dy = -60 * abs(math.sin(math.pi * 1.8 * t))
    if pose == "corre":
        dx = 230 * t
        dy = -20 * abs(math.sin(t * 16))
    if tiembla:
        r = random.Random(int(t * 60))
        dx += r.uniform(-7, 7)
        dy += r.uniform(-5, 5)
    s = [f'<g transform="translate({f(x + dx)} {f(gy + dy)}) scale({f(k * mira)} {f(k)})">']
    # cola con meneo
    ang = 8 * math.sin(t * 5)
    s.append(f'<g transform="rotate({f(ang)} 90 -170)"><path d="M90 -210 C 220 -210 300 -150 360 -70 C 300 -40 220 -70 100 -110 Z" fill="{ROSA}" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/></g>')
    # piernas
    if pose == "corre":
        a = 40 * math.sin(t * 16)
        s.append(f'<polyline points="-50,-120 {f(-80 + a)},-2" fill="none" stroke="{INK}" stroke-width="22" stroke-linecap="round"/>'
                 f'<polyline points="50,-120 {f(80 - a)},-2" fill="none" stroke="{INK}" stroke-width="22" stroke-linecap="round"/>')
    else:
        s.append(f'<polyline points="-50,-120 -80,-2" fill="none" stroke="{INK}" stroke-width="22" stroke-linecap="round"/>'
                 f'<polyline points="50,-120 90,-2" fill="none" stroke="{INK}" stroke-width="22" stroke-linecap="round"/>'
                 f'<ellipse cx="-95" cy="2" rx="34" ry="14" fill="{INK}"/><ellipse cx="105" cy="2" rx="34" ry="14" fill="{INK}"/>')
    # cuerpo y barriga
    ex = 1 + panza / 110
    resp = 1 + 0.02 * math.sin(t * 5)
    s.append(f'<ellipse cx="{f(panza * 0.35)}" cy="-270" rx="{f(160 * ex * resp)}" ry="{f(175 + panza * 0.25)}" fill="{ROSA}" stroke="{INK}" stroke-width="10"/>'
             f'<ellipse cx="{f(panza * 0.45)}" cy="-250" rx="{f(100 * ex * resp)}" ry="{f(125 + panza * 0.2)}" fill="{ROSA_C}"/>')
    if panza > 60:
        s.append(f'<path d="M{f(panza * 0.45 - 40)} -250 q 40 14 80 0" stroke="{ROJO}" stroke-width="6" fill="none" opacity="0.6"/>')
    # brazos
    bl, br, mano_r, inclin = brazos_pose(pose, t)
    for pts in (bl, br):
        s.append(f'<polyline points="{" ".join(f"{f(a)},{f(b)}" for a, b in pts)}" fill="none" stroke="{INK}" stroke-width="22" stroke-linecap="round" stroke-linejoin="round"/>')
        s.append(f'<circle cx="{f(pts[-1][0])}" cy="{f(pts[-1][1])}" r="18" fill="{INK}"/>')
    if pose == "pulgar":
        s.append(f'<rect x="242" y="-520" width="16" height="42" rx="8" fill="{INK}"/>')
    # branquias que se mueven
    for lado in (-1, 1):
        for i, (ddy, a0) in enumerate(((-90, -35), (0, 0), (90, 35))):
            a = a0 + 7 * math.sin(t * 6 + i)
            cx, cy = lado * 270, -540 + ddy * 0.9
            s.append(f'<g transform="translate({cx} {f(cy)}) rotate({f(a * lado)})">'
                     f'<ellipse cx="{lado * 40}" cy="0" rx="78" ry="28" fill="{ROJO}" stroke="{INK}" stroke-width="8"/>'
                     + "".join(f'<line x1="{lado * (j * 22)}" y1="-22" x2="{lado * (j * 22 + 10)}" y2="-38" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>' for j in range(4))
                     + '</g>')
    # cabeza
    s.append(f'<ellipse cx="0" cy="-540" rx="245" ry="190" fill="{ROSA}" stroke="{INK}" stroke-width="10"/>')
    s.append(f'<path d="M-205 -590 C -200 -740 200 -740 205 -590 C 100 -630 -100 -630 -205 -590 Z" fill="#FFFFFF" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
             '<path d="M-15 -708 L 15 -708 L 40 -618 L -40 -618 Z" fill="#E53935"/>'
             f'<polygon transform="translate(0 -672)" points="0,-24 8,-6 26,-6 12,6 18,26 0,14 -18,26 -12,6 -26,-6 -8,-6" fill="#FFD54F" stroke="{INK}" stroke-width="4"/>')
    # ojos
    parpadeo = (t % 3.2) < 0.12
    for ex_ in (-85, 85):
        if ojos == "feliz" or parpadeo:
            s.append(f'<path d="M{ex_ - 22} -525 Q {ex_} -552 {ex_ + 22} -525" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>')
        elif ojos == "grandes":
            s.append(f'<circle cx="{ex_}" cy="-535" r="32" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/><circle cx="{ex_}" cy="-532" r="14" fill="{INK}"/>')
        elif ojos == "espiral":
            rot = (t * 400) % 360
            s.append(f'<g transform="rotate({f(rot)} {ex_} -532)"><path d="M{ex_} -532 m -4 0 a 4 4 0 1 1 8 0 a 9 9 0 1 1 -17 0 a 14 14 0 1 1 27 0 a 19 19 0 1 1 -37 0" '
                     f'fill="none" stroke="{INK}" stroke-width="6"/></g>')
        elif ojos == "cansado":
            s.append(f'<circle cx="{ex_}" cy="-528" r="20" fill="{INK}"/><path d="M{ex_ - 26} -538 L {ex_ + 26} -538 L {ex_ + 24} -556 L {ex_ - 24} -556 Z" fill="{ROSA}"/>'
                     f'<line x1="{ex_ - 26}" y1="-538" x2="{ex_ + 26}" y2="-538" stroke="{INK}" stroke-width="6"/>'
                     f'<path d="M{ex_ - 22} -500 Q {ex_} -488 {ex_ + 22} -500" fill="none" stroke="#AD1457" stroke-width="5" opacity="0.6"/>')
        else:
            s.append(f'<circle cx="{ex_}" cy="-530" r="20" fill="{INK}"/><circle cx="{ex_ + 7}" cy="-538" r="7" fill="#FFFFFF"/>')
    # boca
    if inclin is not None:
        boca = "o"
    if boca == "o":
        s.append(f'<ellipse cx="0" cy="-462" rx="26" ry="{f(30 + 6 * math.sin(t * 9))}" fill="#880E4F" stroke="{INK}" stroke-width="8"/>')
    elif boca == "grande":
        s.append(f'<path d="M-95 -485 Q 0 -360 95 -485 Z" fill="#880E4F" stroke="{INK}" stroke-width="9" stroke-linejoin="round"/>'
                 '<path d="M-40 -440 Q 0 -415 40 -440" fill="#F06292"/>')
    elif boca == "ondas":
        s.append(f'<path d="M-80 -465 q 20 -18 40 0 q 20 18 40 0 q 20 -18 40 0 q 20 18 40 0" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>')
    else:
        s.append(f'<path d="M-80 -470 Q 0 -410 80 -470" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>')
    s.append('<ellipse cx="-130" cy="-475" rx="34" ry="18" fill="#F06292" opacity="0.5"/><ellipse cx="130" cy="-475" rx="34" ry="18" fill="#F06292" opacity="0.5"/>')
    s.append(f'<g transform="rotate(-25 135 -560)"><rect x="100" y="-575" width="70" height="28" rx="12" fill="#FFCC80" stroke="{INK}" stroke-width="5"/>'
             '<rect x="124" y="-571" width="22" height="20" fill="#FFE0B2"/></g>')
    if ojos == "espiral" or (sudor and panza > 100):
        s.append(f'<ellipse cx="0" cy="-540" rx="245" ry="190" fill="#66BB6A" opacity="{f(0.12 + 0.06 * math.sin(t * 4))}"/>')
    # lata o botella en la mano
    if inclin is not None:
        if pose == "toma_agua":
            s.append(f'<g transform="translate({f(mano_r[0])} {f(mano_r[1] - 40)}) rotate({f(-inclin)})"><rect x="-26" y="-80" width="52" height="150" rx="16" fill="#B3E5FC" stroke="{INK}" stroke-width="5"/>'
                     f'<rect x="-14" y="-102" width="28" height="24" rx="5" fill="#1E88E5" stroke="{INK}" stroke-width="4"/>'
                     '<rect x="-26" y="-20" width="52" height="40" fill="#4FC3F7"/></g>')
        else:
            s.append(lata(mano_r[0], mano_r[1] - 40, 1.0, -inclin))
    if sudor:
        g = []
        for i, (gx, gy0) in enumerate(((-250, -680), (250, -700), (-230, -560))):
            fr = (t * 1.4 + i * 0.37) % 1.0
            g.append(f'<path transform="translate({gx} {f(gy0 + fr * 80)})" opacity="{f(1 - fr)}" d="M0 0 q -14 26 0 36 q 14 -10 0 -36 Z"/>')
        s.append(f'<g fill="#4FC3F7" stroke="#0277BD" stroke-width="3">{"".join(g)}</g>')
    if tiembla:
        s.append(f'<g stroke="{INK}" stroke-width="7" stroke-linecap="round" opacity="0.7"><path d="M-300 -400 l -30 -10 M-300 -330 l -36 0 M300 -400 l 30 -10 M300 -330 l 36 0"/></g>')
    s.append('</g>')
    return "".join(s)


# ------------------------------------------------------------------ objetos y fondos
def pared_latas(n, x0=600):
    top = GY - 260
    s = [f'<rect x="{x0}" y="{top}" width="480" height="26" rx="8" fill="#A1887F" stroke="{INK}" stroke-width="6"/>',
         f'<rect x="{x0 + 25}" y="{top + 26}" width="22" height="234" fill="#8D6E63" stroke="{INK}" stroke-width="5"/>',
         f'<rect x="{x0 + 433}" y="{top + 26}" width="22" height="234" fill="#8D6E63" stroke="{INK}" stroke-width="5"/>']
    for i in range(n):
        fila, col = i // 10, i % 10
        s.append(lata(x0 + 42 + col * 44, top - 32 - fila * 64, 0.6, 0, abierta=False))
    return "".join(s)


def icono(nombre, x, y, t=0.0):
    if nombre in ("alerta", "check", "higado", "rinones", "gas"):
        return HV.icono(nombre, x, y)
    if nombre == "calendario_latas":
        return (f'<g transform="translate({x} {y})"><rect x="-230" y="-200" width="460" height="420" rx="20" fill="#FFFFFF" stroke="{INK}" stroke-width="10"/>'
                f'<rect x="-230" y="-200" width="460" height="100" rx="20" fill="#E53935" stroke="{INK}" stroke-width="10"/>'
                f'<text x="0" y="-130" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="50" fill="#FFFFFF">TODOS LOS DÍAS</text>'
                + "".join(lata(-170 + (i % 5) * 85, -20 + (i // 5) * 100, 0.55) for i in range(10)) + '</g>')
    if nombre == "garrafon":
        nivel = 0.5 + 0.5 * math.sin(t * 2)
        return (f'<g transform="translate({x} {y})"><rect x="-130" y="-250" width="260" height="380" rx="60" fill="#E1F5FE" stroke="{INK}" stroke-width="10"/>'
                f'<rect x="-120" y="{f(-60 - 40 * nivel)}" width="240" height="{f(180 + 40 * nivel)}" rx="50" fill="#81D4FA"/>'
                f'<rect x="-50" y="-310" width="100" height="70" rx="12" fill="#1E88E5" stroke="{INK}" stroke-width="8"/>'
                f'<text x="0" y="40" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="60" fill="#01579B">18 L</text></g>')
    if nombre == "azucar":
        s = [f'<g transform="translate({x} {y})">']
        filas = (6, 5, 4, 3, 2, 1)
        for r, nfila in enumerate(filas):
            for c in range(nfila):
                cx = -nfila * 38 + 38 + c * 76
                cy = 120 - r * 70
                s.append(f'<rect x="{cx - 34}" y="{cy - 34}" width="68" height="64" rx="8" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
                         f'<rect x="{cx - 26}" y="{cy - 28}" width="20" height="12" fill="#ECEFF1"/>')
        s.append('</g>')
        return "".join(s)
    if nombre == "pancreas":
        pulso = 1 + 0.05 * math.sin(t * 10)
        return (f'<g transform="translate({x} {y}) scale({f(pulso)})"><path d="M-260 20 C -260 -60 -120 -90 0 -60 C 120 -40 220 -110 270 -40 C 300 10 230 60 150 50 C 60 40 -40 90 -150 100 C -230 105 -260 70 -260 20 Z" '
                f'fill="#FFB74D" stroke="{INK}" stroke-width="10"/>'
                + "".join(f'<circle cx="{cx}" cy="{cy}" r="12" fill="#FFA726"/>' for cx, cy in ((-180, 30), (-80, 0), (40, -20), (150, -10), (-120, 60)))
                + f'<text x="0" y="200" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="52" fill="{INK}">PÁNCREAS</text></g>')
    if nombre == "cerebro":
        k = 1 + 0.06 * math.sin(t * 9)
        s = (f'<g transform="translate({x} {y}) scale({f(k)})"><path d="M-200 0 C -230 -120 -120 -200 -20 -170 C 40 -230 180 -200 200 -100 C 260 -60 240 60 170 80 C 150 150 40 160 0 120 '
             f'C -60 170 -170 140 -170 80 C -230 70 -230 20 -200 0 Z" fill="#F48FB1" stroke="{INK}" stroke-width="10"/>'
             '<path d="M-120 -120 q 40 30 0 70 M-20 -150 q -30 60 20 100 M80 -150 q 40 40 0 90 M150 -40 q -40 20 -10 60 M-150 30 q 50 -10 70 30" fill="none" stroke="#AD1457" stroke-width="8" stroke-linecap="round"/>')
        rr = random.Random(int(t * 8))
        chispas = "".join(f'<polygon transform="translate({rr.randint(-260, 260)} {rr.randint(-260, 160)}) scale(0.8)" points="0,-30 8,-8 30,0 8,8 0,30 -8,8 -30,0 -8,-8" fill="#FFEB3B" stroke="{INK}" stroke-width="4"/>' for _ in range(5))
        return s + chispas + '</g>'
    if nombre == "corazon":
        lat = (t * 3.2) % 1.0
        k = 1.0 + (0.18 if lat < 0.12 else (0.08 if 0.25 < lat < 0.35 else 0))
        return (f'<g transform="translate({x} {y}) scale({f(k * 4)})">{HV.corazon(0, -40, 50, "#E53935")}</g>'
                f'<polyline points="{x - 300},{y + 260} {x - 120},{y + 260} {x - 80},{y + 180} {x - 40},{y + 330} {x},{y + 220} {x + 40},{y + 260} {x + 300},{y + 260}" fill="none" stroke="#43A047" stroke-width="10" stroke-linejoin="round"/>')
    if nombre == "bano":
        return (f'<g transform="translate({x} {y})"><rect x="-180" y="-330" width="360" height="610" rx="10" fill="#8D6E63" stroke="{INK}" stroke-width="10"/>'
                f'<rect x="-110" y="-280" width="220" height="120" rx="16" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>'
                f'<text x="0" y="-195" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="72" fill="#1E88E5">WC</text>'
                f'<circle cx="130" cy="0" r="16" fill="#FFD54F" stroke="{INK}" stroke-width="5"/>'
                f'<rect x="-120" y="-120" width="240" height="70" rx="10" fill="#E53935" stroke="{INK}" stroke-width="6"/>'
                f'<text x="0" y="-72" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="40" fill="#FFFFFF">¡OCUPADO!</text></g>')
    if nombre == "hospital":
        return (f'<g transform="translate({x} {y})"><rect x="-260" y="-200" width="520" height="400" rx="20" fill="#FFFFFF" stroke="{INK}" stroke-width="10"/>'
                f'<rect x="-50" y="-150" width="100" height="300" fill="#E53935"/><rect x="-150" y="-50" width="300" height="100" fill="#E53935"/>'
                f'<text x="0" y="290" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="58" fill="{INK}">URGENCIAS</text></g>')
    if nombre == "diente":
        temb = 6 * math.sin(t * 25)
        return (f'<g transform="translate({f(x + temb)} {y})"><path d="M-150 -170 C -230 -170 -230 -30 -170 40 C -140 80 -150 220 -100 230 C -50 240 -40 110 0 110 C 40 110 50 240 100 230 '
                f'C 150 220 140 80 170 40 C 230 -30 230 -170 150 -170 C 90 -170 60 -140 0 -140 C -60 -140 -90 -170 -150 -170 Z" fill="#FFFDE7" stroke="{INK}" stroke-width="10"/>'
                f'<path d="M-60 -60 C -80 -20 -40 10 -70 50" fill="none" stroke="{INK}" stroke-width="7"/>'
                '<circle cx="80" cy="-60" r="28" fill="#A1887F"/><circle cx="40" cy="-10" r="16" fill="#A1887F"/>'
                f'<circle cx="-70" cy="-80" r="14" fill="{INK}"/><circle cx="60" cy="-80" r="14" fill="{INK}"/>'
                f'<ellipse cx="-5" cy="-20" rx="22" ry="28" fill="{INK}"/></g>')
    if nombre == "botella":
        return (f'<g transform="translate({x} {y}) rotate({f(5 * math.sin(t * 2))})"><rect x="-90" y="-240" width="180" height="440" rx="50" fill="#B3E5FC" stroke="{INK}" stroke-width="10"/>'
                f'<rect x="-45" y="-310" width="90" height="80" rx="14" fill="#1E88E5" stroke="{INK}" stroke-width="8"/>'
                '<rect x="-84" y="-40" width="168" height="230" rx="40" fill="#4FC3F7"/>'
                f'<rect x="-90" y="-130" width="180" height="70" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
                f'<text x="0" y="-82" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="44" fill="#1E88E5">AGUA</text>'
                '<path d="M-50 -10 q -10 60 0 120" stroke="#FFFFFF" stroke-width="10" fill="none" opacity="0.6" stroke-linecap="round"/></g>')
    if nombre == "musculo":
        temb = 4 * math.sin(t * 30)
        return (f'<g transform="translate({x} {f(y + temb)})"><path d="M-250 120 L -250 30 C -200 -40 -130 -30 -100 -90 C -80 -170 0 -230 70 -180 C 140 -130 110 -40 60 -10 '
                f'C 140 -20 220 30 230 120 Z" fill="#FFCC80" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
                f'<path d="M-60 -60 q 40 -40 90 -10" fill="none" stroke="{INK}" stroke-width="7"/>'
                f'<text x="0" y="230" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="54" fill="#E53935">POTASIO ↓</text></g>')
    return ""


def burbujas_gas(t):
    r = random.Random(3)
    s = []
    for _ in range(40):
        x0, v, rad = r.randint(100, 1800), r.uniform(120, 260), r.randint(8, 26)
        y = GY - ((t * v + r.randint(0, 900)) % 900)
        s.append(f'<circle cx="{f(x0 + 15 * math.sin(t * 3 + x0))}" cy="{f(y)}" r="{rad}" fill="#FFFFFF" fill-opacity="0.45" stroke="#B0BEC5" stroke-width="3"/>')
    return "".join(s)


def reloj_pared(texto):
    return (f'<g transform="translate(1500 230)"><circle r="95" fill="#FFFFFF" stroke="{INK}" stroke-width="10"/>'
            f'<line x1="0" y1="0" x2="0" y2="-62" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
            f'<line x1="0" y1="0" x2="-50" y2="0" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>'
            f'<text x="0" y="150" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="46" fill="{INK}">{escape(texto)} A.M.</text></g>')


def contador(n):
    p = n / 50
    return (f'<g transform="translate(620 36)"><rect width="430" height="150" rx="26" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
            + lata(70, 76, 0.95)
            + f'<text x="140" y="68" font-family="Arial" font-weight="bold" font-size="38" fill="#455A64">LATA</text>'
            f'<text x="140" y="125" font-family="Arial Black, Arial" font-weight="900" font-size="64" fill="{INK}">{n}<tspan font-size="40" fill="#90A4AE"> / 50</tspan></text>'
            f'<rect x="0" y="170" width="430" height="26" rx="13" fill="#ECEFF1" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="0" y="170" width="{f(max(430 * p, 26))}" height="26" rx="13" fill="#E53935" stroke="{INK}" stroke-width="5"/></g>')
