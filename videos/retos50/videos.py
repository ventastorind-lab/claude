"""Guiones de la serie "Byron vs. 50" (10 videos).

Cada escena es (narración, especificación). Claves útiles:
n (contador y pila automáticos), byron, icono, tarjeta, burbuja, onomatopeya, reloj, titulo, confeti, suscribete, objeto_grande.
"""

FONDO_CUENTA = "cocina"


def _b(pose="toma", x=420, **kw):
    d = dict(pose=pose, x=x)
    d.update(kw)
    return d


def intro(titulo, que):
    return (f"¡Hola, hola! Soy Byron, el ajolote que lo prueba todo... para que tú no tengas que hacerlo. Hoy: ¿qué pasa si te {que} en un solo día? ¡Agárrense!",
            dict(fondo="cocina", byron=_b("saluda", ojos="feliz"), pila=50, titulo=(titulo, "en un solo día")))


def aviso(texto="Recuerda: a mí todo me vuelve a crecer. A ti no. ¡Así que no lo intentes en casa!"):
    return (texto, dict(fondo="plano", byron=_b("pulgar", 520), icono=("alerta", 1300, 470)))


def cuenta(n, narr, pose="toma", **kw):
    extra = {k: kw.pop(k) for k in list(kw) if k in ("icono", "tarjeta", "burbuja", "onomatopeya", "confeti", "burbujas_gas")}
    spec = dict(fondo=FONDO_CUENTA, n=n, pila=50 - n, byron=_b(pose, **kw))
    spec.update(extra)
    return (narr, spec)


def dato(narr, pose="senala", x=440, n=None, **kw):
    extra = {k: kw.pop(k) for k in list(kw) if k in ("icono", "tarjeta", "burbuja", "onomatopeya", "objeto_grande", "reloj")}
    spec = dict(fondo=kw.pop("fondo", "plano"), byron=_b(pose, x, **kw))
    if n is not None:
        spec["n"] = n
    spec.update(extra)
    return (narr, spec)


def despues(reloj, narr, pose="triste", **kw):
    extra = {k: kw.pop(k) for k in list(kw) if k in ("icono", "tarjeta", "onomatopeya")}
    fondo = "noche" if "A.M." in reloj else "cuarto"
    spec = dict(fondo=fondo, reloj=reloj, byron=_b(pose, 700 if fondo == "noche" else 520, **kw))
    spec.update(extra)
    return (narr, spec)


def bueno(narr):
    return (narr, dict(fondo="cocina", pila=2, byron=_b("pulgar", ojos="feliz"), icono=("check", 1450, 420)))


def final():
    return ("¿Qué quieres que pruebe la próxima vez? ¡Escríbelo en los comentarios! Yo me arriesgo por ti.",
            dict(fondo="cocina", pila=0, byron=_b("saluda", ojos="feliz"), titulo=("¿PRÓXIMO RETO?", "Escríbelo en los comentarios")))


def suscr():
    return ("¡Y suscríbete! Que a mí me vuelve a crecer la cola... pero los suscriptores no.",
            dict(fondo="plano", byron=_b("celebra", 480, ojos="feliz", boca="grande"), suscribete=True))


def tc(titulo, numero, unidad, y=150):
    return dict(titulo=titulo, numero=numero, unidad=unidad, x=1560, y=y, chica=True)


def tf(titulo, filas, grande=False):
    d = dict(titulo=titulo, filas=filas)
    if grande:
        d.update(grande=True, x=1340, y=150)
    return d


def tb(titulo, barras, unidad):
    m = max(v for _, v, _ in barras)
    colores = ["#90A4AE", "#78909C", "#E53935"]
    return dict(titulo=titulo, barras=[(k, v, m, c if c else colores[i]) for i, (k, v, c) in enumerate(barras)], unidad_barra=unidad)


def total(n_titulo, filas, narr):
    return (narr, dict(fondo="cocina", n=50, pila=0, byron=_b("celebra", ojos="feliz", boca="grande"), confeti=True, tarjeta=tf(n_titulo, filas)))


def compara(narr, filas):
    return (narr, dict(fondo="plano", byron=_b("panza", 420, ojos="grandes"), tarjeta=tf("Byron vs. lo normal", filas, grande=True)))


VIDEOS = {}

