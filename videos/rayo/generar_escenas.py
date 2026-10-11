"""Genera las 50 escenas (SVG 1920x1080) de la historia de Rayo, el motociclista.

Uso: python3 generar_escenas.py <carpeta_salida>
"""
import json
import math
import os
import random
import sys
from html import escape

W, H = 1920, 1080
GY = 900  # línea del suelo

# ----------------------------------------------------------------- historia
# Cada escena: (narración, especificación del dibujo)
ESCENAS = [
    ("Esta es la historia de Rayo, un motociclista que nadie ha visto sin su casco.",
     dict(cielo="atardecer", suelo="carretera", fondo="ciudad", rayo=dict(modo="moto", x=470), titulo="RAYO", subtitulo="El motociclista sin rostro")),
    ("Vive en la gran ciudad, y todos lo conocen por su casco azul y su visera oscura.",
     dict(cielo="dia", suelo="acera", fondo="ciudad", rayo=dict(pose="saluda", x=860))),
    ("Nadie sabe cómo es su cara. Algunos dicen que es tímido; otros, que es un superhéroe.",
     dict(cielo="dia", suelo="acera", fondo="ciudad", rayo=dict(pose="piensa", x=760),
          burbuja=dict(texto="?", x=1150, y=200, de=(900, 330), pensamiento=True))),
    ("Rayo trabaja como mensajero. Su misión: entregar cada paquete, sin importar a dónde.",
     dict(cielo="dia", suelo="acera", fondo="bodega", rayo=dict(pose="carga", x=980))),
    ("Una mañana, su teléfono sonó con un pedido muy especial.",
     dict(cielo="dia", suelo="acera", fondo="ciudad", rayo=dict(pose="telefono", x=760),
          telefono=dict(x=1300, y=430, texto="¡Nuevo pedido!"))),
    ("El destino era Pueblo Escondido, un lugar lejos de la ciudad, al otro lado de las montañas.",
     dict(cielo="dia", suelo="pasto", fondo="montanas", rayo=dict(pose="senala", x=520),
          letrero=dict(x=1250, texto="PUEBLO ESCONDIDO", sub="→ 120 km"))),
    ("El paquete decía: Frágil. Entregar hoy mismo. Es un regalo de cumpleaños.",
     dict(cielo="dia", suelo="acera", fondo="bodega", caja_grande=True)),
    ("Rayo no lo dudó. Ajustó su casco, bajó la visera, y dijo: ¡Vamos!",
     dict(cielo="dia", suelo="acera", fondo="ciudad", rayo=dict(pose="celebra", x=900),
          burbuja=dict(texto="¡Vamos!", x=1280, y=230, de=(1080, 330)))),
    ("Encendió su moto y salió rodando entre los edificios.",
     dict(cielo="dia", suelo="carretera", fondo="ciudad", rayo=dict(modo="moto", x=900, caja=True, vel=True))),
    ("El tráfico era pesado, pero Rayo conocía cada atajo de la ciudad.",
     dict(cielo="dia", suelo="carretera", fondo="ciudad", carros=[300, 1550], rayo=dict(modo="moto", x=930, caja=True, vel=True))),
    ("Pronto dejó atrás la ciudad. Un letrero marcaba ciento veinte kilómetros.",
     dict(cielo="dia", suelo="carretera", fondo="afueras", letrero=dict(x=1450, texto="PUEBLO ESCONDIDO", sub="120 km"),
          rayo=dict(modo="moto", x=760, caja=True, vel=True))),
    ("La carretera se volvió verde, con montañas a lado y lado.",
     dict(cielo="dia", suelo="carretera", fondo="montanas", arboles=True, rayo=dict(modo="moto", x=960, caja=True, vel=True))),
    ("En el camino saludó a un campesino que lo miró con curiosidad.",
     dict(cielo="dia", suelo="pasto", fondo="montanas", arboles=True, rayo=dict(modo="moto_parado", x=700, caja=True),
          personas=[dict(tipo="campesino", x=1350, pose="saluda", mira=-1)])),
    ("¿Y usted por qué nunca se quita el casco?, le preguntó el campesino.",
     dict(cielo="dia", suelo="pasto", fondo="montanas", arboles=True, rayo=dict(modo="moto_parado", x=700, caja=True),
          personas=[dict(tipo="campesino", x=1350, pose="normal", mira=-1)],
          burbuja=dict(texto="¿Y usted por qué nunca se quita el casco?", x=1020, y=170, de=(1250, 330), ancho=560))),
    ("Rayo solo levantó el pulgar... y siguió su camino.",
     dict(cielo="dia", suelo="pasto", fondo="montanas", arboles=True, rayo=dict(pose="pulgar", x=860),
          personas=[dict(tipo="campesino", x=1400, pose="normal", mira=-1)])),
    ("Pero de pronto, el cielo se puso gris.",
     dict(cielo="nublado", suelo="carretera", fondo="montanas", rayo=dict(modo="moto", x=900, caja=True, vel=True))),
    ("Empezó a llover con fuerza. Las gotas golpeaban su visera.",
     dict(cielo="lluvia", suelo="carretera", fondo="montanas", lluvia=True, rayo=dict(modo="moto", x=900, caja=True, vel=True))),
    ("Rayo protegió el paquete con su chaqueta. Nada podía mojarse.",
     dict(cielo="lluvia", suelo="carretera", fondo="montanas", lluvia=True, rayo=dict(pose="carga", x=900))),
    ("Siguió adelante, despacio y con cuidado, sobre la carretera mojada.",
     dict(cielo="lluvia", suelo="carretera", fondo="montanas", lluvia=True, charcos=True, rayo=dict(modo="moto", x=900, caja=True))),
    ("Y entonces... ¡pum! La llanta trasera se pinchó.",
     dict(cielo="lluvia", suelo="carretera", fondo="montanas", lluvia=True, rayo=dict(modo="moto_pinchada", x=900),
          onomatopeya=dict(texto="¡PUM!", x=420, y=700))),
    ("Estaba a mitad de camino, bajo la lluvia, y sin llanta de repuesto.",
     dict(cielo="lluvia", suelo="carretera", fondo="montanas", lluvia=True, letrero=dict(x=1600, texto="PUEBLO ESCONDIDO", sub="60 km"),
          rayo=dict(pose="piensa", x=520), moto_sola=dict(x=1000, pinchada=True))),
    ("Por un momento, pensó que no lo lograría.",
     dict(cielo="lluvia", suelo="carretera", fondo="montanas", lluvia=True, rayo=dict(pose="triste", x=900))),
    ("Pero la lluvia paró, y apareció un niño corriendo por la carretera.",
     dict(cielo="dia", suelo="carretera", fondo="montanas", arcoiris=True, rayo=dict(pose="normal", x=600),
          personas=[dict(tipo="nino", x=1300, pose="corre", mira=-1)])),
    ("¡Mi papá arregla motos! ¡Venga conmigo!, gritó el niño.",
     dict(cielo="dia", suelo="carretera", fondo="montanas", arcoiris=True, rayo=dict(pose="normal", x=600),
          personas=[dict(tipo="nino", x=1200, pose="saluda", mira=-1)],
          burbuja=dict(texto="¡Mi papá arregla motos! ¡Venga conmigo!", x=1060, y=260, de=(1190, 560), ancho=560))),
    ("Rayo empujó su moto hasta un pequeño taller junto al camino.",
     dict(cielo="dia", suelo="pasto", fondo="taller", rayo=dict(pose="empuja", x=640), moto_sola=dict(x=930, pinchada=True),
          personas=[dict(tipo="nino", x=1250, pose="saluda", mira=-1)])),
    ("El mecánico, Don Tulio, revisó la llanta y sonrió.",
     dict(cielo="dia", suelo="pasto", fondo="taller", moto_sola=dict(x=820, pinchada=True),
          personas=[dict(tipo="mecanico", x=1220, pose="normal", mira=-1)], rayo=dict(pose="normal", x=420))),
    ("En diez minutos queda como nueva, dijo Don Tulio.",
     dict(cielo="dia", suelo="pasto", fondo="taller", moto_sola=dict(x=820, pinchada=True),
          personas=[dict(tipo="mecanico", x=1220, pose="pulgar", mira=-1)], rayo=dict(pose="normal", x=420),
          burbuja=dict(texto="¡En diez minutos queda como nueva!", x=1120, y=230, de=(1230, 380), ancho=520))),
    ("Mientras tanto, el niño miraba a Rayo con los ojos muy abiertos.",
     dict(cielo="dia", suelo="pasto", fondo="taller", rayo=dict(pose="normal", x=700),
          personas=[dict(tipo="nino", x=1150, pose="normal", mira=-1, asombro=True)])),
    ("¿Usted es un superhéroe?, preguntó en voz baja.",
     dict(cielo="dia", suelo="pasto", fondo="taller", rayo=dict(pose="normal", x=700),
          personas=[dict(tipo="nino", x=1150, pose="normal", mira=-1, asombro=True)],
          burbuja=dict(texto="¿Usted es un superhéroe?", x=1100, y=330, de=(1150, 560), ancho=440))),
    ("Rayo señaló el paquete. Su único superpoder era cumplir.",
     dict(cielo="dia", suelo="pasto", fondo="taller", rayo=dict(pose="senala_abajo", x=700), caja_suelo=dict(x=930),
          personas=[dict(tipo="nino", x=1250, pose="normal", mira=-1)])),
    ("La moto quedó lista. Don Tulio no quiso cobrarle nada.",
     dict(cielo="dia", suelo="pasto", fondo="taller", moto_sola=dict(x=820, brillo=True),
          personas=[dict(tipo="mecanico", x=1250, pose="pulgar", mira=-1)])),
    ("Rayo se despidió agradecido, y volvió a la carretera.",
     dict(cielo="dia", suelo="pasto", fondo="taller", rayo=dict(modo="moto_parado", x=650, caja=True, saluda=True),
          personas=[dict(tipo="mecanico", x=1250, pose="saluda", mira=-1), dict(tipo="nino", x=1480, pose="saluda", mira=-1)])),
    ("El sol empezaba a caer. Quedaba poco tiempo.",
     dict(cielo="atardecer", suelo="carretera", fondo="montanas", rayo=dict(modo="moto", x=900, caja=True, vel=True))),
    ("De repente, una roca enorme bloqueaba el camino.",
     dict(cielo="atardecer", suelo="carretera", fondo="montanas", roca=dict(x=1350), rayo=dict(modo="moto_parado", x=650, caja=True),
          onomatopeya=dict(texto="¡OH NO!", x=1000, y=380))),
    ("Pero Rayo vio un camino de tierra entre los árboles. Un atajo.",
     dict(cielo="atardecer", suelo="carretera", fondo="montanas", arboles=True, roca=dict(x=1500), rayo=dict(pose="senala", x=700),
          letrero=dict(x=1150, texto="ATAJO", sub="←→", pequeno=True))),
    ("Tomó el atajo, saltando piedras y charcos.",
     dict(cielo="atardecer", suelo="tierra", fondo="bosque", charcos=True, rayo=dict(modo="moto", x=900, caja=True, vel=True, salto=40))),
    ("Cruzó un pequeño río de un salto. ¡Qué maniobra!",
     dict(cielo="atardecer", suelo="tierra", fondo="bosque", rio=True, rayo=dict(modo="moto", x=960, caja=True, vel=True, salto=110, inclina=-12))),
    ("Hasta un perro salió a perseguirlo... y luego se hicieron amigos.",
     dict(cielo="atardecer", suelo="tierra", fondo="bosque", rayo=dict(modo="moto", x=1050, caja=True, vel=True), perro=dict(x=520, corre=True))),
    ("Cayó la noche. La luz de su moto iluminaba el camino.",
     dict(cielo="noche", suelo="carretera", fondo="montanas", rayo=dict(modo="moto", x=800, caja=True, vel=True, luz=True))),
    ("Por fin, un letrero: Bienvenidos a Pueblo Escondido.",
     dict(cielo="noche", suelo="carretera", fondo="montanas", letrero=dict(x=1350, texto="BIENVENIDOS A", sub="PUEBLO ESCONDIDO", grande=True),
          rayo=dict(modo="moto_parado", x=650, caja=True, luz=True))),
    ("Las casas tenían las luces encendidas. Faltaba encontrar la dirección.",
     dict(cielo="noche", suelo="tierra", fondo="pueblo", rayo=dict(modo="moto", x=900, caja=True, luz=True))),
    ("Rayo llegó a una casita azul y tocó la puerta.",
     dict(cielo="noche", suelo="tierra", fondo="casa", rayo=dict(pose="carga", x=820), onomatopeya=dict(texto="TOC TOC", x=1420, y=330, chico=True))),
    ("Abrió Doña Marta, una abuelita que no esperaba visitas.",
     dict(cielo="noche", suelo="tierra", fondo="casa", puerta_abierta=True, rayo=dict(pose="carga", x=820),
          personas=[dict(tipo="abuela", x=1260, pose="normal", mira=-1, asombro=True)])),
    ("Entrega para usted, dijo Rayo, entregando el paquete.",
     dict(cielo="noche", suelo="tierra", fondo="casa", puerta_abierta=True, rayo=dict(pose="entrega", x=880),
          personas=[dict(tipo="abuela", x=1260, pose="recibe_sin", mira=-1)],
          burbuja=dict(texto="Entrega para usted", x=520, y=200, de=(780, 300), ancho=420))),
    ("Dentro había una carta y una foto de su nieta, que vivía en la ciudad.",
     dict(cielo="noche", suelo="tierra", fondo="casa", puerta_abierta=True, regalo_abierto=True)),
    ("¡Hoy es mi cumpleaños!, dijo emocionada. Pensé que nadie se acordaría.",
     dict(cielo="noche", suelo="tierra", fondo="casa", puerta_abierta=True, corazones=True, rayo=dict(pose="normal", x=800),
          personas=[dict(tipo="abuela", x=1260, pose="feliz", mira=-1)],
          burbuja=dict(texto="¡Hoy es mi cumpleaños!", x=1150, y=230, de=(1250, 380), ancho=460))),
    ("Lo invitó a pasar a tomar un tinto, pero Rayo tenía que volver.",
     dict(cielo="noche", suelo="tierra", fondo="casa", puerta_abierta=True, rayo=dict(pose="saluda", x=800),
          personas=[dict(tipo="abuela", x=1260, pose="taza", mira=-1)],
          burbuja=dict(texto="¿Se toma un tintico?", x=1170, y=230, de=(1250, 380), ancho=420))),
    ("Esa noche, Rayo entendió que no llevaba paquetes. Llevaba alegrías.",
     dict(cielo="noche", suelo="tierra", fondo="casa", puerta_abierta=True, corazones=True, rayo=dict(pose="celebra", x=820),
          personas=[dict(tipo="abuela", x=1260, pose="feliz", mira=-1)])),
    ("Y volvió a la ciudad bajo la luna, listo para la siguiente entrega.",
     dict(cielo="noche", suelo="carretera", fondo="ciudad_lejos", rayo=dict(modo="moto", x=900, vel=True, luz=True, mira=-1))),
    ("¿Quién está detrás de la visera? Nadie lo sabe... Continuará.",
     dict(cielo="atardecer", suelo="carretera", fondo="ciudad", rayo=dict(pose="saluda", x=420), titulo="CONTINUARÁ...", subtitulo="¿Quién está detrás de la visera?", titulo_x=1250, titulo_fs=140)),
]

