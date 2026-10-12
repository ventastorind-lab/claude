"""Render de "Pedro, el niño sagaz": ilustraciones y clips de KIE, narración, música de Suno y subtítulos.

  python3 render.py <salida.mp4> [fps]     # voz: voz/NN.mp3 si existen (ElevenLabs vía KIE), si no, voz local Kokoro
  python3 render.py --muestra <carpeta>    # un cuadro por escena
"""
import base64
import io
import os
import subprocess
import sys
from multiprocessing import Pool

import numpy as np
import soundfile as sf
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import guion as GU  # noqa: E402

W, H, SR, FPS_CLIP = 1920, 1080, 44100, 24
FUNDIDO = 0.5
TTS_KOKORO = os.environ.get("KOKORO_DIR", "")
VOZ_SID, VOZ_VELOCIDAD = 53, 1.0  # em_santa: voz grave de cuentacuentos


def c01(x):
    return max(0.0, min(1.0, x))


def suave(x):
    x = c01(x)
    return x * x * (3 - 2 * x)


# ---------------------------------------------------------------- imágenes
_CACHE = {}


def uri_jpg(ruta, ancho=W, alto=H):
    clave = (ruta, ancho)
    if clave not in _CACHE:
        buf = io.BytesIO()
        Image.open(ruta).convert("RGB").resize((ancho, alto), Image.LANCZOS).save(buf, "JPEG", quality=90)
        _CACHE[clave] = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    return _CACHE[clave]


def cuadros_clip(i):
    carpeta = os.path.join(AQUI, "clips", f"{i:02d}_cuadros")
    return sorted(os.listdir(carpeta)) if os.path.isdir(carpeta) else []


def base(i, t, dur):
    """Imagen de fondo de la escena i en el instante t: clip de Kling y luego zoom lento (Ken Burns)."""
    e = GU.E[i][1]
    cl = cuadros_clip(i)
    dc = len(cl) / FPS_CLIP
    carpeta = os.path.join(AQUI, "clips", f"{i:02d}_cuadros")
    if cl and t < dc:
        ruta = os.path.join(carpeta, cl[min(int(t * FPS_CLIP), len(cl) - 1)])
        with open(ruta, "rb") as fh:
            return f'<image href="data:image/jpeg;base64,{base64.b64encode(fh.read()).decode()}" width="{W}" height="{H}"/>'
    if cl:
        href, t0 = uri_jpg(os.path.join(carpeta, cl[-1])), dc
    else:
        href, t0 = uri_jpg(os.path.join(AQUI, "imagenes", e["img"] + ".jpg")), 0.0
    p = suave((t - t0) / max(dur - t0, 1.0))
    modo = i % 4
    if modo == 0:      # acercar al centro
        k, dx, dy = 1.0 + 0.08 * p, 0, 0
    elif modo == 1:    # alejar
        k, dx, dy = 1.09 - 0.08 * p, 0, 0
    elif modo == 2:    # paneo a la derecha
        k, dx, dy = 1.1, -70 + 140 * p, 0
    else:              # paneo a la izquierda y arriba
        k, dx, dy = 1.1, 70 - 140 * p, 20 - 40 * p
    return (f'<g transform="translate({960 + dx:.1f} {540 + dy:.1f}) scale({k:.4f}) translate(-960 -540)">'
            f'<image href="{href}" width="{W}" height="{H}"/></g>')


# ---------------------------------------------------------------- textos
def texto(x, y, s, tam, color="#FFFFFF", borde="#2B1B0E", grosor=None, familia="DejaVu Serif", peso="bold", extra=""):
    g = grosor or max(6, tam * 0.16)
    return (f'<text x="{x}" y="{y}" text-anchor="middle" font-family="{familia}" font-weight="{peso}" font-size="{tam}" fill="{color}" '
            f'stroke="{borde}" stroke-width="{g:.1f}" paint-order="stroke" stroke-linejoin="round" {extra}>{s}</text>')


_FUENTE = {}


def ancho_texto(s, tam):
    from PIL import ImageFont
    if tam not in _FUENTE:
        _FUENTE[tam] = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", tam)
    return _FUENTE[tam].getlength(s)


