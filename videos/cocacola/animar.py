"""Render animado: ¿Qué pasa si te tomas 50 Coca-Colas en un día? (Byron).

Uso: python3 animar.py <carpeta_tts> <salida.mp4> [fps]
<carpeta_tts> debe contener kokoro-multi-lang-v1_0/.
"""
import importlib.util
import math
import os
import subprocess
import sys
from multiprocessing import Pool

import numpy as np
import soundfile as sf

AQUI = os.path.dirname(os.path.abspath(__file__))


def _cargar(nombre, ruta):
    spec = importlib.util.spec_from_file_location(nombre, ruta)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


C = _cargar("cola_escenas", os.path.join(AQUI, "escenas.py"))
A = _cargar("huevos_animar", os.path.join(AQUI, "..", "huevos", "animar.py"))
HV = C.HV
W, H, GY, INK = C.W, C.H, C.GY, C.INK
SR = 44100
pop, prog, ease_out, ease_back, lerp, c01, f = A.pop, A.prog, A.ease_out, A.ease_back, A.lerp, A.c01, A.f

VOZ_SID = 53          # em_santa (Kokoro v1.0), la voz con más rango de tono
VOZ_VELOCIDAD = 1.12
TONO = 1.19           # +3 semitonos aprox.: más caricaturesco


# ------------------------------------------------------------------ cámara
def foco(e):
    if "tarjeta" in e:
        tj = e["tarjeta"]
        if tj.get("chica") or tj.get("grande"):
            return tj.get("x", 1440), tj.get("y", 150) + 200
        return 1460, 330
    if "icono" in e:
        return e["icono"][1], e["icono"][2]
    b = e.get("byron")
    if b:
        return b["x"] + 40, GY - 520
    return W / 2, H / 2


def camara(e, t, dur, sac):
    if dur > 4.5 and t >= dur * 0.52:
        z = lerp(1.26, 1.17, ease_out(prog(t, dur * 0.52, 0.3)))
        fx, fy = foco(e)
    else:
        z, fx, fy = lerp(1.1, 1.0, ease_out(prog(t, 0, 0.45))), W / 2, H / 2
    vw, vh = W / z, H / z
    left = min(max(fx - vw / 2, 0), W - vw)
    top = min(max(fy - vh / 2, 0), H - vh)
    sx = sy = 0.0
    if sac is not None and 0 <= t - sac < 0.5:
        a = 16 * (1 - (t - sac) / 0.5)
        sx, sy = a * math.sin(t * 95), a * math.cos(t * 81)
    entrada = (1 - ease_out(prog(t, 0, 0.22))) * 260
    return f'translate({f(entrada)} 0) scale({f(z)}) translate({f(-left + sx)} {f(-top + sy)})'


# ------------------------------------------------------------------ escena
def escena_a(i, narr, e, prev, t, dur):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">', HV.DEFS,
         f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>']
    sac = 0.5 if "onomatopeya" in e else (0.2 if "titulo" in e else None)
    s.append(f'<g transform="{camara(e, t, dur, sac)}">')
    s.append(HV.fondo(e.get("fondo", "plano")))
    if "reloj_pared" in e:
        s.append(C.reloj_pared(e["reloj_pared"]))
    if "latas" in e:
        n0 = prev.get("latas", e["latas"]) if prev else e["latas"]
        n = round(lerp(n0, e["latas"], ease_out(prog(t, 0.15, 0.9))))
        s.append(C.pared_latas(n))
    if "icono" in e:
        nom, x, y = e["icono"][:3]
        bob = 0 if nom in ("corazon", "bano") else 8 * math.sin(2 * math.pi * 0.7 * t)
        svg = f'<g transform="translate(0 {f(bob)})">{C.icono(nom, x, y, t)}</g>'
        if nom == "gas":
            svg = f'<g transform="translate({f(t * 25)} {f(-t * 12)})">{svg}</g>'
        s.append(pop(svg, x, y, t, 0.3, 0.5))
    b = e.get("byron")
    if b:
        pb = prev.get("byron") if prev else None
        pz0 = pb.get("panza", 0) if pb else b.get("panza", 0)
        pz = lerp(pz0, b.get("panza", 0), ease_out(prog(t, 0, 1.0)))
        s.append(C.byron(b["x"], t=t, pose=b.get("pose", "normal"), panza=pz, ojos=b.get("ojos", "normal"), boca=b.get("boca", "sonrisa"),
                         sudor=b.get("sudor", False), tiembla=b.get("tiembla", False), mira=b.get("mira", 1)))
    if e.get("burbujas_gas"):
        s.append(C.burbujas_gas(t))
    if e.get("confeti"):
        s.append(A.confeti_a(t))
    if "tarjeta" in e:
        s.append(A.tarjeta_a(e["tarjeta"], t))
    if "burbuja" in e:
        bb = e["burbuja"]
        s.append(pop(HV.burbuja(**bb), bb["x"], bb["y"], t, 0.6))
    if "onomatopeya" in e:
        tx, x, y = e["onomatopeya"]
        w = 7 * math.sin(t * 22) * c01(1 - (t - 0.5) / 1.0)
        s.append(pop(f'<g transform="rotate({f(w)} {x} {y})">{HV.onomatopeya(tx, x, y)}</g>', x, y, t, 0.5, 0.35))
    s.append('</g>')
    if "contador" in e:
        c0 = prev.get("contador", 0) if prev else 0
        q = prog(t, 0.15, 0.75)
        n = round(lerp(c0, e["contador"], ease_out(q)))
        k = 1 + 0.08 * math.sin(math.pi * q) if c0 != e["contador"] else 1
        s.append(f'<g transform="translate(835 135) scale({f(k)}) translate(-835 -135)">{C.contador(n)}</g>')
    if "reloj" in e:
        dyr = (1 - ease_back(prog(t, 0.05, 0.45))) * -260
        s.append(f'<g transform="translate(0 {f(dyr)})">{HV.reloj(e["reloj"])}</g>')
    if "titulo" in e:
        p = prog(t, 0.2, 0.55)
        if p > 0:
            s.append(f'<g transform="translate(0 {f((1 - ease_back(p)) * -500)})">{HV.titulo(*e["titulo"])}</g>')
    if e.get("suscribete"):
        s.append(A.suscribete_a(t))
    s.append(HV.subtitulo(narr))
    s.append('</svg>')
    return "".join(s)


