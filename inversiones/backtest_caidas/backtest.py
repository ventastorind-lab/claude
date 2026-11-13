"""Backtest: comprar USD 100 tras caídas de X% desde la referencia y vender cada lote a +Y%.

Datos: Yahoo Finance (yfinance), cierres diarios ajustados por splits y dividendos (auto_adjust=True).
Uso: python3 backtest.py   → genera resultados/*.xlsx, *.png y resumen.json
"""
import json
import os
from datetime import date

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import yfinance as yf  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
SALIDA = os.path.join(AQUI, "resultados")
INICIO = "2022-01-03"
MONTO = 100.0
ESCENARIOS = [(0.20, 0.30), (0.15, 0.20), (0.25, 0.30), (0.20, 0.40)]


def yahoo(t):
    return t.replace(".", "-")


def descargar(tickers):
    d = yf.download(sorted(set(tickers)), start=INICIO, auto_adjust=True, progress=False, threads=True)["Close"]
    d.index = pd.to_datetime(d.index).tz_localize(None)
    return d


# ---------------------------------------------------------------- motor
def simular(precios, ticker, caida, subida):
    """Aplica las reglas a una serie de cierres. Devuelve (operaciones, lotes_abiertos)."""
    serie = precios.dropna()
    ops, abiertos = [], []
    ref = None
    for fecha, p in serie.items():
        p = float(p)
        if ref is None:
            ref = p
            continue
        # 1) ventas: cada lote por separado a +subida sobre su compra
        vendidos = [l for l in abiertos if p >= l["precio"] * (1 + subida)]
        for l in vendidos:
            abiertos.remove(l)
            ops.append(dict(fecha=fecha, accion=ticker, tipo="VENTA", precio=p, acciones=l["acciones"], monto=l["acciones"] * p,
                            costo=MONTO, ganancia=l["acciones"] * p - MONTO, fecha_compra=l["fecha"], precio_compra=l["precio"]))
        if vendidos:
            ref = p                      # la referencia se reinicia en el precio de venta
        else:
            ref = max(ref, p)            # nuevos máximos actualizan la referencia
        # 2) compra: cierre ≥ caida% bajo la referencia
        if p <= ref * (1 - caida):
            lote = dict(fecha=fecha, precio=p, acciones=MONTO / p)
            abiertos.append(lote)
            ops.append(dict(fecha=fecha, accion=ticker, tipo="COMPRA", precio=p, acciones=lote["acciones"], monto=MONTO,
                            costo=MONTO, ganancia=np.nan, fecha_compra=fecha, precio_compra=p))
            ref = p                      # la nueva referencia es el precio de compra
    return ops, abiertos


def xirr(flujos):
    """flujos: lista (fecha, monto); negativo = sale dinero. Bisección sobre la tasa anual."""
    if not flujos:
        return np.nan
    t0 = min(f for f, _ in flujos)
    dias = np.array([(f - t0).days / 365.0 for f, _ in flujos])
    m = np.array([v for _, v in flujos])

    def vpn(r):
        return float(np.sum(m / (1 + r) ** dias))
    lo, hi = -0.99, 10.0
    if vpn(lo) * vpn(hi) > 0:
        return np.nan
    for _ in range(200):
        mid = (lo + hi) / 2
        if vpn(lo) * vpn(mid) <= 0:
            hi = mid
        else:
            lo = mid
    return (lo + hi) / 2