INK = "#1A1A1A"


def fmt(v):
    return f"{v:.1f}".rstrip("0").rstrip(".")


# ------------------------------------------------------------ cielo y suelo
def cielo(tipo, rnd):
    paletas = {
        "dia": ("#8EC9F5", "#E6F4FF"),
        "atardecer": ("#F78C6B", "#FFD9A0"),
        "noche": ("#0B1633", "#26375E"),
        "nublado": ("#9AA6B2", "#D5DCE3"),
        "lluvia": ("#5F6B78", "#A9B3BD"),
    }
    a, b = paletas[tipo]
    s = [f'<defs><linearGradient id="cielo" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs>',
         f'<rect width="{W}" height="{H}" fill="url(#cielo)"/>']
    if tipo == "dia":
        s.append('<circle cx="1720" cy="150" r="70" fill="#FFD54F"/>')
        for cx, cy in ((380, 170), (1180, 120)):
            s.append(nube(cx, cy, "#FFFFFF"))
    elif tipo == "atardecer":
        s.append('<circle cx="1550" cy="560" r="120" fill="#FFB74D" opacity="0.9"/>')
    elif tipo == "noche":
        for _ in range(70):
            x, y = rnd.randint(0, W), rnd.randint(0, 520)
            s.append(f'<circle cx="{x}" cy="{y}" r="{rnd.choice((1.5, 2, 2.5))}" fill="#FFFFFF" opacity="{rnd.choice((0.5, 0.8, 1))}"/>')
        s.append('<circle cx="1650" cy="160" r="65" fill="#F5F3CE"/><circle cx="1680" cy="140" r="58" fill="#0E1A3A"/>')
    elif tipo in ("nublado", "lluvia"):
        for cx, cy in ((250, 140), (700, 110), (1150, 150), (1600, 120)):
            s.append(nube(cx, cy, "#7C8792" if tipo == "lluvia" else "#B9C2CB", 1.3))
    return "".join(s)


