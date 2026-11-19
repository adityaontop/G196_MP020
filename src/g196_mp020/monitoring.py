from __future__ import annotations

import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error

from .data import NUMERIC_FEATURES
from .modeling import predict


def psi(reference: pd.Series, current: pd.Series, bins: int = 10) -> float:
    ref = pd.to_numeric(reference, errors="coerce").dropna().to_numpy()
    cur = pd.to_numeric(current, errors="coerce").dropna().to_numpy()
    edges = np.unique(np.quantile(ref, np.linspace(0, 1, bins + 1)))
    if len(edges) < 2:
        return 0.0
    edges[0] = -np.inf
    edges[-1] = np.inf
    ref_counts = np.histogram(ref, bins=edges)[0].astype(float)
    cur_counts = np.histogram(cur, bins=edges)[0].astype(float)
    ref_pct = np.clip(ref_counts / max(ref_counts.sum(), 1), 1e-6, None)
    cur_pct = np.clip(cur_counts / max(cur_counts.sum(), 1), 1e-6, None)
    return float(np.sum((cur_pct - ref_pct) * np.log(cur_pct / ref_pct)))


def psi_report(train_clean: pd.DataFrame, later_clean: pd.DataFrame, bins: int = 10) -> dict[str, float]:
    return {col: psi(train_clean[col], later_clean[col], bins=bins) for col in NUMERIC_FEATURES}


def group_mae(model, later_raw: pd.DataFrame) -> dict[str, float]:
    preds = predict(model, later_raw)
    actual = later_raw["litres_per_day"].astype(float).where(later_raw["litres_per_day"] <= 100000, later_raw["litres_per_day"] / 10.0)
    groups = later_raw["zone"].astype(str).str.strip().str.title()
    return {str(group): float(mean_absolute_error(actual[groups == group], preds[groups == group])) for group in sorted(groups.unique())}