# ------------------------------------------------------------------ sonido
def eventos_sfx(e, prev, dur):
    ev = [(0.0, "whoosh", 0.45)]
    if "tarjeta" in e:
        ev.append((0.35, "swoosh", 0.6))
        tj = e["tarjeta"]
        if tj.get("barras") or tj.get("numero"):
            ev += [(0.85 + k * 0.1, "tick", 0.5) for k in range(7)]
        if tj.get("filas"):
            ev += [(0.8 + k * 0.28, "pop", 0.45) for k in range(len(tj["filas"]))]
    if "icono" in e:
        nom = e["icono"][0]
        ev.append((0.3, "pop", 0.6))
        if nom in ("alerta", "hospital"):
            ev.append((0.45, "alarma", 0.5))
        if nom == "check":
            ev.append((0.45, "ding", 0.7))
        if nom == "gas":
            ev.append((0.6, "burp", 0.4))
        if nom == "corazon":
            ev += [(0.3 + k / 3.2, "boom", 0.25) for k in range(int((dur - 0.3) * 3.2))]
    if "contador" in e and (not prev or prev.get("contador") != e["contador"]):
        ev += [(0.2, "abrir", 0.8), (0.9, "ding", 0.5)]
    if "burbuja" in e:
        ev.append((0.6, "pop", 0.7))
    if "onomatopeya" in e:
        tx = e["onomatopeya"][0]
        ev.append((0.5, "burp" if ("BURP" in tx or "PRRR" in tx) else ("glup" if "GLUP" in tx else "boom"), 1.0))
    if "titulo" in e:
        ev.append((0.35, "boom", 0.6))
    if e.get("confeti"):
        ev.append((0.1, "fanfarria", 0.9))
    if e.get("suscribete"):
        ev += [(0.3, "pop", 0.6), (1.75, "click", 0.8), (2.0, "campana", 0.7)]
    if "reloj" in e:
        ev.append((0.1, "tick", 0.7))
    if e.get("burbujas_gas"):
        ev.append((0.2, "fizz", 0.6))
    b = e.get("byron") or {}
    if b.get("pose") in ("toma", "toma_agua"):
        k = 0
        while True:
            tt = (k + 0.3) / 0.8
            if tt > dur - 0.3:
                break
            ev.append((tt, "trago", 0.55))
            k += 1
    if b.get("tiembla"):
        ev.append((0.1, "vibra", 0.35))
    return ev


def sfx_abrir():
    n = int(SR * 0.5)
    rng = np.random.default_rng(1)
    click = rng.standard_normal(int(SR * 0.015)) * 0.6
    tt = np.arange(n) / SR
    hiss = A.lowpass(rng.standard_normal(n), 0.5) * np.exp(-tt * 7) * 0.5
    out = np.zeros(n)
    out[:len(click)] += click
    out[int(SR * 0.02):] += hiss[:n - int(SR * 0.02)]
    return out