def nube(cx, cy, color, k=1.0):
    return (f'<g fill="{color}"><ellipse cx="{cx}" cy="{cy}" rx="{110*k}" ry="{45*k}"/>'
            f'<circle cx="{cx-45*k}" cy="{cy-25*k}" r="{45*k}"/><circle cx="{cx+30*k}" cy="{cy-40*k}" r="{55*k}"/></g>')


def suelo(tipo, noche):
    if tipo == "carretera":
        c = "#2E3238" if noche else "#3C4048"
        s = [f'<rect x="0" y="{GY}" width="{W}" height="{H-GY}" fill="{c}"/>',
             f'<rect x="0" y="{GY}" width="{W}" height="10" fill="#6B7079"/>']
        for x in range(40, W, 320):
            s.append(f'<rect x="{x}" y="{GY+75}" width="170" height="12" rx="6" fill="#F2F2F2" opacity="0.9"/>')
        return "".join(s)
    if tipo == "acera":
        c = "#B9BEC6" if not noche else "#5A606A"
        s = [f'<rect x="0" y="{GY}" width="{W}" height="{H-GY}" fill="{c}"/>']
        for x in range(0, W, 160):
            s.append(f'<line x1="{x}" y1="{GY}" x2="{x}" y2="{H}" stroke="#9EA4AD" stroke-width="3"/>')
        return "".join(s)
    if tipo == "pasto":
        c = "#7CC36B" if not noche else "#2F5A35"
        return f'<rect x="0" y="{GY}" width="{W}" height="{H-GY}" fill="{c}"/><rect x="0" y="{GY}" width="{W}" height="10" fill="#5FA552"/>'
    if tipo == "tierra":
        c = "#B58A5A" if not noche else "#5B4632"
        s = [f'<rect x="0" y="{GY}" width="{W}" height="{H-GY}" fill="{c}"/>']
        for x in range(60, W, 230):
            s.append(f'<ellipse cx="{x}" cy="{GY+60 + (x % 3) * 25}" rx="22" ry="9" fill="#8C6A44"/>')
        return "".join(s)
    return ""


# ----------------------------------------------------------------- fondos
def edificios(noche, rnd, alto=1.0, base_y=GY, alpha=1.0, gris=False):
    s = []
    x = -20
    while x < W:
        w = rnd.randint(130, 220)
        h = int(rnd.randint(260, 520) * alto)
        col = rnd.choice(("#7B8BA1", "#90A0B5", "#6E7F96", "#A3B1C4")) if not noche else rnd.choice(("#1E2B47", "#24345A", "#1A2540"))
        if gris:
            col = "#55617A" if noche else "#B4BECB"
        s.append(f'<rect x="{x}" y="{base_y-h}" width="{w}" height="{h}" fill="{col}" opacity="{alpha}"/>')
        if not gris:
            for wy in range(base_y - h + 30, base_y - 40, 60):
                for wx in range(x + 20, x + w - 30, 45):
                    lit = noche and rnd.random() < 0.55
                    fill = "#FFE082" if lit else ("#D9E6F2" if not noche else "#2E3D63")
                    s.append(f'<rect x="{wx}" y="{wy}" width="24" height="32" fill="{fill}"/>')
        x += w + rnd.randint(8, 30)
    return "".join(s)


def montanas(noche, atardecer=False):
    a = "#5E8C6A" if not noche else "#1C2C3A"
    b = "#79A983" if not noche else "#24394A"
    if atardecer:
        a, b = "#9C6B7A", "#C38A85"
    return (f'<polygon points="-50,{GY} 250,420 520,{GY}" fill="{a}"/>'
            f'<polygon points="300,{GY} 700,330 1100,{GY}" fill="{b}"/>'
            f'<polygon points="900,{GY} 1300,400 1700,{GY}" fill="{a}"/>'
            f'<polygon points="1450,{GY} 1800,450 2100,{GY}" fill="{b}"/>'
            + ("" if noche or atardecer else
               '<polygon points="700,330 640,410 680,400 700,420 725,395 760,410" fill="#FFFFFF" opacity="0.85"/>'))


def arbol(x, k=1.0, noche=False):
    hoja = "#3E8E41" if not noche else "#1F4A2A"
    return (f'<rect x="{x-12*k}" y="{GY-150*k}" width="{24*k}" height="{150*k}" fill="#7A5230"/>'
            f'<circle cx="{x}" cy="{GY-190*k}" r="{85*k}" fill="{hoja}"/>'
            f'<circle cx="{x-55*k}" cy="{GY-150*k}" r="{55*k}" fill="{hoja}"/>'
            f'<circle cx="{x+55*k}" cy="{GY-150*k}" r="{55*k}" fill="{hoja}"/>')