def correr(precios, universo, spy, caida, subida, detalle=True):
    fin = precios.index.max()
    todas, abiertos_todos, filas = [], [], []
    for t in universo:
        s = precios[yahoo(t)].loc[INICIO:]
        ops, abiertos = simular(s, t, caida, subida)
        ultimo = float(s.dropna().iloc[-1])
        fecha_ult = s.dropna().index[-1]
        comp = [o for o in ops if o["tipo"] == "COMPRA"]
        vent = [o for o in ops if o["tipo"] == "VENTA"]
        realizada = sum(o["ganancia"] for o in vent)
        valor_ab = sum(l["acciones"] * ultimo for l in abiertos)
        costo_ab = MONTO * len(abiertos)
        for l in abiertos:
            abiertos_todos.append(dict(accion=t, fecha_compra=l["fecha"], precio_compra=l["precio"], precio_hoy=ultimo,
                                       valor_hoy=l["acciones"] * ultimo, resultado=l["acciones"] * ultimo - MONTO,
                                       rend=ultimo / l["precio"] - 1))
        filas.append(dict(accion=t, compras=len(comp), ventas=len(vent), lotes_abiertos=len(abiertos), invertido=MONTO * len(comp),
                          ganancia_realizada=realizada, costo_lotes_abiertos=costo_ab, valor_lotes_abiertos=valor_ab,
                          ganancia_no_realizada=valor_ab - costo_ab, resultado_total=realizada + valor_ab - costo_ab,
                          ultimo_precio=ultimo, ultima_fecha=fecha_ult.date()))
        todas += ops
    ops = pd.DataFrame(todas).sort_values(["fecha", "accion", "tipo"]).reset_index(drop=True) if todas else pd.DataFrame()
    acc = pd.DataFrame(filas)
    lotes = pd.DataFrame(abiertos_todos)

    # ---- totales y curva diaria
    idx = precios.loc[INICIO:].index
    compras = ops[ops.tipo == "COMPRA"] if len(ops) else ops
    ventas = ops[ops.tipo == "VENTA"] if len(ops) else ops
    flujo_c = compras.groupby("fecha")["monto"].sum().reindex(idx, fill_value=0) if len(ops) else pd.Series(0, idx)
    flujo_v = ventas.groupby("fecha")["monto"].sum().reindex(idx, fill_value=0) if len(ops) else pd.Series(0, idx)
    # acciones en cartera por día
    pos = pd.DataFrame(0.0, index=idx, columns=[yahoo(t) for t in universo])
    for o in todas:
        signo = 1 if o["tipo"] == "COMPRA" else -1
        pos.loc[o["fecha"]:, yahoo(o["accion"])] += signo * o["acciones"]
    valor_abierto = (pos * precios.loc[idx, pos.columns].ffill()).sum(axis=1)
    inv_acum = flujo_c.cumsum()
    cobro_acum = flujo_v.cumsum()
    neto = inv_acum - cobro_acum                          # dinero propio neto (si las ventas financian compras)
    costo_abierto = pd.Series(0.0, index=idx)
    for o in todas:
        costo_abierto.loc[o["fecha"]:] += MONTO if o["tipo"] == "COMPRA" else -MONTO
    total_invertido = float(inv_acum.iloc[-1])
    realizada = float(acc.ganancia_realizada.sum())
    no_realizada = float(acc.ganancia_no_realizada.sum())
    valor_final = float(valor_abierto.iloc[-1] + cobro_acum.iloc[-1])
    flujos = [(f, -MONTO) for f in compras["fecha"]] + [(f, float(m)) for f, m in zip(ventas["fecha"], ventas["monto"])]
    flujos.append((fin, float(valor_abierto.iloc[-1])))
    tir = xirr(flujos) if total_invertido else np.nan

    # ---- comparación SPY: mismos montos, mismas fechas, mantener
    spy_s = spy.loc[INICIO:]
    unidades_spy = sum(MONTO / float(spy_s.loc[f]) for f in compras["fecha"])
    valor_spy = unidades_spy * float(spy_s.iloc[-1])
    tir_spy = xirr([(f, -MONTO) for f in compras["fecha"]] + [(fin, valor_spy)]) if total_invertido else np.nan
    curva_spy = pd.Series(0.0, index=idx)
    for f in compras["fecha"]:
        curva_spy.loc[f:] += MONTO / float(spy_s.loc[f])
    curva_spy = curva_spy * spy_s.reindex(idx).ffill()

    # ---- comprar y mantener USD 100 por acción desde el 3-ene-2022
    bh = []
    for t in universo:
        s = precios[yahoo(t)].loc[INICIO:].dropna()
        bh.append(dict(accion=t, valor_hoy=MONTO * float(s.iloc[-1]) / float(s.iloc[0])))
    bh = pd.DataFrame(bh)
    anios = (fin - pd.Timestamp(INICIO)).days / 365.0
    bh_total = float(bh.valor_hoy.sum())
    bh_inv = MONTO * len(universo)

    res = dict(caida=caida, subida=subida, fecha_final=str(fin.date()), compras=int(len(compras)), ventas=int(len(ventas)),
               lotes_abiertos=int(acc.lotes_abiertos.sum()), capital_total_invertido=total_invertido,
               capital_max_neto=float(neto.max()) if len(neto) else 0.0,
               capital_max_lotes_abiertos=float(costo_abierto.max()),
               ganancia_realizada=realizada, ganancia_no_realizada=no_realizada,
               valor_lotes_abiertos=float(valor_abierto.iloc[-1]), cobrado_por_ventas=float(cobro_acum.iloc[-1]),
               valor_total_hoy=valor_final, ganancia_total=realizada + no_realizada,
               rentabilidad_total=(realizada + no_realizada) / total_invertido if total_invertido else np.nan,
               rentabilidad_sobre_capital_max=(realizada + no_realizada) / float(neto.max()) if total_invertido else np.nan,
               tir_anual=tir, spy_valor_hoy=valor_spy, spy_ganancia=valor_spy - total_invertido,
               spy_rentabilidad=valor_spy / total_invertido - 1 if total_invertido else np.nan, spy_tir=tir_spy,
               bh_invertido=bh_inv, bh_valor_hoy=bh_total, bh_rentabilidad=bh_total / bh_inv - 1,
               bh_anualizada=(bh_total / bh_inv) ** (1 / anios) - 1)
    curvas = pd.DataFrame(dict(invertido_acumulado=inv_acum, valor_portafolio=valor_abierto + cobro_acum,
                               valor_lotes_abiertos=valor_abierto, cobrado_acumulado=cobro_acum, capital_neto=neto,
                               costo_lotes_abiertos=costo_abierto, valor_spy_mismos_flujos=curva_spy))
    return res, ops, acc, lotes, curvas, bh


