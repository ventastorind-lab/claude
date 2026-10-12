"""Render de Byron vs. 50 Coca-Colas v2 (viaje dentro del cuerpo).

Uso:
  python3 render.py <salida.mp4> [fps]                    # voz de KIE en voz/NN.mp3 (obligatoria)
  python3 render.py <salida.mp4> [fps] --voz-local <tts>  # vista previa con la voz local anterior
  python3 render.py --muestra <carpeta>                   # cuadros de prueba de cada escena

Los clips de KIE en clips/NN.mp4 (si existen) reemplazan los primeros segundos de su escena.
"""
import base64
import importlib.util
import math
import os
import subprocess
import sys
from multiprocessing import Pool

import numpy as np
import soundfile as sf

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import anatomia as AN  # noqa: E402
import guion as GU  # noqa: E402


def _cargar(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


CA = _cargar("cola_animar", os.path.join(AQUI, "..", "cocacola", "animar.py"))
C, A, HV = CA.C, CA.A, CA.HV
CA.HV.subtitulo = lambda texto: ""  # este video usa subtítulos estilo viral propios
W, H, SR, INK = 1920, 1080, CA.SR, C.INK
f, prog, ease_out, c01, lerp = A.f, A.prog, A.ease_out, A.c01, A.lerp
FPS_CLIP = 24


# ---------------------------------------------------------------- subtítulos virales
def subtitulos(texto, t, vdur):
    palabras = texto.split()
    if not palabras:
        return ""
    pesos = [len(p) + 1 + (5 if p[-1] in ",;:" else 0) + (9 if p[-1] in ".?!" else 0) for p in palabras]
    tot = sum(pesos)
    pos = c01((t - 0.1) / max(0.5, vdur - 0.35)) * tot
    acum, actual = 0, len(palabras) - 1
    for i, w in enumerate(pesos):
        if acum + w > pos:
            actual = i
            break
        acum += w
    # grupos de hasta 3 palabras (cortando en puntuación)
    grupos, g = [], []
    for i, p in enumerate(palabras):
        g.append(i)
        if len(g) == 3 or p[-1] in ".,?!;:":
            grupos.append(g)
            g = []
    if g:
        grupos.append(g)
    grupo = next(gr for gr in grupos if actual in gr)
    fs = 74
    anchos = [sum(0.78 if ch.isalpha() and ch.upper() not in "IJ" else 0.48 for ch in palabras[i]) * fs for i in grupo]
    esp = fs * 0.35
    total = sum(anchos) + esp * (len(grupo) - 1)
    if total > 1500:
        k = 1500 / total
        fs *= k
        anchos = [w * k for w in anchos]
        esp *= k
    x = 960 - (sum(anchos) + esp * (len(grupo) - 1)) / 2
    s = []
    for i, w in zip(grupo, anchos):
        activa = i == actual
        k = 1.14 if activa else 1.0
        col = "#FFE600" if activa else "#FFFFFF"
        cx = x + w / 2
        s.append(f'<g transform="translate({f(cx)} 985) scale({k}) rotate({-3 if activa else 0})">'
                 f'<text x="0" y="0" text-anchor="middle" font-family="Arial Black, Arial" font-weight="900" font-size="{fs}" fill="{col}" '
                 f'stroke="#000000" stroke-width="14" paint-order="stroke" stroke-linejoin="round">{palabras[i].upper()}</text></g>')
        x += w + esp
    return "".join(s)


# ---------------------------------------------------------------- escenas
def byron_para_cam(cam, t):
    return C.byron(960, t=t, pose=cam.get("pose", "normal"), panza=cam.get("panza", 0), ojos=cam.get("ojos", "normal"),
                   boca=cam.get("boca", "sonrisa"), sudor=cam.get("sudor", False), tiembla=cam.get("tiembla", False))


def cuerpo(e, t, dur):
    org, fase = e["cuerpo"]
    k = 1.0 + 0.04 * t / max(dur, 1)
    s = [f'<g transform="translate(960 540) scale({k:.4f}) translate(-960 -540)">{AN.ORGANOS[org](fase, t, dur)}</g>']
    if "cam" in e:
        s.append(AN.byron_cam(byron_para_cam(e["cam"], t), t))
    return "".join(s)


def iris(svg_dentro, t, cx=960, cy=540):
    """Entrada circular al interior del cuerpo."""
    p = ease_out(prog(t, 0, 0.55))
    r = 40 + 1250 * p
    return (f'<rect width="{W}" height="{H}" fill="#1A1A1A"/><clipPath id="iris"><circle cx="{cx}" cy="{cy}" r="{f(r)}"/></clipPath>'
            f'<g clip-path="url(#iris)">{svg_dentro}</g><circle cx="{cx}" cy="{cy}" r="{f(r)}" fill="none" stroke="#FFE600" stroke-width="{f(18 * (1 - p) + 2)}"/>')


def frame_clip(i, t):
    """Cuadro del clip de KIE (como data URI JPG) si existe y t está dentro de su duración."""
    carpeta = os.path.join(AQUI, "clips", f"{i:02d}_cuadros")
    if not os.path.isdir(carpeta):
        return None
    n = int(t * FPS_CLIP) + 1
    ruta = os.path.join(carpeta, f"{n:04d}.jpg")
    if not os.path.exists(ruta):
        return None
    with open(ruta, "rb") as fh:
        return "data:image/jpeg;base64," + base64.b64encode(fh.read()).decode()


_IMG = {}


def img_uri(ruta):
    """Imagen reducida a 1920x1080 en JPG (data URI), con caché por proceso."""
    if ruta not in _IMG:
        import io
        from PIL import Image
        buf = io.BytesIO()
        Image.open(ruta).convert("RGB").resize((W, H), Image.LANCZOS).save(buf, "JPEG", quality=90)
        _IMG[ruta] = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()
    return _IMG[ruta]


def dur_clip(i):
    carpeta = os.path.join(AQUI, "clips", f"{i:02d}_cuadros")
    return len(os.listdir(carpeta)) / FPS_CLIP if os.path.isdir(carpeta) else 0.0


def ilustracion(i, e, t, dur):
    """Escena con ilustración de KIE: zoom lento (Ken Burns); si hay clip, sigue desde su último cuadro."""
    dc = dur_clip(i) if "kie" in e else 0.0
    if dc and t < dc and frame_clip(i, t):
        return f'<image href="{frame_clip(i, t)}" x="0" y="0" width="{W}" height="{H}"/>'
    if dc and t >= dc:
        ruta = os.path.join(AQUI, "clips", f"{i:02d}_cuadros", f"{int(dc * FPS_CLIP):04d}.jpg")
        with open(ruta, "rb") as fh:
            href = "data:image/jpeg;base64," + base64.b64encode(fh.read()).decode()
        t0 = dc
    else:
        href = img_uri(os.path.join(AQUI, "imagenes", e["imagen"]["nombre"] + ".png"))
        t0 = 0.0
    k = 1.0 + 0.07 * (t - t0) / max(dur - t0, 1)
    ox, oy = e["imagen"].get("foco", (960, 540))
    s = (f'<rect width="{W}" height="{H}" fill="#000000"/><g transform="translate({ox} {oy}) scale({k:.4f}) translate({-ox} {-oy})">'
         f'<image href="{href}" x="0" y="0" width="{W}" height="{H}"/></g>')
    if t < 0.25:
        s += f'<rect width="{W}" height="{H}" fill="#FFFFFF" opacity="{f(1 - t / 0.25)}"/>'
    return s


def previa(i):
    """Escena anterior que no sea ilustración (para que latas, contador y panza continúen bien)."""
    for j in range(i - 1, -1, -1):
        if "imagen" not in GU.E[j][1]:
            return GU.E[j][1]
    return None


def escena(i, narr, e, prev, t, dur, vdur):
    if "imagen" in e:
        cuerpo_svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{ilustracion(i, e, t, dur)}'
        return cuerpo_svg + subtitulos(narr, t, vdur) + "</svg>"
    if "cuerpo" in e:
        dentro = cuerpo(e, t, dur)
        if (not prev or "cuerpo" not in prev) and t < 0.6:
            dentro = iris(dentro, t)
        cuerpo_svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">{HV.DEFS}{dentro}')
    else:
        cuerpo_svg = CA.escena_a(i, narr, e, previa(i) or {}, t, dur).replace("</svg>", "")
    clipf = frame_clip(i, t) if "kie" in e else None
    if clipf:
        cuerpo_svg += f'<image href="{clipf}" x="0" y="0" width="{W}" height="{H}" preserveAspectRatio="xMidYMid slice"/>'
    return cuerpo_svg + subtitulos(narr, t, vdur) + "</svg>"


def _png(svg):
    return subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-f", "png"], input=svg.encode("utf-8"), capture_output=True, check=True).stdout


def _cuadro(args):
    return _png(escena(*args))


def cuadro_inicial(i, destino):
    """Cuadro de arranque de la escena i (sin subtítulos), para usar como imagen inicial de KIE."""
    narr, e = GU.E[i]
    prev = GU.E[i - 1][1] if i else None
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    svg = escena(i, "", e, prev, 1.2, 6.0, 1.0)
    with open(destino, "wb") as fh:
        fh.write(_png(svg))
    return destino


def preparar_clips():
    for i, (_, e) in enumerate(GU.E):
        mp4 = os.path.join(AQUI, "clips", f"{i:02d}.mp4")
        carpeta = os.path.join(AQUI, "clips", f"{i:02d}_cuadros")
        if "kie" in e and os.path.exists(mp4) and not os.path.isdir(carpeta):
            os.makedirs(carpeta)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", mp4, "-vf", f"fps={FPS_CLIP},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
                            "-q:v", "3", os.path.join(carpeta, "%04d.jpg")], check=True)


