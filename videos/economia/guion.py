"""Guion: ¿Qué pasa si imprimimos dinero infinito? La inflación explicada (≈ 9 min).

Cada línea: (hablante, texto, especificación de la escena).
Hablantes: byron, gertrudis, tornillo, tinto, socrates. Rayo nunca habla.
"""

# Repartos frecuentes (x de cada personaje en pantalla)
TODOS = [("gertrudis", 250), ("tornillo", 500), ("billetin", 740), ("byron", 960), ("buho", 1190), ("tinto", 1430), ("socrates", 1680)]

L = []


def l(quien, texto, **spec):
    L.append((quien, texto, spec))


def duo(a, xa, b, xb):
    return [(a, xa), (b, xb)]


# ------------------------------------------------------------------ ACTO 1 · Intro
l("byron", "¡Hola, hola! Soy Byron. Hoy no me voy a comer nada raro... hoy voy a hacer algo mucho más loco: ¡imprimir dinero infinito y regalárselo a todo Pueblo Escondido!",
  fondo="pueblo", reparto=[("byron", 520)], escala=0.75, titulo=("DINERO INFINITO", "¿Qué pasaría?"))
l("byron", "Y esta vez no estoy solo. Les presento a mis amigos: Doña Gertrudis, Don Tornillo, Billetín, la Doctora Búho, el detective Tinto, el filósofo Sócrates... y Rayo, que nunca habla.",
  fondo="pueblo", reparto=TODOS + [("rayo", 1860)], escala=0.42, presentacion=True)
l("gertrudis", "¡Mijo, ya lo vi todo desde el dron! ¿Dinero gratis para todos? ¡Yo me apunto!",
  fondo="pueblo", reparto=duo("gertrudis", 600, "byron", 1250), escala=0.68)
l("tornillo", "En mis tiempos, el dinero se ganaba trabajando. Esto me huele a problema.",
  fondo="ferreteria", reparto=duo("tornillo", 620, "byron", 1250), escala=0.68)
l("byron", "Tranquilos: esto es una historia para aprender economía. No es asesoría financiera, ¿listo?",
  fondo="plano", reparto=[("byron", 560)], escala=0.75, icono=("alerta", 1350, 470))

# ------------------------------------------------------------------ ACTO 2 · ¿Qué es el dinero?
l("socrates", "Un momento, Byron. Antes de imprimir dinero, hay que preguntarse algo muy profundo: ¿qué es el dinero?",
  fondo="plano", reparto=duo("socrates", 560, "byron", 1300), escala=0.68, burbuja_pensar=(900, 230))
l("socrates", "Hace miles de años no había billetes. La gente hacía trueque: cambiaba, por ejemplo, arepas por tornillos.",
  fondo="plano", reparto=[("socrates", 420)], escala=0.68, trueque=True)
l("socrates", "El problema: si Don Tornillo no quería arepas, no había negocio. Por eso inventamos el dinero: algo que todos aceptan a cambio de cualquier cosa.",
  fondo="plano", reparto=duo("socrates", 420, "tornillo", 1500), escala=0.62, burbuja=dict(texto="¿Arepas? No, gracias.", x=1400, y=180, de=(1480, 330)))
l("socrates", "El dinero sirve para tres cosas: para intercambiar, para ponerle precio a las cosas y para guardar valor para el futuro.",
  fondo="plano", reparto=[("socrates", 420)], escala=0.68,
  tarjeta=dict(titulo="El dinero sirve para…", filas=[("1. Intercambiar", "✔"), ("2. Poner precios", "✔"), ("3. Ahorrar valor", "✔")]))
l("socrates", "Pero ojo: un billete es solo papel. Vale porque todos confiamos en que mañana alguien lo va a aceptar. El dinero... es confianza.",
  fondo="plano", reparto=[("socrates", 420)], escala=0.68, billete_grande=(1250, 450, "$ 1.000"))
l("billetin", "¡Exacto! Mucho gusto, soy Billetín, un billete de dos mil pesos. Por fuera soy papel... pero por dentro soy pura confianza.",
  fondo="plano", reparto=duo("socrates", 420, "billetin", 1300), escala=0.68)