# ------------------------------------------------------------------ 1. BANANOS
VIDEOS["01_bananos"] = dict(objeto="banano", etiqueta="BANANO", color="#FBC02D", bebida=False, escenas=[
    intro("50 BANANOS", "comes cincuenta bananos"),
    aviso(),
    dato("Cincuenta bananos medianos pesan casi seis kilos. ¡Seis kilos de fruta!", pose="celebra", ojos="grandes", boca="o",
         objeto_grande=(1050, 560), tarjeta=tc("Peso total", "5,9 kg", "de banano")),
    cuenta(1, "Banano número uno. ¡Delicioso! Unas ciento cinco calorías, catorce gramos de azúcar natural, tres de fibra y mucho potasio.",
           tarjeta=tf("1 banano", [("Calorías", "105"), ("Azúcar", "14 g"), ("Fibra", "3 g"), ("Potasio", "420 mg")])),
    cuenta(3, "Hasta aquí todo perfecto. Comer uno o dos bananos al día es buenísimo para la mayoría de personas.", pose="pulgar", ojos="feliz", icono=("check", 1450, 420)),
    cuenta(10, "Banano diez. Ya llevo más de cuatro mil miligramos de potasio: más de lo que un adulto necesita en todo un día.",
           tarjeta=tb("Potasio", [("Necesidad diaria", 3500, None), ("Byron", 4200, "#FBC02D")], "mg")),
    dato("¿Y si me paso de potasio? Si los riñones están sanos, sacan el exceso por la orina. El peligro real es para personas con enfermedad renal.",
         pose="piensa", n=10, icono=("rinones", 1300, 450)),
    cuenta(15, "Banano quince. Cuarenta y cinco gramos de fibra: más de lo que se recomienda para todo un día.",
           tarjeta=tb("Fibra", [("Recomendado", 30, None), ("Byron", 45, "#43A047")], "g")),
    cuenta(20, "Banano veinte. Mi barriga empieza a hacer ruiditos. Tanta fibra fermenta en el intestino y produce... gases.",
           pose="panza", boca="grande", onomatopeya=("¡PRRR!", 1300, 360)),
    cuenta(25, "¡Mitad del reto! Dos mil seiscientas calorías y trescientos cincuenta gramos de azúcar. Más calorías que en todo un día normal.",
           tarjeta=tb("Calorías", [("Un día normal", 2000, None), ("Byron", 2625, "#FB8C00")], "kcal"), sudor=True),
    dato("¡Dato loco! Los bananos son un poquito radiactivos, por el potasio cuarenta. ¡Hasta existe una unidad llamada dosis equivalente a un banano!",
         ojos="grandes", boca="o", n=25, icono=("radiacion", 1300, 470)),
    dato("Pero es muchísimo menos que un vuelo en avión: un viaje de Nueva York a Los Ángeles equivale a unos cuatrocientos bananos. ¡Cero miedo!",
         pose="pulgar", n=25, tarjeta=tc("Vuelo NY → LA", "≈ 400", "bananos de radiación")),
    cuenta(35, "Banano treinta y cinco. Ya no quiero ver nada amarillo. Me siento lleno, pesado e inflado.", pose="panza", ojos="espiral", sudor=True),
    cuenta(45, "Banano cuarenta y cinco. Mis mandíbulas están cansadas de tanto masticar... ¡ya casi!", sudor=True),
    total("Total del día", [("Calorías", "5.250"), ("Azúcar", "700 g"), ("Fibra", "150 g"), ("Potasio", "21 g")],
          "¡BANANO CINCUENTA! ¡Lo logré! Más de cinco mil calorías, setecientos gramos de azúcar, ciento cincuenta de fibra y veintiún gramos de potasio."),
    compara("Comparado con lo recomendado: cinco veces la fibra, seis veces el potasio y más del doble de las calorías.",
            [("Fibra", "×5"), ("Potasio", "×6"), ("Calorías", "×2,6")]),
    despues("+2 HORAS", "Dos horas después: inflamación, cólicos y gases que podrían inflar un globo.", pose="panza", panza=110, icono=("gas", 950, 700)),
    despues("+6 HORAS", "Seis horas después: tanta fibra de golpe puede causar diarrea... o todo lo contrario. ¡Mi intestino está confundido!", pose="piensa", panza=90, icono=("bano", 1300, 520)),
    despues("+1 DÍA", "Al día siguiente: con riñones sanos, el potasio de más ya salió. Me queda la barriga adolorida y cero ganas de bananos.", ojos="cansado", panza=40),
    bueno("La buena noticia: el banano es una fruta excelente. Uno o dos al día te dan energía, potasio y fibra."),
    final(), suscr(),
])

# ------------------------------------------------------------------ 2. CAFÉ
VIDEOS["02_cafes"] = dict(objeto="tinto", etiqueta="CAFÉ", color="#6D4C41", bebida=True, escenas=[
    intro("50 CAFÉS", "tomas cincuenta tazas de café"),
    aviso(),
    dato("Cincuenta tazas son doce litros de café, y unos cuatro mil setecientos cincuenta miligramos de cafeína.", pose="celebra", ojos="grandes", boca="o",
         objeto_grande=(1050, 560), tarjeta=tc("Cafeína total", "4.750 mg", "en 50 tazas")),
    cuenta(1, "Taza número uno. Una taza de café filtrado de doscientos cuarenta mililitros tiene unos noventa y cinco miligramos de cafeína, y casi cero calorías si no le echas azúcar.",
           tarjeta=tf("1 taza (240 ml)", [("Cafeína", "95 mg"), ("Calorías", "≈ 2"), ("Azúcar", "0 g")])),
    cuenta(3, "Hasta tres o cuatro tazas al día, para la mayoría de adultos sanos, está bien. ¡Buenos días, cerebro!", pose="pulgar", ojos="feliz", icono=("check", 1450, 420)),
    cuenta(5, "Taza cinco. Cuatrocientos setenta y cinco miligramos. Ya pasé los cuatrocientos que la FDA considera seguros para un adulto.",
           tarjeta=tb("Cafeína", [("Seguro (FDA)", 400, None), ("Byron", 475, "#6D4C41")], "mg")),
    cuenta(8, "Taza ocho. Me tiemblan las manos, el corazón va a mil y hablo rapidísimo. ¡Rapidísimo! ¡RAPIDÍSIMO!", pose="normal", tiembla=True, sudor=True, ojos="grandes"),
    dato("La cafeína bloquea la adenosina, la sustancia que le avisa al cerebro que estás cansado. Por eso te sientes alerta... y acelerado.", n=8, icono=("cerebro", 1300, 420)),
    cuenta(13, "Taza trece. Más de mil doscientos miligramos. La FDA advierte que esa cantidad, tomada de golpe, puede causar convulsiones.",
           tarjeta=tb("Cafeína", [("Seguro (FDA)", 400, None), ("Riesgo de golpe", 1200, None), ("Byron", 1235, "#6D4C41")], "mg"), tiembla=True),
    dato("En la vida real, aquí ya tocaría ir a urgencias. ¡Por eso esto lo hace un ajolote profesional!", pose="pulgar", n=13, icono=("hospital", 1300, 470)),
    cuenta(20, "Taza veinte. Me arde el estómago: el café estimula el ácido. ¡Tengo un volcán en la panza!", pose="panza", boca="o", sudor=True, icono=("fuego", 1450, 470)),
    cuenta(25, "¡Mitad del reto! Seis litros de café. ¡Voy al baño cada diez minutos!", pose="normal", tiembla=True, icono=("bano", 1450, 520)),
    dato("¿Cuánta cafeína sería mortal? Se calcula que unos diez gramos: más o menos ciento cinco tazas de café. Los expertos dicen que con café normal es casi imposible llegar ahí.",
         ojos="grandes", n=25, tarjeta=tc("Dosis peligrosa", "≈ 10 g", "≈ 105 tazas de café")),
    dato("El peligro real está en la cafeína en polvo o en pastillas: una sola cucharadita de cafeína pura puede ser una sobredosis.", pose="piensa", n=25, icono=("alerta", 1300, 470)),
    cuenta(40, "Taza cuarenta. Veo colores, escucho mi corazón... ¡y creo que puedo oír los colores!", pose="normal", tiembla=True, ojos="espiral", sudor=True),
    total("Total del día", [("Café", "12 L"), ("Cafeína", "4.750 mg"), ("Calorías", "≈ 100")],
          "¡TAZA CINCUENTA! ¡Lo logré! Doce litros de café y cuatro mil setecientos cincuenta miligramos de cafeína."),
    compara("Eso es casi doce veces la cafeína que se considera segura, y unas cuatro veces el líquido que el cuerpo necesita en un día.",
            [("Cafeína", "×12"), ("Líquido", "×4")]),
    despues("+3 HORAS", "Tres horas después: ansiedad, náuseas y el corazón todavía acelerado.", pose="normal", tiembla=True, ojos="grandes", panza=60),
    despues("3:00 A.M.", "En la noche: cero sueño. La mitad de la cafeína sigue en el cuerpo unas cinco horas después.", pose="normal", ojos="grandes", panza=40),
    despues("+1 DÍA", "Al día siguiente: dolor de cabeza, cansancio... y una resaca de café terrible.", ojos="cansado", panza=20),
    bueno("La buena noticia: el café con moderación te ayuda a estar alerta y tiene antioxidantes. ¡Saludos a mi amigo Tinto, el detective!"),
    final(), suscr(),
])

