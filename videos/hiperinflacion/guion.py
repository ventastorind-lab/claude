"""Documental: Hiperinflación — cómo 7 países llegaron al abismo y cómo salieron (versión ilustrada).

Cada escena: (texto narrado, especificación visual). Visuales: mapas reales animados e ilustraciones
(gente, dinero, calles, tiendas, imprentas, minas...). Sin presentadores ni personajes fijos.
"""

E = []


def e(texto, vis, **v):
    v["vis"] = vis
    E.append((texto, v))


MUNDO = (5, 25, 5.4)
SIETE = ["DEU", "HUN", "BOL", "ARG", "BRA", "ZWE", "VEN"]
HIPER = ["FRA", "DEU", "AUT", "HUN", "POL", "RUS", "GRC", "CHN", "TWN", "PHL", "CHL", "BOL", "PER", "ARG", "BRA", "NIC", "SRB",
         "ZWE", "UKR", "GEO", "ARM", "AZE", "KAZ", "TKM", "TJK", "KGZ", "BLR", "MDA", "BGR", "COD", "AGO", "PRK", "VEN"]

# ------------------------------------------------------------------ INTRO
e("Imagina ir al mercado y que el pan cueste el doble que ayer. Y mañana, el doble otra vez.",
  "panaderia", era="2010", de=1000, dias=7)
e("Eso tiene nombre: hiperinflación. La definición clásica, del economista Phillip Cagan, es cuando los precios suben más del cincuenta por ciento en un solo mes.",
  "mercado", era="2010", sube=1.5, dato=("50 %", "de inflación en UN mes", "Definición de Phillip Cagan (1956)", "rojo"))
e("Al cincuenta por ciento mensual, en un año los precios se multiplican por casi ciento treinta.",
  "pan_vs_billetes", meses=12, factor=130)
e("Los economistas Steve Hanke y Nicholas Krus contaron cincuenta y seis episodios de hiperinflación en la historia moderna.",
  "mapa_hiper", dato=("56", "hiperinflaciones registradas", "Hanke y Krus · en el mapa, algunas de ellas", "dorado"))
e("Hoy vamos a recorrer siete de ellos: cómo llegaron al abismo... y, sobre todo, cómo lograron salir.",
  "mapa_siete")

# ------------------------------------------------------------------ 1. ALEMANIA
e("Capítulo uno. Alemania, mil novecientos veintitrés.", "capitulo", num=1, iso="DEU", pais="ALEMANIA", anio="1923", desde="mundo",
  pins=[(13.40, 52.52, "Berlín")])
e("Después de la Primera Guerra Mundial, Alemania quedó con deudas enormes y la obligación de pagar reparaciones de guerra a los vencedores.",
  "paneles", items=[("guerra", "Derrota en la Primera Guerra"), ("deuda", "Reparaciones: 132.000 millones de marcos oro")])
e("En enero de mil novecientos veintitrés, Francia y Bélgica ocuparon el Ruhr, su principal región industrial, porque Alemania se había atrasado en los pagos.",
  "mapa", iso="DEU", relleno=0.62, dx=0.08, resaltar=["DEU"], colores={"FRA": "#3D6FB6", "BEL": "#3D6FB6"},
  region=(7.2, 51.45, 70, "RUHR"), flechas=[((2.35, 48.85), (6.9, 51.35), "Francia"), ((4.35, 50.85), (6.9, 51.5), "Bélgica")],
  dato=("ENE 1923", "Ocupación del Ruhr", "Corazón industrial: carbón y acero", "rojo"))
e("El gobierno apoyó a los trabajadores en huelga... imprimiendo dinero para pagarles. La producción cayó, y la cantidad de billetes se disparó.",
  "huelga_imprenta", era="1920", color="marco")
e("Los precios llegaron a duplicarse en cuestión de días. En octubre de mil novecientos veintitrés, la inflación mensual llegó a casi treinta mil por ciento.",
  "grafica", iso="DEU", titulo="Marcos por 1 dólar (escala logarítmica, aprox.)", valores=[4.2, 190, 18000, 350000, 99000000, 4.2e12],
  etiquetas=["1914", "1922", "ene 23", "jul 23", "sep 23", "nov 23"], log=True, color="rojo", final="4,2 billones")
e("En noviembre, un dólar llegó a valer cuatro coma dos billones de marcos. Y un pan costaba unos doscientos mil millones.",
  "carretilla", era="1920", precio="200.000.000.000 MARCOS", dato=("4,2 billones", "de marcos por 1 dólar", "Noviembre de 1923", "rojo"))
