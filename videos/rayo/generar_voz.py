"""Genera un WAV por escena con voz neuronal (Piper es_MX vía sherpa-onnx).

Uso: python3 generar_voz.py <guion.json> <carpeta_modelo> <carpeta_salida>
"""
import json, os, sys
import numpy as np
import sherpa_onnx
import soundfile as sf

guion, modelo, out = sys.argv[1:4]
os.makedirs(out, exist_ok=True)
nombre = [f for f in os.listdir(modelo) if f.endswith(".onnx")][0]
cfg = sherpa_onnx.OfflineTtsConfig(model=sherpa_onnx.OfflineTtsModelConfig(
    vits=sherpa_onnx.OfflineTtsVitsModelConfig(model=os.path.join(modelo, nombre), tokens=os.path.join(modelo, "tokens.txt"),
                                               data_dir=os.path.join(modelo, "espeak-ng-data")), num_threads=4))
tts = sherpa_onnx.OfflineTts(cfg)
duraciones = {}
for e in json.load(open(guion, encoding="utf-8")):
    a = tts.generate(e["narracion"], sid=0, speed=0.92)
    sr = a.sample_rate
    pausa = np.zeros(int(sr * 0.35), dtype=np.float32)
    audio = np.concatenate([pausa, np.array(a.samples, dtype=np.float32), pausa, pausa])
    sf.write(os.path.join(out, f"escena_{e['n']:02d}.wav"), audio, sr)
    duraciones[e["n"]] = round(len(audio) / sr, 3)
json.dump(duraciones, open(os.path.join(out, "duraciones.json"), "w"), indent=1)
print("total", round(sum(duraciones.values()), 1), "s")