def casa(x, ancho, alto, color, noche, puerta_abierta=False, techo="#B5523B", luz=True):
    y = GY - alto
    s = [f'<rect x="{x}" y="{y}" width="{ancho}" height="{alto}" fill="{color}" stroke="{INK}" stroke-width="6"/>',
         f'<polygon points="{x-30},{y} {x+ancho/2},{y-alto*0.55} {x+ancho+30},{y}" fill="{techo}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>']
    vent = "#FFE082" if (noche and luz) else "#CFE8FF"
    s.append(f'<rect x="{x+40}" y="{y+60}" width="90" height="80" fill="{vent}" stroke="{INK}" stroke-width="5"/>')
    pw, ph = 110, 200
    px = x + ancho - pw - 50
    if puerta_abierta:
        s.append(f'<rect x="{px}" y="{GY-ph}" width="{pw}" height="{ph}" fill="#FFE9A8" stroke="{INK}" stroke-width="5"/>')
        s.append(f'<polygon points="{px+pw},{GY-ph} {px+pw+45},{GY-ph+20} {px+pw+45},{GY-15} {px+pw},{GY}" fill="#8D5A3B" stroke="{INK}" stroke-width="5"/>')
    else:
        s.append(f'<rect x="{px}" y="{GY-ph}" width="{pw}" height="{ph}" fill="#8D5A3B" stroke="{INK}" stroke-width="5"/>')
        s.append(f'<circle cx="{px+pw-22}" cy="{GY-ph/2}" r="7" fill="#FFD54F"/>')
    return "".join(s)


def fondo(tipo, cielo_t, rnd, esc):
    noche = cielo_t == "noche"
    atar = cielo_t == "atardecer"
    s = []
    if tipo == "ciudad":
        s.append(edificios(noche, rnd, alto=0.75, gris=True, base_y=GY - 40))
        s.append(edificios(noche, rnd))
    elif tipo == "ciudad_lejos":
        s.append(montanas(noche))
        s.append(edificios(noche, rnd, alto=0.45, base_y=GY - 80))
    elif tipo == "afueras":
        s.append(montanas(noche, atar))
        s.append(edificios(noche, rnd, alto=0.5, base_y=GY))
        s[-1] = f'<g transform="translate(-900 0)">{s[-1]}</g>'
        s.append(arbol(1150, 0.9))
    elif tipo == "montanas":
        s.append(montanas(noche, atar))
        if esc.get("arboles"):
            for x in (180, 1650, 1820):
                s.append(arbol(x, 0.9, noche))
    elif tipo == "bosque":
        s.append(montanas(noche, atar))
        for x, k in ((120, 1.2), (380, 0.9), (1500, 1.1), (1760, 1.3), (1960, 1.0)):
            s.append(arbol(x, k, noche))
    elif tipo == "bodega":
        s.append(edificios(noche, rnd, alto=0.6, gris=True, base_y=GY - 30))
        s.append(f'<rect x="120" y="{GY-520}" width="760" height="520" fill="#C9884B" stroke="{INK}" stroke-width="8"/>')
        s.append(f'<rect x="200" y="{GY-340}" width="300" height="340" fill="#8C8C8C" stroke="{INK}" stroke-width="6"/>')
        for yy in range(GY - 320, GY, 40):
            s.append(f'<line x1="205" y1="{yy}" x2="495" y2="{yy}" stroke="#6E6E6E" stroke-width="4"/>')
        s.append(f'<rect x="300" y="{GY-480}" width="420" height="90" rx="10" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>')
        s.append(f'<text x="510" y="{GY-418}" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="54" fill="{INK}">BODEGA</text>')
        for bx, by in ((560, 0), (660, 0), (610, 1)):
            s.append(caja(bx, GY - 70 - by * 90, 90))
    elif tipo == "taller":
        s.append(montanas(noche, atar))
        s.append(f'<rect x="1350" y="{GY-430}" width="540" height="430" fill="#E0E0E0" stroke="{INK}" stroke-width="8"/>')
        s.append(f'<polygon points="1320,{GY-430} 1620,{GY-560} 1920,{GY-430}" fill="#546E7A" stroke="{INK}" stroke-width="8" stroke-linejoin="round"/>')
        s.append(f'<rect x="1420" y="{GY-400}" width="400" height="80" rx="8" fill="#FFC107" stroke="{INK}" stroke-width="6"/>')
        s.append(f'<text x="1620" y="{GY-345}" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="46" fill="{INK}">TALLER</text>')
        s.append(f'<rect x="1450" y="{GY-290}" width="340" height="290" fill="#37474F"/>')
        s.append(llanta(1720, GY - 60, 55))
        s.append(llanta(1770, GY - 60, 55))
    elif tipo == "pueblo":
        s.append(montanas(noche))
        for x, c in ((80, "#E57373"), (620, "#FFF176"), (1180, "#81C784"), (1640, "#64B5F6")):
            s.append(casa(x, 360, 300, c, noche))
    elif tipo == "casa":
        s.append(montanas(noche))
        s.append(casa(1030, 520, 420, "#64B5F6", noche, puerta_abierta=esc.get("puerta_abierta", False)))
        s.append(f'<rect x="1040" y="{GY-560}" width="0" height="0"/>')
    return "".join(s)


# ------------------------------------------------------------ objetos
def caja(x, y, t=90, abierta=False):
    s = [f'<rect x="{x-t/2}" y="{y-t*0.75}" width="{t}" height="{t*0.75}" fill="#D9A066" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>',
         f'<rect x="{x-t*0.08}" y="{y-t*0.75}" width="{t*0.16}" height="{t*0.75}" fill="#F3D7A6"/>']
    if abierta:
        s.append(f'<polygon points="{x-t/2},{y-t*0.75} {x-t*0.8},{y-t*1.1} {x-t*0.1},{y-t*1.0} {x},{y-t*0.75}" fill="#C98F55" stroke="{INK}" stroke-width="5"/>')
        s.append(f'<polygon points="{x+t/2},{y-t*0.75} {x+t*0.8},{y-t*1.1} {x+t*0.1},{y-t*1.0} {x},{y-t*0.75}" fill="#C98F55" stroke="{INK}" stroke-width="5"/>')
    return "".join(s)


def llanta(cx, cy, r, pinchada=False):
    if pinchada:
        return (f'<ellipse cx="{cx}" cy="{cy+r*0.35}" rx="{r*1.12}" ry="{r*0.65}" fill="#212121" stroke="{INK}" stroke-width="6"/>'
                f'<ellipse cx="{cx}" cy="{cy+r*0.35}" rx="{r*0.45}" ry="{r*0.28}" fill="#9E9E9E"/>')
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#212121" stroke="{INK}" stroke-width="6"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r*0.45}" fill="#9E9E9E"/><circle cx="{cx}" cy="{cy}" r="{r*0.12}" fill="#424242"/>')


def moto(pinchada=False, caja_atras=False, luz=False):
    """Moto en coordenadas locales: origen en el suelo, mirando a la derecha."""
    s = []
    if luz:
        s.append('<polygon points="215,-245 900,-330 900,-60" fill="#FFF59D" opacity="0.35"/>')
    s.append(llanta(-185, -78, 78, pinchada))
    s.append(llanta(190, -78, 78))
    # chasis
    s.append(f'<path d="M-185 -78 L-60 -175 L95 -175 L190 -78" fill="none" stroke="#455A64" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/>')
    s.append(f'<path d="M190 -78 L135 -300" fill="none" stroke="#455A64" stroke-width="14" stroke-linecap="round"/>')
    # motor
    s.append(f'<rect x="-40" y="-200" width="110" height="80" rx="16" fill="#607D8B" stroke="{INK}" stroke-width="5"/>')
    # tanque y carenaje
    s.append(f'<path d="M-30 -215 C -20 -280 120 -290 150 -230 L 140 -195 L -25 -195 Z" fill="#1E88E5" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>')
    # asiento
    s.append(f'<path d="M-170 -215 C -170 -245 -40 -248 -25 -222 L -25 -200 L -170 -200 Z" fill="#263238" stroke="{INK}" stroke-width="5"/>')
    # guardabarros trasero
    s.append(f'<path d="M-275 -110 C -255 -175 -160 -185 -120 -150" fill="none" stroke="#1E88E5" stroke-width="12" stroke-linecap="round"/>')
    # manubrio y farola
    s.append(f'<line x1="120" y1="-305" x2="175" y2="-318" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>')
    s.append(f'<circle cx="208" cy="-245" r="22" fill="#FFF59D" stroke="{INK}" stroke-width="5"/>')
    # exosto
    s.append(f'<path d="M-60 -120 L-230 -120" stroke="#9E9E9E" stroke-width="14" stroke-linecap="round"/>')
    if caja_atras:
        s.append(caja(-150, -230, 110))
    return "".join(s)


