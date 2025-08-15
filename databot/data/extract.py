from __future__ import annotations

import datetime as dt
from typing import Dict, Any

import pandas as pd
import requests

from databot.config import OPEN_METEO_BASE_URL, DEFAULT_TIMEZONE
from databot.utils.logging import setup_logging

logger = setup_logging(name="databot.extract")


def _format_date(value: dt.date | str) -> str:
    if isinstance(value, dt.date):
        return value.strftime("%Y-%m-%d")
    return str(value)


def fetch_weather_daily(
    latitude: float,
    longitude: float,
    start_date: dt.date | str,
    end_date: dt.date | str,
    timezone: str = DEFAULT_TIMEZONE,
) -> pd.DataFrame:
    """Busca dados diários de clima na API Open-Meteo (sem necessidade de chave).

    Coleta: temperatura máxima, mínima e precipitação diária.
    Retorna um DataFrame com colunas: date, tmax, tmin, precip.
    """
    params: Dict[str, Any] = {
        "latitude": latitude,
        "longitude": longitude,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
        "timezone": timezone,
        "start_date": _format_date(start_date),
        "end_date": _format_date(end_date),
    }
    logger.info(
        f"Coletando clima diário em {latitude:.4f},{longitude:.4f} de {params['start_date']} até {params['end_date']}"
    )
    response = requests.get(OPEN_METEO_BASE_URL, params=params, timeout=30)
    response.raise_for_status()
    payload = response.json()

    if "daily" not in payload:
        raise ValueError("Resposta da API sem bloco 'daily'")

    daily = payload["daily"]
    df = pd.DataFrame(
        {
            "date": pd.to_datetime(daily["time"]).date,
            "tmax": daily.get("temperature_2m_max"),
            "tmin": daily.get("temperature_2m_min"),
            "precip": daily.get("precipitation_sum"),
        }
    )
    return df
