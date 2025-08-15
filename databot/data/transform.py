from __future__ import annotations

import pandas as pd

from databot.utils.logging import setup_logging

logger = setup_logging(name="databot.transform")

REQUIRED_COLUMNS = ["date", "tmax", "tmin", "precip"]


def _validate_input(df: pd.DataFrame) -> None:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Colunas ausentes no DataFrame: {missing}")


def enrich_daily(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica limpezas simples e cria features derivadas.

    - Converte date para datetime
    - Cria tavg (média diária)
    - Cria range_temp (amplitude)
    - Cria médias móveis de 7 e 14 dias para tavg
    - Ordena por date e remove duplicatas
    """
    _validate_input(df)

    df_proc = df.copy()
    df_proc["date"] = pd.to_datetime(df_proc["date"])  # date -> Timestamp

    df_proc = df_proc.sort_values("date").drop_duplicates(subset=["date"])  # ordena

    # Conversões numéricas robustas
    for c in ["tmax", "tmin", "precip"]:
        df_proc[c] = pd.to_numeric(df_proc[c], errors="coerce")

    # Features
    df_proc["tavg"] = (df_proc["tmax"] + df_proc["tmin"]) / 2.0
    df_proc["range_temp"] = df_proc["tmax"] - df_proc["tmin"]
    df_proc["tavg_ma7"] = df_proc["tavg"].rolling(window=7, min_periods=1).mean()
    df_proc["tavg_ma14"] = df_proc["tavg"].rolling(window=14, min_periods=1).mean()

    # Índice temporal opcional
    df_proc = df_proc.set_index("date")

    logger.info(
        f"Dados processados: {len(df_proc)} linhas, colunas: {list(df_proc.columns)}"
    )
    return df_proc