# ------------------------------------------------------------------ 3. JALAPEÑOS
VIDEOS["03_jalapenos"] = dict(objeto="chile", etiqueta="JALAPEÑO", color="#43A047", bebida=False, escenas=[
    intro("50 JALAPEÑOS", "comes cincuenta chiles jalapeños"),
    aviso(),
    dato("Un jalapeño tiene entre dos mil quinientas y ocho mil unidades Scoville, la escala que mide el picante. El Carolina Reaper pasa del millón y medio.",
         ojos="grandes", boca="o", objeto_grande=(1000, 560), tarjeta=tf("Picante (Scoville)", [("Jalapeño", "2.500–8.000"), ("Carolina Reaper", "1,6 M")])),
    cuenta(1, "Chile número uno. ¡Ay, ay, ay! El culpable es la capsaicina: engaña a tu lengua para que sienta que se está quemando.",
           boca="o", sudor=True, icono=("fuego", 1450, 470)),
    dato("La capsaicina activa un receptor llamado TRPV1, el mismo que detecta el calor de verdad. Tu cerebro cree que tu boca está en llamas.", pose="piensa", n=1, icono=("cerebro", 1300, 420)),
    cuenta(5, "Chile cinco. Me lloran los ojos, me gotea la nariz y sudo como si estuviera en el desierto.", pose="normal", ojos="grandes", boca="o", sudor=True),
    dato("¿Y si tomo agua? ¡Error! La capsaicina no se disuelve en agua. Lo que ayuda es la leche, porque su grasa y su proteína se la llevan.",
         pose="piensa", n=5, icono=("botella", 1300, 520), burbuja=dict(texto="¡NO SIRVE!", x=1300, y=170, de=(1300, 260))),
    cuenta(10, "Chile diez. ¡Hipo! El picante puede irritar el diafragma. ¡Hip! ¡Hip!", pose="normal", boca="o", onomatopeya=("¡HIP!", 1300, 360)),
    cuenta(15, "Chile quince. El estómago empieza a arder. ¡Tengo un volcán adentro!", pose="panza", sudor=True, boca="o", icono=("fuego", 1450, 470)),
    cuenta(20, "Chile veinte. Dato curioso: el jalapeño tiene vitamina C. ¡Ya llevo más de trescientos miligramos!",
           tarjeta=tb("Vitamina C", [("Recomendado", 90, None), ("Byron", 332, "#43A047")], "mg"), sudor=True),
    cuenta(25, "¡Mitad del reto! Ya no siento la lengua. Mi boca está dormida y mi cara roja como un tomate.", pose="normal", ojos="espiral", sudor=True),
    dato("¿Por qué a tanta gente le encanta el picante? Porque el cerebro aprende que ese fuego no es peligroso, y la emoción se vuelve divertida.", pose="pulgar", n=25, icono=("cerebro", 1300, 420)),
    cuenta(35, "Chile treinta y cinco. Náuseas, ardor en el pecho y lágrimas. Esto ya no es divertido.", pose="panza", tiembla=True, sudor=True, ojos="grandes"),
    cuenta(45, "Chile cuarenta y cinco. ¡Leche, por favor! ¡Mucha leche!", pose="normal", boca="grande", sudor=True,
           burbuja=dict(texto="¡LECHE!", x=1250, y=260, de=(640, 330))),
    total("Total del día", [("Calorías", "≈ 200"), ("Vitamina C", "≈ 830 mg"), ("Picante", "MÁXIMO")],
          "¡CHILE CINCUENTA! ¡Sobreviví! Solo unas doscientas calorías... pero un incendio total en mi boca."),
    dato("La vitamina C llegó a unos ochocientos treinta miligramos, todavía por debajo del límite de dos mil. Lo malo aquí no es la nutrición... ¡es el fuego!",
         pose="pulgar", tarjeta=tb("Vitamina C", [("Byron", 830, "#43A047"), ("Límite máximo", 2000, None)], "mg")),
    despues("+2 HORAS", "Dos horas después: acidez y retorcijones. El estómago sigue protestando.", pose="panza", panza=60, icono=("fuego", 1300, 520)),
    despues("+8 HORAS", "Y lo peor... la capsaicina sale igual que entró: ardiendo. ¡El baño se convierte en un volcán!", pose="normal", ojos="grandes", panza=40, icono=("bano", 1300, 520)),
    dato("Y ojo: en dos mil dieciocho, un hombre terminó en el hospital con un dolor de cabeza terrible después de comerse un Carolina Reaper en un concurso.",
         pose="triste", tarjeta=tc("Caso real · 2018", "1 chile", "Carolina Reaper")),
    bueno("La buena noticia: con moderación, el picante es seguro para la mayoría de personas, y le da muchísimo sabor a la comida."),
    final(), suscr(),
])

