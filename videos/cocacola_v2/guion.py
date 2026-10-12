"""Byron vs. 50 Coca-Colas — versión 2: viaje DENTRO del cuerpo.

Cada escena: (narración, spec). Claves de spec iguales al video original (videos/cocacola/escenas.py)
más:
  cuerpo=(órgano, fase)  → escena interior del cuerpo (anatomia.py), con BYRON CAM reaccionando.
  cam=dict(...)          → pose de Byron en la BYRON CAM.
  kie=dict(prompt=...)   → clip de video de KIE (imagen→video) que reemplaza el arranque de la escena.

Datos por lata (355 ml): 140 kcal, 39 g de azúcar, 34 mg de cafeína. 50 latas: 17,75 L, 1.950 g, 1.700 mg, 7.000 kcal.
"""
E = []


def esc(narr, **spec):
    E.append((narr, spec))


CAF = 34

# ------------------------------------------------------------------ gancho
esc("¿Qué le pasa a tu cuerpo si te tomas cincuenta Coca-Colas en un solo día? Hoy no solo lo voy a hacer... ¡nos vamos a meter ADENTRO del cuerpo para verlo todo!",
    fondo="cocina", byron=dict(pose="saluda", x=420, ojos="feliz"), latas=50, titulo=("50 COCA-COLAS", "¿qué pasa adentro?"),
    kie=dict(prompt="The pink cartoon axolotl waves enthusiastically at the camera and bounces with excitement in front of a wall of red soda cans, gills wiggling, camera slowly pushes in. Keep the exact same flat 2D cartoon style, thick black outlines, same character design, no text changes."))
esc("Soy Byron, el ajolote que lo prueba todo para que tú no tengas que hacerlo. Y en serio: no lo intentes en casa.",
    fondo="plano", byron=dict(pose="pulgar", x=520), icono=("alerta", 1300, 470))
esc("Cincuenta latas son casi dieciocho litros de gaseosa, casi dos kilos de azúcar y mil setecientos miligramos de cafeína. ¿Listo? ¡Vamos!",
    fondo="plano", byron=dict(pose="senala", x=440, boca="o", ojos="grandes"),
    tarjeta=dict(titulo="El reto", filas=[("Líquido", "17,7 L"), ("Azúcar", "1,95 kg"), ("Cafeína", "1.700 mg"), ("Calorías", "7.000")]))

# ------------------------------------------------------------------ boca
esc("Lata uno. El primer trago ni siquiera ha llegado al estómago... y el ataque ya empezó. En tus dientes.",
    fondo="cocina", byron=dict(pose="toma", x=420), latas=49, contador=1)
esc("La Coca-Cola tiene un pH de alrededor de dos y medio: es casi tan ácida como el jugo de limón. Y su ácido fosfórico ablanda el esmalte.",
    cuerpo=("dientes", "acido"), cam=dict(pose="normal", ojos="grandes", boca="o"))
esc("Encima, las bacterias de tu boca se dan un banquete con el azúcar... y fabrican todavía más ácido.",
    cuerpo=("dientes", "bacterias"), cam=dict(pose="panza", ojos="grandes"))

# ------------------------------------------------------------------ estómago
esc("Bajamos al estómago. Vacío, es más o menos del tamaño de un puño, y normalmente aguanta alrededor de un litro.",
    cuerpo=("estomago", "tamano"), cam=dict(pose="toma"))
esc("Pero cada lata trae gas: dióxido de carbono. Las burbujas inflan el estómago como un globo, y la presión tiene que salir por algún lado...",
    cuerpo=("estomago", "gas"), cam=dict(pose="panza", panza=20, ojos="grandes", boca="o"),
    kie=dict(prompt="The cartoon pink stomach character inflates like a balloon, soda bubbles rise and pop inside it, the pressure gauge needle swings to the red, its eyes go wide. Keep the exact same flat 2D cartoon style, thick black outlines, no text changes."))
esc("...¡por arriba! El gas sube por el esófago. ¡BUUURP!",
    fondo="cocina", byron=dict(pose="panza", x=420, panza=20, boca="grande"), latas=48, contador=2, onomatopeya=("¡BUUURP!", 1250, 380), burbujas_gas=True,
    kie=dict(prompt="The pink cartoon axolotl holds his big belly and lets out a huge burp, his whole body shakes, cheeks puff, bubbles burst out of his mouth and float upward. Keep the exact same flat 2D cartoon style, thick black outlines, same character design, no text changes."))

# ------------------------------------------------------------------ sangre y páncreas
esc("Ahora mira esto: toda la sangre de tu cuerpo tiene apenas unos cuatro o cinco gramos de azúcar disueltos. Una cucharadita.",
    cuerpo=("sangre", "normal"), cam=dict(pose="piensa"))
