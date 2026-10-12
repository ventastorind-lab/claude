"""Pedro, el niño sagaz — cuento animado con ilustraciones y clips de KIE.

Inspirado en los cuentos populares de Pedro Urdemales (folclor latinoamericano), adaptado para niños:
Pedro usa la astucia para ayudar a su pueblo, nunca para hacer daño.

Cada escena: (narración, spec)
  img="nombre"           → imagenes/<nombre>.png (Nano Banana Pro, con personajes de referencia)
  prompt="..."           → descripción de la ilustración
  refs=("pedro", ...)    → personajes de referencia (personajes/<nombre>.png)
  clip="..."             → movimiento para Kling (imagen → video de 5 s)
  capitulo="..."         → rótulo de capítulo sobre la imagen
  titulo=True            → título del cuento
"""
E = []


def esc(narr, img, prompt, refs=(), **kw):
    E.append((narr, dict(img=img, prompt=prompt, refs=tuple(refs), **kw)))


# Personajes (hojas de referencia que se generan primero)
PERSONAJES = {
    "pedro": "A clever 10-year-old Latin American boy named Pedro: tanned skin, big bright mischievous brown eyes, messy black hair, "
             "a worn straw hat, a small red-and-yellow striped poncho over a white shirt, rolled-up brown pants, simple sandals. "
             "Full body, standing, friendly confident smile, plain light background, character reference sheet style.",
    "mama": "Pedro's mother, Doña Rosa: a kind hard-working Latin American woman in her thirties, long black braid, "
            "simple blue dress with a white apron, warm smile. Full body, plain light background, character reference sheet style.",
    "ambrosio": "Don Ambrosio, a greedy rich landowner: round belly, big curly black mustache, small suspicious eyes, black suit "
                "with a golden vest and a shiny gold pocket watch chain, a tall black hat, holding a cane. Comic, not scary. "
                "Full body, plain light background, character reference sheet style.",
    "canelo": "Canelo, Pedro's small brown donkey with a cream muzzle, big ears, a funny grin and a tiny red scarf. "
              "Full body, plain light background, character reference sheet style.",
}

# ------------------------------------------------------------------ inicio
esc("Había una vez, en un pueblito escondido entre montañas verdes, un niño llamado Pedro. No era el más fuerte, ni el más rico... pero sí el más sagaz.",
    "pueblo", "A colorful little Latin American mountain village at sunrise: adobe houses with red tile roofs, a white chapel, a plaza with a fountain, "
    "green mountains and mist, Pedro walking happily down a dirt road with his donkey Canelo.", ("pedro", "canelo"), titulo=True,
    clip="Slow aerial camera glide over the village at sunrise, birds fly across the sky, Pedro and the donkey walk down the road, gentle mist moves.")
esc("Pedro vivía en una casita de barro con su mamá, doña Rosa, y con Canelo, un burrito terco que solo obedecía si le cantaban.",
    "casa", "A humble adobe house with flowers in clay pots, Doña Rosa hanging laundry, Pedro singing to the stubborn donkey Canelo who refuses to move.",
    ("pedro", "mama", "canelo"))
esc("Eran pobres. Doña Rosa lavaba ropa ajena desde que salía el sol, y Pedro ayudaba en lo que podía: cargaba agua, vendía huevos y arreglaba cercas.",
    "trabajo", "Doña Rosa washing clothes at a stone washboard by a river while Pedro carries two buckets of water on a wooden yoke, morning light.",
    ("pedro", "mama"))
esc("Pero Pedro tenía un tesoro que nadie le podía quitar: su cabeza. Cuando los demás veían un problema, él veía una idea.",
    "idea", "Close-up of Pedro tapping his temple with one finger and smiling cleverly, a glowing light bulb of golden sparkles above his head, warm background.",
    ("pedro",), clip="Pedro taps his temple and grins, golden sparkles burst above his head like a light bulb turning on, his eyes shine.")

