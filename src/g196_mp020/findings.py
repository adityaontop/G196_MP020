from __future__ import annotations

from pathlib import Path
import yaml
import pandas as pd
from .data import detect_issues


def write_data_findings(train_path: str, holdout_path: str, later_path: str, output_path: str) -> dict:
    train = pd.read_csv(train_path)
    holdout = pd.read_csv(holdout_path)
    later = pd.read_csv(later_path)
    findings = detect_issues(train, holdout, later)
    template = {
        "group_id": "G196", "problem_id": "MP020", "data_issues": findings,
        "tracking": {"experiment_name": None, "best_run_id": None, "registered_model_name": None, "champion_version": None},
        "monitoring": {"psi": {c: None for c in ["highway_distance_km","nearby_pumps","price_rs","trucks_passing","temp_c","staff"]}, "most_drifted_feature": None, "mae_by_group": {"Highway": None,"City": None,"Industrial": None}, "worst_served_group": None, "mae_v1_on_check": None, "mae_v2_on_check": None, "decision": None},
    }
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(yaml.safe_dump(template, sort_keys=False), encoding="utf-8")
    return template

if __name__ == "__main__":
    write_data_findings("data/raw/train.csv", "data/raw/holdout_features.csv", "data/raw/later.csv", "reports/findings.yaml")