esc("Una sola lata trae treinta y nueve gramos. Casi nueve veces todo el azúcar de tu sangre... y va entrando desde el intestino.",
    cuerpo=("sangre", "azucar"), cam=dict(pose="normal", ojos="grandes", boca="o"),
    kie=dict(prompt="Inside a cartoon blood vessel: red blood cells stream from left to right while a flood of small white sugar hexagons pours in and swirls through the vessel, dynamic flow. Keep the exact same flat 2D cartoon style, thick black outlines, no text changes."))
esc("El páncreas da la alarma y suelta insulina: una especie de llave que abre las células para que el azúcar salga de la sangre.",
    cuerpo=("pancreas", ""), cam=dict(pose="senala"))
esc("Las células del hígado y de los músculos lo guardan como reserva. Pero esa bodega es pequeña: unos cien gramos en el hígado y unos cuatrocientos en los músculos.",
    cuerpo=("bodega", ""), cam=dict(pose="piensa", ojos="grandes"))

# ------------------------------------------------------------------ cerebro
esc("Lata cinco. Tu cerebro está de fiesta: el azúcar dispara dopamina, la química de la recompensa. ¡Por eso se siente tan rico!",
    cuerpo=("cerebro", "dopamina"), cam=dict(pose="celebra", ojos="feliz", boca="grande"))
esc("Y la cafeína bloquea a la adenosina, la molécula que le dice al cerebro: 'estoy cansado'. Resultado: cero sueño.",
    cuerpo=("cerebro", "cafeina"), cam=dict(pose="normal", ojos="grandes"))

# ------------------------------------------------------------------ corazón
esc("Lata doce. Cuatrocientos ocho miligramos de cafeína. Ya pasé lo que la FDA considera seguro para un adulto en todo un día.",
    fondo="cocina", byron=dict(pose="normal", x=420, panza=30, tiembla=True, ojos="grandes", sudor=True), latas=38, contador=12,
    tarjeta=dict(titulo="Cafeína", barras=[("Seguro (FDA)", 400, 420, "#90A4AE"), ("Byron", 12 * CAF, 420, "#6D4C41")], unidad_barra="mg"))
esc("El corazón se acelera, la presión sube y las venas sienten cada golpe. ¡Tum-tum, tum-tum, tum-tum!",
    cuerpo=("corazon", ""), cam=dict(pose="panza", panza=30, ojos="grandes", sudor=True),
    kie=dict(prompt="The cartoon red heart character beats extremely fast and bounces, the green heartbeat line races across the monitor, purple veins pulse with each beat. Keep the exact same flat 2D cartoon style, thick black outlines, no text changes."))

# ------------------------------------------------------------------ hígado
esc("Lata veinte. Setecientos ochenta gramos de azúcar. Y aquí va un dato clave: la mitad del azúcar de mesa es fructosa, y la fructosa va casi toda al hígado.",
    cuerpo=("higado", "fructosa"), cam=dict(pose="toma", panza=45))
esc("Cuando el hígado se satura, convierte lo que sobra en grasa. Gotitas de grasa que se van acumulando... así empieza el hígado graso.",
    cuerpo=("higado", "grasa"), cam=dict(pose="triste", panza=45, ojos="cansado"))

# ------------------------------------------------------------------ riñones
esc("Lata veinticinco. ¡Casi nueve litros adentro! Los riñones filtran como locos, pero solo pueden sacar alrededor de un litro por hora.",
    cuerpo=("rinones", ""), cam=dict(pose="panza", panza=75, ojos="grandes", boca="o"))
esc("Si el líquido entra más rápido de lo que sale, la sangre se diluye y el sodio baja: eso se llama hiponatremia. Las células se hinchan... incluso las del cerebro. Es peligroso de verdad.",
    cuerpo=("sangre", "hipo"), cam=dict(pose="piensa", panza=75))
esc("Y la vejiga se llena una y otra vez. ¡Voy al baño cada veinte minutos!",
    fondo="plano", byron=dict(pose="corre", x=300, panza=75), icono=("bano", 1450, 520), contador=25)

# ------------------------------------------------------------------ intestino
esc("Lata treinta. Al intestino llega tanta fructosa que no la alcanza a absorber. La mayoría absorbe bien entre veinticinco y cincuenta gramos de una vez... y yo llevo casi seiscientos.",
    cuerpo=("colon", "fructosa"), cam=dict(pose="panza", panza=85, ojos="grandes"))
esc("Lo que no se absorbe llega al colon, donde billones de bacterias lo fermentan. Resultado: gases, inflamación... y agua que entra al intestino.",
    cuerpo=("colon", "diarrea"), cam=dict(pose="panza", panza=85, ojos="espiral"),
    kie=dict(prompt="Inside a cartoon purple intestine tube: little green and purple bacteria characters munch orange sugar pieces and release lots of gas bubbles that float up, water drops drip in. Keep the exact same flat 2D cartoon style, thick black outlines, no text changes."))