# ------------------------------------------------------------------ el problema
esc("En el pueblo también vivía don Ambrosio, el hombre más rico de toda la región. Tenía tierras, vacas, caballos... y un corazón más duro que una piedra.",
    "ambrosio", "Don Ambrosio standing proudly in front of his huge hacienda mansion with fields, cows and horses behind him, counting gold coins in his hand.",
    ("ambrosio",), clip="Don Ambrosio counts gold coins greedily, coins clink and shine, he twirls his mustache with a sly grin.")
esc("Don Ambrosio contrataba a la gente del pueblo para trabajar en sus campos, y al final de la semana siempre encontraba una excusa para no pagarles completo.",
    "campos", "Tired villagers harvesting corn in a big field under the hot sun while Don Ambrosio watches from the shade with a cane, looking at his gold watch.",
    ("ambrosio",))
esc("Un día, doña Rosa le lavó toda la ropa de la hacienda: sábanas, manteles y treinta camisas. Pero don Ambrosio le dio apenas una moneda.",
    "pago", "Don Ambrosio dropping a single tiny coin into Doña Rosa's open hand next to an enormous pile of clean folded laundry, she looks sad, Pedro watches angrily.",
    ("ambrosio", "mama", "pedro"))
esc("Eso es todo lo que vale tu trabajo, dijo, y cerró la puerta. Esa noche, Pedro vio a su mamá contar la moneda una y otra vez, preocupada.",
    "noche", "Night inside the humble house lit by a candle: Doña Rosa sitting at a wooden table looking worried at one coin, Pedro watching from the doorway, moonlight.",
    ("mama", "pedro"))
esc("Pedro no dijo nada. Se acostó, miró las estrellas por la ventana... y sonrió. Ya tenía un plan.",
    "plan", "Pedro lying in a simple bed looking out a window at a starry night sky, a sly smile on his face, the stars form the shape of a coin.",
    ("pedro",), clip="Pedro lying in bed looks at the stars, his smile grows slowly into a clever grin, stars twinkle in the window.")

# ------------------------------------------------------------------ cuento 1: el árbol de las monedas
esc("Primer cuento: el árbol que daba monedas.",
    "arbol_titulo", "A magical-looking lonely tree on a hill at dawn with shiny objects glinting in its branches, golden light, storybook mood.",
    (), capitulo="1 · El árbol que daba monedas")
esc("A la mañana siguiente, Pedro juntó las pocas monedas que tenían en casa y las pegó con miel a las ramas de un árbol que había junto al camino de la hacienda.",
    "pegando", "Pedro on a wooden ladder sticking small coins to the branches of a tree with a little jar of honey, bees around, Canelo watching curiously.",
    ("pedro", "canelo"), clip="Pedro sticks shiny coins on the branches with honey, the coins sparkle in the sunlight, a bee buzzes around, the donkey tilts its head.")
esc("Luego se sentó debajo, con su sombrero en la mano, y esperó. Al rato pasó don Ambrosio en su caballo.",
    "esperando", "Pedro sitting under the tree with coins shining in its branches, holding his straw hat, while Don Ambrosio rides up on a black horse in the distance.",
    ("pedro", "ambrosio"))
esc("Pedro sacudió una rama: ¡clin, clin, clin! Las monedas cayeron dentro del sombrero. Don Ambrosio casi se cae del caballo.",
    "sacude", "Pedro shaking a tree branch and coins raining into his straw hat, Don Ambrosio on his horse with eyes popping out in shock, mouth wide open.",
    ("pedro", "ambrosio"), clip="Pedro shakes the branch and shiny coins rain down into his hat, Don Ambrosio's eyes pop wide open in amazement on his horse.")
esc("¡Muchacho! ¿Qué árbol es ese? Ah, don Ambrosio, es un árbol de monedas. Lo heredé de mi abuelo. Cada mañana da un poquito.",
    "dialogo1", "Don Ambrosio leaning down from his horse greedily talking to Pedro, who innocently holds a hat full of coins next to the tree.",
    ("pedro", "ambrosio"))