def subtitulos(narr, t, vdur):
    palabras = narr.split()
    if not palabras:
        return ""
    pesos = [len(p) + 1 + (5 if p[-1] in ",;:" else 0) + (9 if p[-1] in ".?!" else 0) for p in palabras]
    pos = c01((t - 0.15) / max(0.5, vdur - 0.3)) * sum(pesos)
    acum, actual = 0, len(palabras) - 1
    for i, w in enumerate(pesos):
        if acum + w > pos:
            actual = i
            break
        acum += w
    grupos, g = [], []
    for i, p in enumerate(palabras):
        g.append(i)
        if len(g) == 4 or p[-1] in ".,?!;:":
            grupos.append(g)
            g = []
    if g:
        grupos.append(g)
    grupo = next(gr for gr in grupos if actual in gr)
    fs = 66
    anchos = [ancho_texto(palabras[i].upper(), fs) * 1.1 for i in grupo]
    esp = fs * 0.32
    tot = sum(anchos) + esp * (len(grupo) - 1)
    if tot > 1600:
        k = 1600 / tot
        fs, anchos, esp = fs * k, [a * k for a in anchos], esp * k
        tot = 1600
    x = 960 - tot / 2
    s = []
    for i, w in zip(grupo, anchos):
        activa = i == actual
        col = "#FFD54F" if activa else "#FFFFFF"
        esc_ = 1.1 if activa else 1.0
        s.append(f'<g transform="translate({x + w / 2:.1f} 990) scale({esc_})">'
                 + texto(0, 0, palabras[i].upper().replace("&", "&amp;"), round(fs), col, "#1A0F06", fs * 0.2, "DejaVu Sans", "bold") + "</g>")
        x += w + esp
    return "".join(s)


def titulo(t):
    p = suave((t - 0.6) / 0.9)
    if p <= 0:
        return ""
    y = 300 - 40 * (1 - p)
    return (f'<g opacity="{p:.3f}"><rect x="360" y="{y - 150:.0f}" width="1200" height="250" rx="40" fill="#2B1B0E" fill-opacity="0.55"/>'
            + texto(960, y - 20, "PEDRO", 128, "#FFD54F", "#5A2E0E", 18)
            + texto(960, y + 70, "el niño sagaz", 72, "#FFFFFF", "#5A2E0E", 12, extra='font-style="italic"') + "</g>")


def capitulo(nombre, t, dur):
    p = suave((t - 0.2) / 0.6) * suave((dur - t) / 0.4)
    if p <= 0:
        return ""
    return (f'<g opacity="{p:.3f}"><path d="M330 430 L1590 430 L1530 540 L1590 650 L330 650 L390 540 Z" fill="#7B2D12" stroke="#FFD54F" stroke-width="8"/>'
            + texto(960, 572, nombre, 84, "#FFF3D6", "#3E1405", 10) + "</g>")


def fin(t, dur):
    p = suave((t - (dur - 3.2)) / 1.2)
    if p <= 0:
        return ""
    return f'<g opacity="{p:.3f}">' + texto(960, 300, "FIN", 170, "#FFD54F", "#5A2E0E", 22) + "</g>"


VINETA = ('<defs><radialGradient id="vin" cx="50%" cy="50%" r="75%"><stop offset="60%" stop-color="#000" stop-opacity="0"/>'
          '<stop offset="100%" stop-color="#1A0F06" stop-opacity="0.55"/></radialGradient></defs>')


def cuadro_svg(i, t, dur, vdur, prev_dur):
    narr, e = GU.E[i]
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{VINETA}<rect width="{W}" height="{H}" fill="#1A0F06"/>']
    if i > 0 and t < FUNDIDO:
        s.append(base(i - 1, prev_dur, prev_dur))
        s.append(f'<g opacity="{suave(t / FUNDIDO):.3f}">{base(i, t, dur)}</g>')
    elif i == 0 and t < 0.8:
        s.append(f'<g opacity="{suave(t / 0.8):.3f}">{base(i, t, dur)}</g>')
    else:
        s.append(base(i, t, dur))
    s.append(f'<rect width="{W}" height="{H}" fill="url(#vin)"/>')
    if e.get("titulo"):
        s.append(titulo(t))
    if e.get("capitulo"):
        s.append(capitulo(e["capitulo"], t, dur))
    if e.get("fin"):
        s.append(fin(t, dur))
        if t > dur - 1.0:
            s.append(f'<rect width="{W}" height="{H}" fill="#000" opacity="{c01(t - (dur - 1.0)):.3f}"/>')
    s.append(subtitulos(narr, t, vdur))
    s.append("</svg>")
    return "".join(s)


def _png(svg):
    return subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-f", "png"], input=svg.encode(), capture_output=True, check=True).stdout


def _cuadro(args):
    return _png(cuadro_svg(*args))


def preparar_clips():
    for i, (_, e) in enumerate(GU.E):
        mp4 = os.path.join(AQUI, "clips", f"{i:02d}.mp4")
        carpeta = os.path.join(AQUI, "clips", f"{i:02d}_cuadros")
        if os.path.exists(mp4) and not os.path.isdir(carpeta):
            os.makedirs(carpeta)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp4, "-vf", f"fps={FPS_CLIP},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                            "-q:v", "3", os.path.join(carpeta, "%04d.jpg")], check=True)


