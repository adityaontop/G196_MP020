from __future__ import annotations

from pathlib import Path
import argparse
import json
import mlflow
import pandas as pd
from mlflow import MlflowClient
from sklearn.metrics import mean_absolute_error

from g196_mp020.data import clean_frame
from g196_mp020.modeling import fit_all, load_model, predict, save_model
from g196_mp020.monitoring import group_mae, psi_report


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", default="data/raw/train.csv")
    ap.add_argument("--later", default="data/raw/later.csv")
    ap.add_argument("--holdout", default="data/raw/holdout_features.csv")
    args = ap.parse_args()
    train = pd.read_csv(args.train); later = pd.read_csv(args.later); holdout = pd.read_csv(args.holdout)
    train_clean = clean_frame(train); later_clean = clean_frame(later)
    v1_path = "models/v1_model.joblib" if Path("models/v1_model.joblib").exists() else "models/model.joblib"
    v1 = load_model(v1_path)
    ordered = later.sort_values("date").reset_index(drop=True)
    cut = int(len(ordered) * 0.70)
    later_fit, check = ordered.iloc[:cut], ordered.iloc[cut:]
    v1_check = float(mean_absolute_error(check["litres_per_day"].where(check["litres_per_day"] <= 100000, check["litres_per_day"] / 10.0), predict(v1, check)))
    v2 = fit_all(pd.concat([train, later_fit], ignore_index=True))
    v2_check = float(mean_absolute_error(check["litres_per_day"].where(check["litres_per_day"] <= 100000, check["litres_per_day"] / 10.0), predict(v2, check)))
    decision = "promote" if v2_check <= 0.90 * v1_check else "keep"
    mlflow.set_tracking_uri("sqlite:///mlflow.db")
    mlflow.set_experiment("MP020_Fuel_Station_Sales")
    model_name = "MP020_Fuel_Station_Model"
    with mlflow.start_run(run_name="v2_retraining") as run:
        mlflow.log_param("model_type", "extra_trees")
        mlflow.log_param("retraining_fraction", 0.70)
        mlflow.log_metric("mae_check", v2_check)
        logged = mlflow.sklearn.log_model(v2, "model", registered_model_name=model_name, serialization_format="cloudpickle")
        client = MlflowClient()
        versions = client.search_model_versions(f"name='{model_name}'")
        v2_version = max(int(v.version) for v in versions)
        if decision == "promote":
            client.set_registered_model_alias(model_name, "champion", v2_version)
    champion = v2 if decision == "promote" else v1
    save_model(champion, "models/model.joblib")
    preds = pd.DataFrame({"record_id": holdout["record_id"], "prediction": predict(champion, holdout).clip(lower=0)})
    Path("predictions").mkdir(exist_ok=True)
    preds.to_csv("predictions/holdout_predictions.csv", index=False)
    result = {"psi": psi_report(train_clean, later_clean), "mae_by_group": group_mae(v1, later), "mae_v1_on_check": v1_check, "mae_v2_on_check": v2_check, "decision": decision, "v2_version": v2_version}
    result["most_drifted_feature"] = max(result["psi"], key=result["psi"].get)
    result["worst_served_group"] = max(result["mae_by_group"], key=result["mae_by_group"].get)
    Path("artifacts").mkdir(exist_ok=True)
    Path("artifacts/monitoring.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