e("¿Cómo salieron? El quince de noviembre de mil novecientos veintitrés lanzaron una moneda nueva: el Rentenmark.",
  "nuevo_billete", viejo="marco", nuevo="rentenmark", valor="1", moneda="RENTENMARK", fecha="15 · XI · 1923", era="1920")
e("Un Rentenmark equivalía a un billón de marcos viejos. Doce ceros eliminados de un plumazo.",
  "ceros", numero="1.000.000.000.000", quitar=12, moneda="MARK", color="marco", nuevo_color="rentenmark", nueva_moneda="RENTENMARK")
e("Pero la clave no fue cambiar el billete: se prohibió seguir financiando al gobierno con la impresora, y el nuevo dinero estaba respaldado por hipotecas sobre tierras e industria.",
  "paneles", items=[("candado", "Se apagó la impresora"), ("respaldo", "Respaldo: tierras e industria"), ("balanza", "Gasto público bajo control")], era="1920")
e("Con Hjalmar Schacht al frente del banco central, la confianza volvió y los precios se frenaron en cuestión de días. En mil novecientos veinticuatro llegó el Reichsmark.",
  "periodicos", era="1920", eventos=[("NOV 1923", "Nace el Rentenmark", "billete"), ("DIC 1923", "Schacht asume el Reichsbank", "banco"), ("AGO 1924", "Llega el Reichsmark", "billete")])
e("Pero el daño ya estaba hecho: la clase media perdió sus ahorros, y esa herida marcó la política alemana de los años siguientes.",
  "ahorros", era="1920")

# ------------------------------------------------------------------ 2. HUNGRÍA
e("Capítulo dos. Hungría, mil novecientos cuarenta y seis: la peor hiperinflación de la historia.",
  "capitulo", num=2, iso="HUN", pais="HUNGRÍA", anio="1946", desde="DEU", pins=[(19.04, 47.50, "Budapest")])
e("La Segunda Guerra Mundial destruyó cerca del cuarenta por ciento de la riqueza del país, y Hungría además tenía que pagar reparaciones y los costos de la ocupación soviética.",
  "ruinas", dato=("≈ 40 %", "de la riqueza nacional destruida", "Los puentes de Budapest, volados en 1945", "rojo"))
e("Sin impuestos suficientes y con todo por reconstruir, el gobierno cubrió el déficit... imprimiendo.",
  "imprenta", era="1940", color="pengo")
e("En julio de mil novecientos cuarenta y seis, los precios subieron casi cuarenta y dos mil billones por ciento en un solo mes. Se duplicaban cada quince horas.",
  "reloj", era="1940", dato=("4,19 × 10¹⁶ %", "de inflación en julio de 1946", "Récord mundial · precios × 2 cada 15 horas", "rojo"))
e("Hungría llegó a imprimir un billete de cien trillones de pengő: un uno con veinte ceros. Nunca alcanzó a circular.",
  "billete", valor="100.000.000.000.000.000.000", moneda="PENGŐ", color="pengo", sello="NUNCA CIRCULÓ", era="1940")
e("Intentaron crear una unidad paralela, el pengő de impuestos, para proteger el valor... pero también se derrumbó.",
  "adopengo", era="1940")
e("La salida llegó el primero de agosto de mil novecientos cuarenta y seis: una moneda nueva, el forinto, con un control estricto del gasto y nuevas reglas para el banco central.",
  "paneles", items=[("forinto", "Moneda nueva: el forinto"), ("balanza", "Control estricto del gasto"), ("banco", "Reglas nuevas al banco central")], era="1940")
e("Un forinto equivalía a cuatrocientos mil cuatrillones de pengős. Y el forinto sigue siendo la moneda de Hungría hasta hoy.",
  "montana_vs", color="pengo", contra="forinto", dato=("4 × 10²⁹", "pengő = 1 forinto", "El forinto sigue vigente hoy", "verde"))

# ------------------------------------------------------------------ 3. BOLIVIA
e("Capítulo tres. Bolivia, mil novecientos ochenta y cinco.", "capitulo", num=3, iso="BOL", pais="BOLIVIA", anio="1985", desde="HUN",
  pins=[(-68.15, -16.50, "La Paz")])
e("A comienzos de los ochenta, Bolivia tenía una deuda externa enorme, se le cerró el crédito internacional y sus exportaciones, como el estaño, valían cada vez menos.",
  "paneles", items=[("deuda_ext", "Deuda externa impagable"), ("banco_cerrado", "Sin crédito internacional"), ("estano", "El estaño vale cada vez menos")], era="1980")