# ---------------------------------------------------------------- audio
def leer(ruta):
    tmp = ruta + ".tmp.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ruta, "-ac", "1", "-ar", str(SR), tmp], check=True)
    y, _ = sf.read(tmp)
    os.remove(tmp)
    return y


def voces():
    rutas = [os.path.join(AQUI, "voz", f"{i:02d}.mp3") for i in range(len(GU.E))]
    if all(os.path.exists(r) for r in rutas):
        print("voz: ElevenLabs (KIE)", flush=True)
        ys = [leer(r) for r in rutas]
    else:
        print("voz: local (Kokoro)", flush=True)
        import sherpa_onnx
        k = os.path.join(TTS_KOKORO, "kokoro-multi-lang-v1_0")
        cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
            model=f"{k}/model.onnx", voices=f"{k}/voices.bin", tokens=f"{k}/tokens.txt", data_dir=f"{k}/espeak-ng-data",
            dict_dir=f"{k}/dict", lexicon=f"{k}/lexicon-us-en.txt,{k}/lexicon-zh.txt", lang="es"), num_threads=4))
        tts = sherpa_onnx.OfflineTts(cfg)
        ys = []
        for narr, _ in GU.E:
            a = tts.generate(narr, sid=VOZ_SID, speed=VOZ_VELOCIDAD)
            y = np.array(a.samples, dtype=np.float64)
            ys.append(np.interp(np.arange(int(len(y) * SR / a.sample_rate)) / SR, np.arange(len(y)) / a.sample_rate, y))
    return [np.concatenate([np.zeros(int(SR * 0.35)), y, np.zeros(int(SR * 0.55))]) for y in ys]


def musica(total):
    pistas = [os.path.join(AQUI, n) for n in ("musica.mp3", "musica_1.mp3") if os.path.exists(os.path.join(AQUI, n))]
    if not pistas:
        return np.zeros(int(SR * total))
    partes = [leer(p) for p in pistas]
    m = partes[0]
    cruce = int(SR * 3)
    for p in partes[1:]:
        r = np.linspace(1, 0, cruce)
        m = np.concatenate([m[:-cruce], m[-cruce:] * r + p[:cruce] * (1 - r), p[cruce:]])
    while len(m) < SR * total:
        m = np.concatenate([m, m])
    m = m[:int(SR * total)]
    m[-int(SR * 4):] *= np.linspace(1, 0, int(SR * 4))
    return m / max(1e-9, np.abs(m).max())


def main():
    if sys.argv[1] == "--muestra":
        carpeta = sys.argv[2]
        os.makedirs(carpeta, exist_ok=True)
        preparar_clips()
        for i in range(len(GU.E)):
            with open(os.path.join(carpeta, f"{i:02d}.png"), "wb") as fh:
                fh.write(_png(cuadro_svg(i, 6.5, 9.0, 8.0, 9.0)))
        print("ok")
        return
    salida = sys.argv[1]
    fps = int(sys.argv[2]) if len(sys.argv) > 2 else 24
    preparar_clips()
    vs = voces()
    durs = [len(v) / SR for v in vs]
    durs[-1] += 2.5  # cierre con "FIN"
    total = sum(durs)
    print(f"{len(GU.E)} escenas · {total:.1f} s", flush=True)
    voz = np.zeros(int(SR * total) + SR)
    t0 = 0.0
    for v, d in zip(vs, durs):
        i0 = int(SR * t0)
        voz[i0:i0 + len(v)] += v
        t0 += d
    voz = voz[:int(SR * total)]
    voz /= max(1e-9, np.abs(voz).max())
    pista = 0.9 * voz + 0.16 * musica(total)
    pista /= max(1.0, np.abs(pista).max() / 0.95)
    wav = salida + ".wav"
    sf.write(wav, pista.astype(np.float32), SR)
    tareas = []
    for i, d in enumerate(durs):
        vd = len(vs[i]) / SR - 0.75
        pd = durs[i - 1] if i else 0
        for fi in range(int(round(d * fps))):
            tareas.append((i, fi / fps, d, vd, pd))
    print(f"{len(tareas)} cuadros", flush=True)
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(fps), "-i", "-", "-i", wav,
                           "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-shortest", "-movflags", "+faststart", salida], stdin=subprocess.PIPE)
    with Pool(4) as pool:
        for n, png in enumerate(pool.imap(_cuadro, tareas, chunksize=4)):
            ff.stdin.write(png)
            if n % 960 == 0:
                print(f"cuadro {n}/{len(tareas)}", flush=True)
    ff.stdin.close()
    ff.wait()
    os.remove(wav)
    print("listo", salida, flush=True)


if __name__ == "__main__":
    main()