l("byron", "¿Y quién imprime el dinero de verdad? En Colombia, el Banco de la República. En otros países, su banco central.",
  fondo="banco", reparto=[("byron", 420)], escala=0.68)
l("tornillo", "Y no imprimen lo que se les antoja, muchacho. Tienen reglas, justamente para que no pase lo que vas a hacer tú.",
  fondo="banco", reparto=duo("byron", 420, "tornillo", 1500), escala=0.62)

# ------------------------------------------------------------------ ACTO 3 · La impresora
l("byron", "¡Demasiada teoría! Les presento... ¡la Imprimidora tres mil! Imprime un millón de pesos por segundo.",
  fondo="sotano", reparto=[("byron", 420)], escala=0.7, impresora=(1250, 640), onomatopeya=("¡BRRRR!", 1450, 260))
l("byron", "¡Un millón para cada habitante de Pueblo Escondido! ¡Dinero para todos!",
  fondo="pueblo", reparto=TODOS, escala=0.44, lluvia_billetes=True, todos_felices=True)
l("byron", "Rayo se encarga de repartirlo. Rápido, puntual... y sin decir una sola palabra.",
  fondo="pueblo", rayo_moto=True, carretilla=(1450, 900))
l("gertrudis", "¡Ay, qué felicidad! Con este millón me voy a comprar todas las arepas del mercado.",
  fondo="mercado", reparto=[("gertrudis", 420)], escala=0.68, precio=("AREPA", 2000, 2000))
l("byron", "Al principio todo es fiesta. La arepa cuesta dos mil pesos, y todos compran, compran y compran.",
  fondo="mercado", reparto=[("gertrudis", 300), ("byron", 640)], escala=0.6, precio=("AREPA", 2000, 2000), arepas_vuelan=True)
l("tornillo", "¡Me están vaciando la ferretería! Vendí en una mañana lo que vendo en un mes.",
  fondo="ferreteria", estantes_vacios=True, reparto=[("tornillo", 600)], escala=0.7)
l("tornillo", "Pero tengo un problema: no puedo fabricar tornillos más rápido. La fábrica produce lo mismo que ayer.",
  fondo="ferreteria", estantes_vacios=True, reparto=[("tornillo", 600)], escala=0.7,
  tarjeta=dict(titulo="Fábrica de tornillos", filas=[("Ayer", "1.000 / día"), ("Hoy", "1.000 / día")]))
l("socrates", "Y aquí está la clave: el pueblo tiene muchísimo más dinero... pero la misma cantidad de cosas para comprar.",
  fondo="plano", reparto=[("socrates", 400)], escala=0.66, balanza=True)
l("socrates", "Cuando hay más gente queriendo comprar y no hay más productos, los vendedores pueden subir los precios. Es la ley de la oferta y la demanda.",
  fondo="plano", reparto=[("socrates", 400)], escala=0.66, balanza=True, grafica=dict(titulo="Precios", puntos=[1, 1, 1.4, 2, 3.2], x=1100, y=150))
l("tornillo", "Si todos quieren mis tornillos y no me alcanzan, pues los subo. Antes quinientos pesos... ahora mil quinientos.",
  fondo="ferreteria", reparto=[("tornillo", 500)], escala=0.7, precio=("TORNILLO", 500, 1500))
l("gertrudis", "¡¿Seis mil pesos por una arepa?! ¡Esto es un robo!",
  fondo="mercado", reparto=[("gertrudis", 420)], escala=0.68, precio=("AREPA", 2000, 6000), enojada=True)
l("billetin", "¡Ay, no! Antes yo alcanzaba para una arepa entera... ¡y ahora no alcanzo ni para un pedacito!",
  fondo="mercado", reparto=[("billetin", 420)], escala=0.7, billetin=(1.0, 0.65), precio=("AREPA", 6000, 6000))
l("byron", "¡No se preocupen! ¡Imprimo otro millón para cada uno!",
  fondo="sotano", reparto=[("byron", 420)], escala=0.7, impresora=(1250, 640), onomatopeya=("¡BRRRR!", 1450, 260))