# ------------------------------------------------------------------ 4. DONAS
VIDEOS["04_donas"] = dict(objeto="dona", etiqueta="DONA", color="#F06292", bebida=False, escenas=[
    intro("50 DONAS", "comes cincuenta donas"),
    aviso(),
    dato("Cincuenta donas glaseadas suman unas diez mil calorías. ¡Lo que muchas personas comen en cinco días!", pose="celebra", ojos="grandes", boca="o",
         objeto_grande=(1050, 560), tarjeta=tc("Calorías totales", "10.000", "≈ 5 días de comida")),
    cuenta(1, "Dona número uno. Una dona glaseada tiene, aproximadamente, doscientas calorías, once gramos de grasa y diez de azúcar.",
           tarjeta=tf("1 dona (aprox.)", [("Calorías", "200"), ("Grasa", "11 g"), ("Azúcar", "10 g")])),
    cuenta(3, "Una dona de vez en cuando no le hace daño a nadie. ¡Es un antojo delicioso!", pose="pulgar", ojos="feliz", icono=("check", 1450, 420)),
    cuenta(5, "Dona cinco. ¡Subidón de azúcar! Tengo energía para correr una maratón.", pose="celebra", ojos="feliz", boca="grande"),
    dato("El páncreas trabaja a toda máquina, soltando insulina para meter todo ese azúcar en las células.", n=5, icono=("pancreas", 1250, 520),
         burbuja=dict(texto="¡INSULINA!", x=1250, y=200, de=(1250, 380))),
    cuenta(10, "Dona diez. Dos mil calorías. Ya comí lo de todo un día... y apenas es mediodía.",
           tarjeta=tb("Calorías", [("Un día normal", 2000, None), ("Byron", 2000, "#F06292")], "kcal")),
    cuenta(15, "Dona quince. La grasa hace que el estómago se vacíe más lento. Me siento pesado como una piedra.", pose="panza", ojos="grandes"),
    cuenta(20, "Dona veinte. Doscientos veinte gramos de grasa. Casi tres veces el valor diario recomendado.",
           tarjeta=tb("Grasa", [("Valor diario", 78, None), ("Byron", 220, "#8E24AA")], "g"), sudor=True),
    cuenta(25, "¡Mitad del reto! Empalagado total. Ya no siento lo dulce, solo lo pesado.", pose="panza", ojos="espiral", boca="ondas"),
    dato("¿Engordaría? Para ganar un kilo de grasa hace falta un exceso de unas siete mil setecientas calorías. Con este reto, podría ganar alrededor de un kilo de grasa real.",
         pose="piensa", n=25, tarjeta=tc("Grasa ganada", "≈ 1 kg", "en un solo día")),
    cuenta(35, "Dona treinta y cinco. Náuseas. Mi cuerpo grita: ¡no más dulce!", pose="panza", sudor=True, ojos="espiral", boca="ondas"),
    cuenta(45, "Dona cuarenta y cinco. Masticar ya es un deporte extremo.", sudor=True),
    total("Total del día", [("Calorías", "10.000"), ("Azúcar", "500 g"), ("Grasa", "550 g")],
          "¡DONA CINCUENTA! Diez mil calorías, quinientos gramos de azúcar y quinientos cincuenta de grasa."),
    compara("Cinco veces las calorías de un día, diez veces el límite de azúcar y unas siete veces la grasa recomendada.",
            [("Calorías", "×5"), ("Azúcar", "×10"), ("Grasa", "×7")]),
    despues("+1 HORA", "Una hora después: el bajón de azúcar. Sueño, cansancio y mal humor.", ojos="cansado", panza=110),
    despues("+4 HORAS", "Cuatro horas después: pesadez, acidez y una barriga que no cabe en el sofá.", pose="panza", panza=100, icono=("gas", 950, 700)),
    despues("+1 DÍA", "Al día siguiente: la báscula marca varios kilos más, pero casi todo es comida y agua. De grasa real, cerca de un kilo.",
            pose="piensa", panza=50, icono=("bascula", 1150, 700)),
    bueno("La buena noticia: un antojo de vez en cuando está bien. El problema es convertirlo en costumbre."),
    final(), suscr(),
])