# ---------------------------------------------------------------- Rayo
def casco():
    """Casco integral en coordenadas locales: el cuello queda en (0,-460)."""
    return (
        '<path d="M-145 -545 C -158 -675 -70 -740 15 -737 C 115 -733 178 -660 172 -560 L 168 -500 '
        'C 164 -465 140 -450 105 -450 L -85 -450 C -122 -450 -142 -477 -144 -510 Z" fill="url(#gcasco)" '
        f'stroke="{INK}" stroke-width="12" stroke-linejoin="round"/>'
        '<path d="M-90 -707 C -30 -733 50 -735 110 -707" fill="none" stroke="#FFFFFF" stroke-width="16" stroke-linecap="round" opacity="0.9"/>'
        '<path d="M-5 -637 C 60 -651 135 -641 168 -613 L 165 -530 C 115 -515 45 -517 -12 -530 C -22 -560 -20 -610 -5 -637 Z" '
        f'fill="url(#gvisera)" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>'
        '<path d="M18 -615 C 60 -625 105 -622 135 -610" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity="0.55"/>'
        '<path d="M22 -593 C 45 -598 65 -598 82 -595" fill="none" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round" opacity="0.35"/>'
        f'<circle cx="-30" cy="-583" r="16" fill="#0D47A1" stroke="{INK}" stroke-width="6"/>'
        '<g stroke="#0D47A1" stroke-width="7" stroke-linecap="round"><line x1="90" y1="-490" x2="135" y2="-490"/>'
        '<line x1="90" y1="-473" x2="128" y2="-473"/></g>'
    )


BRAZOS = {
    "normal": ["0,-380 -45,-280 -55,-190", "0,-380 45,-280 55,-190"],
    "saluda": ["0,-370 -75,-300 -15,-250", "0,-385 160,-400 245,-515"],
    "piensa": ["0,-370 -75,-300 -15,-250", "0,-385 105,-330 125,-445"],
    "carga": ["0,-380 80,-330 150,-345", "0,-370 70,-290 150,-290"],
    "entrega": ["0,-380 130,-350 230,-370", "0,-370 120,-300 230,-310"],
    "celebra": ["0,-380 -95,-470 -120,-600", "0,-380 95,-470 120,-600"],
    "senala": ["0,-370 -75,-300 -15,-250", "0,-385 140,-410 280,-440"],
    "senala_abajo": ["0,-370 -75,-300 -15,-250", "0,-385 130,-330 230,-250"],
    "pulgar": ["0,-370 -75,-300 -15,-250", "0,-385 130,-360 175,-450"],
    "telefono": ["0,-370 -75,-300 -15,-250", "0,-385 110,-360 150,-470"],
    "triste": ["0,-380 -30,-280 -35,-185", "0,-380 30,-280 35,-185"],
    "empuja": ["0,-380 120,-380 230,-330", "0,-370 110,-320 230,-300"],
}
PIERNAS = {
    "normal": ["0,-195 -75,0", "0,-195 80,0"],
    "celebra": ["0,-195 -110,0", "0,-195 115,0"],
    "triste": ["0,-195 -45,0", "0,-195 45,0"],
    "corre": ["0,-195 -60,-100 -150,-40", "0,-195 90,-110 110,0"],
    "empuja": ["0,-195 -120,0", "0,-195 50,-100 60,0"],
}


def rayo(x, pose="normal", mira=1, k=1.0, gy=GY):
    br = BRAZOS.get(pose, BRAZOS["normal"])
    pi = PIERNAS.get(pose, PIERNAS["normal"])
    rot = ' transform="rotate(14 0 -460)"' if pose == "triste" else ""
    inclina = ' transform="rotate(8 0 -195)"' if pose == "empuja" else ""
    s = [f'<g transform="translate({x} {gy}) scale({k*mira} {k})">', f'<g{inclina}>',
         f'<g stroke="{INK}" stroke-width="20" stroke-linecap="round" stroke-linejoin="round" fill="none">',
         '<line x1="0" y1="-465" x2="0" y2="-195"/>']
    for p in pi + br:
        s.append(f'<polyline points="{p}"/>')
    s.append('</g>')
    for p in br:
        hx, hy = p.split()[-1].split(",")
        s.append(f'<circle cx="{hx}" cy="{hy}" r="17" fill="{INK}"/>')
    if pose == "carga" or pose == "entrega":
        cx = 190 if pose == "carga" else 270
        s.append(caja(cx, -270, 130))
    if pose == "telefono":
        s.append(f'<rect x="125" y="-545" width="55" height="95" rx="10" fill="#263238" stroke="{INK}" stroke-width="5"/>'
                 '<rect x="133" y="-535" width="39" height="70" rx="4" fill="#4FC3F7"/>')
    if pose == "saluda":
        s.append('<g stroke="#2F8DEB" stroke-width="9" stroke-linecap="round" fill="none">'
                 '<path d="M285 -560 Q305 -540 300 -510"/><path d="M315 -585 Q345 -545 335 -495"/></g>')
    s.append(f'<g{rot}>{casco()}</g>')
    s.append('</g></g>')
    return "".join(s)


def rayo_en_moto(x, mira=1, caja_atras=False, vel=False, luz=False, salto=0, inclina=0, pinchada=False,
                 saluda=False, parado=False):
    gy = GY - salto
    s = [f'<g transform="translate({x} {gy}) scale({mira} 1) rotate({inclina})">']
    if vel:
        s.append('<g stroke="#FFFFFF" stroke-width="10" stroke-linecap="round" opacity="0.8">'
                 '<line x1="-470" y1="-330" x2="-330" y2="-330"/><line x1="-520" y1="-240" x2="-340" y2="-240"/>'
                 '<line x1="-450" y1="-150" x2="-320" y2="-150"/></g>')
    s.append(moto(pinchada=pinchada, caja_atras=caja_atras, luz=luz))
    # piloto sentado
    s.append(f'<g stroke="{INK}" stroke-width="20" stroke-linecap="round" stroke-linejoin="round" fill="none">'
             '<line x1="-85" y1="-235" x2="-10" y2="-470"/>'
             '<polyline points="-85,-235 30,-200 20,-110"/>')
    if saluda:
        s.append('<polyline points="-35,-400 60,-470 70,-600"/>')
    else:
        s.append('<polyline points="-35,-400 70,-350 130,-310"/>')
    s.append('</g>')
    hx, hy = (70, -600) if saluda else (130, -310)
    s.append(f'<circle cx="{hx}" cy="{hy}" r="17" fill="{INK}"/>')
    s.append(f'<g transform="translate(-10 -5) scale(0.95)">{casco()}</g>')
    s.append('</g>')
    return "".join(s)


