"""Documental: Hiperinflación — cómo 7 países llegaron al abismo y cómo salieron.

Cada escena: (texto narrado, especificación visual). Sin personajes: solo gráficos animados.
Tipos visuales: precio_ticker, numero, capitulo, lista, grafica, barras, ceros, billete, tiempo, texto, paises, suscribete.
"""

E = []


def e(texto, **v):
    E.append((texto, v))


# ------------------------------------------------------------------ INTRO
e("Imagina ir al mercado y que el pan cueste el doble que ayer. Y mañana, el doble otra vez.",
  tipo="precio_ticker", producto="PAN", de=1000, dias=7)
e("Eso tiene nombre: hiperinflación. La definición clásica, del economista Phillip Cagan, es cuando los precios suben más del cincuenta por ciento en un solo mes.",
  tipo="numero", valor="50 %", etiqueta="de inflación en UN mes", nota="Definición de Phillip Cagan (1956)", color="rojo")
e("Al cincuenta por ciento mensual, en un año los precios se multiplican por casi ciento treinta.",
  tipo="numero", valor="×130", etiqueta="los precios en un año", nota="1,5 elevado a la 12", color="dorado")
e("Los economistas Steve Hanke y Nicholas Krus contaron cincuenta y seis episodios de hiperinflación en la historia moderna.",
  tipo="numero", valor="56", etiqueta="hiperinflaciones registradas", nota="Hanke y Krus, Instituto Cato", color="dorado")
e("Hoy vamos a recorrer siete de ellos: cómo llegaron al abismo... y, sobre todo, cómo lograron salir.",
  tipo="paises")

# ------------------------------------------------------------------ 1. ALEMANIA
e("Capítulo uno. Alemania, mil novecientos veintitrés.", tipo="capitulo", num=1, pais="ALEMANIA", anio="1923", bandera="alemania", cap=True)
e("Después de la Primera Guerra Mundial, Alemania quedó con deudas enormes y la obligación de pagar reparaciones de guerra a los vencedores.",
  tipo="lista", titulo="¿Cómo llegó ahí?", modo="causa", items=[("guerra", "Derrota en la Primera Guerra"), ("deuda", "Reparaciones de guerra enormes")])
e("En enero de mil novecientos veintitrés, Francia y Bélgica ocuparon el Ruhr, su principal región industrial, porque Alemania se había atrasado en los pagos.",
  tipo="lista", titulo="¿Cómo llegó ahí?", modo="causa", items=[("guerra", "Derrota en la Primera Guerra"), ("deuda", "Reparaciones de guerra enormes"), ("fabrica", "Ocupación del Ruhr (1923)")], ya=2)
e("El gobierno apoyó a los trabajadores en huelga... imprimiendo dinero para pagarles. La producción cayó, y la cantidad de billetes se disparó.",
  tipo="lista", titulo="¿Cómo llegó ahí?", modo="causa", items=[("guerra", "Derrota en la Primera Guerra"), ("deuda", "Reparaciones de guerra enormes"), ("fabrica", "Ocupación del Ruhr (1923)"), ("imprenta", "Imprimir para pagar huelgas")], ya=3)
e("Los precios llegaron a duplicarse en cuestión de días. En octubre de mil novecientos veintitrés, la inflación mensual llegó a casi treinta mil por ciento.",
  tipo="grafica", titulo="Marcos por 1 dólar · escala logarítmica (aprox.)", valores=[4.2, 190, 18000, 350000, 99000000, 4.2e12],
  etiquetas=["1914", "1922", "ene 23", "jul 23", "sep 23", "nov 23"], log=True, color="rojo", final="4,2 billones")
e("En noviembre, un dólar llegó a valer cuatro coma dos billones de marcos. Y un pan costaba unos doscientos mil millones.",
  tipo="numero", valor="4,2 billones", etiqueta="de marcos por 1 dólar", nota="Pan: ≈ 200.000.000.000 marcos", color="rojo")
e("¿Cómo salieron? El quince de noviembre de mil novecientos veintitrés lanzaron una moneda nueva: el Rentenmark.",
  tipo="texto", frase="La salida: el *RENTENMARK*", sub="15 de noviembre de 1923")
e("Un Rentenmark equivalía a un billón de marcos viejos. Doce ceros eliminados de un plumazo.",
  tipo="ceros", numero="1.000.000.000.000", quitar=12, resultado="= 1 Rentenmark", moneda="marcos")