# ------------------------------------------------------------------ 5. BEBIDAS ENERGÉTICAS
VIDEOS["05_energeticas"] = dict(objeto="energetica", etiqueta="LATA", color="#1E3A8A", bebida=True, escenas=[
    intro("50 ENERGÉTICAS", "tomas cincuenta bebidas energéticas"),
    aviso("Este es el reto más peligroso hasta ahora. En serio: ¡nunca lo intentes!"),
    dato("Cincuenta latas de doscientos cincuenta mililitros: doce litros y medio, cuatro mil miligramos de cafeína y más de un kilo de azúcar.",
         pose="celebra", ojos="grandes", boca="o", objeto_grande=(1000, 560),
         tarjeta=tf("50 latas", [("Líquido", "12,5 L"), ("Cafeína", "4.000 mg"), ("Azúcar", "1,35 kg")])),
    cuenta(1, "Lata número uno. Ochenta miligramos de cafeína, veintisiete gramos de azúcar y unas ciento diez calorías.",
           tarjeta=tf("1 lata (250 ml)", [("Cafeína", "80 mg"), ("Azúcar", "27 g"), ("Calorías", "≈ 110")])),
    cuenta(2, "Lata dos. Ya pasé el límite diario de azúcar que recomienda la OMS... ¡con solo dos latas!",
           tarjeta=tb("Azúcar", [("Límite (OMS)", 50, None), ("Byron", 54, "#E53935")], "g")),
    cuenta(5, "Lata cinco. Cuatrocientos miligramos de cafeína: justo el límite que la FDA considera seguro.",
           tarjeta=tb("Cafeína", [("Seguro (FDA)", 400, None), ("Byron", 400, "#1E3A8A")], "mg")),
    cuenta(8, "Lata ocho. ¡Siento que vuelo! Bueno, no... pero me tiemblan hasta las branquias.", pose="normal", tiembla=True, sudor=True, ojos="grandes"),
    dato("El corazón late rapidísimo. Mucha cafeína y azúcar juntas pueden alterar el ritmo del corazón.", pose="panza", n=8, ojos="grandes", sudor=True, icono=("corazon", 1250, 470)),
    cuenta(15, "Lata quince. Mil doscientos miligramos de cafeína. La FDA advierte que esto, tomado rápido, puede causar convulsiones.",
           tarjeta=tb("Cafeína", [("Seguro (FDA)", 400, None), ("Riesgo de golpe", 1200, None), ("Byron", 1200, "#1E3A8A")], "mg"), tiembla=True),
    dato("En la vida real, este reto terminaría en urgencias mucho antes de la mitad. Las bebidas energéticas no son para tomarlas como agua.",
         pose="pulgar", n=15, icono=("hospital", 1300, 470)),
    cuenta(25, "¡Mitad del reto! Seis litros y cuarto, y dos mil miligramos de cafeína. Estoy sudando, temblando y con náuseas.",
           pose="panza", tiembla=True, sudor=True, ojos="espiral"),
    dato("Muchas energéticas traen taurina y otros ingredientes, pero el mayor problema sigue siendo la combinación de cafeína y azúcar en exceso.", pose="piensa", n=25),
    cuenta(35, "Lata treinta y cinco. Mi corazón suena como un tambor de carnaval.", pose="normal", tiembla=True, sudor=True, ojos="grandes", boca="o"),
    total("Total del día", [("Cafeína", "4.000 mg"), ("Azúcar", "1,35 kg"), ("Calorías", "5.500"), ("Líquido", "12,5 L")],
          "¡LATA CINCUENTA! Cuatro mil miligramos de cafeína, mil trescientos cincuenta gramos de azúcar y cinco mil quinientas calorías."),
    compara("Diez veces la cafeína segura y veintisiete veces el límite de azúcar... ¡esto es una bomba!", [("Cafeína", "×10"), ("Azúcar", "×27")]),
    despues("+1 HORA", "Una hora después: el corazón sigue acelerado, me duele la cabeza y no me puedo quedar quieto.", pose="normal", tiembla=True, panza=100),
    despues("3:00 A.M.", "En la noche: insomnio total. Cuento ovejas... y las ovejas también están aceleradas.", pose="normal", ojos="grandes", panza=80),
    despues("+1 DÍA", "Al día siguiente: bajón brutal. Cansancio, dolor de cabeza y mal genio.", ojos="cansado", panza=30),
    dato("Por eso las autoridades de salud recomiendan que niños y adolescentes eviten estas bebidas, y que nadie las mezcle con alcohol.", pose="senala", icono=("alerta", 1300, 470)),
    bueno("Si necesitas energía, lo mejor es dormir bien, comer bien y tomar agua. ¡Aburrido, pero funciona!"),
    final(), suscr(),
])

# ------------------------------------------------------------------ 6. CHOCOLATINAS
VIDEOS["06_chocolatinas"] = dict(objeto="chocolatina", etiqueta="CHOCOLATINA", color="#6D4C41", bebida=False, escenas=[
    intro("50 CHOCOLATINAS", "comes cincuenta chocolatinas"),
    aviso(),
    dato("Cincuenta barras de chocolate con leche de cuarenta y cinco gramos son más de dos kilos de chocolate.", pose="celebra", ojos="grandes", boca="o",
         objeto_grande=(1050, 560), tarjeta=tc("Chocolate total", "2,25 kg", "de chocolate con leche")),
    cuenta(1, "Chocolatina número uno. ¡Mmm! Unas doscientas treinta y cinco calorías, veinticuatro gramos de azúcar y trece de grasa.",
           tarjeta=tf("1 barra (45 g)", [("Calorías", "235"), ("Azúcar", "24 g"), ("Grasa", "13 g")])),
    cuenta(2, "Un pedacito de chocolate de vez en cuando es un placer. ¡Y el chocolate oscuro hasta tiene antioxidantes!", pose="pulgar", ojos="feliz", icono=("check", 1450, 420)),
    cuenta(5, "Chocolatina cinco. Ciento veinte gramos de azúcar: más del doble del límite de la OMS.",
           tarjeta=tb("Azúcar", [("Límite (OMS)", 50, None), ("Byron", 120, "#E53935")], "g")),
    dato("El chocolate tiene teobromina, una prima de la cafeína. Te da un empujoncito de energía... y de alegría.", n=5, icono=("cerebro", 1300, 420)),
    cuenta(10, "Chocolatina diez. Dos mil trescientas cincuenta calorías. Ya me comí todo un día... en chocolate.",
           tarjeta=tb("Calorías", [("Un día normal", 2000, None), ("Byron", 2350, "#6D4C41")], "kcal")),
    cuenta(15, "Chocolatina quince. Manos manchadas, cara manchada... ¡hasta el casco manchado!", pose="celebra", ojos="feliz", boca="grande"),
    cuenta(20, "Chocolatina veinte. Casi dos gramos de teobromina. En dosis altas puede causar sudor, temblores y dolor de cabeza.", pose="normal", tiembla=True, sudor=True),
    dato("¡Importante! Lo que para mí es un exceso, para un perro puede ser mortal: su cuerpo elimina la teobromina muy despacio. ¡Nunca le des chocolate a tu perro!",
         pose="senala", n=20, icono=("perro", 1300, 520)),
    cuenta(25, "¡Mitad del reto! Empalagado y con el estómago revuelto.", pose="panza", ojos="espiral", boca="ondas"),
    cuenta(35, "Chocolatina treinta y cinco. Mi corazón late más rápido y siento que sudo chocolate.", pose="normal", sudor=True, tiembla=True),
    total("Total del día", [("Calorías", "11.750"), ("Azúcar", "1,2 kg"), ("Grasa", "650 g")],
          "¡CHOCOLATINA CINCUENTA! Once mil setecientas cincuenta calorías, mil doscientos gramos de azúcar y seiscientos cincuenta de grasa."),
    compara("Casi seis veces las calorías de un día, veinticuatro veces el límite de azúcar y más de ocho veces la grasa.",
            [("Calorías", "×6"), ("Azúcar", "×24"), ("Grasa", "×8")]),
    despues("+2 HORAS", "Dos horas después: náuseas y dolor de barriga. Tanta grasa y azúcar caen pesadísimas.", pose="panza", panza=110, ojos="espiral"),
    despues("3:00 A.M.", "En la noche: la teobromina y un poquito de cafeína no me dejan dormir bien.", pose="normal", ojos="grandes", panza=80),
    despues("+1 DÍA", "Al día siguiente: más de un kilo de grasa ganada y un antojo extraño de... ¡ensalada!", pose="piensa", panza=40),
    bueno("La buena noticia: unos cuadritos de chocolate, mejor si es oscuro, pueden ser parte de una alimentación sana."),
    final(), suscr(),
])

