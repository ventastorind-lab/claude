"""Segunda pasada: reintenta (en serie) las empresas sin dato y usa el balance anual de Yahoo
('Ordinary Shares Number') como respaldo para las acciones en circulación."""
import time

import pandas as pd
import yfinance as yf

import universo as U

FECHA = U.FECHA


def acciones_balance(tk):
    for freq in ("yearly", "quarterly"):
        try:
            b = tk.get_balance_sheet(freq=freq)
        except Exception:  # noqa: BLE001
            continue
        if b is None or b.empty or "OrdinarySharesNumber" not in b.index:
            continue
        s = b.loc["OrdinarySharesNumber"].dropna()
        s.index = pd.to_datetime(s.index)
        if len(s):
            i = abs((s.index - FECHA).days).argmin()
            return float(s.iloc[i]), s.index[i]
    return None, None


def reintentar(t):
    yt = U.yahoo(t)
    tk = yf.Ticker(yt)
    h = tk.history(start="2021-12-28", end="2022-01-05", auto_adjust=False)
    if h.empty:
        return None, "sin precios (Yahoo no tiene el histórico)"
    h.index = h.index.tz_localize(None)
    cierre = float(h.loc[:FECHA]["Close"].iloc[-1])
    sp = tk.splits
    sp.index = sp.index.tz_localize(None)
    post = sp[sp.index > FECHA]
    factor = float(post.prod()) if len(post) else 1.0
    acc = None
    try:
        acc = tk.get_shares_full(start="2021-06-01", end="2022-07-31")
    except Exception:  # noqa: BLE001
        pass
    if acc is not None and len(acc):
        acc.index = acc.index.tz_localize(None)
        i = abs((acc.index - FECHA).days).argmin()
        n, fecha_n, fuente = float(acc.iloc[i]), acc.index[i], "get_shares_full"
        return cierre * factor * n, f"cierre {cierre * factor:.2f} × {n:,.0f} acc. ({fecha_n.date()}, {fuente})"
    n, fecha_n = acciones_balance(tk)
    if n is None:
        return None, "sin acciones en circulación"
    # el balance de Yahoo viene expresado en acciones ajustadas por splits: se usa con el precio ajustado
    return cierre * n, f"cierre ajustado {cierre:.2f} × {n:,.0f} acc. ajustadas (balance {fecha_n.date()})"


d = pd.read_csv("caps_2022_todas.csv")
for i, r in d[d.cap_2022.isna()].iterrows():
    for intento in range(3):
        try:
            cap, det = reintentar(r.ticker_yahoo)
            break
        except Exception as e:  # noqa: BLE001
            cap, det = None, f"error {e}"
            time.sleep(3)
    d.loc[i, "cap_2022"], d.loc[i, "detalle"] = cap, det
    print(r.ticker_2022, r.ticker_yahoo, None if cap is None else round(cap / 1e9, 1), det, flush=True)
    time.sleep(0.8)
d.to_csv("caps_2022_todas.csv", index=False)
