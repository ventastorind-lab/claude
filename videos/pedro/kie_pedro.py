"""Genera con KIE todo lo visual y la música de "Pedro, el niño sagaz".

  python3 kie_pedro.py personajes   # hojas de referencia → personajes/<nombre>.png
  python3 kie_pedro.py imagenes     # una ilustración por escena → imagenes/<img>.png
  python3 kie_pedro.py clips        # clips Kling de las escenas con clip=... → clips/NN.mp4
  python3 kie_pedro.py musica       # música instrumental (Suno vía KIE) → musica.mp3
Todo se salta si el archivo ya existe.
"""
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "cocacola_v2"))
sys.path.insert(0, AQUI)
import kie  # noqa: E402  (cliente KIE compartido)
import guion as GU  # noqa: E402

ESTILO = (" Style: warm colorful 2D storybook cartoon illustration for children, soft painterly textures, clean black outlines,"
          " Latin American village setting, cinematic wide 16:9 composition, consistent character designs."
          " Absolutely no text, no letters, no words, no signs with writing.")


def gen_imagen(prompt, destino, refs):
    tarea = kie.crear_tarea("nano-banana-pro", {"prompt": prompt + ESTILO, "image_input": list(refs), "aspect_ratio": "16:9",
                                                "resolution": "2K", "output_format": "png"})
    kie.descargar(kie.esperar(tarea, 900)[0], destino + ".png")
    from PIL import Image
    Image.open(destino + ".png").convert("RGB").save(destino, quality=92)
    os.remove(destino + ".png")
    return destino


def en_paralelo(trabajos, n=4):
    def uno(t):
        nombre, fn = t
        for intento in range(3):
            try:
                print(nombre, fn(), flush=True)
                return
            except Exception as e:  # noqa: BLE001
                print(nombre, "ERROR", intento + 1, e, flush=True)
                time.sleep(10)
    with ThreadPoolExecutor(n) as ex:
        list(ex.map(uno, trabajos))


def personajes():
    trabajos = []
    for nombre, desc in GU.PERSONAJES.items():
        destino = os.path.join(AQUI, "personajes", nombre + ".jpg")
        if not os.path.exists(destino):
            trabajos.append((nombre, lambda d=desc, x=destino: gen_imagen(d, x, [])))
    en_paralelo(trabajos)


def imagenes():
    urls = {}
    for nombre in GU.PERSONAJES:
        urls[nombre] = kie.subir(os.path.join(AQUI, "personajes", nombre + ".jpg"))
    trabajos = []
    for i, (_, e) in enumerate(GU.E):
        destino = os.path.join(AQUI, "imagenes", e["img"] + ".jpg")
        if os.path.exists(destino):
            continue
        nombres = {"pedro": "Pedro (the boy)", "mama": "Doña Rosa (the mother)", "ambrosio": "Don Ambrosio (the rich man)",
                   "canelo": "Canelo (the donkey)"}
        guia = ""
        if e["refs"]:
            guia = " Reference images, in order: " + ", ".join(nombres[r] for r in e["refs"]) + ". Keep their exact designs."
        trabajos.append((f"{i:02d} {e['img']}", lambda p=e["prompt"] + guia, x=destino, r=[urls[n] for n in e["refs"]]: gen_imagen(p, x, r)))
    en_paralelo(trabajos)


def clips():
    from PIL import Image
    trabajos = []
    for i, (_, e) in enumerate(GU.E):
        if "clip" not in e:
            continue
        destino = os.path.join(AQUI, "clips", f"{i:02d}.mp4")
        if os.path.exists(destino):
            continue
        inicio = os.path.join(AQUI, "clips", f"inicio_{i:02d}.png")
        os.makedirs(os.path.dirname(inicio), exist_ok=True)
        Image.open(os.path.join(AQUI, "imagenes", e["img"] + ".jpg")).convert("RGB").resize((1920, 1080)).save(inicio)
        prompt = e["clip"] + " Keep the exact same 2D storybook cartoon style and character designs, smooth gentle motion, no text."
        trabajos.append((f"{i:02d}", lambda a=inicio, p=prompt, d=destino: kie.clip(a, p, d)))
    en_paralelo(trabajos)


def musica():
    destino = os.path.join(AQUI, "musica.mp3")
    if os.path.exists(destino):
        return
    r = kie._peticion("POST", f"{kie.API}/generate", {
        "prompt": "Gentle whimsical Latin American folk lullaby for a children's storybook: soft nylon guitar, charango, light marimba, "
                  "warm flute, playful and tender, slow tempo, no drums, instrumental",
        "customMode": False, "instrumental": True, "model": "V4_5", "callBackUrl": "https://example.com/callback"})
    if r.get("code") != 200:
        raise RuntimeError(f"Suno falló: {r}")
    tarea = r["data"]["taskId"]
    for _ in range(200):
        d = kie._peticion("GET", f"{kie.API}/generate/record-info?taskId={tarea}").get("data") or {}
        estado = d.get("status")
        canciones = ((d.get("response") or {}).get("sunoData")) or []
        if estado == "SUCCESS" and canciones:
            for k, c in enumerate(canciones):
                kie.descargar(c["audioUrl"], destino if k == 0 else destino.replace(".mp3", f"_{k}.mp3"))
            print("música", [c.get("duration") for c in canciones])
            return
        if estado and "FAIL" in estado or estado == "SENSITIVE_WORD_ERROR":
            raise RuntimeError(f"Suno falló: {d}")
        time.sleep(8)
    raise TimeoutError("Suno no terminó")


if __name__ == "__main__":
    {"personajes": personajes, "imagenes": imagenes, "clips": clips, "musica": musica}[sys.argv[1]]()
    print("créditos restantes:", kie.saldo())
