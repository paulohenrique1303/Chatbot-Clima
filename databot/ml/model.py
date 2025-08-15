from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_absolute_error

from databot.utils.logging import setup_logging

logger = setup_logging(name="databot.ml")


@dataclass
class TrainedModel:
    pipeline: Pipeline
    feature_names: List[str]
    target: str
    mae_validation: float


def _build_supervised_frame(df: pd.DataFrame, target: str = "tmax") -> Tuple[pd.DataFrame, pd.Series]:
    if target not in df.columns:
        raise ValueError(f"Target {target} não existe no DataFrame")

    # Lags de 1 dia
    supervised = df.copy()
    for col in ["tmax", "tmin", "tavg", "precip", "tavg_ma7", "tavg_ma14"]:
        if col in supervised.columns:
            supervised[f"{col}_lag1"] = supervised[col].shift(1)

    supervised = supervised.dropna()

    feature_cols = [c for c in supervised.columns if c != target]
    X = supervised[feature_cols]
    y = supervised[target]
    return X, y


def train_regressor(df: pd.DataFrame, target: str = "tmax") -> TrainedModel:
    X, y = _build_supervised_frame(df, target)

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("rf", RandomForestRegressor(n_estimators=200, random_state=42)),
        ]
    )

    model.fit(X_train, y_train)
    preds = model.predict(X_val)
    mae = float(mean_absolute_error(y_val, preds))

    logger.info(f"Modelo {target} MAE validação: {mae:.3f}")

    return TrainedModel(
        pipeline=model,
        feature_names=list(X.columns),
        target=target,
        mae_validation=mae,
    )


def predict_next_day(df: pd.DataFrame, trained: TrainedModel) -> float:
    """Gera previsão 1 dia à frente usando a última linha disponível."""
    last = df.iloc[[-1]].copy()

    # Gerar linha de features para D+1 com base na última observação (lag1)
    feature_values = {}
    base_cols = ["tmax", "tmin", "tavg", "precip", "tavg_ma7", "tavg_ma14"]
    for col in base_cols:
        if col in df.columns:
            feature_values[f"{col}_lag1"] = float(last[col].iloc[0])

    # Ordenar conforme feature_names do pipeline
    X_next = pd.DataFrame([{k: feature_values.get(k, np.nan) for k in trained.feature_names}])

    # Imputer do pipeline cuidará de NaN
    y_pred = float(trained.pipeline.predict(X_next)[0])
    return y_pred
