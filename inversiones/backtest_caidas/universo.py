"""Universo del backtest: 50 mayores del S&P 500 por capitalización (al 3-ene-2022 y hoy).

Fuentes reales:
- Composición del S&P 500 al 3-ene-2022: versión archivada de Wikipedia "List of S&P 500 companies"
  (revisión 1062834329 del 30-dic-2021, la última antes del 3-ene-2022) → sp500_2022-01-03_wikipedia.csv.
- Composición actual: la misma página de Wikipedia hoy.
- Capitalización al 3-ene-2022: precio de cierre real de ese día (Yahoo, desajustado de splits con el
  historial de splits de Yahoo) × acciones en circulación reportadas por Yahoo (get_shares_full) más cercanas.
- Capitalización hoy: Yahoo fast_info.market_cap.
"""
import io
import json
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import yfinance as yf

FECHA = pd.Timestamp("2022-01-03")
URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"


def leer_wikipedia():
    req = urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0 (backtest de investigación)"})
    html = urllib.request.urlopen(req, timeout=60).read().decode()
    tablas = pd.read_html(io.StringIO(html))
    actual, cambios = tablas[0], tablas[1]
    return actual, cambios


def miembros_en(fecha, actual, cambios):
    miembros = set(actual["Symbol"].astype(str))
    nombres = dict(zip(actual["Symbol"], actual["Security"]))
    c = cambios.copy()
    c.columns = ["_".join([str(x) for x in col if "Unnamed" not in str(x)]).strip("_") if isinstance(col, tuple) else col for col in c.columns]
    col_fecha = [k for k in c.columns if k.lower().startswith("effective date") or k.lower() == "date"][0]
    col_add = [k for k in c.columns if "Added" in k and "Ticker" in k][0]
    col_rem = [k for k in c.columns if "Removed" in k and "Ticker" in k][0]
    col_rem_n = [k for k in c.columns if "Removed" in k and "Security" in k][0]
    c["_f"] = pd.to_datetime(c[col_fecha], errors="coerce")
    posteriores = c[c["_f"] > fecha].sort_values("_f", ascending=False)
    for _, r in posteriores.iterrows():
        a, q = r[col_add], r[col_rem]
        if isinstance(a, str) and a in miembros:
            miembros.discard(a)
        if isinstance(q, str) and q.strip():
            miembros.add(q)
            nombres.setdefault(q, r[col_rem_n])
    return sorted(miembros), nombres


def yahoo(t):
    return t.replace(".", "-")


def cap_2022(t):
    """Capitalización real al 3-ene-2022 o None si Yahoo no tiene los datos."""
    yt = yahoo(t)
    try:
        tk = yf.Ticker(yt)
        h = tk.history(start="2021-12-28", end="2022-01-05", auto_adjust=False, actions=True)
        if h.empty:
            return t, None, "sin precios"
        h.index = h.index.tz_localize(None)
        fila = h.loc[:FECHA].iloc[-1]
        cierre = float(fila["Close"])  # ajustado por splits posteriores
        sp = tk.splits
        sp.index = sp.index.tz_localize(None)
        factor = float(sp[sp.index > FECHA].prod()) if len(sp[sp.index > FECHA]) else 1.0
        cierre_real = cierre * factor
        acc = tk.get_shares_full(start="2021-09-01", end="2022-04-30")
        if acc is None or len(acc) == 0:
            return t, None, "sin acciones en circulación"
        acc.index = acc.index.tz_localize(None)
        acc = acc[~acc.index.duplicated(keep="last")]
        i = abs((acc.index - FECHA).days).argmin()
        n = float(acc.iloc[i])
        return t, cierre_real * n, f"cierre {cierre_real:.2f} × {n:,.0f} acc. ({acc.index[i].date()})"
    except Exception as e:  # noqa: BLE001
        return t, None, f"error: {e}"


# tickers que cambiaron de símbolo después de 2022 (Yahoo guarda la historia bajo el nuevo)
RENOMBRADOS = {"FB": "META", "ANTM": "ELV", "FISV": "FI", "PEAK": "DOC", "FLT": "CPAY", "ABC": "COR", "RE": "EG",
               "PKI": "RVTY", "BLL": "BALL", "WLTW": "WTW", "FBHS": "FBIN", "DISCA": "WBD", "TWTR": None}


def main():
    actual, _ = leer_wikipedia()
    w22 = pd.read_csv("sp500_2022-01-03_wikipedia.csv")
    nombres = dict(zip(w22["Symbol"], w22["Security"]))
    m22 = list(w22["Symbol"].astype(str))
    print("miembros al 3-ene-2022:", len(m22), flush=True)
    consulta = [RENOMBRADOS.get(t, t) or t for t in m22]
    res = []
    with ThreadPoolExecutor(6) as ex:
        for k, r in enumerate(ex.map(cap_2022, consulta)):
            res.append(r)
            if k % 100 == 0:
                print(k, flush=True)
    df = pd.DataFrame(res, columns=["ticker_yahoo", "cap_2022", "detalle"])
    df.insert(0, "ticker_2022", m22)
    df["empresa"] = df["ticker_2022"].map(nombres)
    df.to_csv("caps_2022_todas.csv", index=False)
    nombres_hoy = dict(zip(actual["Symbol"], actual["Security"]))
    hoy = []
    for t in actual["Symbol"]:
        try:
            hoy.append((t, float(yf.Ticker(yahoo(t)).fast_info["market_cap"])))
        except Exception:  # noqa: BLE001
            hoy.append((t, None))
    dh = pd.DataFrame(hoy, columns=["ticker", "cap_hoy"])
    dh["empresa"] = dh["ticker"].map(nombres_hoy)
    dh.to_csv("caps_hoy_todas.csv", index=False)
    print("listo")


if __name__ == "__main__":
    main()