# ---------------------------------------------------------------- salida
def grafica(curvas, titulo, ruta):
    fig, ax = plt.subplots(figsize=(12, 6.5))
    ax.plot(curvas.index, curvas.invertido_acumulado, label="Capital invertido acumulado (suma de compras)", color="#555555", lw=2)
    ax.plot(curvas.index, curvas.valor_portafolio, label="Valor de la estrategia (lotes abiertos + dinero cobrado en ventas)", color="#1565C0", lw=2.2)
    ax.plot(curvas.index, curvas.valor_spy_mismos_flujos, label="Mismos montos y fechas en SPY", color="#E65100", lw=1.8, ls="--")
    ax.plot(curvas.index, curvas.capital_neto, label="Dinero propio neto comprometido", color="#2E7D32", lw=1.3, ls=":")
    ax.set_title(titulo, fontsize=13, weight="bold")
    ax.set_ylabel("USD")
    ax.grid(alpha=0.3)
    ax.legend(loc="upper left", fontsize=9)
    fig.tight_layout()
    fig.savefig(ruta, dpi=140)
    plt.close(fig)


def excel(ruta, nombre, res, ops, acc, lotes, bh, sens, universo_df, png):
    with pd.ExcelWriter(ruta, engine="openpyxl") as xw:
        resumen = pd.DataFrame([(k, v) for k, v in res.items()], columns=["métrica", "valor"])
        resumen.to_excel(xw, sheet_name="Resumen", index=False)
        o = ops.copy()
        o["fecha"] = o["fecha"].dt.date
        o["fecha_compra"] = pd.to_datetime(o["fecha_compra"]).dt.date
        o.rename(columns=dict(fecha="Fecha", accion="Acción", tipo="Compra/Venta", precio="Precio", acciones="Acciones (fracción)",
                              monto="Monto USD", costo="Costo del lote", ganancia="Ganancia realizada", fecha_compra="Fecha de compra del lote",
                              precio_compra="Precio de compra del lote")).to_excel(xw, sheet_name="Operaciones", index=False)
        acc.sort_values("resultado_total", ascending=False).to_excel(xw, sheet_name="Por acción", index=False)
        if len(lotes):
            l = lotes.copy()
            l["fecha_compra"] = pd.to_datetime(l["fecha_compra"]).dt.date
            l.sort_values("rend").to_excel(xw, sheet_name="Lotes abiertos", index=False)
        bh.to_excel(xw, sheet_name="Comprar y mantener", index=False)
        sens.to_excel(xw, sheet_name="Sensibilidad", index=False)
        universo_df.to_excel(xw, sheet_name="Universo", index=False)
    from openpyxl import load_workbook
    from openpyxl.drawing.image import Image
    wb = load_workbook(ruta)
    ws = wb.create_sheet("Gráfica")
    ws.add_image(Image(png), "A1")
    for hoja in wb.worksheets:
        for col in hoja.columns:
            ancho = max(len(str(c.value)) if c.value is not None else 0 for c in col[:200])
            hoja.column_dimensions[col[0].column_letter].width = min(42, max(10, ancho + 2))
    wb.save(ruta)