esc("Los ojos de don Ambrosio brillaron como dos monedas. Te lo compro, dijo. Pedro se rascó la cabeza. Uy, no sé... es lo único que tenemos.",
    "ojos", "Close-up of Don Ambrosio with gold coins reflected in his greedy eyes, rubbing his hands together, Pedro behind pretending to hesitate.",
    ("ambrosio", "pedro"))
esc("¡Te doy una bolsa de oro! Bueno... está bien, dijo Pedro. Pero eso sí: el árbol solo da monedas si lo riega alguien honrado.",
    "trato", "Don Ambrosio handing a big heavy bag of gold to Pedro next to the coin tree, shaking hands, Pedro with a polite innocent smile.",
    ("ambrosio", "pedro"))
esc("Al día siguiente, don Ambrosio regó el árbol una vez. Y otra. Y otra. Lo regó con baldes, con mangueras, con agua de la fuente... y el árbol no dio ni un centavo.",
    "regando", "Don Ambrosio sweaty and frustrated watering the tree with many buckets, puddles everywhere, the tree has no coins, only leaves, comic scene.",
    ("ambrosio",), clip="Don Ambrosio splashes bucket after bucket of water on the tree, water flies everywhere, he stomps his feet angrily, no coins fall.")
esc("Mientras tanto, Pedro y su mamá fueron casa por casa, devolviéndole a cada trabajador lo que don Ambrosio le debía.",
    "repartir", "Pedro and Doña Rosa happily giving gold coins to poor villagers at their doors, families smiling and hugging, warm afternoon light.",
    ("pedro", "mama"), clip="Pedro hands gold coins to a smiling family, children jump with joy, Doña Rosa smiles warmly, warm light.")

# ------------------------------------------------------------------ cuento 2: la olla que hervía sola
esc("Segundo cuento: la olla que hervía sola.",
    "olla_titulo", "A black clay cooking pot steaming magically on a dirt road with no fire under it, mysterious and funny, storybook mood.",
    (), capitulo="2 · La olla que hervía sola")
esc("Don Ambrosio estaba furioso. Recorrió el pueblo buscando a Pedro, y lo encontró sentado al lado del camino, cocinando un sancocho.",
    "furioso", "Don Ambrosio stomping angrily down a village street with steam coming out of his ears, looking for Pedro, villagers peeking from windows.",
    ("ambrosio",))
esc("Pero Pedro era más rápido que el enojo de don Ambrosio. Cuando lo vio venir, quitó la olla del fuego, la puso en el suelo y tapó las brasas con tierra.",
    "truco_olla", "Pedro quickly moving a big black clay pot of soup off a campfire onto the ground and covering the embers with dirt with his foot, looking over his shoulder.",
    ("pedro",))
esc("Luego empezó a darle golpecitos a la olla con un palito, cantando: hierve, ollita, hierve. Y la sopa seguía burbujeando, ¡sin fuego!",
    "golpecitos", "Pedro tapping the black pot with a little stick and singing, the soup bubbling and steaming with no fire under it, Don Ambrosio arriving amazed.",
    ("pedro", "ambrosio"), clip="Pedro taps the clay pot with a stick, the soup bubbles and steam rises, Don Ambrosio stops in his tracks with his jaw dropping.")
esc("Don Ambrosio se olvidó del árbol en un segundo. ¡Una olla que cocina sin leña! Imagínate todo lo que podría ahorrar.",
    "imagina", "Don Ambrosio daydreaming, a thought bubble above his head showing piles of saved money and a kitchen with no firewood, greedy smile.",
    ("ambrosio",))
esc("Esa olla vale una fortuna, dijo Pedro. Pero... si de verdad la quiere, se la cambio por pagarle completo a todos sus trabajadores este mes.",
    "trato2", "Pedro standing with arms crossed next to the steaming pot, negotiating confidently with Don Ambrosio who is pulling out a long payment list.",
    ("pedro", "ambrosio"))