# ---------------------------------------------------------------- audio
def leer_audio(ruta):
    tmp = ruta + ".wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ruta, "-ac", "1", "-ar", str(SR), tmp], check=True)
    y, _ = sf.read(tmp)
    os.remove(tmp)
    return y


def voces_kie():
    out = []
    for i in range(len(GU.E)):
        ruta = os.path.join(AQUI, "voz", f"{i:02d}.mp3")
        if not os.path.exists(ruta):
            sys.exit(f"Falta la voz {ruta}. Genera las voces con: python3 kie.py voces --voz liam")
        y = leer_audio(ruta)
        out.append(np.concatenate([np.zeros(int(SR * 0.1)), y, np.zeros(int(SR * 0.25))]))
    return out


def eventos(e, prev, dur):
    if "imagen" in e:
        return [(0.0, "swoosh", 0.5)]
    if "cuerpo" not in e:
        return CA.eventos_sfx(e, prev, dur)
    org, fase = e["cuerpo"]
    ev = [(0.0, "whoosh", 0.6)]
    if not prev or "cuerpo" not in prev:
        ev.append((0.05, "swoosh", 0.6))
    extra = {"estomago": [(0.4, "fizz", 0.6), (1.4, "glup", 0.6)], "corazon": [(0.3 + k * 0.5, "boom", 0.25) for k in range(int(dur / 0.5))],
             "dientes": [(0.6, "alarma", 0.35)], "pancreas": [(0.4, "alarma", 0.45)] + [(0.8 + j * 0.45, "pop", 0.5) for j in range(4)],
             "bodega": [(0.6, "pop", 0.4), (2.2, "boom", 0.5)], "cerebro": [(0.5, "fanfarria" if fase == "dopamina" else "tick", 0.5)],
             "higado": [(0.6, "pop", 0.4)], "rinones": [(0.5, "tick", 0.5), (2.2, "alarma", 0.45)], "colon": [(0.8, "burp", 0.5)],
             "sangre": [(0.4, "whoosh", 0.4)], "resumen": [(0.4 + k * 0.5, "pop", 0.45) for k in range(8)]}
    return ev + extra.get(org, [])


