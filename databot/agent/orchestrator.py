from __future__ import annotations

from typing import Optional

import pandas as pd

from databot.ml.model import TrainedModel, train_regressor, predict_next_day
from databot.nlp.summarize import summarize_weather


def _last_n_days(df: pd.DataFrame, days: int = 7) -> pd.DataFrame:
    if df.empty:
        return df
    cutoff = df.index.max() - pd.Timedelta(days=days - 1)
    return df.loc[df.index >= cutoff]


def answer_question(question: str, df: pd.DataFrame, model: Optional[TrainedModel] = None) -> str:
    q = question.lower()

    if any(k in q for k in ["média", "media"]) and any(k in q for k in ["temperatura", "tavg", "tmax", "tmin"]):
        window = 7
        dfw = _last_n_days(df, window)
        if dfw.empty:
            return "Não há dados suficientes para calcular a média."
        tavg = dfw["tavg"].mean()
        return f"A temperatura média dos últimos {window} dias foi de {tavg:.1f}°C."

    if "precip" in q or "chuva" in q:
        window = 7
        dfw = _last_n_days(df, window)
        if dfw.empty:
            return "Não há dados suficientes para precipitação."
        precip = dfw["precip"].sum()
        return f"A precipitação acumulada nos últimos {window} dias foi de {precip:.1f} mm."

    if "previs" in q or "amanh" in q:
        mdl = model or train_regressor(df, target="tmax")
        pred = predict_next_day(df, mdl)
        return f"Previsão de temperatura máxima para o próximo dia: {pred:.1f}°C (MAE val ~ {mdl.mae_validation:.1f})."

    # fallback: resumo geral
    return summarize_weather(df)