esc("Don Ambrosio aceptó y se llevó la olla corriendo. La puso en la mesa de su comedor, le dio golpecitos con una cuchara de plata y cantó: hierve, ollita, hierve.",
    "comedor", "Don Ambrosio in his elegant dining room tapping a black clay pot on a fancy table with a silver spoon, singing, the pot is cold, servants giggling behind.",
    ("ambrosio",), clip="Don Ambrosio taps the cold pot with a silver spoon and sings, nothing happens, he frowns, servants hide their giggles behind their hands.")
esc("Cantó toda la tarde. Cantó toda la noche. Y la olla, fría como una piedra. Pero eso sí: ese mes, por primera vez, todos cobraron su sueldo completo.",
    "fria", "Night scene: exhausted Don Ambrosio asleep on the dining table next to the cold pot, while outside villagers celebrate under lanterns with their pay.",
    ("ambrosio",))

# ------------------------------------------------------------------ cuento 3: la sopa de piedra
esc("Tercer cuento: la sopa de piedra.",
    "piedra_titulo", "A smooth round grey stone sitting in a big copper pot of clear water in a village plaza, storybook mood, soft light.",
    (), capitulo="3 · La sopa de piedra")
esc("Ese invierno fue muy duro. Llovió tanto que se perdieron las cosechas, y cada familia escondía lo poquito que tenía, sin compartir con nadie.",
    "invierno", "A rainy grey village in winter, families closing their doors and hiding small bags of food, puddles in the plaza, sad atmosphere.",
    (), clip="Heavy rain falls on the grey village, a door slowly closes, puddles ripple, a cold wind blows leaves across the plaza.")
esc("Pedro tuvo una idea. Puso una olla grandota en la plaza, la llenó de agua, prendió el fuego... y echó adentro una piedra lisa del río.",
    "olla_plaza", "Pedro in the rainy village plaza putting a smooth river stone into a huge copper pot of water over a fire, Canelo next to him with an umbrella on his head.",
    ("pedro", "canelo"))
esc("¿Qué haces, Pedro?, preguntó una vecina. Una sopa de piedra, respondió él. Es deliciosa... aunque le faltaría un poquito de papa.",
    "vecina", "A curious old neighbor woman with a shawl peeking at the big pot, Pedro stirring with a wooden spoon and smiling, steam rising.",
    ("pedro",))
esc("La vecina trajo dos papas. Otro vecino trajo zanahorias. La señora de la tienda, cebolla y cilantro. Los niños trajeron mazorcas.",
    "ingredientes", "Villagers of all ages arriving with potatoes, carrots, onions, cilantro and corn cobs, dropping them into the big pot, the sun coming out through clouds.",
    ("pedro",), clip="Villagers drop potatoes, carrots, corn and onions into the big steaming pot one after another, the clouds open and sunlight shines.")
esc("Hasta don Ambrosio, oliendo desde su ventana, mandó un pedazo de carne. Muy a su manera, claro, sin decir buenos días.",
    "ambrosio_carne", "Don Ambrosio at his mansion window sniffing the delicious smell, grumpily lowering a piece of meat in a basket with a rope toward the plaza.",
    ("ambrosio",))
esc("Al final, la sopa de piedra alcanzó para todo el pueblo. Comieron juntos bajo el sol, y por primera vez en mucho tiempo, se rieron.",
    "banquete", "The whole village eating soup together at long tables in the sunny plaza, laughing, children playing, Pedro and Doña Rosa serving bowls.",
    ("pedro", "mama", "canelo"), clip="Villagers eat soup and laugh together at long tables, children run around, Pedro serves steaming bowls, festive sunlight.")
esc("¿Y la piedra?, preguntaron los niños. Pedro la sacó, la secó y se la guardó en el bolsillo. La piedra no hace la sopa, dijo. La hacemos entre todos.",
    "la_piedra", "Pedro holding up the smooth wet stone with a wise smile, surrounded by curious children listening closely, warm golden light.",
    ("pedro",))