e("El gobierno siguió gastando sin ingresos suficientes y lo cubrió con emisión. La inflación pasó de trescientos por ciento en mil novecientos ochenta y tres a más de dos mil en mil novecientos ochenta y cuatro.",
  "grafica", iso="BOL", titulo="Inflación anual en Bolivia", valores=[329, 2177, 8170], etiquetas=["1983", "1984", "1985"], log=False, color="rojo", final="8.170 %", unidad="%")
e("En mil novecientos ochenta y cinco superó el ocho mil por ciento anual, y solo en febrero los precios subieron ciento ochenta y tres por ciento.",
  "mercado", era="1980", andino=True, sube=2.83, dato=("8.170 %", "de inflación en 1985", "Solo en febrero: +183 %", "rojo"))
e("Un dólar llegó a costar alrededor de un millón de pesos bolivianos. Para hacer mercado, la gente cargaba bolsas de billetes.",
  "bolsas", era="1980", color="peso_bo", dato=("1 US$ ≈ 1.000.000", "de pesos bolivianos", "1985", "dorado"))
e("¿Cómo salieron? El veintinueve de agosto de mil novecientos ochenta y cinco, el gobierno firmó el Decreto Supremo veintiún mil sesenta.",
  "decreto", titulo="DECRETO SUPREMO 21060", lineas=["La Paz, 29 de agosto de 1985", "Nueva Política Económica"], bandera="bolivia")
e("Fue una terapia de choque: se dejó de financiar el gasto con emisión, se recortó el déficit, se liberaron los precios y se unificó el tipo de cambio.",
  "paneles", items=[("candado", "Fin de la emisión para gastar"), ("tijera", "Recorte del déficit"), ("etiqueta", "Precios liberados"), ("cambio", "Un solo tipo de cambio")], era="1980")
e("La hiperinflación se frenó casi de inmediato. Y en mil novecientos ochenta y siete nació el boliviano, que equivalía a un millón de pesos viejos.",
  "ceros", numero="1.000.000", quitar=6, moneda="PESOS BOLIVIANOS", color="peso_bo", nuevo_color="real", nueva_moneda="BOLIVIANO")
e("El costo social fue alto: con el cierre y la reestructuración de las minas estatales, miles de mineros perdieron su empleo.",
  "mineros", dato=("MILES", "de mineros sin empleo", "Reestructuración de la minería estatal", "rojo"))

# ------------------------------------------------------------------ 4. ARGENTINA
e("Capítulo cuatro. Argentina, mil novecientos ochenta y nueve.", "capitulo", num=4, iso="ARG", pais="ARGENTINA", anio="1989", desde="BOL",
  pins=[(-58.40, -34.60, "Buenos Aires")])
e("Argentina venía de años de déficit fiscal. En mil novecientos ochenta y cinco lanzó el Plan Austral, con moneda nueva... pero sin arreglar el gasto, la inflación volvió.",
  "periodicos", era="1980", eventos=[("1985", "Lanzan el Plan Austral", "billete"), ("1987", "La inflación vuelve", "grafica"), ("1989", "Hiperinflación", "grafica")])
e("En mil novecientos ochenta y nueve explotó: la inflación superó el tres mil por ciento y los precios se multiplicaron por cincuenta en un solo año.",
  "remarcar", dato=("3.079 %", "de inflación en 1989", "Precios × 50 en un año", "rojo"))
e("Hubo saqueos a supermercados, y el presidente Raúl Alfonsín entregó el poder cinco meses antes de lo previsto.",
  "saqueos", dato=("5 MESES", "antes de lo previsto", "Alfonsín entrega el poder · julio de 1989", "dorado"))
e("La solución llegó en mil novecientos noventa y uno: la Ley de Convertibilidad. Un peso nuevo equivalía a diez mil australes... y a un dólar.",
  "ceros", numero="10.000", quitar=4, moneda="AUSTRALES", color="austral", nuevo_color="real", nueva_moneda="PESO", extra="= 1 US$")
e("El banco central solo podía emitir pesos si tenía dólares en reserva para respaldarlos. Se acabó la impresora.",
  "boveda")
e("Funcionó: en pocos años, la inflación cayó a un solo dígito.",
  "grafica", iso="ARG", titulo="Inflación anual en Argentina (aprox.)", valores=[3079, 2314, 172, 25, 11, 4], etiquetas=["1989", "1990", "1991", "1992", "1993", "1994"],
  log=True, color="verde", final="un dígito", unidad="%")
