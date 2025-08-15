from __future__ import annotations

import datetime as dt

from databot.config import DEFAULT_LATITUDE, DEFAULT_LONGITUDE, DEFAULT_HISTORY_DAYS
from databot.data import fetch_weather_daily, enrich_daily
from databot.ml.model import train_regressor, predict_next_day
from databot.nlp.summarize import summarize_weather


def main() -> None:
    end = dt.date.today()
    start = end - dt.timedelta(days=DEFAULT_HISTORY_DAYS - 1)

    raw = fetch_weather_daily(DEFAULT_LATITUDE, DEFAULT_LONGITUDE, start, end)
    proc = enrich_daily(raw)

    print("Dados processados:\n", proc.tail())

    summary = summarize_weather(proc)
    print("\nResumo:\n", summary)

    model = train_regressor(proc, target="tmax")
    pred = predict_next_day(proc, model)
    print(f"\nPrevisão de Tmáx para D+1: {pred:.1f}°C (MAE val ~ {model.mae_validation:.1f})")


if __name__ == "__main__":
    main()