l("byron", "Y entonces... la arepa subió a veinte mil. Espera... ¿por qué no funciona?",
  fondo="mercado", reparto=[("byron", 420)], escala=0.7, byron_ojos="espiral", precio=("AREPA", 6000, 20000))

# ------------------------------------------------------------------ ACTO 4 · Tinto investiga
l("tinto", "Tres de la mañana. No duermo... investigo. Y este caso me tiene intrigado: el caso de la arepa carísima.",
  fondo="oficina", reparto=[("tinto", 520)], escala=0.75, titulo=("EL CASO DE LA AREPA", "Tinto investiga"))
l("tinto", "El culpable tiene nombre: inflación. Es cuando los precios de casi todo suben al mismo tiempo, durante un buen rato.",
  fondo="oficina", reparto=[("tinto", 420)], escala=0.7, expediente=("SOSPECHOSO", "INFLACIÓN"))
l("tinto", "Y la víctima es el poder de compra: con el mismo billete, cada vez puedes comprar menos cosas.",
  fondo="oficina", reparto=[("tinto", 420)], escala=0.7, poder_compra=True)
l("billetin", "¡Esa víctima soy yo! Sigo diciendo dos mil pesos... pero cada día valgo un poquito menos.",
  fondo="oficina", reparto=duo("tinto", 420, "billetin", 1300), escala=0.66, billetin=(0.8, 0.5))
l("buho", "Si me permite, detective: para medirla, en Colombia el DANE revisa los precios de una canasta de productos: comida, arriendo, transporte, salud, educación... Eso se llama el IPC.",
  fondo="oficina", reparto=duo("tinto", 300, "buho", 700), escala=0.6, canasta=(1350, 560))
l("buho", "Si la canasta costaba cien mil pesos y un año después cuesta ciento diez mil, la inflación de ese año fue del diez por ciento. Primero los datos, después las opiniones.",
  fondo="oficina", reparto=[("buho", 420)], escala=0.62,
  tarjeta=dict(titulo="Inflación = 10 %", barras=[("Año 1", 100000, 110000, "#90A4AE"), ("Año 2", 110000, 110000, "#E53935")], unidad_barra="$"))
l("tinto", "Pista número uno: demasiado dinero persiguiendo muy pocos productos. Exactamente lo que hizo Byron con su impresora.",
  fondo="oficina", reparto=duo("tinto", 420, "byron", 1450), escala=0.65, pista=1, byron_ojos="grandes")
l("tinto", "Pista número dos: los costos. Si sube la gasolina, a Rayo le cuesta más repartir, y ese costo termina en el precio de todo.",
  fondo="pueblo", rayo_moto=True, pista=2, precio=("GASOLINA", 15000, 17500))
l("tornillo", "Y si a mí me sube el acero, el tornillo me sale más caro de fabricar. ¿Y quién paga la diferencia? El cliente.",
  fondo="ferreteria", reparto=[("tornillo", 500)], escala=0.7, precio=("ACERO (kg)", 4000, 5200))
l("tinto", "Pista número tres: las expectativas. Si todos creen que mañana todo será más caro, compran hoy, suben precios hoy... y la profecía se cumple sola.",
  fondo="oficina", reparto=[("tinto", 420)], escala=0.7, pista=3, grafica=dict(titulo="Expectativas", puntos=[1, 1.2, 1.5, 1.9, 2.5], x=1100, y=150))
l("tinto", "Caso resuelto: Byron imprimió dinero, pero no creó ni una sola arepa más. Y el dinero, sin cosas que comprar, pierde valor.",
  fondo="oficina", reparto=duo("tinto", 420, "byron", 1450), escala=0.65, sello="CASO RESUELTO")
l("byron", "O sea... ¿que el dinero no es la riqueza?",
  fondo="plano", reparto=duo("byron", 520, "socrates", 1380), escala=0.65, byron_ojos="grandes")
l("socrates", "Exacto. La riqueza son las arepas, los tornillos, las casas y el trabajo de la gente. El dinero solo es la forma de intercambiarlos.",
  fondo="plano", reparto=duo("byron", 260, "socrates", 680), escala=0.62, riqueza=True)