# ----------------------------------------------------------- otras personas
def persona(x, tipo="campesino", pose="normal", mira=1, asombro=False):
    k = {"nino": 0.62, "abuela": 0.8}.get(tipo, 0.9)
    s = [f'<g transform="translate({x} {GY}) scale({k*mira} {k})">']
    br = {
        "normal": ["0,-380 -45,-280 -55,-190", "0,-380 45,-280 55,-190"],
        "saluda": ["0,-380 -45,-280 -55,-190", "0,-385 130,-420 190,-540"],
        "pulgar": ["0,-380 -45,-280 -55,-190", "0,-385 120,-360 160,-450"],
        "corre": ["0,-380 -80,-330 -140,-380", "0,-380 90,-300 150,-330"],
        "recibe": ["0,-380 -90,-330 -170,-350", "0,-370 -80,-300 -170,-310"],
        "recibe_sin": ["0,-380 -90,-330 -170,-350", "0,-370 -80,-300 -170,-310"],
        "feliz": ["0,-380 -95,-470 -120,-590", "0,-380 95,-470 120,-590"],
        "taza": ["0,-380 -45,-280 -55,-190", "0,-385 -80,-330 -150,-350"],
    }[pose]
    pi = PIERNAS["corre"] if pose == "corre" else PIERNAS["normal"]
    if tipo == "abuela":
        s.append(f'<path d="M-95 -195 L 95 -195 L 60 -420 L -60 -420 Z" fill="#AB47BC" stroke="{INK}" stroke-width="10" stroke-linejoin="round"/>')
    s.append(f'<g stroke="{INK}" stroke-width="20" stroke-linecap="round" stroke-linejoin="round" fill="none">'
             '<line x1="0" y1="-450" x2="0" y2="-195"/>')
    for p in pi + br:
        s.append(f'<polyline points="{p}"/>')
    s.append('</g>')
    for p in br:
        hx, hy = p.split()[-1].split(",")
        s.append(f'<circle cx="{hx}" cy="{hy}" r="16" fill="{INK}"/>')
    # cabeza con cara
    s.append(f'<circle cx="0" cy="-545" r="95" fill="#FFFFFF" stroke="{INK}" stroke-width="12"/>')
    s.append('<circle cx="25" cy="-560" r="11" fill="#1A1A1A"/><circle cx="62" cy="-560" r="11" fill="#1A1A1A"/>')
    if asombro:
        s.append(f'<ellipse cx="45" cy="-505" rx="16" ry="20" fill="{INK}"/>')
    else:
        s.append(f'<path d="M15 -515 Q45 -485 75 -515" fill="none" stroke="{INK}" stroke-width="9" stroke-linecap="round"/>')
    if tipo == "campesino":
        s.append(f'<ellipse cx="0" cy="-615" rx="165" ry="28" fill="#F0D58C" stroke="{INK}" stroke-width="8"/>'
                 f'<path d="M-80 -620 C -75 -720 75 -720 80 -620 Z" fill="#F0D58C" stroke="{INK}" stroke-width="8"/>'
                 '<rect x="-80" y="-650" width="160" height="18" fill="#8D6E63"/>')
    elif tipo == "mecanico":
        s.append(f'<path d="M-90 -590 C -90 -680 90 -680 90 -590 Z" fill="#E53935" stroke="{INK}" stroke-width="8"/>'
                 f'<path d="M60 -600 L 170 -590 L 165 -575 L 60 -585 Z" fill="#E53935" stroke="{INK}" stroke-width="6"/>')
        s.append(f'<g transform="translate(-60 -190) rotate(-30)"><rect x="-8" y="-90" width="16" height="90" fill="#9E9E9E" stroke="{INK}" stroke-width="4"/>'
                 f'<circle cx="0" cy="-95" r="20" fill="none" stroke="#9E9E9E" stroke-width="12"/></g>')
    elif tipo == "nino":
        s.append(f'<path d="M-85 -585 C -60 -660 60 -670 90 -590 C 50 -620 -20 -625 -85 -585 Z" fill="#5D4037" stroke="{INK}" stroke-width="6"/>')
    elif tipo == "abuela":
        s.append(f'<circle cx="-70" cy="-625" r="42" fill="#CFD8DC" stroke="{INK}" stroke-width="7"/>'
                 f'<path d="M-90 -580 C -80 -650 60 -665 92 -575 C 40 -620 -40 -620 -90 -580 Z" fill="#CFD8DC" stroke="{INK}" stroke-width="6"/>'
                 '<circle cx="25" cy="-560" r="22" fill="none" stroke="#1A1A1A" stroke-width="5"/>'
                 '<circle cx="65" cy="-560" r="22" fill="none" stroke="#1A1A1A" stroke-width="5"/>')
        if pose == "recibe":
            s.append(caja(-200, -310, 130))
        if pose == "taza":
            s.append(f'<rect x="-190" y="-395" width="60" height="55" rx="8" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>'
                     '<path d="M-175 -415 q10 -20 0 -40 M-150 -415 q10 -20 0 -40" stroke="#B0BEC5" stroke-width="5" fill="none"/>')
    s.append('</g>')
    return "".join(s)


def perro(x, corre=False):
    s = [f'<g transform="translate({x} {GY})">']
    s.append(f'<g stroke="{INK}" stroke-width="14" stroke-linecap="round" fill="none">'
             '<line x1="-90" y1="-120" x2="70" y2="-120"/>')
    if corre:
        s.append('<line x1="-90" y1="-120" x2="-150" y2="-60"/><line x1="-90" y1="-120" x2="-40" y2="-10"/>'
                 '<line x1="70" y1="-120" x2="20" y2="-30"/><line x1="70" y1="-120" x2="140" y2="-50"/>')
    else:
        s.append('<line x1="-80" y1="-120" x2="-80" y2="0"/><line x1="60" y1="-120" x2="60" y2="0"/>')
    s.append('<path d="M-90 -120 Q -150 -180 -130 -220"/></g>')
    s.append(f'<circle cx="115" cy="-165" r="55" fill="#D7A86E" stroke="{INK}" stroke-width="9"/>'
             f'<path d="M80 -205 L 70 -270 L 115 -215 Z" fill="#8D6E63" stroke="{INK}" stroke-width="6"/>'
             f'<circle cx="135" cy="-180" r="8" fill="{INK}"/><circle cx="168" cy="-160" r="10" fill="{INK}"/>'
             f'<path d="M140 -130 q 15 20 30 0" stroke="#E57373" stroke-width="8" fill="none" stroke-linecap="round"/>')
    s.append('</g>')
    return "".join(s)


def carro(x, color="#E53935"):
    return (f'<g transform="translate({x} {GY})">'
            f'<path d="M-200 -60 L -200 -150 L -110 -160 L -60 -240 L 110 -240 L 170 -160 L 210 -150 L 210 -60 Z" fill="{color}" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<path d="M-45 -225 L 100 -225 L 145 -165 L -90 -165 Z" fill="#B3E5FC" stroke="{INK}" stroke-width="5"/>'
            f'{llanta(-120, -55, 55)}{llanta(130, -55, 55)}</g>')


# ------------------------------------------------------- textos y efectos
def ancho_texto(t, fs):
    return len(t) * fs * 0.56


def envolver(texto, fs, ancho):
    palabras, lineas, actual = texto.split(), [], ""
    for p in palabras:
        prueba = (actual + " " + p).strip()
        if ancho_texto(prueba, fs) > ancho and actual:
            lineas.append(actual)
            actual = p
        else:
            actual = prueba
    lineas.append(actual)
    return lineas