# ------------------------------------------------------------------ 7. NARANJAS
VIDEOS["07_naranjas"] = dict(objeto="naranja", etiqueta="NARANJA", color="#FB8C00", bebida=False, escenas=[
    intro("50 NARANJAS", "comes cincuenta naranjas"),
    aviso(),
    dato("Cincuenta naranjas medianas pesan unos seis kilos y medio.", pose="celebra", ojos="grandes", boca="o",
         objeto_grande=(1050, 560), tarjeta=tc("Peso total", "6,5 kg", "de naranjas")),
    cuenta(1, "Naranja número uno. Unas sesenta calorías, doce gramos de azúcar natural, tres de fibra y unos setenta miligramos de vitamina C.",
           tarjeta=tf("1 naranja", [("Calorías", "62"), ("Azúcar", "12 g"), ("Fibra", "3 g"), ("Vitamina C", "70 mg")])),
    cuenta(2, "Con una o dos naranjas ya cubres la vitamina C de todo el día. ¡Así de poderosas son!", pose="pulgar", ojos="feliz", icono=("check", 1450, 420)),
    cuenta(10, "Naranja diez. Setecientos miligramos de vitamina C. El cuerpo usa lo que necesita, y el resto lo saca por la orina.",
           tarjeta=tb("Vitamina C", [("Recomendado", 90, None), ("Byron", 700, "#FB8C00")], "mg")),
    cuenta(15, "Naranja quince. ¡Cuánta acidez! Me arde la boca y siento los dientes ásperos.", pose="normal", boca="o", icono=("diente", 1400, 430)),
    cuenta(20, "Naranja veinte. Mil cuatrocientos miligramos de vitamina C... y me acerco al límite.", sudor=True),
    cuenta(29, "Naranja veintinueve. ¡Pasé los dos mil miligramos! Ese es el límite máximo diario de vitamina C para adultos.",
           tarjeta=tb("Vitamina C", [("Límite máximo", 2000, None), ("Byron", 2030, "#E53935")], "mg"), ojos="grandes"),
    dato("Pasarse de vitamina C no suele ser grave, pero puede causar náuseas, cólicos... y diarrea.", pose="panza", n=29, icono=("bano", 1300, 520)),
    cuenta(35, "Naranja treinta y cinco. Ciento cinco gramos de fibra. ¡Mi intestino está haciendo horas extra!", pose="panza", ojos="grandes"),
    dato("El ácido de los cítricos también puede causar agruras, sobre todo si comes tantos de golpe.", pose="panza", n=35, icono=("fuego", 1300, 470)),
    total("Total del día", [("Calorías", "3.100"), ("Azúcar", "600 g"), ("Fibra", "150 g"), ("Vitamina C", "3.500 mg")],
          "¡NARANJA CINCUENTA! Tres mil cien calorías, seiscientos gramos de azúcar natural, ciento cincuenta de fibra y tres mil quinientos miligramos de vitamina C."),
    compara("Casi cuarenta veces la vitamina C recomendada y cinco veces la fibra.", [("Vitamina C", "×39"), ("Fibra", "×5")]),
    despues("+2 HORAS", "Dos horas después: cólicos y ruidos en la barriga.", pose="panza", panza=110, icono=("gas", 950, 700)),
    despues("+4 HORAS", "Cuatro horas después: ¡carrera al baño! La vitamina C de más y la fibra hacen su trabajo.", pose="normal", ojos="grandes", panza=90, icono=("bano", 1300, 520)),
    despues("+1 DÍA", "Al día siguiente: el exceso de vitamina C ya salió por la orina. El cuerpo no la guarda, así que tanta naranja no te hace súper inmune.", pose="piensa", panza=40),
    dato("Ojo: a quienes tienen tendencia a cálculos en el riñón, los médicos suelen recomendarles evitar dosis altas de vitamina C.", pose="senala", icono=("rinones", 1300, 450)),
    bueno("La buena noticia: una o dos naranjas al día son una gran fuente de vitamina C y fibra. ¡Mejor enteras que en jugo!"),
    final(), suscr(),
])

