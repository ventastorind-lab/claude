"""¿Cuánto daría invertir COP 500.000 cada mes en SPY durante 10 años? Simulación con datos reales de Yahoo Finance:
SPY ajustado por dividendos (reinvertidos) y la tasa de cambio USD/COP (COP=X) de cada fecha de compra."""
import pandas as pd
import yfinance as yf

APORTE = 500_000
FIN = pd.Timestamp.today().normalize()
INI = FIN - pd.DateOffset(years=10)
d = yf.download(["SPY", "COP=X"], start=INI - pd.Timedelta(days=10), auto_adjust=True, progress=False)["Close"]
d.index = d.index.tz_localize(None)
d = d.ffill().dropna()
d = d[d.index >= INI]
fechas = d.groupby([d.index.year, d.index.month]).head(1).index[:120]   # primer día hábil de cada mes, 120 meses
unidades, filas = 0.0, []
for f in fechas:
    usd = APORTE / d.loc[f, "COP=X"]
    unidades += usd / d.loc[f, "SPY"]
    filas.append(dict(fecha=f.date(), trm=d.loc[f, "COP=X"], spy=d.loc[f, "SPY"], usd=usd, unidades_acum=unidades,
                      valor_cop=unidades * d.loc[f, "SPY"] * d.loc[f, "COP=X"], aportado=APORTE * len(filas) + APORTE))
hoy = d.index[-1]
valor_usd = unidades * d.loc[hoy, "SPY"]
valor_cop = valor_usd * d.loc[hoy, "COP=X"]
aportado = APORTE * len(fechas)
# TIR mensual en pesos
import numpy as np
flujos = [(f, -APORTE) for f in fechas] + [(hoy, valor_cop)]
t0 = fechas[0]
def vpn(r): return sum(m / (1 + r) ** ((f - t0).days / 365.25) for f, m in flujos)
lo, hi = -0.9, 2.0
for _ in range(200):
    mid = (lo + hi) / 2
    lo, hi = (lo, mid) if vpn(lo) * vpn(mid) <= 0 else (mid, hi)
pd.DataFrame(filas).to_csv("aportes_mensuales.csv", index=False)
print(f"meses: {len(fechas)} ({fechas[0].date()} a {fechas[-1].date()}), valorado al {hoy.date()}")
print(f"aportado: COP {aportado:,.0f}")
print(f"valor hoy: USD {valor_usd:,.0f} = COP {valor_cop:,.0f}  (TRM hoy {d.loc[hoy,'COP=X']:,.0f}; TRM inicio {d.loc[fechas[0],'COP=X']:,.0f})")
print(f"ganancia: COP {valor_cop-aportado:,.0f}  ({valor_cop/aportado-1:.1%}); TIR anual en pesos {lo:.2%}")
# peor momento del camino
v = pd.DataFrame(filas).set_index("fecha")
v["gan"] = v.valor_cop / v.aportado - 1
print("peor momento (fin de mes de compra):", v.gan.idxmin(), f"{v.gan.min():.1%}")
