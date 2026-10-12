# Byron vs. 50 Coca-Colas — versión 2 (viaje dentro del cuerpo)

- `guion.py`: 37 escenas; 11 son "dentro del cuerpo": dientes, estómago, sangre, páncreas, reservas de azúcar, cerebro, corazón y venas, hígado, riñones y vejiga, intestino y colon, y un resumen.
- `anatomia.py`: órganos caricatura con carita que reaccionan, más la "BYRON CAM".
- `kie.py`: voz ElevenLabs vía KIE y clips imagen→video (Kling).
- `render.py`: arma el video con subtítulos estilo viral (palabra activa en amarillo).

## Cuando KIE esté habilitado (secreto de red Bearer para api.kie.ai, *.redpandaai.co y *.aiquickdraw.com; sesión nueva)

```bash
cd videos/cocacola_v2
python3 kie.py saldo
python3 kie.py muestras            # 4 voces de prueba en voz_muestras/
python3 kie.py voces --voz liam    # o will / charlie / antoni / <voice_id>
python3 kie.py clips               # 8 clips de 5 s
python3 render.py byron_cocacola_v2.mp4 24
```
