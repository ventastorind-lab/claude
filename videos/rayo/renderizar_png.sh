#!/bin/bash
# render.sh <svg_dir> <png_dir>
CH=/opt/pw-browsers/chromium-1194/chrome-linux/chrome
for f in "$1"/escena_*.svg; do
  n=$(basename "$f" .svg)
  printf '<html><head><meta charset="utf-8"></head><body style="margin:0;overflow:hidden">%s</body></html>' "$(cat "$f")" > "$2/$n.html"
  $CH --headless=new --no-sandbox --disable-gpu --hide-scrollbars --window-size=1920,1300 --screenshot="$2/$n.full.png" "file://$2/$n.html" >/dev/null 2>&1 &
  while [ $(jobs -r | wc -l) -ge 6 ]; do sleep 0.2; done
done
wait
python3 -c "
import glob
from PIL import Image
for p in sorted(glob.glob('$2/*.full.png')):
    Image.open(p).crop((0,0,1920,1080)).convert('RGB').save(p.replace('.full.png','.png'))
"
rm -f "$2"/*.full.png "$2"/*.html
ls "$2" | wc -l