def main():
    os.makedirs(SALIDA, exist_ok=True)
    u22 = pd.read_csv(os.path.join(AQUI, "top50_2022.csv"))
    uhoy = pd.read_csv(os.path.join(AQUI, "top50_hoy.csv"))
    universos = {"top50_2022": (list(u22.ticker_yahoo), u22[["rank", "ticker_2022", "ticker_yahoo", "empresa", "cap_2022", "detalle"]]),
                 "top50_hoy": (list(uhoy.ticker), uhoy)}
    todos = sorted({yahoo(t) for lst, _ in universos.values() for t in lst} | {"SPY"})
    precios = descargar(todos)
    precios.to_csv(os.path.join(SALIDA, "precios_yahoo_ajustados.csv"))
    faltan = [t for t in todos if t not in precios.columns or precios[t].loc[INICIO:].dropna().empty]
    if faltan:
        raise SystemExit(f"Yahoo no devolvió precios para: {faltan}. Me detengo.")
    spy = precios["SPY"]
    resumen = {"fuente": "Yahoo Finance vía yfinance " + yf.__version__ + " (auto_adjust=True)",
               "descargado": str(date.today()), "primer_cierre": str(precios.index.min().date()), "ultimo_cierre": str(precios.index.max().date())}
    for nombre, (lst, udf) in universos.items():
        sens = []
        for caida, subida in ESCENARIOS:
            r, *_ = correr(precios, lst, spy, caida, subida)
            sens.append({k: r[k] for k in ("caida", "subida", "compras", "ventas", "lotes_abiertos", "capital_total_invertido", "capital_max_neto",
                                         "ganancia_realizada", "ganancia_no_realizada", "ganancia_total", "rentabilidad_total", "tir_anual",
                                         "spy_rentabilidad", "spy_tir")})
        sens = pd.DataFrame(sens)
        res, ops, acc, lotes, curvas, bh = correr(precios, lst, spy, 0.20, 0.30)
        png = os.path.join(SALIDA, f"grafica_{nombre}.png")
        grafica(curvas, f"Estrategia -20% / +30% · universo {nombre.replace('_', ' ')} · Yahoo Finance", png)
        curvas.to_csv(os.path.join(SALIDA, f"curvas_{nombre}.csv"))
        excel(os.path.join(SALIDA, f"backtest_{nombre}.xlsx"), nombre, res, ops, acc, lotes, bh, sens, udf, png)
        resumen[nombre] = dict(base=res, sensibilidad=sens.to_dict("records"),
                               mejores=acc.nlargest(5, "resultado_total")[["accion", "resultado_total", "compras", "ventas", "lotes_abiertos"]].to_dict("records"),
                               peores=acc[acc.compras > 0].nsmallest(5, "resultado_total")[["accion", "resultado_total", "compras", "ventas", "lotes_abiertos"]].to_dict("records"),
                               atrapadas=(lotes[lotes.resultado < 0].groupby("accion").agg(lotes=("resultado", "size"), perdida=("resultado", "sum"),
                                          peor_rend=("rend", "min")).sort_values("perdida").reset_index().to_dict("records") if len(lotes) else []),
                               por_accion=acc.to_dict("records"))
    with open(os.path.join(SALIDA, "resumen.json"), "w") as fh:
        json.dump(resumen, fh, indent=1, default=str, ensure_ascii=False)
    print(json.dumps({k: (v if k in ("fuente", "ultimo_cierre") else None) for k, v in resumen.items()}, indent=0, default=str))


if __name__ == "__main__":
    main()