# ------------------------------------------------------------------ ACTO 5 · La historia real
l("byron", "¿Y esto ha pasado de verdad? ¡Claro que sí! Viajemos a Alemania, en mil novecientos veintitrés.",
  fondo="historia", pais=("ALEMANIA", "1923", "alemania"), reparto=[("byron", 420)], escala=0.7)
l("tornillo", "Después de la Primera Guerra Mundial, Alemania tenía deudas enormes, y el gobierno empezó a imprimir billetes sin parar.",
  fondo="historia", pais=("ALEMANIA", "1923", "alemania"), reparto=[("tornillo", 420)], escala=0.7, impresora=(1350, 640))
l("byron", "Los precios llegaron a duplicarse en cuestión de días. La gente cobraba el sueldo y corría a gastarlo antes de que perdiera valor.",
  fondo="historia", pais=("ALEMANIA", "1923", "alemania"), reparto=[("byron", 420)], escala=0.7, precio=("PAN", 1000, 200000000000))
l("byron", "Se cuenta que una carretilla llena de billetes no alcanzaba ni para comprar un periódico.",
  fondo="historia", pais=("ALEMANIA", "1923", "alemania"), reparto=[("byron", 420)], escala=0.7, carretilla=(1300, 880))
l("socrates", "Los billetes valían tan poco que hay fotos famosas de niños jugando con fajos de billetes y usándolos para hacer cometas.",
  fondo="historia", pais=("ALEMANIA", "1923", "alemania"), reparto=[("socrates", 420)], escala=0.7, cometa=(1300, 360))
l("tinto", "En noviembre de mil novecientos veintitrés, un solo dólar llegó a valer cuatro coma dos billones de marcos. Billones, con be.",
  fondo="historia", pais=("ALEMANIA", "1923", "alemania"), reparto=[("tinto", 420)], escala=0.7,
  tarjeta=dict(titulo="Noviembre de 1923", numero="4,2 billones", unidad="de marcos por 1 dólar", x=1300, y=170, chica=False, grande=True))
l("byron", "Otro caso: Zimbabue, en dos mil ocho. El gobierno imprimió tanto dinero que los precios subían casi a diario.",
  fondo="historia", pais=("ZIMBABUE", "2008", "zimbabue"), reparto=[("byron", 420)], escala=0.7, lluvia_billetes=True)
l("gertrudis", "¡Mijo! ¿Ese billete dice cien billones? ¡Con eso me compro el barrio!",
  fondo="historia", pais=("ZIMBABUE", "2008", "zimbabue"), reparto=[("gertrudis", 420)], escala=0.7, billete_grande=(1250, 450, "100 BILLONES"))
l("billetin", "¡Primo! ¿Qué te pasó? ¡Tienes catorce ceros y no vales nada!",
  fondo="historia", pais=("ZIMBABUE", "2008", "zimbabue"), reparto=[("billetin", 420)], escala=0.7, billetin=(0.6, 0.6), billete_grande=(1250, 450, "100 BILLONES"))
l("tinto", "Ni el barrio, ni la cuadra. A comienzos de dos mil nueve sacaron un billete de cien billones de dólares zimbabuenses... y meses después, el país dejó de usar su propia moneda.",
  fondo="historia", pais=("ZIMBABUE", "2009", "zimbabue"), reparto=[("tinto", 420)], escala=0.7, billete_grande=(1250, 450, "100 BILLONES"), tachado=True)
l("tinto", "El economista Steve Hanke estimó que en noviembre de dos mil ocho los precios subieron unos setenta y nueve mil millones por ciento... en un solo mes.",
  fondo="historia", pais=("ZIMBABUE", "2008", "zimbabue"), reparto=[("tinto", 420)], escala=0.7,
  tarjeta=dict(titulo="Nov. 2008 (estimado)", numero="79.600.000.000 %", unidad="de inflación en un mes", x=1250, y=170, grande=True))
l("byron", "Y más cerca de nosotros: Venezuela. En dos mil dieciocho, el Fondo Monetario Internacional proyectó una inflación de un millón por ciento.",
  fondo="historia", pais=("VENEZUELA", "2018", "venezuela"), reparto=[("byron", 420)], escala=0.7,
  tarjeta=dict(titulo="Proyección del FMI · 2018", numero="1.000.000 %", unidad="de inflación anual", x=1250, y=170, grande=True))
