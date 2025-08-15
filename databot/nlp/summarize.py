from __future__ import annotations

import pandas as pd


def summarize_weather(df: pd.DataFrame) -> str:
    """Gera um resumo textual simples do período disponível no DataFrame.

    Espera índice temporal em "date" (Timestamp) e colunas tmax, tmin, tavg, precip.
    """
    if df.empty:
        return "Sem dados para resumir."

    start = df.index.min().date()
    end = df.index.max().date()

    tmax_mean = df["tmax"].mean()
    tmin_mean = df["tmin"].mean()
    tavg_mean = df["tavg"].mean()
    precip_total = df["precip"].sum()

    text = (
        f"Período analisado: {start} a {end}. "
        f"Temperatura média: {tavg_mean:.1f}°C (máx média {tmax_mean:.1f}°C, mín média {tmin_mean:.1f}°C). "
        f"Precipitação total: {precip_total:.1f} mm."
    )
    return text
