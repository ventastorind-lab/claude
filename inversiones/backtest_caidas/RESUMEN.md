# Backtest "compra tras caída de 20 %, vende cada lote a +30 %"

**Datos:** Yahoo Finance vía `yfinance` 1.8.0, cierres diarios ajustados por splits y dividendos (`auto_adjust=True`), del 3-ene-2022 al **12-nov-2026** (último cierre disponible). Stooq no respondió desde este entorno, así que no se usó.

## Universo (sin sesgo de supervivencia)
- Composición del S&P 500 al 3-ene-2022: versión archivada de Wikipedia "List of S&P 500 companies" (revisión 1062834329, 30-dic-2021, la última antes del 3-ene-2022; 505 símbolos).
- Capitalización al 3-ene-2022 = cierre real de ese día (Yahoo, desajustado de splits posteriores) × acciones en circulación reportadas por Yahoo en la fecha más cercana. Alphabet cuenta una sola vez (GOOGL).
- 42 empresas del índice de 2022 no tienen histórico en Yahoo (fusionadas o deslistadas: Activision, Twitter, Xilinx, Pioneer, Hess, Marsh & McLennan, etc.) y no pudieron rankearse. El corte del puesto 50 fue de USD 178.800 millones.
- El borde es estrecho: #50 Intuit (178,8 mil M) frente a #51 Morgan Stanley (177,5 mil M).

**Top 50 al 3-ene-2022:** AAPL, MSFT, GOOGL, AMZN, TSLA, FB (META), NVDA, BRK.B, V, JPM, UNH, JNJ, HD, WMT, PG, BAC, MA, PFE, DIS, AVGO, NFLX, XOM, CSCO, ADBE, NKE, LLY, ACN, KO, TMO, CRM, COST, ABT, PYPL, ABBV, PEP, ORCL, CMCSA, CVX, DHR, INTC, VZ, QCOM, WFC, MCD, MRK, UPS, AMD, T, NEE, INTU.

**Top 50 hoy (referencia, con sesgo de retrospectiva):** AAPL, NVDA, MSFT, GOOGL, AMZN, AVGO, META, TSLA, LLY, BRK.B, WMT, AMD, JPM, MU, V, XOM, JNJ, MA, ABBV, COST, CVX, KO, PLTR, CSCO, ORCL, PG, UNH, MRK, BAC, HD, GE, INTC, PM, AMAT, MS, LRCX, TXN, CAT, RTX, PANW, GS, ANET, TMO, WFC, NFLX, AMGN, LIN, DELL, CRWD, IBM.

## Resultados base (−20 % / +30 %)

| Métrica | Top 50 de 2022 | Top 50 de hoy |
|---|---|---|
| Compras / ventas / lotes abiertos | 339 / 226 / 113 | 361 / 290 / 71 |
| Capital total invertido (suma de compras) | USD 33.900 | USD 36.100 |
| Capital máximo neto necesario (las ventas financian compras) | USD 9.916 | USD 9.951 |
| Costo máximo de lotes abiertos al mismo tiempo | USD 11.400 | USD 10.300 |
| Ganancia realizada | USD 7.420 | USD 9.531 |
| Ganancia no realizada | −USD 958 | −USD 163 |
| Ganancia total | USD 6.462 | USD 9.368 |
| Rentabilidad sobre lo invertido / sobre el capital máximo | 19,1 % / 65,2 % | 26,0 % / 94,1 % |
| TIR anual (XIRR) | 20,4 % | 41,5 % |
| SPY con los mismos montos y fechas | +USD 18.645 (55,0 %), TIR 18,1 % | +USD 19.754 (54,7 %), TIR 18,2 % |
| USD 100 por acción el 3-ene-2022 y mantener | 5.000 → 8.529 (+70,6 %, 11,6 %/año) | 5.000 → 14.245 (+184,9 %, 24,0 %/año) |

SPY comprado el 3-ene-2022 y mantenido: +68,9 % (448,37 → 757,12).

## Sensibilidad (top 50 de 2022)

| Caída / venta | Compras | Capital máx. neto | Ganancia total | Rent. s/ invertido | TIR |
|---|---|---|---|---|---|
| 20 % / 30 % | 339 | 9.916 | 6.462 | 19,1 % | 20,4 % |
| 15 % / 20 % | 617 | 14.587 | 8.791 | 14,2 % | 20,2 % |
| 25 % / 30 % | 207 | 5.960 | 3.738 | 18,1 % | 22,3 % |
| 20 % / 40 % | 339 | 10.936 | 8.098 | 23,9 % | 21,2 % |

Mejores (2022): TSLA +690, AMD +564, NVDA +441, INTC +407, META +364.
Peores con operaciones (2022): NKE −422 (11 lotes atrapados), ADBE −50, CMCSA −6, MCD +4, PEP +14. JNJ y KO nunca dispararon una compra.
Lotes atrapados en pérdida (2022): NKE (10 lotes, −455, el peor −69 %), PYPL (7, −205), ADBE (6, −182), ORCL (5, −132), NFLX (5, −111), INTU (4, −109), INTC (3, −91), CMCSA, UPS, ACN, PFE, CRM, UNH y pérdidas menores en otras.

Archivos: `resultados/backtest_top50_2022.xlsx`, `resultados/backtest_top50_hoy.xlsx` (todas las operaciones, por acción, lotes abiertos, sensibilidad, universo, gráfica), `resultados/grafica_*.png`, `resultados/precios_yahoo_ajustados.csv`.
Código: `universo.py`, `universo_completar.py`, `backtest.py`.
