# Pedro, el niño sagaz

Cuento animado de 6:09 inspirado en los cuentos populares de Pedro Urdemales, adaptado para niños.
Tres cuentos: el árbol que daba monedas, la olla que hervía sola y la sopa de piedra.

- `pedro_nino_sagaz.mp4` (1080p) y `pedro_nino_sagaz_liviano.mp4` (720p)
- `guion.py`: 43 escenas con narración, prompts de ilustración y de movimiento
- `personajes/`: hojas de referencia (Pedro, doña Rosa, don Ambrosio, Canelo)
- `imagenes/`: 43 ilustraciones (KIE · Nano Banana Pro 2K, con los personajes como referencia)
- `clips/`: 18 clips de 5 s (KIE · Kling, imagen → video)
- `musica.mp3`, `musica_1.mp3`: música instrumental (KIE · Suno)

```bash
python3 kie_pedro.py personajes && python3 kie_pedro.py imagenes && python3 kie_pedro.py clips && python3 kie_pedro.py musica
KOKORO_DIR=<carpeta con kokoro-multi-lang-v1_0> python3 render.py pedro_nino_sagaz.mp4 24
```
La narración usa la voz local (Kokoro) porque ElevenLabs en KIE respondía error 500. Si existen `voz/NN.mp3`,
`render.py` las usa en su lugar.