e("Pero el uno a uno tenía un precio: sin poder ajustar el tipo de cambio y con deuda creciente, terminó en la crisis de dos mil uno. La ley se derogó en enero de dos mil dos.",
  "periodicos", era="2010", eventos=[("1991", "Convertibilidad: 1 a 1", "billete"), ("2001", "Estalla la crisis", "grafica"), ("ENE 2002", "Fin del 1 a 1", "billete")])

# ------------------------------------------------------------------ 5. BRASIL
e("Capítulo cinco. Brasil, mil novecientos noventa y cuatro.", "capitulo", num=5, iso="BRA", pais="BRASIL", anio="1994", desde="ARG",
  pins=[(-47.88, -15.79, "Brasilia")])
e("Brasil vivió años de inflación altísima y cambió de moneda una y otra vez: cruzado, cruzado nuevo, cruzeiro, cruzeiro real...",
  "billetes_serie", items=[("CRUZADO", "1986", "#C7D99A"), ("CRUZADO NOVO", "1989", "#E8C39E"), ("CRUZEIRO", "1990", "#B9D3E8"), ("CRUZEIRO REAL", "1993", "#E3B9C6")])
e("Los planes anteriores congelaban los precios a la fuerza. Al levantar el congelamiento, la inflación volvía con más fuerza.",
  "hielo")
e("En mil novecientos noventa y tres, la inflación fue de casi dos mil quinientos por ciento.",
  "mercado", era="1980", sube=1.35, dato=("2.477 %", "de inflación en 1993", "Índice IPCA", "rojo"))
e("La solución fue muy creativa: el Plan Real. Primero crearon una moneda virtual, la URV, que valía lo mismo que un dólar, y precios y salarios se expresaban también en URV.",
  "urv")
e("La gente se acostumbró a pensar en una unidad estable mientras seguía pagando con la moneda vieja. Así se rompió la memoria inflacionaria.",
  "paneles", items=[("urv", "Precios pensados en URV"), ("real", "La URV se vuelve el real"), ("balanza", "Más control del gasto")], era="1980")
e("El primero de julio de mil novecientos noventa y cuatro, la URV se convirtió en el real. Un real equivalía a dos mil setecientos cincuenta cruzeiros reales.",
  "montana_vs", color="cruzeiro", contra="real", n_fajos=2750, dato=("2.750", "cruzeiros reales = 1 real", "1 de julio de 1994", "verde"))
e("Con más disciplina fiscal y un banco central más firme, la inflación bajó a un dígito en pocos años. Y el real sigue siendo la moneda de Brasil.",
  "mapa", iso="BRA", relleno=0.6, dx=-0.18, resaltar=["BRA"], colores={"BRA": "#2A9D5C"}, billete_real=True,
  dato=("1994 → HOY", "el real sigue vigente", "Una de las salidas más exitosas", "verde"))

# ------------------------------------------------------------------ 6. ZIMBABUE
e("Capítulo seis. Zimbabue, dos mil ocho.", "capitulo", num=6, iso="ZWE", pais="ZIMBABUE", anio="2008", desde="BRA",
  pins=[(31.05, -17.83, "Harare")])
e("A partir del año dos mil, una reforma agraria desordenada hizo caer la producción de alimentos. Las exportaciones se desplomaron y el gobierno gastaba mucho más de lo que tenía.",
  "paneles", items=[("campo", "Cae la producción agrícola"), ("exportaciones", "Se desploman las exportaciones"), ("imprenta", "Gasto pagado con emisión")], era="2010")
e("El economista Steve Hanke estimó que en noviembre de dos mil ocho la inflación mensual llegó a unos setenta y nueve mil seiscientos millones por ciento.",
  "tienda_vacia", dato=("79.600 millones %", "de inflación en un mes", "Nov. 2008 · estimación de Steve Hanke", "rojo"))
e("Llegaron a imprimir billetes de cien billones de dólares zimbabuenses: un uno con catorce ceros.",
  "billete", valor="100.000.000.000.000", moneda="ONE HUNDRED TRILLION DOLLARS", color="zim", era="2010")
e("¿La salida? En dos mil nueve, Zimbabue dejó de usar su propia moneda y permitió el dólar estadounidense y otras monedas extranjeras.",
  "dolarizacion")
e("Los precios se estabilizaron rápido. Pero renunciar a tu moneda significa perder el control de la política monetaria. Años después, Zimbabue intentó volver a una moneda propia... y los problemas regresaron.",
  "periodicos", era="2010", eventos=[("2008", "Hiperinflación", "grafica"), ("2009", "Llega el dólar", "billete"), ("2019", "Vuelve la moneda propia", "billete"), ("DESPUÉS", "La inflación regresa", "grafica")])