# ------------------------------------------------------------------ 8. AGUA
VIDEOS["08_agua"] = dict(objeto="vaso_agua", etiqueta="VASO", color="#039BE5", bebida=True, escenas=[
    intro("50 VASOS DE AGUA", "tomas cincuenta vasos de agua"),
    aviso("Parece el reto más sano... pero puede ser uno de los más peligrosos. ¡No lo intentes!"),
    dato("Cincuenta vasos de doscientos cincuenta mililitros son doce litros y medio de agua.", pose="celebra", ojos="grandes", boca="o",
         objeto_grande=(1050, 560), tarjeta=tc("Agua total", "12,5 L", "en un solo día")),
    cuenta(1, "Vaso número uno. Agua: cero calorías, cero azúcar. ¡El cuerpo la ama!",
           tarjeta=tf("1 vaso", [("Agua", "250 ml"), ("Calorías", "0"), ("Azúcar", "0 g")])),
    cuenta(8, "Vaso ocho. Dos litros. Más o menos lo que un adulto necesita al día, contando lo que viene en la comida.", pose="pulgar", ojos="feliz", icono=("check", 1450, 420)),
    dato("Los riñones son unos campeones, pero tienen un límite: pueden sacar alrededor de un litro de agua por hora.", pose="piensa", n=8, icono=("rinones", 1300, 450)),
    cuenta(12, "Vaso doce. Tres litros. ¡Voy al baño cada quince minutos!", pose="normal", ojos="grandes", icono=("bano", 1450, 520)),
    cuenta(20, "Vaso veinte. Cinco litros. ¡Mi barriga hace olas!", pose="panza", boca="o", onomatopeya=("¡GLUP!", 1300, 330)),
    dato("Si tomas agua más rápido de lo que los riñones la sacan, la sangre se diluye y el sodio baja. Eso se llama hiponatremia.",
         pose="piensa", n=20, tarjeta=tc("Hiponatremia", "Na ↓", "sodio bajo en la sangre")),
    dato("Con poco sodio, las células se hinchan, incluidas las del cerebro. Por eso causa dolor de cabeza, confusión y, en casos graves, convulsiones.",
         pose="triste", n=20, icono=("cerebro", 1300, 420)),
    cuenta(25, "¡Mitad del reto! Seis litros y cuarto. Me duele la cabeza y estoy confundido. Esto ya es una señal de alarma.", pose="normal", ojos="espiral", sudor=True),
    dato("Y pasó de verdad: en dos mil siete, en un concurso de radio en Estados Unidos, una mujer tomó unos seis litros de agua en pocas horas para ganar una consola. Murió por intoxicación de agua.",
         pose="triste", n=25, tarjeta=tc("Caso real · 2007", "≈ 6 L", "en pocas horas")),
    cuenta(35, "Vaso treinta y cinco. Náuseas, vómito y calambres. Solo un ajolote de caricatura podría seguir.", pose="panza", tiembla=True, sudor=True, ojos="espiral"),
    ("¡Vaso cincuenta! Doce litros y medio. En una persona real, tomar esto en pocas horas podría ser mortal.",
     dict(fondo="cocina", n=50, pila=0, byron=_b("panza", ojos="espiral", sudor=True),
          tarjeta=tf("Total del día", [("Agua", "12,5 L"), ("Lo normal", "2–3 L")]))),
    compara("Es entre cuatro y seis veces lo que una persona necesita en un día.", [("Agua", "×4 a ×6")]),
    despues("+1 HORA", "Una hora después: baño, baño y más baño.", pose="normal", ojos="grandes", panza=100, icono=("bano", 1300, 520)),
    despues("+3 HORAS", "Tres horas después: si los riñones logran ponerse al día, el sodio vuelve poco a poco a la normalidad.", pose="piensa", panza=60, icono=("rinones", 1300, 450)),
    dato("Los deportistas de resistencia también pueden sufrir hiponatremia si toman demasiada agua sin reponer sales. Por eso existen las bebidas con electrolitos.", pose="senala", icono=("botella", 1300, 520)),
    bueno("La buena noticia: tomar agua es buenísimo. La clave es tomarla poco a poco durante el día, guiándote por tu sed."),
    final(), suscr(),
])

# ------------------------------------------------------------------ 9. HAMBURGUESAS
VIDEOS["09_hamburguesas"] = dict(objeto="hamburguesa", etiqueta="HAMBURGUESA", color="#8D6E63", bebida=False, escenas=[
    intro("50 HAMBURGUESAS", "comes cincuenta hamburguesas"),
    aviso(),
    dato("Cincuenta hamburguesas de comida rápida pesan más de diez kilos. ¡Diez kilos de comida en un día!", pose="celebra", ojos="grandes", boca="o",
         objeto_grande=(1050, 560), tarjeta=tc("Peso total", "≈ 10 kg", "de hamburguesas")),
    cuenta(1, "Hamburguesa número uno. Una de comida rápida tiene, aproximadamente, quinientas cincuenta calorías, veinticinco gramos de proteína y unos mil miligramos de sodio.",
           tarjeta=tf("1 hamburguesa (aprox.)", [("Calorías", "550"), ("Proteína", "25 g"), ("Grasa", "30 g"), ("Sodio", "1.000 mg")])),
    cuenta(2, "Hamburguesa dos. Ya llevo dos mil miligramos de sodio: el límite que recomienda la OMS para todo el día.",
           tarjeta=tb("Sodio", [("Límite (OMS)", 2000, None), ("Byron", 2000, "#8D6E63")], "mg")),
    cuenta(4, "Hamburguesa cuatro. Dos mil doscientas calorías. ¡Ya comí lo de un día entero!",
           tarjeta=tb("Calorías", [("Un día normal", 2000, None), ("Byron", 2200, "#FB8C00")], "kcal")),
    dato("Tanta sal da mucha sed. El cuerpo retiene agua para diluir el sodio, y te sientes hinchado.", pose="normal", n=4, ojos="grandes", icono=("salero", 1300, 420)),
    cuenta(8, "Hamburguesa ocho. Mi estómago dice: ¡estoy lleno! Normalmente aguanta entre uno y uno y medio litros.", pose="panza", ojos="grandes", icono=("estomago", 1400, 450)),
    dato("Estirado al máximo, el estómago llega a unos cuatro litros... pero cincuenta hamburguesas son más de diez kilos. ¡Es físicamente imposible!",
         pose="panza", n=8, ojos="grandes", tarjeta=tc("Estómago estirado", "≈ 4 L", "vs. 10 kg de comida")),
    cuenta(12, "Por suerte, soy un ajolote de caricatura. ¡Hamburguesa doce!", pose="celebra", ojos="feliz", boca="grande"),
    cuenta(20, "Hamburguesa veinte. Veinte mil miligramos de sodio. ¡Diez veces el límite diario!",
           tarjeta=tb("Sodio", [("Límite (OMS)", 2000, None), ("Byron", 20000, "#E53935")], "mg"), sudor=True),
    dato("Tanto sodio sube la presión arterial y pone al corazón a trabajar extra.", pose="panza", n=20, sudor=True, icono=("corazon", 1250, 470)),
    cuenta(30, "Hamburguesa treinta. Novecientos gramos de grasa. Siento que mi cuerpo es una freidora.", pose="panza", sudor=True, ojos="espiral"),
    cuenta(40, "Hamburguesa cuarenta. Ya no mastico, solo respiro... ¡y hasta respirar me cuesta!", pose="normal", ojos="espiral", sudor=True, tiembla=True),
    total("Total del día", [("Calorías", "27.500"), ("Sodio", "50 g"), ("Grasa", "1,5 kg")],
          "¡HAMBURGUESA CINCUENTA! Veintisiete mil quinientas calorías, cincuenta gramos de sodio y mil quinientos gramos de grasa."),
    compara("Casi catorce veces las calorías de un día y veinticinco veces el límite de sodio.", [("Calorías", "×14"), ("Sodio", "×25")]),
    despues("+2 HORAS", "Dos horas después: una sed terrible. Me tomaría un río entero.", pose="normal", ojos="grandes", panza=120, icono=("botella", 1300, 520)),
    despues("+6 HORAS", "Seis horas después: acidez, pesadez y una siesta obligatoria.", ojos="cansado", panza=110),
    despues("+1 DÍA", "Al día siguiente: la báscula sube varios kilos, sobre todo por agua retenida y comida. De grasa real, unos tres kilos.",
            pose="piensa", panza=70, icono=("bascula", 1150, 700)),
    bueno("La buena noticia: una hamburguesa de vez en cuando, con ensalada y agua, puede caber en una alimentación equilibrada."),
    final(), suscr(),
])