l("socrates", "Detrás de esas cifras hay personas reales: ahorros que se evaporaron, sueldos que no alcanzaban, y millones de personas que tuvieron que emigrar.",
  fondo="historia", pais=("VENEZUELA", "2018", "venezuela"), reparto=[("socrates", 420)], escala=0.7, triste=True, maletas=(1250, 760))
l("tornillo", "Por eso, muchacho, imprimir dinero sin control no es un juego. Es de lo peor que le puede pasar a una economía.",
  fondo="ferreteria", reparto=duo("tornillo", 520, "byron", 1400), escala=0.65, byron_ojos="grandes")

# ------------------------------------------------------------------ ACTO 6 · Los ahorros y el banco central
l("gertrudis", "Ay, y yo que tengo mis ahorritos guardados debajo del colchón...",
  fondo="cuarto", reparto=[("gertrudis", 420)], escala=0.7, colchon=(1250, 820))
l("socrates", "Doña Gertrudis, la inflación es como un ladrón silencioso. Si es del diez por ciento, su millón de pesos compra en un año lo que hoy compran unos novecientos mil.",
  fondo="cuarto", reparto=duo("gertrudis", 360, "socrates", 820), escala=0.6, alcancia=True,
  tarjeta=dict(titulo="$1.000.000 con 10 % de inflación", barras=[("Hoy", 1000000, 1000000, "#43A047"), ("En 1 año", 909000, 1000000, "#E53935")], unidad_barra="$"))
l("tinto", "Y no hace falta ir tan lejos. En Colombia, la inflación de dos mil veintidós fue del trece coma doce por ciento: la más alta desde mil novecientos noventa y nueve.",
  fondo="plano", pais=("COLOMBIA", "2022", "colombia"), reparto=[("tinto", 420)], escala=0.7,
  tarjeta=dict(titulo="Colombia · 2022 (DANE)", numero="13,12 %", unidad="la más alta desde 1999", x=1300, y=200, grande=True))
l("tinto", "Y los alimentos subieron mucho más: casi un veintiocho por ciento en ese año.",
  fondo="mercado", reparto=[("tinto", 420)], escala=0.7, precio=("AREPA", 2000, 2560),
  tarjeta=dict(titulo="Colombia · 2022", barras=[("Inflación total", 13.12, 27.81, "#90A4AE"), ("Alimentos", 27.81, 27.81, "#E53935")], unidad_barra="%"))
l("byron", "¿Y quién nos defiende de la inflación?",
  fondo="banco", reparto=duo("byron", 420, "buho", 1500), escala=0.62, byron_ojos="grandes")
l("buho", "Para eso estamos los bancos centrales. Soy la Doctora Búho. En Colombia, el Banco de la República busca que la inflación esté cerca del tres por ciento al año.",
  fondo="banco", reparto=[("buho", 420)], escala=0.62, tarjeta=dict(titulo="Meta BanRep", numero="≈ 3 %", unidad="de inflación al año", x=1350, y=170, chica=True))
l("buho", "Mi herramienta principal son las tasas de interés. Si la inflación sube, suben las tasas: los préstamos se encarecen, la gente gasta un poco menos y los precios se calman.",
  fondo="banco", reparto=[("buho", 420)], escala=0.62, perilla=True)
l("tornillo", "A finales de dos mil veintidós, el Banco de la República subió su tasa al doce por ciento. Más caro para los que debíamos plata, pero necesario para frenar los precios.",
  fondo="ferreteria", reparto=[("tornillo", 420)], escala=0.7, tarjeta=dict(titulo="Tasa BanRep", numero="12 %", unidad="diciembre de 2022", x=1350, y=170, chica=True))
l("byron", "¿Y por qué no apuntan a cero por ciento de inflación?",
  fondo="plano", reparto=duo("byron", 520, "buho", 1380), escala=0.65, byron_ojos="grandes", burbuja_pensar=(950, 230))