def burbuja(texto, x, y, de, ancho=380, pensamiento=False):
    fs = 44
    lineas = envolver(texto, fs, ancho - 60)
    w = max(ancho_texto(l, fs) for l in lineas) + 70
    h = len(lineas) * fs * 1.2 + 50
    bx, by = x - w / 2, y - h / 2
    s = []
    tx, ty = de
    if pensamiento:
        for i, r in enumerate((14, 22, 30)):
            fx = tx + (x - tx) * (i + 1) / 4.5
            fy = ty + (y + h / 2 - ty) * (i + 1) / 4.5
            s.append(f'<circle cx="{fmt(fx)}" cy="{fmt(fy)}" r="{r}" fill="#FFFFFF" stroke="{INK}" stroke-width="6"/>')
        s.append(f'<ellipse cx="{x}" cy="{y}" rx="{w/2+20}" ry="{h/2+10}" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>')
    else:
        bxm = min(max(tx, bx + 40), bx + w - 40)
        s.append(f'<polygon points="{fmt(bxm-28)},{fmt(by+h-4)} {fmt(bxm+28)},{fmt(by+h-4)} {tx},{ty}" fill="#FFFFFF" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>')
        s.append(f'<rect x="{fmt(bx)}" y="{fmt(by)}" width="{fmt(w)}" height="{fmt(h)}" rx="34" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>')
        s.append(f'<rect x="{fmt(bxm-24)}" y="{fmt(by+h-14)}" width="48" height="14" fill="#FFFFFF"/>')
    for i, l in enumerate(lineas):
        ly = y - (len(lineas) - 1) * fs * 0.6 + i * fs * 1.2 + fs * 0.35
        s.append(f'<text x="{x}" y="{fmt(ly)}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="bold" font-size="{fs}" fill="{INK}">{escape(l)}</text>')
    return "".join(s)


def onomatopeya(texto, x, y, chico=False):
    fs = 70 if chico else 110
    pts = []
    for i in range(24):
        a = math.pi * 2 * i / 24
        r = (1.0 if i % 2 == 0 else 0.72) * (ancho_texto(texto, fs) / 2 + 60)
        pts.append(f"{fmt(x + r * math.cos(a))},{fmt(y + r * 0.6 * math.sin(a))}")
    return (f'<polygon points="{" ".join(pts)}" fill="#FFEB3B" stroke="{INK}" stroke-width="7" stroke-linejoin="round"/>'
            f'<text x="{x}" y="{y + fs*0.35}" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="{fs}" fill="#E53935" stroke="{INK}" stroke-width="3">{escape(texto)}</text>')


def letrero(x, texto, sub="", grande=False, pequeno=False):
    w = 640 if grande else (300 if pequeno else 520)
    h = 200 if grande else 160
    top = GY - 420
    return (f'<rect x="{x-12}" y="{top+h}" width="24" height="{GY-top-h}" fill="#8D6E63" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="{x-w/2}" y="{top}" width="{w}" height="{h}" rx="14" fill="#2E7D32" stroke="#FFFFFF" stroke-width="8"/>'
            f'<rect x="{x-w/2}" y="{top}" width="{w}" height="{h}" rx="14" fill="none" stroke="{INK}" stroke-width="4"/>'
            f'<text x="{x}" y="{top+h*0.45}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="bold" font-size="{50 if grande else 44}" fill="#FFFFFF">{escape(texto)}</text>'
            f'<text x="{x}" y="{top+h*0.82}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="bold" font-size="{50 if grande else 42}" fill="#FFFFFF">{escape(sub)}</text>')


def telefono(x, y, texto):
    return (f'<g transform="translate({x} {y})">'
            f'<rect x="-150" y="-230" width="300" height="470" rx="40" fill="#263238" stroke="{INK}" stroke-width="8"/>'
            '<rect x="-128" y="-195" width="256" height="400" rx="16" fill="#E3F2FD"/>'
            f'<rect x="-110" y="-150" width="220" height="150" rx="18" fill="#FFFFFF" stroke="#1E88E5" stroke-width="6"/>'
            f'<text x="0" y="-95" text-anchor="middle" font-family="Arial, sans-serif" font-weight="bold" font-size="30" fill="#1E88E5">{escape(texto)}</text>'
            '<text x="0" y="-45" text-anchor="middle" font-family="Arial, sans-serif" font-size="24" fill="#455A64">Pueblo Escondido</text>'
            f'{caja(0, 150, 130)}'
            '<g stroke="#FFC107" stroke-width="9" stroke-linecap="round"><line x1="-190" y1="-250" x2="-225" y2="-285"/>'
            '<line x1="190" y1="-250" x2="225" y2="-285"/><line x1="0" y1="-260" x2="0" y2="-305"/></g></g>')


def caja_grande():
    x, y = 960, 760
    return (caja(x, y, 560)
            + f'<rect x="{x-200}" y="{y-330}" width="400" height="150" rx="12" fill="#FFFFFF" stroke="{INK}" stroke-width="6" transform="rotate(-4 {x} {y-255})"/>'
            + f'<text x="{x}" y="{y-280}" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="62" fill="#E53935" transform="rotate(-4 {x} {y-255})">FRÁGIL</text>'
            + f'<text x="{x}" y="{y-215}" text-anchor="middle" font-family="Arial, sans-serif" font-weight="bold" font-size="34" fill="{INK}" transform="rotate(-4 {x} {y-255})">Entregar HOY · Regalo</text>'
            + corazon(x + 200, y - 380, 60))


def corazon(x, y, t=50, color="#E91E63"):
    return (f'<path transform="translate({x} {y}) scale({t/50})" d="M0 15 C -10 -10 -50 -10 -50 18 C -50 45 -15 60 0 78 '
            f'C 15 60 50 45 50 18 C 50 -10 10 -10 0 15 Z" fill="{color}" stroke="{INK}" stroke-width="5"/>')


def regalo_abierto():
    x = 960
    return (caja(x, 880, 420, abierta=True)
            + f'<g transform="rotate(-8 {x-170} 420)"><rect x="{x-330}" y="250" width="320" height="380" rx="10" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
            f'<rect x="{x-305}" y="275" width="270" height="250" fill="#B3E5FC"/>'
            f'<circle cx="{x-170}" cy="370" r="45" fill="#FFFFFF" stroke="{INK}" stroke-width="7"/>'
            f'<circle cx="{x-185}" cy="365" r="6" fill="{INK}"/><circle cx="{x-155}" cy="365" r="6" fill="{INK}"/>'
            f'<path d="M{x-190} 390 Q{x-170} 408 {x-150} 390" stroke="{INK}" stroke-width="5" fill="none"/>'
            f'<path d="M{x-215} 330 C {x-200} 300 {x-140} 300 {x-125} 330" stroke="#6D4C41" stroke-width="16" fill="none" stroke-linecap="round"/>'
            f'<line x1="{x-170}" y1="415" x2="{x-170}" y2="510" stroke="{INK}" stroke-width="8"/>'
            f'<text x="{x-170}" y="590" text-anchor="middle" font-family="Arial, sans-serif" font-weight="bold" font-size="34" fill="{INK}">Tu nieta</text></g>'
            + f'<g transform="rotate(7 {x+180} 430)"><rect x="{x+40}" y="270" width="290" height="330" fill="#FFF8E1" stroke="{INK}" stroke-width="8"/>'
            + "".join(f'<line x1="{x+70}" y1="{340+i*45}" x2="{x+300}" y2="{340+i*45}" stroke="#90A4AE" stroke-width="6"/>' for i in range(5))
            + f'<text x="{x+185}" y="320" text-anchor="middle" font-family="Georgia, serif" font-style="italic" font-size="34" fill="{INK}">Querida abuela</text>'
            + corazon(x + 260, 520, 30) + '</g>'
            + corazon(x - 420, 220, 45) + corazon(x + 420, 200, 55) + corazon(x + 360, 330, 30))


def lluvia(rnd):
    s = ['<g stroke="#DDEBF7" stroke-width="5" stroke-linecap="round" opacity="0.75">']
    for _ in range(160):
        x, y = rnd.randint(-100, W), rnd.randint(-50, H)
        s.append(f'<line x1="{x}" y1="{y}" x2="{x-18}" y2="{y+55}"/>')
    s.append('</g>')
    return "".join(s)