def sfx_fizz():
    n = int(SR * 1.6)
    rng = np.random.default_rng(2)
    y = np.zeros(n)
    for _ in range(180):
        i = rng.integers(0, n - 400)
        d = rng.integers(60, 300)
        y[i:i + d] += rng.standard_normal(d) * np.exp(-np.arange(d) / 40) * 0.4
    return y * np.sin(np.pi * np.arange(n) / n)


def sfx_trago():
    n = int(SR * 0.28)
    tt = np.arange(n) / SR
    fr = 180 + 260 * np.exp(-tt * 18)
    y = np.sin(2 * np.pi * np.cumsum(fr) / SR) * np.exp(-tt * 14)
    return 0.6 * A.lowpass(y, 0.2) / 0.2 * 0.25


def sfx_glup():
    out = np.zeros(int(SR * 0.7))
    t1 = sfx_trago()
    for k in range(3):
        i0 = int(SR * 0.2 * k)
        out[i0:i0 + len(t1)] += t1 * (1.3 - 0.2 * k)
    return out


def sfx_vibra():
    n = int(SR * 1.2)
    tt = np.arange(n) / SR
    y = np.sign(np.sin(2 * np.pi * 120 * tt)) * (np.sin(2 * np.pi * 6 * tt) > 0)
    return 0.12 * A.lowpass(y, 0.15)


def musica_fiesta(total):
    """Loop alegre y bailable: Am-F-C-G a 124 bpm con bajo saltarín, palmas y melodía."""
    bpm = 124
    beat = 60 / bpm
    rng = np.random.default_rng(9)
    acordes = [(220.0, 261.6, 329.6), (174.6, 220.0, 261.6), (261.6, 329.6, 392.0), (196.0, 246.9, 293.7)]
    bajos = [110.0, 87.3, 130.8, 98.0]
    melodia = [[659, 0, 784, 659, 523, 0, 587, 659], [698, 0, 659, 523, 440, 0, 523, 0],
               [784, 0, 659, 784, 1047, 0, 988, 784], [740, 0, 784, 587, 494, 0, 587, 0]]
    compas = int(SR * beat * 4)
    loop = np.zeros(compas * 4)

    def tono(fr, d, forma="cuadrada", tau=0.12, vol=0.2):
        n = int(SR * d)
        tt = np.arange(n) / SR
        if forma == "cuadrada":
            y = np.sign(np.sin(2 * np.pi * fr * tt)) * 0.6 + np.sin(2 * np.pi * fr * tt) * 0.4
        else:
            y = np.sin(2 * np.pi * fr * tt)
        return vol * A.lowpass(y, 0.35) * np.exp(-tt / tau)

    for c in range(4):
        base = c * compas
        for k in range(4):  # bombo
            n = int(SR * 0.25)
            tt = np.arange(n) / SR
            i0 = base + int(SR * beat * k)
            loop[i0:i0 + n] += 0.5 * np.sin(2 * np.pi * (50 + 90 * np.exp(-tt * 30)) * tt) * np.exp(-tt * 14)
        for k in (1, 3):  # palmas
            n = int(SR * 0.12)
            i0 = base + int(SR * beat * k)
            loop[i0:i0 + n] += 0.22 * A.lowpass(rng.standard_normal(n), 0.6) * np.exp(-np.arange(n) / (SR * 0.025))
        for k in range(8):  # platillo
            n = int(SR * 0.04)
            i0 = base + int(SR * beat / 2 * k + SR * beat / 4)
            loop[i0:i0 + n] += 0.05 * rng.standard_normal(n) * np.exp(-np.arange(n) / (SR * 0.008))
        for k in range(8):  # bajo saltarín (octavas)
            fr = bajos[c] * (2 if k % 2 else 1) / 2
            nota = tono(fr, beat / 2 * 0.9, "seno", 0.15, 0.32)
            i0 = base + int(SR * beat / 2 * k)
            loop[i0:i0 + len(nota)] += nota
        for k in (0, 2):  # acordes en stab
            for fr in acordes[c]:
                nota = tono(fr, beat * 0.5, "cuadrada", 0.08, 0.05)
                i0 = base + int(SR * beat * (k + 0.5))
                loop[i0:i0 + len(nota)] += nota
        for k, fr in enumerate(melodia[c]):  # melodía
            if fr:
                nota = tono(fr, beat / 2 * 0.95, "cuadrada", 0.1, 0.07)
                i0 = base + int(SR * beat / 2 * k)
                loop[i0:i0 + len(nota)] += nota
    reps = int(np.ceil(total * SR / len(loop)))
    m = np.tile(loop, reps)[:int(total * SR)]
    fade = int(SR * 3)
    m[-fade:] *= np.linspace(1, 0, fade)
    m[:int(SR * 0.4)] *= np.linspace(0, 1, int(SR * 0.4))
    return 0.35 * m / (np.abs(m).max() + 1e-9)