l("buho", "Porque un poquito de inflación es normal en una economía que crece. Y lo contrario también es peligroso: si los precios bajan siempre, la gente deja de comprar esperando que todo sea más barato, y la economía se frena. Eso se llama deflación.",
  fondo="plano", reparto=[("buho", 420)], escala=0.62, grafica=dict(titulo="Deflación", puntos=[3, 2.6, 2.1, 1.6, 1.2], x=1100, y=150, color="#1E88E5"))

# ------------------------------------------------------------------ ACTO 7 · Consejos y cierre
l("gertrudis", "¿Y entonces qué hago con mis ahorros, mijo?",
  fondo="cuarto", reparto=duo("gertrudis", 520, "tornillo", 1380), escala=0.65)
l("tornillo", "Consejos de viejo, no de asesor: primero, no guarde todo debajo del colchón. Busque opciones seguras que le paguen intereses, ojalá por encima de la inflación.",
  fondo="ferreteria", reparto=[("tornillo", 420)], escala=0.7, consejo=(1, "Ahorra donde te paguen intereses"))
l("tinto", "Segundo: cuidado con las deudas de tasas altas, como algunas tarjetas de crédito. Con inflación alta, suelen ponerse todavía más caras.",
  fondo="oficina", reparto=[("tinto", 420)], escala=0.7, consejo=(2, "Cuidado con las deudas caras"))
l("socrates", "Tercero: la mejor inversión es aprender. Un oficio, una habilidad o un negocio no se los come la inflación tan fácil.",
  fondo="plano", reparto=[("socrates", 420)], escala=0.7, consejo=(3, "Invierte en aprender"))
l("byron", "Y cuarto: compara precios antes de comprar. ¡Cada peso cuenta!",
  fondo="mercado", reparto=[("byron", 420)], escala=0.7, consejo=(4, "Compara precios"))
l("byron", "Bueno... creo que voy a apagar la Imprimidora tres mil.",
  fondo="sotano", reparto=[("byron", 420)], escala=0.7, impresora=(1250, 640), impresora_apagada=True, onomatopeya=("¡CLIC!", 1450, 260))
l("tornillo", "¡Por fin dices algo sensato, muchacho!",
  fondo="ferreteria", reparto=duo("tornillo", 520, "byron", 1400), escala=0.65)
l("billetin", "¡Y yo por fin dejé de encogerme! ¡Vuelvo a sentirme como un billete de verdad!",
  fondo="pueblo", reparto=[("billetin", 600)], escala=0.75, billetin=(0.55, 1.0), todos_felices=True)
l("byron", "Hasta Rayo está de acuerdo. Y eso que nunca dice nada.",
  fondo="pueblo", reparto=[("byron", 600), ("rayo", 1300)], escala=0.65, rayo_pulgar=True)
l("byron", "Resumen: imprimir dinero no crea riqueza. Si hay más billetes, pero no más cosas, los precios suben. Y la inflación golpea más a quienes menos tienen.",
  fondo="pueblo", reparto=TODOS, escala=0.44,
  tarjeta=dict(titulo="Lo que aprendimos", grande=True, x=960, y=40,
               filas=[("Más billetes ≠ riqueza", "✔"), ("Más dinero = precios ↑", "✔"), ("Golpea al que menos tiene", "✔")]))
l("socrates", "Solo sé que no sé nada... pero ahora sé qué es la inflación.",
  fondo="plano", reparto=[("socrates", 600)], escala=0.75)
l("gertrudis", "Y yo ya saqué la plata del colchón. ¡Gracias, muchachos!",
  fondo="cuarto", reparto=[("gertrudis", 600)], escala=0.75)
l("byron", "¿Qué tema de economía quieres que expliquemos la próxima vez? ¿Las criptomonedas? ¿Los impuestos? ¿Cómo funciona un banco? ¡Escríbelo en los comentarios!",
  fondo="pueblo", reparto=TODOS + [("rayo", 1860)], escala=0.42, titulo=("¿PRÓXIMO TEMA?", "Escríbelo en los comentarios"))
l("byron", "¡Y suscríbete! Que en este canal, el conocimiento no tiene inflación.",
  fondo="plano", reparto=[("byron", 480)], escala=0.7, suscribete=True)
