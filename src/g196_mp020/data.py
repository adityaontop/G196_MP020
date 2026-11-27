from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

TARGET = "litres_per_day"
LEAKING_COLUMN = "litres_from_tank_dip_next_day"
NUMERIC_FEATURES = [
    "highway_distance_km", "nearby_pumps", "price_rs", "trucks_passing", "temp_c", "staff"
]
CATEGORICAL_FEATURES = ["ownership", "zone"]
MODEL_FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES + ["month", "day_of_week", "day_of_year"]


def sha256_file(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# Map spelling/abbreviation variants onto the three canonical training categories.
def canonical_ownership(value: Any) -> str:
    text = str(value).strip().lower().replace(".", "").replace("_", " ")
    mapping = {
        "cooperative": "cooperative", "coo": "cooperative",
        "private": "private", "pri": "private",
        "public sector": "public_sector", "publicsector": "public_sector", "pub": "public_sector",
    }
    return mapping.get(text, text)


def clean_frame(frame: pd.DataFrame, *, has_target: bool = True) -> pd.DataFrame:
    """Clean the provided frame without changing the source CSV."""
    df = frame.copy()
    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    # Repair the known zone-specific unit mix-up before treating extreme prices as missing.
    # Industrial rows were recorded in paise-like 100x units; normalize only clear anomalies.
    industrial = df["zone"].astype(str).str.strip().str.lower().eq("industrial")
    df.loc[industrial & (df["price_rs"] > 500), "price_rs"] /= 100.0
    df.loc[df["price_rs"] >= 500, "price_rs"] = np.nan
    # The sentinel is not a valid observation; median imputation keeps the row usable.
    # The known sentinel is missing information, not a real price.
    df["price_rs"] = df["price_rs"].fillna(df["price_rs"].median())
    df["ownership"] = df["ownership"].map(canonical_ownership)
    df["zone"] = df["zone"].astype(str).str.strip().str.title()
    if has_target and TARGET in df:
        # Correct only the identified extra-zero scale errors in the target column.
        typo = df[TARGET] > 100000
        df.loc[typo, TARGET] = df.loc[typo, TARGET] / 10.0
    # Drop target and post-event tank-dip measurement to prevent label leakage.
    # Never expose post-event information to the model.
    feature = df.drop(columns=[LEAKING_COLUMN, TARGET], errors="ignore")
    if "date" in feature.columns:
        feature["month"] = feature["date"].dt.month
        feature["day_of_week"] = feature["date"].dt.dayofweek
        feature["day_of_year"] = feature["date"].dt.dayofyear
    else:
        # The serving contract has no date; these neutral values keep feature columns aligned.
        # The live API contract has no date field; use neutral defaults for date features.
        feature["month"] = 1
        feature["day_of_week"] = 0
        feature["day_of_year"] = 1
    return feature


def load_clean(path: str | Path, *, has_target: bool = True) -> pd.DataFrame:
    return clean_frame(pd.read_csv(path), has_target=has_target)


def detect_issues(train: pd.DataFrame, holdout: pd.DataFrame, later: pd.DataFrame) -> dict[str, Any]:
    """Return the seven findings in the exact shape needed by findings.yaml."""
    df = train.copy()
    df["date"] = pd.to_datetime(df["date"])
    ownership_levels = {canonical_ownership(x) for x in df["ownership"].unique()}
    raw_text_levels = set(df["ownership"].astype(str))
    variants_present = len(raw_text_levels) > len(ownership_levels)
    # Unit mix-up: Industrial price values are approximately 100x the clean groups.
    industrial = df.loc[df.zone.eq("Industrial"), "price_rs"]
    normal = df.loc[~df.zone.eq("Industrial"), "price_rs"]
    unit_present = bool(len(industrial) and industrial.median() > normal.median() * 50)
    # A run of five or more identical consecutive readings is flagged for investigation.
    # A stuck-sensor detector: exact repeated values in a contiguous run after date sorting.
    stuck = {"present": False, "column": None, "start_date": None, "end_date": None}
    ordered = df.sort_values("date").reset_index(drop=True)
    for col in NUMERIC_FEATURES:
        start = 0
        for i in range(1, len(ordered) + 1):
            if i == len(ordered) or ordered.loc[i, col] != ordered.loc[start, col]:
                if i - start >= 5:
                    stuck = {"present": True, "column": col, "start_date": ordered.loc[start, "date"].strftime("%Y-%m-%d"), "end_date": ordered.loc[i - 1, "date"].strftime("%Y-%m-%d")}
                    break
                start = i
        if stuck["present"]:
            break
    sentinel_mask = df["price_rs"].eq(9999)
    typo_mask = df[TARGET] / df[LEAKING_COLUMN].replace(0, np.nan) > 5
    return {
        "leaking_column": {"present": LEAKING_COLUMN in train.columns and LEAKING_COLUMN not in holdout.columns, "column": LEAKING_COLUMN if LEAKING_COLUMN in train.columns and LEAKING_COLUMN not in holdout.columns else None},
        "unit_mixup": {"present": unit_present, "column": "price_rs" if unit_present else None, "group_value": "Industrial" if unit_present else None, "factor": 100 if unit_present else None},
        "sentinel_value": {"present": bool(sentinel_mask.any()), "column": "price_rs" if sentinel_mask.any() else None, "value": 9999 if sentinel_mask.any() else None, "count": int(sentinel_mask.sum()) if sentinel_mask.any() else None},
        "duplicate_rows": {"present": bool(train.duplicated().sum()), "count": int(train.duplicated().sum()) if train.duplicated().sum() else None},
        "stuck_sensor": stuck,
        "target_typos": {"present": bool(typo_mask.sum()), "count": int(typo_mask.sum()) if typo_mask.sum() else None},
        "spelling_variants": {"present": variants_present, "column": "ownership" if variants_present else None, "true_levels": len(ownership_levels) if variants_present else None},
    }