esc("Traducción: diarrea. ¡Y unos gases que suenan a trompeta! ¡PRRR!",
    fondo="cocina", byron=dict(pose="panza", x=420, panza=90, boca="grande", ojos="grandes"), latas=20, contador=30, onomatopeya=("¡PRRR!", 1300, 360))

# ------------------------------------------------------------------ peligro
esc("Lata treinta y cinco. Mil ciento noventa miligramos de cafeína. La FDA advierte que alrededor de mil doscientos miligramos de golpe pueden causar convulsiones.",
    fondo="cocina", byron=dict(pose="panza", x=420, panza=95, tiembla=True, sudor=True, ojos="grandes", boca="o"), latas=15, contador=35,
    tarjeta=dict(titulo="Cafeína", barras=[("Seguro (FDA)", 400, 1200, "#90A4AE"), ("Riesgo de golpe", 1200, 1200, "#E53935"), ("Byron", 35 * CAF, 1200, "#6D4C41")], unidad_barra="mg"))
esc("Sudor, temblor, ansiedad, náuseas... ¡vibro como celular en silencio!",
    fondo="cocina", byron=dict(pose="normal", x=420, panza=100, tiembla=True, sudor=True, ojos="espiral"), latas=15, contador=35,
    burbuja=dict(texto="¡BZZZ!", x=1100, y=260, de=(640, 330)),
    kie=dict(prompt="The pink cartoon axolotl vibrates rapidly like a phone on silent, sweat drops fly off, his spiral eyes spin, small motion lines around him. Keep the exact same flat 2D cartoon style, thick black outlines, same character design, no text changes."))
esc("En la vida real, esto termina en urgencias. Yo soy un ajolote profesional: no lo copies.",
    fondo="plano", byron=dict(pose="pulgar", x=440, panza=100), icono=("hospital", 1300, 470))

# ------------------------------------------------------------------ final
esc("¡LATA CINCUENTA! ¡Lo logré! Siete mil calorías, casi dos kilos de azúcar y mil setecientos miligramos de cafeína.",
    fondo="cocina", byron=dict(pose="celebra", x=420, panza=125, ojos="feliz", boca="grande"), latas=0, contador=50, confeti=True,
    tarjeta=dict(titulo="Total del día", filas=[("Calorías", "7.000"), ("Azúcar", "1,95 kg"), ("Cafeína", "1.700 mg"), ("Líquido", "17,7 L")]),
    kie=dict(prompt="The pink cartoon axolotl with a huge round belly jumps and celebrates with both arms up, colorful confetti rains down. Keep the exact same flat 2D cartoon style, thick black outlines, same character design, no text changes."))
esc("Este es el resumen de todo lo que le pasó al cuerpo, de la cabeza al colon.",
    cuerpo=("resumen", ""))
esc("Una hora después llega el bajón: la insulina barrió el azúcar y quedé agotado... pero la cafeína no me deja dormir.",
    fondo="cuarto", byron=dict(pose="triste", x=520, panza=110, ojos="cansado"), reloj="+1 HORA")
esc("La cafeína tarda unas cinco horas en bajar a la mitad. A las tres de la mañana sigo con los ojos como platos.",
    fondo="noche", byron=dict(pose="normal", x=700, panza=90, ojos="grandes"), reloj="3:00 A.M.")
esc("Al día siguiente: dolor de cabeza, mucha sed y cero energía.",
    fondo="plano", byron=dict(pose="triste", x=520, panza=40, ojos="cansado"), reloj="+1 DÍA", icono=("botella", 1300, 520))
esc("Y esto no es solo un chiste: hay casos médicos de personas que tomaban entre cuatro y seis litros de cola al día. Terminaron con el potasio muy bajo y debilidad muscular.",
    fondo="plano", byron=dict(pose="senala", x=440),
    tarjeta=dict(titulo="Casos reales", numero="4 a 6 L", unidad="de cola al día", x=1500, y=150, chica=True))
esc("Si lo hiciera todos los días: diabetes tipo dos, hígado graso, caries y muchos kilos de más.",
    fondo="plano", byron=dict(pose="panza", x=440, panza=125, ojos="grandes"), icono=("calendario_latas", 1300, 450))
esc("La buena noticia: una gaseosa de vez en cuando no te va a hacer daño. El problema es el exceso. Si tienes sed... agua.",
    fondo="plano", byron=dict(pose="toma_agua", x=520, ojos="feliz"), icono=("botella", 1300, 520))
esc("¿Qué quieres que pruebe la próxima vez? Escríbelo en los comentarios. ¡Y suscríbete, que a mí me vuelve a crecer la cola... pero los suscriptores no!",
    fondo="plano", byron=dict(pose="celebra", x=480, ojos="feliz", boca="grande"), suscribete=True)