def arcoiris():
    cols = ("#E53935", "#FB8C00", "#FDD835", "#43A047", "#1E88E5", "#8E24AA")
    return "".join(f'<path d="M 900 {GY} A {700-i*28} {560-i*28} 0 0 1 {2300-i*56} {GY}" fill="none" stroke="{c}" stroke-width="28" opacity="0.55"/>'
                   for i, c in enumerate(cols))


def charcos():
    return "".join(f'<ellipse cx="{x}" cy="{GY+45}" rx="120" ry="18" fill="#90CAF9" opacity="0.7"/>' for x in (300, 1300, 1750))


def rio():
    return (f'<path d="M 650 {GY} C 700 {GY+60} 1200 {GY+60} 1270 {GY} L 1350 {H} L 560 {H} Z" fill="#4FC3F7" stroke="#0288D1" stroke-width="6"/>'
            f'<g stroke="#FFFFFF" stroke-width="6" stroke-linecap="round" opacity="0.8"><line x1="760" y1="{GY+90}" x2="850" y2="{GY+90}"/>'
            f'<line x1="980" y1="{GY+130}" x2="1080" y2="{GY+130}"/></g>'
            '<g fill="#B0BEC5" stroke="#1A1A1A" stroke-width="4"><circle cx="760" cy="760" r="12"/><circle cx="1180" cy="730" r="10"/></g>')


def roca(x):
    return (f'<path d="M {x-260} {GY} C {x-280} {GY-200} {x-120} {GY-330} {x+20} {GY-300} C {x+200} {GY-280} {x+280} {GY-150} {x+250} {GY} Z" '
            f'fill="#8D8D8D" stroke="{INK}" stroke-width="8"/>'
            f'<path d="M {x-120} {GY-200} q 60 -30 120 0 M {x+40} {GY-120} q 70 -20 110 20" stroke="#6D6D6D" stroke-width="8" fill="none"/>'
            f'<rect x="{x-260}" y="{GY-40}" width="140" height="40" fill="#FF7043" stroke="{INK}" stroke-width="4"/>'
            + "".join(f'<rect x="{x-250+i*45}" y="{GY-40}" width="20" height="40" fill="#FFFFFF"/>' for i in range(3)))


def titulo(texto, sub, x=1340, fs=190):
    return (f'<text x="{x}" y="250" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" font-weight="900" font-size="{fs}" fill="#FFFFFF" stroke="{INK}" stroke-width="10" paint-order="stroke">{escape(texto)}</text>'
            f'<text x="{x}" y="340" text-anchor="middle" font-family="Arial, sans-serif" font-weight="bold" font-size="56" fill="#FFFFFF" stroke="{INK}" stroke-width="6" paint-order="stroke">{escape(sub)}</text>')


def subtitulo(texto):
    fs = 40
    lineas = envolver(texto, fs, 1500)
    h = len(lineas) * fs * 1.25 + 30
    y0 = H - h - 10
    s = [f'<rect x="160" y="{fmt(y0)}" width="1600" height="{fmt(h)}" rx="20" fill="#000000" opacity="0.62"/>']
    for i, l in enumerate(lineas):
        s.append(f'<text x="960" y="{fmt(y0 + 18 + fs + i * fs * 1.25 - 6)}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" '
                 f'font-weight="bold" font-size="{fs}" fill="#FFFFFF">{escape(l)}</text>')
    return "".join(s)


DEFS = ('<defs><linearGradient id="gvisera" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#3A4256"/>'
        '<stop offset="0.55" stop-color="#121621"/><stop offset="1" stop-color="#05070C"/></linearGradient>'
        '<linearGradient id="gcasco" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2F8DEB"/>'
        '<stop offset="1" stop-color="#1565C0"/></linearGradient></defs>')


def escena(i, narr, e):
    rnd = random.Random(i * 7 + 3)
    noche = e["cielo"] == "noche"
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">', DEFS,
         cielo(e["cielo"], rnd)]
    if e.get("arcoiris"):
        s.append(arcoiris())
    s.append(fondo(e.get("fondo", ""), e["cielo"], rnd, e))
    s.append(suelo(e.get("suelo", "carretera"), noche))
    if e.get("charcos"):
        s.append(charcos())
    if e.get("rio"):
        s.append(rio())
    if "letrero" in e:
        s.append(letrero(**e["letrero"]))
    if "roca" in e:
        s.append(roca(e["roca"]["x"]))
    for cx in e.get("carros", []):
        s.append(carro(cx, "#E53935" if cx < 900 else "#FBC02D"))
    if "moto_sola" in e:
        m = e["moto_sola"]
        s.append(f'<g transform="translate({m["x"]} {GY})">{moto(pinchada=m.get("pinchada", False))}</g>')
        if m.get("brillo"):
            s.append('<g fill="#FFEB3B" stroke="#1A1A1A" stroke-width="4">'
                     + "".join(f'<polygon transform="translate({x} {y})" points="0,-40 10,-10 40,0 10,10 0,40 -10,10 -40,0 -10,-10"/>'
                               for x, y in ((560, 520), (1080, 470), (1010, 700))) + '</g>')
    if "caja_suelo" in e:
        s.append(caja(e["caja_suelo"]["x"], GY, 140))
    if e.get("caja_grande"):
        s.append(caja_grande())
    if e.get("regalo_abierto"):
        s.append(regalo_abierto())
    if "perro" in e:
        s.append(perro(**e["perro"]))
    r = e.get("rayo")
    if r:
        modo = r.get("modo", "pie")
        if modo.startswith("moto"):
            s.append(rayo_en_moto(r["x"], mira=r.get("mira", 1), caja_atras=r.get("caja", False), vel=r.get("vel", False),
                                  luz=r.get("luz", False), salto=r.get("salto", 0), inclina=r.get("inclina", 0),
                                  pinchada=modo == "moto_pinchada", saluda=r.get("saluda", False)))
        else:
            s.append(rayo(r["x"], r.get("pose", "normal"), r.get("mira", 1)))
    for p in e.get("personas", []):
        s.append(persona(p["x"], p["tipo"], p.get("pose", "normal"), p.get("mira", 1), p.get("asombro", False)))
    if e.get("corazones"):
        s.append("".join(corazon(x, y, t) for x, y, t in ((1040, 250, 40), (1500, 200, 55), (980, 420, 30), (1600, 380, 35))))
    if e.get("lluvia"):
        s.append(lluvia(rnd))
    if "telefono" in e:
        s.append(telefono(**e["telefono"]))
    if "burbuja" in e:
        s.append(burbuja(**e["burbuja"]))
    if "onomatopeya" in e:
        s.append(onomatopeya(**e["onomatopeya"]))
    if "titulo" in e:
        s.append(titulo(e["titulo"], e.get("subtitulo", ""), e.get("titulo_x", 1340), e.get("titulo_fs", 190)))
    s.append(subtitulo(narr))
    s.append('</svg>')
    return "".join(s)


def main():
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    guion = []
    for i, (narr, e) in enumerate(ESCENAS, 1):
        with open(os.path.join(out, f"escena_{i:02d}.svg"), "w", encoding="utf-8") as f:
            f.write(escena(i, narr, e))
        guion.append({"n": i, "narracion": narr})
    with open(os.path.join(out, "guion.json"), "w", encoding="utf-8") as f:
        json.dump(guion, f, ensure_ascii=False, indent=1)
    print(len(ESCENAS), "escenas")


if __name__ == "__main__":
    main()