e("Pero la clave no fue cambiar el billete: se prohibió seguir financiando al gobierno con la impresora, y el nuevo dinero estaba respaldado por hipotecas sobre tierras e industria.",
  tipo="lista", titulo="¿Cómo salió?", modo="solucion", items=[("candado", "Se apagó la impresora"), ("moneda", "Moneda nueva y respaldada"), ("balanza", "Gasto público bajo control")])
e("Con Hjalmar Schacht al frente del banco central, la confianza volvió y los precios se frenaron en cuestión de días. En mil novecientos veinticuatro llegó el Reichsmark.",
  tipo="tiempo", eventos=[("nov 1923", "Rentenmark"), ("dic 1923", "Schacht al Reichsbank"), ("ago 1924", "Reichsmark")])
e("Pero el daño ya estaba hecho: la clase media perdió sus ahorros, y esa herida marcó la política alemana de los años siguientes.",
  tipo="texto", frase="Ahorros de toda una vida: *PERDIDOS*", sub="La herida que dejó 1923")

# ------------------------------------------------------------------ 2. HUNGRÍA
e("Capítulo dos. Hungría, mil novecientos cuarenta y seis: la peor hiperinflación de la historia.",
  tipo="capitulo", num=2, pais="HUNGRÍA", anio="1946", bandera="hungria", cap=True)
e("La Segunda Guerra Mundial destruyó cerca del cuarenta por ciento de la riqueza del país, y Hungría además tenía que pagar reparaciones y los costos de la ocupación soviética.",
  tipo="lista", titulo="¿Cómo llegó ahí?", modo="causa", items=[("guerra", "40 % de la riqueza destruida"), ("deuda", "Reparaciones y ocupación")])
e("Sin impuestos suficientes y con todo por reconstruir, el gobierno cubrió el déficit... imprimiendo.",
  tipo="lista", titulo="¿Cómo llegó ahí?", modo="causa", items=[("guerra", "40 % de la riqueza destruida"), ("deuda", "Reparaciones y ocupación"), ("imprenta", "Déficit pagado con la impresora")], ya=2)
e("En julio de mil novecientos cuarenta y seis, los precios subieron casi cuarenta y dos mil billones por ciento en un solo mes. Se duplicaban cada quince horas.",
  tipo="numero", valor="4,19 × 10¹⁶ %", etiqueta="de inflación en julio de 1946", nota="Precios × 2 cada 15 horas · récord mundial", color="rojo", contar=False)
e("Hungría llegó a imprimir un billete de cien trillones de pengő: un uno con veinte ceros. Nunca alcanzó a circular.",
  tipo="billete", valor="100.000.000.000.000.000.000", moneda="PENGŐ", color="#B39DDB")
e("Intentaron crear una unidad paralela, el pengő de impuestos, para proteger el valor... pero también se derrumbó.",
  tipo="texto", frase="Plan B: el *ADÓPENGŐ*", sub="También se derrumbó en semanas")
e("La salida llegó el primero de agosto de mil novecientos cuarenta y seis: una moneda nueva, el forinto, con un control estricto del gasto y nuevas reglas para el banco central.",
  tipo="lista", titulo="¿Cómo salió?", modo="solucion", items=[("moneda", "Moneda nueva: el forinto"), ("balanza", "Control estricto del gasto"), ("banco", "Reglas nuevas al banco central")])
e("Un forinto equivalía a cuatrocientos mil cuatrillones de pengős. Y el forinto sigue siendo la moneda de Hungría hasta hoy.",
  tipo="numero", valor="4 × 10²⁹", etiqueta="pengő = 1 forinto", nota="El forinto sigue vigente hoy", color="verde", contar=False)

# ------------------------------------------------------------------ 3. BOLIVIA
e("Capítulo tres. Bolivia, mil novecientos ochenta y cinco.", tipo="capitulo", num=3, pais="BOLIVIA", anio="1985", bandera="bolivia", cap=True)
e("A comienzos de los ochenta, Bolivia tenía una deuda externa enorme, se le cerró el crédito internacional y sus exportaciones, como el estaño, valían cada vez menos.",
  tipo="lista", titulo="¿Cómo llegó ahí?", modo="causa", items=[("deuda", "Deuda externa impagable"), ("candado", "Sin crédito internacional"), ("grafica_baja", "Exportaciones a la baja")])
e("El gobierno siguió gastando sin ingresos suficientes y lo cubrió con emisión. La inflación pasó de trescientos por ciento en mil novecientos ochenta y tres a más de dos mil en mil novecientos ochenta y cuatro.",
  tipo="grafica", titulo="Inflación anual en Bolivia", valores=[329, 2177, 8170], etiquetas=["1983", "1984", "1985"], log=False, color="rojo", final="8.170 %", unidad="%")
