"""Rentabilidad real de ETFs indexados (mundo y regiones) en los últimos 10 años. Fuente: Yahoo Finance (yfinance),
cierres ajustados por dividendos y splits (rentabilidad total en USD)."""
import pandas as pd
import yfinance as yf

ETFS = {"VT": "Mundo (FTSE All-World)", "ACWI": "Mundo (MSCI ACWI)", "URTH": "Países desarrollados (MSCI World)",
        "SPY": "EE. UU. (S&P 500)", "QQQ": "EE. UU. tecnología (Nasdaq 100)", "VEA": "Desarrollados sin EE. UU.",
        "EZU": "Zona euro", "EWU": "Reino Unido", "EWJ": "Japón", "VWO": "Emergentes (FTSE)", "EEM": "Emergentes (MSCI)",
        "FXI": "China (grandes empresas)", "INDA": "India", "EWZ": "Brasil", "EWW": "México", "GXG": "Colombia", "ILF": "América Latina 40"}
FIN = pd.Timestamp.today().normalize()
INI = FIN - pd.DateOffset(years=10)
d = yf.download(list(ETFS), start=INI - pd.Timedelta(days=10), auto_adjust=True, progress=False)["Close"]
d.index = d.index.tz_localize(None)
filas = []
for t, nom in ETFS.items():
    s = d[t].dropna()
    s = s[s.index >= s.index[s.index.searchsorted(INI) - 1]] if len(s) else s
    if s.empty or s.index[0] > INI + pd.Timedelta(days=10):
        filas.append(dict(etf=t, indice=nom, nota="sin 10 años de datos en Yahoo"))
        continue
    anios = (s.index[-1] - s.index[0]).days / 365.25
    total = s.iloc[-1] / s.iloc[0] - 1
    dd = (s / s.cummax() - 1).min()
    # peor rentabilidad en cualquier ventana de 5 años dentro del periodo
    r5 = (s / s.shift(1260) - 1).dropna()
    filas.append(dict(etf=t, indice=nom, desde=s.index[0].date(), hasta=s.index[-1].date(), rent_total=total,
                      rent_anual=(1 + total) ** (1 / anios) - 1, caida_maxima=dd, peor_5_anios=r5.min() if len(r5) else None,
                      usd_10000_hoy=10000 * (1 + total)))
r = pd.DataFrame(filas).sort_values("rent_anual", ascending=False)
r.to_csv("rentabilidad_10_anios.csv", index=False)
pd.set_option("display.width", 220)
print(r.to_string(index=False, formatters={c: "{:.1%}".format for c in ("rent_total", "rent_anual", "caida_maxima", "peor_5_anios")} | {"usd_10000_hoy": "{:,.0f}".format}))