# ------------------------------------------------------------------ voz
def generar_voz(carpeta, textos):
    import sherpa_onnx
    k = os.path.join(carpeta, "kokoro-multi-lang-v1_0")
    cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(kokoro=sherpa_onnx.OfflineTtsKokoroModelConfig(
        model=f"{k}/model.onnx", voices=f"{k}/voices.bin", tokens=f"{k}/tokens.txt", data_dir=f"{k}/espeak-ng-data",
        dict_dir=f"{k}/dict", lexicon=f"{k}/lexicon-us-en.txt,{k}/lexicon-zh.txt", lang="es"), num_threads=4))
    tts = sherpa_onnx.OfflineTts(cfg)
    voces = []
    for tx in textos:
        a = tts.generate(tx, sid=VOZ_SID, speed=VOZ_VELOCIDAD)
        y = np.array(a.samples, dtype=np.float64)
        y = np.interp(np.arange(int(len(y) * SR / a.sample_rate)) / SR, np.arange(len(y)) / a.sample_rate, y)
        voces.append(np.concatenate([np.zeros(int(SR * 0.1)), y, np.zeros(int(SR * 0.28))]))
    return voces


def subir_tono(y, ruta_tmp):
    sf.write(ruta_tmp + ".in.wav", y.astype(np.float32), SR)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", ruta_tmp + ".in.wav", "-af",
                    f"asetrate={int(SR * TONO)},aresample={SR},atempo={1 / TONO:.5f},highpass=f=70,acompressor=threshold=-18dB:ratio=3:attack=5:release=80",
                    ruta_tmp + ".out.wav"], check=True)
    z, _ = sf.read(ruta_tmp + ".out.wav")
    os.remove(ruta_tmp + ".in.wav")
    os.remove(ruta_tmp + ".out.wav")
    if z.ndim > 1:
        z = z.mean(axis=1)
    out = np.zeros(len(y))
    out[:min(len(z), len(y))] = z[:len(y)]
    return out


# ------------------------------------------------------------------ render
def _cuadro(args):
    i, narr, e, prev, t, dur = args
    svg = escena_a(i, narr, e, prev, t, dur).encode("utf-8")
    return subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-f", "png"], input=svg, capture_output=True, check=True).stdout


def main():
    carpeta, salida = sys.argv[1], sys.argv[2]
    fps = int(sys.argv[3]) if len(sys.argv) > 3 else 24
    escenas = C.E
    print("voz...", flush=True)
    voces = generar_voz(carpeta, [n for n, _ in escenas])
    durs = [max(len(v) / SR, 2.5) for v in voces]
    total = sum(durs)
    print(f"duración total {total:.1f} s", flush=True)
    A.cargar_sfx()
    A.SFX.update(abrir=sfx_abrir(), fizz=sfx_fizz(), trago=sfx_trago(), glup=sfx_glup(), vibra=sfx_vibra())
    voz = np.zeros(int(SR * (total + 1)))
    efectos = np.zeros_like(voz)
    t0 = 0.0
    for k, ((narr, e), v, d) in enumerate(zip(escenas, voces, durs)):
        prev = escenas[k - 1][1] if k else None
        i0 = int(SR * t0)
        voz[i0:i0 + len(v)] += v
        for ts, nombre, vol in eventos_sfx(e, prev, d):
            snd = A.SFX[nombre] * vol * 0.6
            j = i0 + int(SR * ts)
            if j < len(efectos):
                efectos[j:j + len(snd)] += snd[:len(efectos) - j]
        t0 += d
    voz = subir_tono(voz, salida)
    pista = voz * 1.0 + efectos
    pista[:int(SR * total)] += musica_fiesta(total) * 0.3
    pista = pista[:int(SR * total)]
    pista /= max(1.0, np.abs(pista).max() / 0.95)
    wav = salida + ".wav"
    sf.write(wav, pista.astype(np.float32), SR)
    tareas = []
    for k, ((narr, e), d) in enumerate(zip(escenas, durs)):
        prev = escenas[k - 1][1] if k else None
        for fi in range(int(round(d * fps))):
            tareas.append((k + 1, narr, e, prev, fi / fps, d))
    print(f"{len(tareas)} cuadros", flush=True)
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(fps), "-i", "-", "-i", wav,
                           "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-shortest", "-movflags", "+faststart", salida], stdin=subprocess.PIPE)
    with Pool(4) as pool:
        for n, png in enumerate(pool.imap(_cuadro, tareas, chunksize=4)):
            ff.stdin.write(png)
            if n % 480 == 0:
                print(f"cuadro {n}/{len(tareas)}", flush=True)
    ff.stdin.close()
    ff.wait()
    os.remove(wav)
    print("listo", salida, flush=True)


if __name__ == "__main__":
    main()