e("En mil novecientos ochenta y cinco superó el ocho mil por ciento anual, y solo en febrero los precios subieron ciento ochenta y tres por ciento.",
  tipo="numero", valor="8.170 %", etiqueta="de inflación en 1985", nota="Solo en febrero: +183 %", color="rojo")
e("Un dólar llegó a costar alrededor de un millón de pesos bolivianos. Para hacer mercado, la gente cargaba bolsas de billetes.",
  tipo="billete", valor="1.000.000", moneda="PESOS BOLIVIANOS", color="#80CBC4", nota="≈ 1 dólar")
e("¿Cómo salieron? El veintinueve de agosto de mil novecientos ochenta y cinco, el gobierno firmó el Decreto Supremo veintiún mil sesenta.",
  tipo="texto", frase="La salida: *DECRETO 21060*", sub="29 de agosto de 1985")
e("Fue una terapia de choque: se dejó de financiar el gasto con emisión, se recortó el déficit, se liberaron los precios y se unificó el tipo de cambio.",
  tipo="lista", titulo="¿Cómo salió?", modo="solucion", items=[("candado", "Fin de la emisión para gastar"), ("tijera", "Recorte del déficit"), ("etiqueta", "Precios liberados"), ("dolar", "Un solo tipo de cambio")])
e("La hiperinflación se frenó casi de inmediato. Y en mil novecientos ochenta y siete nació el boliviano, que equivalía a un millón de pesos viejos.",
  tipo="ceros", numero="1.000.000", quitar=6, resultado="= 1 boliviano", moneda="pesos")
e("El costo social fue alto: con el cierre y la reestructuración de las minas estatales, miles de mineros perdieron su empleo.",
  tipo="texto", frase="El precio: *MILES DE EMPLEOS*", sub="La terapia de choque también dolió")

# ------------------------------------------------------------------ 4. ARGENTINA
e("Capítulo cuatro. Argentina, mil novecientos ochenta y nueve.", tipo="capitulo", num=4, pais="ARGENTINA", anio="1989", bandera="argentina", cap=True)
e("Argentina venía de años de déficit fiscal. En mil novecientos ochenta y cinco lanzó el Plan Austral, con moneda nueva... pero sin arreglar el gasto, la inflación volvió.",
  tipo="tiempo", eventos=[("1985", "Plan Austral"), ("1987", "La inflación vuelve"), ("1989", "Hiperinflación")])
e("En mil novecientos ochenta y nueve explotó: la inflación superó el tres mil por ciento y los precios se multiplicaron por cincuenta en un solo año.",
  tipo="numero", valor="3.079 %", etiqueta="de inflación en 1989", nota="Precios × 50 en un año", color="rojo")
e("Hubo saqueos a supermercados, y el presidente Raúl Alfonsín entregó el poder cinco meses antes de lo previsto.",
  tipo="texto", frase="Crisis social y *ENTREGA ANTICIPADA*", sub="Julio de 1989")
e("La solución llegó en mil novecientos noventa y uno: la Ley de Convertibilidad. Un peso nuevo equivalía a diez mil australes... y a un dólar.",
  tipo="ceros", numero="10.000", quitar=4, resultado="= 1 peso = 1 US$", moneda="australes")
e("El banco central solo podía emitir pesos si tenía dólares en reserva para respaldarlos. Se acabó la impresora.",
  tipo="lista", titulo="¿Cómo salió?", modo="solucion", items=[("ancla", "Ancla: 1 peso = 1 dólar"), ("banco", "Cada peso respaldado en reservas"), ("candado", "Prohibido imprimir sin respaldo")])
e("Funcionó: en pocos años, la inflación cayó a un solo dígito.",
  tipo="grafica", titulo="Inflación anual en Argentina (aprox.)", valores=[3079, 2314, 172, 25, 11, 4], etiquetas=["1989", "1990", "1991", "1992", "1993", "1994"],
  log=True, color="verde", final="un dígito", unidad="%")
e("Pero el uno a uno tenía un precio: sin poder ajustar el tipo de cambio y con deuda creciente, terminó en la crisis de dos mil uno. La ley se derogó en enero de dos mil dos.",
  tipo="tiempo", eventos=[("1991", "Convertibilidad"), ("2001", "Crisis"), ("ene 2002", "Fin del 1 a 1")])