# ------------------------------------------------------------------ 7. VENEZUELA
e("Capítulo siete. Venezuela, de dos mil diecisiete en adelante.", "capitulo", num=7, iso="VEN", pais="VENEZUELA", anio="2017", desde="ZWE",
  pins=[(-66.90, 10.49, "Caracas")])
e("Venezuela depende casi por completo del petróleo. Cuando su precio se desplomó en dos mil catorce, los ingresos del Estado se hundieron.",
  "petroleo")
e("El gobierno siguió financiando el gasto con dinero del banco central, mantuvo controles de precios y de cambio, y la producción de petróleo también cayó.",
  "paneles", items=[("imprenta", "Gasto financiado con emisión"), ("etiqueta_control", "Controles de precios y cambio"), ("petroleo_cae", "Cae la producción de petróleo")], era="2010")
e("El Fondo Monetario Internacional proyectó una inflación de un millón por ciento para dos mil dieciocho.",
  "pollo", dato=("1.000.000 %", "proyección del FMI para 2018", "Un pollo de 2,4 kg: 14,6 millones de bolívares (Reuters)", "rojo"))
e("Para ordenar las cuentas, Venezuela le quitó ceros a su moneda tres veces: tres en dos mil ocho, cinco en dos mil dieciocho y seis en dos mil veintiuno. Catorce ceros en total.",
  "ceros", numero="100.000.000.000.000", quitar=14, moneda="BOLÍVARES DE 2007", color="bolivar", nuevo_color="real", nueva_moneda="BOLÍVAR DIGITAL", etapas=[3, 5, 6])
e("Pero quitar ceros no cura la inflación: solo cambia la etiqueta. Lo que sí ayudó en parte fue que la economía empezó a usar dólares de forma informal y se redujo la emisión.",
  "paneles", items=[("dolar", "Dolarización informal"), ("candado", "Menos emisión"), ("etiqueta", "Menos controles de precios")], era="2010")
e("Millones de venezolanos emigraron en esos años. La inflación bajó, pero sigue estando entre las más altas del mundo.",
  "migracion", dato=("+7 MILLONES", "de venezolanos fuera del país", "Estimación de la plataforma R4V (ONU)", "dorado"))

# ------------------------------------------------------------------ CONCLUSIÓN
e("Siete países, siete historias. Pero si las miras juntas, el patrón se repite.", "mapa_siete", conclusion=True)
e("Primero: un golpe enorme. Una guerra, una deuda impagable o el desplome de una exportación.",
  "paneles", items=[("guerra", "1. Un golpe enorme")], era="1940", titulo="El patrón")
e("Segundo: un gobierno que gasta mucho más de lo que recauda y lo cubre con la impresora del banco central.",
  "paneles", items=[("guerra", "1. Un golpe enorme"), ("imprenta", "2. Déficit pagado con emisión")], ya=1, era="1940", titulo="El patrón")
e("Tercero: se pierde la confianza. Todos quieren deshacerse del dinero lo más rápido posible, y eso acelera todo.",
  "paneles", items=[("guerra", "1. Un golpe enorme"), ("imprenta", "2. Déficit pagado con emisión"), ("confianza", "3. Se pierde la confianza")], ya=2, era="1940", titulo="El patrón")
e("Y las salidas también se parecen: dejar de imprimir para financiar al gobierno, equilibrar las cuentas, un ancla creíble y un banco central independiente.",
  "paneles", items=[("candado", "Apagar la impresora"), ("balanza", "Equilibrar las cuentas"), ("ancla", "Un ancla creíble"), ("banco", "Banco central independiente")], era="2010", titulo="La receta")
e("Quitar ceros o cambiarle el nombre al billete, por sí solo, nunca ha funcionado. Sin disciplina fiscal, la inflación vuelve.",
  "tijera_ceros")
e("Para dimensionarlo, así se comparan los peores meses de algunos de estos países.",
  "barras", titulo="Peor mes de inflación (escala logarítmica)",
  items=[("HUN", "Hungría · jul 1946", 4.19e16, "41.900 billones %"), ("ZWE", "Zimbabue · nov 2008", 7.96e10, "79.600 millones %"),
         ("DEU", "Alemania · oct 1923", 29500, "29.500 %"), ("BOL", "Bolivia · feb 1985", 183, "183 %")])
e("La lección es simple: el dinero funciona mientras la gente confía en él. Y esa confianza tarda años en construirse... y muy poco en destruirse.",
  "confianza")
e("Si te gustó este recorrido, suscríbete y cuéntanos en los comentarios qué país quieres que analicemos a fondo.",
  "suscribete")