# ------------------------------------------------------------------ desenlace
esc("Pero don Ambrosio no había olvidado nada. Una mañana llegó a la casa de Pedro con dos guardias. ¡Me engañaste con el árbol y con la olla!",
    "guardias", "Don Ambrosio angrily pointing at Pedro at the door of the humble house, two clumsy comic guards behind him, Doña Rosa worried.",
    ("ambrosio", "pedro", "mama"), clip="Don Ambrosio points angrily and shakes his cane, the two clumsy guards bump into each other, Pedro stays calm.")
esc("Pedro lo miró tranquilo. Don Ambrosio, el árbol sí daba monedas... las que usted le debía a la gente. Y la olla sí hervía... con el calor del trabajo que usted no pagaba.",
    "respuesta", "Pedro calmly facing Don Ambrosio with honest eyes, the whole village gathering behind Pedro in support, morning light.",
    ("pedro", "ambrosio"))
esc("Todo el pueblo se había reunido detrás de Pedro. Y don Ambrosio, por primera vez en su vida, no supo qué decir.",
    "pueblo_unido", "Wide shot of the whole village standing together behind Pedro and Doña Rosa, Don Ambrosio alone and speechless in front, his hat slipping.",
    ("pedro", "ambrosio", "mama"))
esc("Esa noche no pudo dormir. Pensó en la sopa, en las risas de la plaza... y se dio cuenta de que con todo su oro, nunca había comido acompañado.",
    "reflexion", "Don Ambrosio alone at night in his huge empty dining room with piles of gold, looking out the window at the warm lights of the village, a tear in his eye.",
    ("ambrosio",), clip="Don Ambrosio looks out the window at the village lights, his mustache trembles, a single tear rolls down his cheek, candle flickers.")
esc("Al día siguiente, don Ambrosio subió los sueldos, arregló el techo de la escuela y, aunque le costó, aprendió a decir gracias.",
    "cambio", "Don Ambrosio, now smiling awkwardly, handing fair pay envelopes to workers and helping fix the roof of a small village school, sunny day.",
    ("ambrosio",))
esc("Y cuentan que cada domingo hay sopa en la plaza. Don Ambrosio trae la carne, doña Rosa la sazón, y Canelo... Canelo se come las zanahorias antes de que lleguen a la olla.",
    "domingo", "A joyful Sunday feast in the plaza: Don Ambrosio carrying meat, Doña Rosa seasoning the pot, Canelo the donkey sneakily eating carrots from a basket.",
    ("ambrosio", "mama", "canelo"), clip="Canelo the donkey sneakily munches carrots from a basket and grins, Doña Rosa laughs, Don Ambrosio shakes his head smiling.")

# ------------------------------------------------------------------ moraleja y cierre
esc("Pedro nunca fue el más fuerte, ni el más rico. Pero aprendió que la astucia es como un cuchillo: puede cortar pan para compartir, o hacer daño. Él siempre eligió el pan.",
    "moraleja", "Pedro sitting on a hill at sunset breaking a loaf of bread to share with Canelo, the village below glowing warmly, peaceful.",
    ("pedro", "canelo"), clip="Pedro breaks a loaf of bread and shares it with the donkey at sunset, the wind moves his poncho, the sun sets over the village.")
esc("Porque ser sagaz no es ser tramposo: es usar la cabeza para que a todos nos vaya mejor.",
    "sagaz", "Close-up of Pedro smiling wisely under his straw hat with a golden sunset behind him, sparkles in the air.",
    ("pedro",))
esc("Y colorín colorado, este cuento se ha acabado. Si te gustó, cuéntaselo a alguien antes de dormir... y suscríbete para más cuentos de Pedro.",
    "fin", "Pedro waving goodbye to the viewer with Canelo and Doña Rosa in front of their little house at night under a starry sky, a big open storybook in the foreground.",
    ("pedro", "canelo", "mama"), fin=True,
    clip="Pedro and his mother wave goodbye, the donkey nods, stars twinkle, the storybook pages flutter gently.")
