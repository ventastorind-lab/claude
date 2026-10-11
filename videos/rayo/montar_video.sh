#!/bin/bash
# Monta el video final: una toma por escena (zoom suave + fundido) con su narración.
# Uso: montar_video.sh <carpeta_png> <carpeta_voz> <salida.mp4>
set -e
PNG=$1; VOZ=$2; OUT=$3
TMP=$(mktemp -d)
FPS=30
for wav in "$VOZ"/escena_*.wav; do
  n=$(basename "$wav" .wav)
  d=$(python3 -c "import json,sys;print(json.load(open('$VOZ/duraciones.json'))[str(int('${n#escena_}'))])")
  frames=$(python3 -c "print(int($d*$FPS)+1)")
  fo=$(python3 -c "print(round($d-0.3,2))")
  i=${n#escena_}; i=$((10#$i))
  # alterna acercamiento y alejamiento para dar movimiento
  if (( i % 2 )); then Z="1+0.06*on/$frames"; else Z="1.06-0.06*on/$frames"; fi
  ffmpeg -loglevel error -y -loop 1 -i "$PNG/$n.png" -i "$wav" \
    -filter_complex "[0:v]scale=2880:-1,zoompan=z='$Z':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$frames:s=1920x1080:fps=$FPS,fade=t=in:st=0:d=0.3,fade=t=out:st=$fo:d=0.3,format=yuv420p[v]" \
    -map "[v]" -map 1:a -t "$d" -c:v libx264 -preset veryfast -crf 20 -c:a aac -b:a 160k -ar 44100 -ac 2 "$TMP/$n.mp4"
  echo "file '$TMP/$n.mp4'" >> "$TMP/lista.txt"
done
ffmpeg -loglevel error -y -f concat -safe 0 -i "$TMP/lista.txt" -c copy -movflags +faststart "$OUT"
rm -rf "$TMP"