# ------------------------------------------------------------------ 10. MANZANAS
VIDEOS["10_manzanas"] = dict(objeto="manzana", etiqueta="MANZANA", color="#E53935", bebida=False, escenas=[
    intro("50 MANZANAS", "comes cincuenta manzanas"),
    aviso(),
    dato("Cincuenta manzanas medianas pesan más de nueve kilos.", pose="celebra", ojos="grandes", boca="o",
         objeto_grande=(1050, 560), tarjeta=tc("Peso total", "9,1 kg", "de manzanas")),
    cuenta(1, "Manzana número uno. Unas noventa y cinco calorías, diecinueve gramos de azúcar natural y más de cuatro gramos de fibra.",
           tarjeta=tf("1 manzana", [("Calorías", "95"), ("Azúcar", "19 g"), ("Fibra", "4,4 g")])),
    cuenta(2, "Dicen que una manzana al día mantiene alejado al médico. Una, sí. Cincuenta... ya veremos.", pose="pulgar", ojos="feliz", icono=("check", 1450, 420)),
    cuenta(7, "Manzana siete. Treinta gramos de fibra. ¡Ya llegué a la meta de fibra de todo el día!",
           tarjeta=tb("Fibra", [("Recomendado", 30, None), ("Byron", 31, "#43A047")], "g")),
    dato("Las manzanas tienen sorbitol, un azúcar que el intestino absorbe mal. En exceso, funciona como laxante.", pose="piensa", n=7, icono=("bano", 1300, 520)),
    cuenta(15, "Manzana quince. ¡Crunch, crunch! Me duelen las mandíbulas de tanto masticar.", boca="grande", onomatopeya=("¡CRUNCH!", 1300, 360)),
    cuenta(20, "Manzana veinte. Mi barriga suena como una orquesta: gases por la fibra y el sorbitol.", pose="panza", boca="o", onomatopeya=("¡PRRR!", 1300, 360)),
    dato("¡Ojo con las semillas! Tienen amigdalina, una sustancia que al masticarse puede liberar cianuro.", pose="senala", n=20, ojos="grandes", icono=("semilla", 1300, 450)),
    dato("Tragarse unas cuantas semillas enteras no pasa nada: salen intactas. El peligro sería masticar cientos de ellas. ¡Por eso hoy no me como las semillas!",
         pose="pulgar", n=20, tarjeta=tc("Semillas en 50 manzanas", "≈ 300", "¡no las mastiques!")),
    cuenta(25, "¡Mitad del reto! Cuatrocientos setenta y cinco gramos de azúcar natural. Aunque venga de la fruta, sigue siendo muchísima azúcar.",
           tarjeta=tc("Azúcar natural", "475 g", "en 25 manzanas"), sudor=True),
    cuenta(35, "Manzana treinta y cinco. Inflado como un globo. ¡Creo que voy a flotar!", pose="panza", ojos="espiral"),
    cuenta(45, "Manzana cuarenta y cinco. Ya no quiero ver nada rojo... ni verde.", sudor=True, ojos="grandes"),
    total("Total del día", [("Calorías", "4.750"), ("Azúcar", "950 g"), ("Fibra", "220 g")],
          "¡MANZANA CINCUENTA! Cuatro mil setecientas cincuenta calorías, novecientos cincuenta gramos de azúcar natural y doscientos veinte de fibra."),
    compara("Más de siete veces la fibra recomendada y más del doble de las calorías de un día.", [("Fibra", "×7"), ("Calorías", "×2,4")]),
    despues("+2 HORAS", "Dos horas después: gases épicos. ¡Podría inflar un dirigible!", pose="panza", panza=120, icono=("gas", 950, 700)),
    despues("+5 HORAS", "Cinco horas después: el sorbitol y la fibra hacen efecto. ¡Al baño, rápido!", pose="normal", ojos="grandes", panza=100, icono=("bano", 1300, 520)),
    despues("+1 DÍA", "Al día siguiente: barriga adolorida, pero sin nada grave... porque no mastiqué las semillas.", pose="pulgar", panza=40),
    bueno("La buena noticia: una o dos manzanas al día son geniales: fibra, vitaminas y nada de colesterol. ¡Con cáscara, mejor!"),
    final(), suscr(),
])