# ------------------------------------------------------------------ 5. BRASIL
e("Capítulo cinco. Brasil, mil novecientos noventa y cuatro.", tipo="capitulo", num=5, pais="BRASIL", anio="1994", bandera="brasil", cap=True)
e("Brasil vivió años de inflación altísima y cambió de moneda una y otra vez: cruzado, cruzado nuevo, cruzeiro, cruzeiro real...",
  tipo="tiempo", eventos=[("1986", "Cruzado"), ("1989", "Cruzado novo"), ("1990", "Cruzeiro"), ("1993", "Cruzeiro real")])
e("Los planes anteriores congelaban los precios a la fuerza. Al levantar el congelamiento, la inflación volvía con más fuerza.",
  tipo="texto", frase="Congelar precios *NO FUNCIONÓ*", sub="La inflación siempre volvía")
e("En mil novecientos noventa y tres, la inflación fue de casi dos mil quinientos por ciento.",
  tipo="numero", valor="2.477 %", etiqueta="de inflación en 1993", nota="Índice IPCA", color="rojo")
e("La solución fue muy creativa: el Plan Real. Primero crearon una moneda virtual, la URV, que valía lo mismo que un dólar, y precios y salarios se expresaban también en URV.",
  tipo="texto", frase="La idea genial: la *URV*", sub="Una moneda virtual estable · desde mayo de 1994")
e("La gente se acostumbró a pensar en una unidad estable mientras seguía pagando con la moneda vieja. Así se rompió la memoria inflacionaria.",
  tipo="lista", titulo="¿Cómo salió?", modo="solucion", items=[("ancla", "Precios pensados en URV"), ("moneda", "La URV se vuelve el real"), ("balanza", "Más control del gasto")])
e("El primero de julio de mil novecientos noventa y cuatro, la URV se convirtió en el real. Un real equivalía a dos mil setecientos cincuenta cruzeiros reales.",
  tipo="ceros", numero="2.750", quitar=0, resultado="cruzeiros reales = 1 real", moneda="")
e("Con más disciplina fiscal y un banco central más firme, la inflación bajó a un dígito en pocos años. Y el real sigue siendo la moneda de Brasil.",
  tipo="texto", frase="El real: *30 AÑOS DESPUÉS* sigue vigente", sub="Una de las salidas más exitosas")

# ------------------------------------------------------------------ 6. ZIMBABUE
e("Capítulo seis. Zimbabue, dos mil ocho.", tipo="capitulo", num=6, pais="ZIMBABUE", anio="2008", bandera="zimbabue", cap=True)
e("A partir del año dos mil, una reforma agraria desordenada hizo caer la producción de alimentos. Las exportaciones se desplomaron y el gobierno gastaba mucho más de lo que tenía.",
  tipo="lista", titulo="¿Cómo llegó ahí?", modo="causa", items=[("campo", "Cae la producción agrícola"), ("grafica_baja", "Se desploman las exportaciones"), ("imprenta", "Gasto pagado con emisión")])
e("El economista Steve Hanke estimó que en noviembre de dos mil ocho la inflación mensual llegó a unos setenta y nueve mil seiscientos millones por ciento.",
  tipo="numero", valor="79.600.000.000 %", etiqueta="de inflación en un mes (nov. 2008)", nota="Estimación de Steve Hanke", color="rojo")
e("Llegaron a imprimir billetes de cien billones de dólares zimbabuenses: un uno con catorce ceros.",
  tipo="billete", valor="100.000.000.000.000", moneda="DÓLARES ZIMBABUENSES", color="#A5D6A7")
e("¿La salida? En dos mil nueve, Zimbabue dejó de usar su propia moneda y permitió el dólar estadounidense y otras monedas extranjeras.",
  tipo="lista", titulo="¿Cómo salió?", modo="solucion", items=[("dolar", "Adiós a la moneda propia"), ("moneda", "Dólar y otras divisas")])
e("Los precios se estabilizaron rápido. Pero renunciar a tu moneda significa perder el control de la política monetaria. Años después, Zimbabue intentó volver a una moneda propia... y los problemas regresaron.",
  tipo="tiempo", eventos=[("2008", "Hiperinflación"), ("2009", "Dolarización"), ("2019", "Moneda propia de nuevo"), ("después", "Vuelve la inflación")])

# ------------------------------------------------------------------ 7. VENEZUELA
e("Capítulo siete. Venezuela, de dos mil diecisiete en adelante.", tipo="capitulo", num=7, pais="VENEZUELA", anio="2017", bandera="venezuela", cap=True)
e("Venezuela depende casi por completo del petróleo. Cuando su precio se desplomó en dos mil catorce, los ingresos del Estado se hundieron.",
  tipo="lista", titulo="¿Cómo llegó ahí?", modo="causa", items=[("petroleo", "Dependencia del petróleo"), ("grafica_baja", "Desplome del precio en 2014")])
