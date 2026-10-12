"""Motor de la serie "Byron vs. 50": convierte un guion (videos.py) en un video animado con voz.

Uso: python3 motor.py <carpeta_tts> <carpeta_salida> [id_video ...]
Sin ids, renderiza todos los videos de videos.py.
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


CA = _cargar("cola_animar", os.path.join(AQUI, "..", "cocacola", "animar.py"))
OB = _cargar("retos_objetos", os.path.join(AQUI, "objetos.py"))
VD = _cargar("retos_videos", os.path.join(AQUI, "videos.py"))
C, A, HV = CA.C, CA.A, CA.HV
W, H, GY, INK, SR = C.W, C.H, C.GY, C.INK, CA.SR
pop, prog, ease_out, ease_back, lerp, c01, f = A.pop, A.prog, A.ease_out, A.ease_back, A.lerp, A.c01, A.f

ESPACIO = dict(banano=(44, 66), tinto=(48, 62), chile=(42, 66), dona=(56, 56), energetica=(40, 70), chocolatina=(44, 66),
               naranja=(54, 56), vaso_agua=(44, 66), hamburguesa=(64, 50), manzana=(56, 60))


def pila(video, n, x0=600):
    obj = OB.OBJETOS[video["objeto"]]
    dx, dy = ESPACIO[video["objeto"]]
    por_fila = max(1, int(420 // dx))
    top = GY - 260
    s = [f'<rect x="{x0}" y="{top}" width="480" height="26" rx="8" fill="#A1887F" stroke="{INK}" stroke-width="6"/>',
         f'<rect x="{x0 + 25}" y="{top + 26}" width="22" height="234" fill="#8D6E63" stroke="{INK}" stroke-width="5"/>',
         f'<rect x="{x0 + 433}" y="{top + 26}" width="22" height="234" fill="#8D6E63" stroke="{INK}" stroke-width="5"/>']
    for i in range(n):
        fila, col = i // por_fila, i % por_fila
        s.append(obj(x0 + 30 + dx / 2 + col * dx, top - dy * 0.55 - fila * dy, 0.55, 0))
    return "".join(s)


def contador(video, n):
    obj = OB.OBJETOS[video["objeto"]]
    p = n / 50
    etq = video["etiqueta"]
    return (f'<g transform="translate(620 36)"><rect width="460" height="150" rx="26" fill="#FFFFFF" stroke="{INK}" stroke-width="8"/>'
            + obj(70, 76, 0.85, 0)
            + f'<text x="140" y="68" font-family="Arial" font-weight="bold" font-size="{38 if len(etq) < 10 else 30}" fill="#455A64">{etq}</text>'
            f'<text x="140" y="125" font-family="Arial Black, Arial" font-weight="900" font-size="64" fill="{INK}">{n}<tspan font-size="40" fill="#90A4AE"> / 50</tspan></text>'
            f'<rect x="0" y="170" width="460" height="26" rx="13" fill="#ECEFF1" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="0" y="170" width="{f(max(460 * p, 26))}" height="26" rx="13" fill="{video.get("color", "#E53935")}" stroke="{INK}" stroke-width="5"/></g>')


def icono(nombre, x, y, t):
    svg = OB.icono_extra(nombre, x, y, t)
    if svg:
        return svg
    svg = C.icono(nombre, x, y, t)
    if svg:
        return svg
    return HV.icono(nombre, x, y, None)


def panza_de(e):
    b = e.get("byron") or {}
    if "panza" in b:
        return b["panza"]
    if "n" in e:
        return 120 * e["n"] / 50
    return 0


def escena_a(video, narr, e, prev, t, dur):
    s = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">', HV.DEFS,
         f'<rect width="{W}" height="{H}" fill="#FFFFFF"/>']
    sac = 0.5 if "onomatopeya" in e else (0.2 if "titulo" in e else None)
    s.append(f'<g transform="{CA.camara(e, t, dur, sac)}">')
    s.append(HV.fondo(e.get("fondo", "plano")))
    if "pila" in e:
        n0 = prev.get("pila", e["pila"]) if prev else e["pila"]
        s.append(pila(video, round(lerp(n0, e["pila"], ease_out(prog(t, 0.15, 0.9))))))
    if "icono" in e:
        nom, x, y = e["icono"][:3]
        bob = 0 if nom in ("corazon", "bano", "radiacion") else 8 * math.sin(2 * math.pi * 0.7 * t)
        svg = f'<g transform="translate(0 {f(bob)})">{icono(nom, x, y, t)}</g>'
        if nom == "gas":
            svg = f'<g transform="translate({f(t * 25)} {f(-t * 12)})">{svg}</g>'
        s.append(pop(svg, x, y, t, 0.3, 0.5))
    if "objeto_grande" in e:
        x, y = e["objeto_grande"]
        s.append(pop(OB.OBJETOS[video["objeto"]](x, y + 8 * math.sin(t * 3), 3.2, 6 * math.sin(t * 2)), x, y, t, 0.3, 0.5))
    b = e.get("byron")
    if b:
        pz0 = panza_de(prev) if prev and prev.get("byron") else panza_de(e)
        pz = lerp(pz0, panza_de(e), ease_out(prog(t, 0, 1.0)))
        pose = b.get("pose", "normal")
        s.append(C.byron(b["x"], t=t, pose=pose, panza=pz, ojos=b.get("ojos", "normal"), boca=b.get("boca", "sonrisa"),
                         sudor=b.get("sudor", False), tiembla=b.get("tiembla", False), mira=b.get("mira", 1),
                         objeto=OB.OBJETOS[video["objeto"]] if pose == "toma" else None))
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
    if "n" in e:
        c0 = prev.get("n", 0) if prev else 0
        q = prog(t, 0.15, 0.75)
        n = round(lerp(c0, e["n"], ease_out(q)))
        k = 1 + 0.08 * math.sin(math.pi * q) if c0 != e["n"] else 1
        s.append(f'<g transform="translate(850 135) scale({f(k)}) translate(-850 -135)">{contador(video, n)}</g>')
    if "reloj" in e:
        s.append(f'<g transform="translate(0 {f((1 - ease_back(prog(t, 0.05, 0.45))) * -260)})">{HV.reloj(e["reloj"])}</g>')
    if "titulo" in e:
        p = prog(t, 0.2, 0.55)
        if p > 0:
            s.append(f'<g transform="translate(0 {f((1 - ease_back(p)) * -500)})">{HV.titulo(*e["titulo"])}</g>')
    if e.get("suscribete"):
        s.append(A.suscribete_a(t))
    s.append(HV.subtitulo(narr))
    s.append('</svg>')
    return "".join(s)


def eventos(video, e, prev, dur):
    ev = CA.eventos_sfx({k: v for k, v in e.items() if k != "byron"}, None, dur)
    ev = [x for x in ev if x[1] not in ("abrir",)]
    if "n" in e and (not prev or prev.get("n") != e["n"]):
        ev += [(0.2, "abrir" if video.get("bebida") else "pop", 0.6), (0.9, "ding", 0.5)]
    b = e.get("byron") or {}
    if b.get("pose") == "toma":
        k = 0
        while True:
            tt = (k + 0.3) / 0.8
            if tt > dur - 0.3:
                break
            ev.append((tt, "trago" if video.get("bebida") else "chomp", 0.55))
            k += 1
    if b.get("tiembla"):
        ev.append((0.1, "vibra", 0.35))
    return ev


def _cuadro(args):
    vid, narr, e, prev, t, dur = args
    svg = escena_a(VD.VIDEOS[vid], narr, e, prev, t, dur).encode("utf-8")
    return subprocess.run(["rsvg-convert", "-w", str(W), "-h", str(H), "-f", "png"], input=svg, capture_output=True, check=True).stdout


def render(vid, carpeta_tts, salida, fps=24):
    video = VD.VIDEOS[vid]
    escenas = video["escenas"]
    voces = CA.generar_voz(carpeta_tts, [n for n, _ in escenas])
    durs = [max(len(v) / SR, 2.5) for v in voces]
    total = sum(durs)
    print(f"[{vid}] {len(escenas)} escenas, {total:.1f} s", flush=True)
    voz = np.zeros(int(SR * (total + 1)))
    efectos = np.zeros_like(voz)
    t0 = 0.0
    for k, ((narr, e), v, d) in enumerate(zip(escenas, voces, durs)):
        prev = escenas[k - 1][1] if k else None
        i0 = int(SR * t0)
        voz[i0:i0 + len(v)] += v
        for ts, nombre, vol in eventos(video, e, prev, d):
            snd = A.SFX[nombre] * vol * 0.6
            j = i0 + int(SR * ts)
            if j < len(efectos):
                efectos[j:j + len(snd)] += snd[:len(efectos) - j]
        t0 += d
    voz = CA.subir_tono(voz, salida)
    pista = voz + efectos
    pista[:int(SR * total)] += CA.musica_fiesta(total) * 0.3
    pista = pista[:int(SR * total)]
    pista /= max(1.0, np.abs(pista).max() / 0.95)
    wav = salida + ".wav"
    sf.write(wav, pista.astype(np.float32), SR)
    tareas = []
    for k, ((narr, e), d) in enumerate(zip(escenas, durs)):
        prev = escenas[k - 1][1] if k else None
        for fi in range(int(round(d * fps))):
            tareas.append((vid, narr, e, prev, fi / fps, d))
    ff = subprocess.Popen(["ffmpeg", "-loglevel", "error", "-y", "-f", "image2pipe", "-framerate", str(fps), "-i", "-", "-i", wav,
                           "-c:v", "libx264", "-preset", "medium", "-crf", "21", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                           "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-shortest", "-movflags", "+faststart", salida], stdin=subprocess.PIPE)
    with Pool(4) as pool:
        for png in pool.imap(_cuadro, tareas, chunksize=4):
            ff.stdin.write(png)
    ff.stdin.close()
    ff.wait()
    os.remove(wav)
    print(f"[{vid}] listo {salida}", flush=True)


def main():
    carpeta_tts, out = sys.argv[1], sys.argv[2]
    ids = sys.argv[3:] or list(VD.VIDEOS)
    os.makedirs(out, exist_ok=True)
    A.cargar_sfx()
    A.SFX.update(abrir=CA.sfx_abrir(), fizz=CA.sfx_fizz(), trago=CA.sfx_trago(), glup=CA.sfx_glup(), vibra=CA.sfx_vibra())
    for vid in ids:
        render(vid, carpeta_tts, os.path.join(out, f"{vid}.mp4"))


if __name__ == "__main__":
    main()
