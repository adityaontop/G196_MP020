from __future__ import annotations

from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import ExtraTreesRegressor, RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

from .data import CATEGORICAL_FEATURES, MODEL_FEATURES, NUMERIC_FEATURES, TARGET, clean_frame


def make_pipeline(kind: str = "extra_trees", random_state: int = 42, n_estimators: int = 300, max_depth: int | None = 12) -> Pipeline:
    prep = ColumnTransformer([
        ("num", "passthrough", NUMERIC_FEATURES + ["month", "day_of_week", "day_of_year"]),
        ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
    ])
    if kind == "random_forest":
        model = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state, n_jobs=-1)
    elif kind == "gradient_boosting":
        model = GradientBoostingRegressor(n_estimators=min(n_estimators, 300), max_depth=4 if max_depth is None else min(max_depth, 8), random_state=random_state, loss="huber")
    else:
        model = ExtraTreesRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=random_state, n_jobs=-1)
    return Pipeline([("preprocess", prep), ("model", model)])


def prepare_xy(raw: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    cleaned = clean_frame(raw, has_target=True)
    return cleaned[MODEL_FEATURES], raw[TARGET].astype(float).where(raw[TARGET] <= 100000, raw[TARGET] / 10.0)


def fit_evaluate(raw: pd.DataFrame, kind: str, random_state: int = 42) -> tuple[Pipeline, float]:
    X, y = prepare_xy(raw)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=random_state)
    pipe = make_pipeline(kind=kind, random_state=random_state)
    pipe.fit(X_train, y_train)
    return pipe, mean_absolute_error(y_test, pipe.predict(X_test))


def fit_all(raw: pd.DataFrame, kind: str = "extra_trees", random_state: int = 42) -> Pipeline:
    X, y = prepare_xy(raw)
    pipe = make_pipeline(kind=kind, random_state=random_state)
    pipe.fit(X, y)
    return pipe


def predict(pipe: Pipeline, raw_features: pd.DataFrame) -> pd.Series:
    X = clean_frame(raw_features, has_target=False)[MODEL_FEATURES]
    return pd.Series(pipe.predict(X), index=raw_features.index, name="prediction")


def save_model(pipe: Pipeline, path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(pipe, path)


def load_model(path: str | Path) -> Pipeline:
    return joblib.load(path)