e("El gobierno siguió financiando el gasto con dinero del banco central, mantuvo controles de precios y de cambio, y la producción de petróleo también cayó.",
  tipo="lista", titulo="¿Cómo llegó ahí?", modo="causa", items=[("petroleo", "Dependencia del petróleo"), ("grafica_baja", "Desplome del precio en 2014"),
                                                               ("imprenta", "Gasto financiado con emisión"), ("etiqueta", "Controles de precios y cambio")], ya=2)
e("El Fondo Monetario Internacional proyectó una inflación de un millón por ciento para dos mil dieciocho.",
  tipo="numero", valor="1.000.000 %", etiqueta="proyección del FMI para 2018", nota="Una cifra con mucha incertidumbre", color="rojo")
e("Para ordenar las cuentas, Venezuela le quitó ceros a su moneda tres veces: tres en dos mil ocho, cinco en dos mil dieciocho y seis en dos mil veintiuno. Catorce ceros en total.",
  tipo="ceros", numero="100.000.000.000.000", quitar=14, resultado="= 1 bolívar digital", moneda="bolívares de 2007", etapas=[3, 5, 6])
e("Pero quitar ceros no cura la inflación: solo cambia la etiqueta. Lo que sí ayudó en parte fue que la economía empezó a usar dólares de forma informal y se redujo la emisión.",
  tipo="lista", titulo="¿Qué ayudó?", modo="solucion", items=[("dolar", "Dolarización informal"), ("candado", "Menos emisión"), ("etiqueta", "Menos controles de precios")])
e("Millones de venezolanos emigraron en esos años. La inflación bajó, pero sigue estando entre las más altas del mundo.",
  tipo="texto", frase="Millones *EMIGRARON*", sub="La inflación bajó, pero sigue siendo de las más altas del mundo")

# ------------------------------------------------------------------ CONCLUSIÓN
e("Siete países, siete historias. Pero si las miras juntas, el patrón se repite.", tipo="paises", conclusion=True)
e("Primero: un golpe enorme. Una guerra, una deuda impagable o el desplome de una exportación.",
  tipo="lista", titulo="El patrón: cómo se llega", modo="causa", items=[("guerra", "1. Un golpe enorme")])
e("Segundo: un gobierno que gasta mucho más de lo que recauda y lo cubre con la impresora del banco central.",
  tipo="lista", titulo="El patrón: cómo se llega", modo="causa", items=[("guerra", "1. Un golpe enorme"), ("imprenta", "2. Déficit pagado con emisión")], ya=1)
e("Tercero: se pierde la confianza. Todos quieren deshacerse del dinero lo más rápido posible, y eso acelera todo.",
  tipo="lista", titulo="El patrón: cómo se llega", modo="causa", items=[("guerra", "1. Un golpe enorme"), ("imprenta", "2. Déficit pagado con emisión"), ("confianza", "3. Se pierde la confianza")], ya=2)
e("Y las salidas también se parecen: dejar de imprimir para financiar al gobierno, equilibrar las cuentas, un ancla creíble y un banco central independiente.",
  tipo="lista", titulo="La receta: cómo se sale", modo="solucion", items=[("candado", "Apagar la impresora"), ("balanza", "Equilibrar las cuentas"), ("ancla", "Un ancla creíble"), ("banco", "Banco central independiente")])
e("Quitar ceros o cambiarle el nombre al billete, por sí solo, nunca ha funcionado. Sin disciplina fiscal, la inflación vuelve.",
  tipo="texto", frase="Quitar ceros *NO ES* la solución", sub="Sin disciplina fiscal, la inflación vuelve")
e("Para dimensionarlo, así se comparan los peores meses de algunos de estos países.",
  tipo="barras", titulo="Peor mes de inflación (escala logarítmica)",
  items=[("Hungría · jul 1946", 4.19e16, "41.900 billones %"), ("Zimbabue · nov 2008", 7.96e10, "79.600 millones %"),
         ("Alemania · oct 1923", 29500, "29.500 %"), ("Bolivia · feb 1985", 183, "183 %")])
e("La lección es simple: el dinero funciona mientras la gente confía en él. Y esa confianza tarda años en construirse... y muy poco en destruirse.",
  tipo="texto", frase="El dinero es *CONFIANZA*", sub="Se construye en años y se pierde en meses")
e("Si te gustó este recorrido, suscríbete y cuéntanos en los comentarios qué país quieres que analicemos a fondo.",
  tipo="suscribete")
