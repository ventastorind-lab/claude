"""Cliente KIE para el video de Byron v2: voz (ElevenLabs vía KIE) y clips de video (imagen → video).

Clave: un "secreto de red" del entorno (Bearer) para api.kie.ai, *.redpandaai.co y *.aiquickdraw.com,
o la variable KIE_API_KEY si se corre en un computador propio.

Uso:
  python3 kie.py saldo
  python3 kie.py muestras                 # la primera línea con varias voces → voz_muestras/
  python3 kie.py voces --voz <voice_id>   # una pista por escena → voz/NN.mp3 (salta las que ya existen)
  python3 kie.py imagenes                 # ilustraciones de las escenas con imagen=... → imagenes/<nombre>.png
  python3 kie.py clips                    # clips de las escenas con kie=... → clips/NN.mp4
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
API = "https://api.kie.ai/api/v1"
SUBIDA = "https://kieai.redpandaai.co/api/file-stream-upload"
MODELO_TTS = "elevenlabs/text-to-speech-multilingual-v2"
MODELO_VIDEO = "kling/v2-1-standard"
MODELO_IMAGEN = "nano-banana-pro"
REFERENCIA = os.path.join(AQUI, "..", "..", "personajes", "nuevos", "01_byron.png")
ESTILO = (" Keep this exact pink cartoon axolotl character design (white headband with red star, bandage on cheek, pink gills,"
          " stick arms and legs). Flat 2D cartoon style, thick black outlines, bright friendly colors, wide 16:9 composition,"
          " absolutely no text, no letters, no logos, no brand names.")
# voces prediseñadas de ElevenLabs (IDs públicos); todas hablan español con el modelo multilingüe
VOCES = {
    "liam": "TX3LPaxmHKxFdv7VOQHJ",      # joven, enérgico
    "will": "bIHbv24MWmeRgasZH58o",      # amigable, relajado
    "charlie": "IKne3meq5aSn9XLyUdCD",   # carismático, expresivo
    "antoni": "ErXwobaYiN019PkySvjV",    # cálido, narrador
}


def _peticion(metodo, url, cuerpo=None, cabeceras=None, datos=None):
    # Con un "secreto de red" en el entorno, el proxy agrega la clave por su cuenta;
    # KIE_API_KEY solo se usa si existe (p. ej. al correrlo en tu propio computador).
    k = os.environ.get("KIE_API_KEY")
    h = {"Authorization": f"Bearer {k}"} if k else {}
    if cuerpo is not None:
        datos = json.dumps(cuerpo).encode()
        h["Content-Type"] = "application/json"
    h.update(cabeceras or {})
    req = urllib.request.Request(url, data=datos, headers=h, method=metodo)
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"{metodo} {url} → HTTP {e.code}: {e.read().decode()[:500]}")


def saldo():
    r = _peticion("GET", f"{API}/chat/credit")
    return r.get("data")


def crear_tarea(modelo, entrada):
    r = _peticion("POST", f"{API}/jobs/createTask", {"model": modelo, "input": entrada})
    if r.get("code") != 200:
        raise RuntimeError(f"createTask falló: {r}")
    return r["data"]["taskId"]


def esperar(tarea, limite=900):
    t0 = time.time()
    while time.time() - t0 < limite:
        r = _peticion("GET", f"{API}/jobs/recordInfo?taskId={tarea}")
        d = r.get("data") or {}
        estado = d.get("state")
        if estado == "success":
            res = d.get("resultJson")
            res = json.loads(res) if isinstance(res, str) else (res or {})
            return res.get("resultUrls") or []
        if estado == "fail":
            raise RuntimeError(f"tarea {tarea} falló: {d.get('failMsg') or d}")
        time.sleep(4)
    raise TimeoutError(f"tarea {tarea} no terminó en {limite} s")


def descargar(url, destino):
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    with urllib.request.urlopen(url, timeout=300) as r, open(destino, "wb") as fh:
        fh.write(r.read())
    return destino


def subir(ruta):
    """Sube un archivo local y devuelve una URL pública temporal (para imagen → video)."""
    limite = "----byron" + str(int(time.time()))
    nombre = os.path.basename(ruta)
    with open(ruta, "rb") as fh:
        contenido = fh.read()
    partes = []
    for campo, valor in (("uploadPath", "byron"), ("fileName", nombre)):
        partes.append(f"--{limite}\r\nContent-Disposition: form-data; name=\"{campo}\"\r\n\r\n{valor}\r\n".encode())
    partes.append(f"--{limite}\r\nContent-Disposition: form-data; name=\"file\"; filename=\"{nombre}\"\r\nContent-Type: image/png\r\n\r\n".encode() + contenido + b"\r\n")
    partes.append(f"--{limite}--\r\n".encode())
    r = _peticion("POST", SUBIDA, datos=b"".join(partes), cabeceras={"Content-Type": f"multipart/form-data; boundary={limite}"})
    d = r.get("data") or {}
    url = d.get("downloadUrl") or d.get("fileUrl") or d.get("url")
    if not url:
        raise RuntimeError(f"subida sin URL: {r}")
    return url


def tts(texto, voz, destino, estabilidad=0.35, similitud=0.8, estilo=0.45, velocidad=1.05):
    tarea = crear_tarea(MODELO_TTS, {"text": texto, "voice": voz, "stability": estabilidad, "similarity_boost": similitud,
                                     "style": estilo, "speed": velocidad})
    urls = esperar(tarea)
    return descargar(urls[0], destino)


def imagen(prompt, destino, ref_url):
    tarea = crear_tarea(MODELO_IMAGEN, {"prompt": prompt + ESTILO, "image_input": [ref_url], "aspect_ratio": "16:9",
                                        "resolution": "2K", "output_format": "png"})
    urls = esperar(tarea, 900)
    return descargar(urls[0], destino)


def clip(imagen, prompt, destino):
    url = subir(imagen)
    tarea = crear_tarea(MODELO_VIDEO, {"prompt": prompt, "image_url": url, "duration": "5",
                                       "negative_prompt": "realistic, 3d render, blurry, distorted face, extra limbs, text artifacts", "cfg_scale": 0.5})
    urls = esperar(tarea, 1800)
    return descargar(urls[0], destino)


def _guion():
    sys.path.insert(0, AQUI)
    import guion
    return guion.E


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    cmd = sys.argv[1]
    if cmd == "saldo":
        print("créditos:", saldo())
    elif cmd == "muestras":
        texto = _guion()[0][0]
        for nombre, vid in VOCES.items():
            print(nombre, tts(texto, vid, os.path.join(AQUI, "voz_muestras", f"{nombre}.mp3")), flush=True)
    elif cmd == "voces":
        voz = VOCES.get(sys.argv[3], sys.argv[3]) if len(sys.argv) > 3 and sys.argv[2] == "--voz" else VOCES["liam"]
        for i, (texto, _) in enumerate(_guion()):
            destino = os.path.join(AQUI, "voz", f"{i:02d}.mp3")
            if os.path.exists(destino):
                continue
            print(i, tts(texto, voz, destino), flush=True)
    elif cmd == "imagenes":
        ref = None
        for i, (texto, spec) in enumerate(_guion()):
            if "imagen" not in spec:
                continue
            destino = os.path.join(AQUI, "imagenes", spec["imagen"]["nombre"] + ".png")
            if os.path.exists(destino):
                continue
            ref = ref or subir(REFERENCIA)
            print(i, imagen(spec["imagen"]["prompt"], destino, ref), flush=True)
    elif cmd == "clips":
        sys.path.insert(0, AQUI)
        import render
        from concurrent.futures import ThreadPoolExecutor
        pendientes = []
        for i, (texto, spec) in enumerate(_guion()):
            if "kie" not in spec:
                continue
            destino = os.path.join(AQUI, "clips", f"{i:02d}.mp4")
            if os.path.exists(destino):
                continue
            img = os.path.join(AQUI, "clips", f"inicio_{i:02d}.png")
            if "imagen" in spec:
                from PIL import Image
                os.makedirs(os.path.dirname(img), exist_ok=True)
                Image.open(os.path.join(AQUI, "imagenes", spec["imagen"]["nombre"] + ".png")).convert("RGB").resize((1920, 1080)).save(img)
            else:
                render.cuadro_inicial(i, img)
            pendientes.append((i, img, spec["kie"]["prompt"], destino))

        def uno(p):
            try:
                print(p[0], clip(*p[1:]), flush=True)
            except Exception as e:  # noqa: BLE001
                print(p[0], "ERROR", e, flush=True)
        with ThreadPoolExecutor(4) as ex:
            list(ex.map(uno, pendientes))
    else:
        sys.exit(__doc__)
    try:
        print("créditos restantes:", saldo())
    except Exception as e:  # noqa: BLE001
        print("no se pudo consultar el saldo:", e)


if __name__ == "__main__":
    main()