def main():
    if sys.argv[1] == "--muestra":
        carpeta = sys.argv[2]
        os.makedirs(carpeta, exist_ok=True)
        for i, (narr, e) in enumerate(GU.E):
            prev = GU.E[i - 1][1] if i else None
            with open(os.path.join(carpeta, f"{i:02d}.png"), "wb") as fh:
                fh.write(_png(escena(i, narr, e, prev, 3.0, 6.0, 5.5)))
        print("ok")
        return
    salida = sys.argv[1]
    fps = int(sys.argv[2]) if len(sys.argv) > 2 and sys.argv[2].isdigit() else 24
    if "--voz-local" in sys.argv:
        tts = sys.argv[sys.argv.index("--voz-local") + 1]
        voces = CA.generar_voz(tts, [n for n, _ in GU.E])
        voces = [CA.subir_tono(v, salida + f".t{k}") for k, v in enumerate(voces)]
    else:
        voces = voces_kie()
    preparar_clips()
    durs = [max(len(v) / SR, 2.5) for v in voces]
    vdurs = [len(v) / SR - 0.3 for v in voces]
    total = sum(durs)
    print(f"{len(GU.E)} escenas · {total:.1f} s", flush=True)
    A.cargar_sfx()
    A.SFX.update(abrir=CA.sfx_abrir(), fizz=CA.sfx_fizz(), trago=CA.sfx_trago(), glup=CA.sfx_glup(), vibra=CA.sfx_vibra())
    voz = np.zeros(int(SR * (total + 1)))
    efectos = np.zeros_like(voz)
    t0 = 0.0
    for k, ((narr, e), v, d) in enumerate(zip(GU.E, voces, durs)):
        prev = GU.E[k - 1][1] if k else None
        i0 = int(SR * t0)
        voz[i0:i0 + len(v)] += v
        for ts, nombre, vol in eventos(e, prev if "cuerpo" in e else previa(k), d):
            snd = A.SFX[nombre] * vol * 0.55
            j = i0 + int(SR * ts)
            if 0 <= j < len(efectos):
                efectos[j:j + len(snd)] += snd[:len(efectos) - j]
        t0 += d
    pista = voz + efectos
    pista[:int(SR * total)] += CA.musica_fiesta(total) * 0.22
    pista = pista[:int(SR * total)]
    pista /= max(1.0, np.abs(pista).max() / 0.95)
    wav = salida + ".wav"
    sf.write(wav, pista.astype(np.float32), SR)
    tareas = []
    for k, ((narr, e), d, vd) in enumerate(zip(GU.E, durs, vdurs)):
        prev = GU.E[k - 1][1] if k else None
        for fi in range(int(round(d * fps))):
            tareas.append((k, narr, e, prev, fi / fps, d, vd))
    print(f"{len(tareas)} cuadros", flush=True)
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(fps), "-i", "-", "-i", wav,
                           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
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
