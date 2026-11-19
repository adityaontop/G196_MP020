from __future__ import annotations

import argparse
from pathlib import Path
import mlflow
import mlflow.sklearn
import pandas as pd
from mlflow import MlflowClient

from g196_mp020.data import sha256_file
from g196_mp020.modeling import fit_evaluate, fit_all, save_model


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--train", default="data/raw/train.csv")
    ap.add_argument("--later", default="data/raw/later.csv")
    ap.add_argument("--db", default="sqlite:///mlflow.db")
    args = ap.parse_args()
    mlflow.set_tracking_uri(args.db)
    mlflow.set_experiment("MP020_Fuel_Station_Sales")
    train = pd.read_csv(args.train)
    data_hash = sha256_file(args.train)
    candidates = ["extra_trees", "random_forest", "gradient_boosting"]
    best = None
    for kind in candidates:
        with mlflow.start_run(run_name=f"v1_{kind}") as run:
            model, mae = fit_evaluate(train, kind)
            mlflow.log_param("model_type", kind)
            mlflow.log_param("data_sha256", data_hash)
            mlflow.log_metric("mae_validation", mae)
            mlflow.sklearn.log_model(model, "model", serialization_format="cloudpickle")
            if best is None or mae < best[0]:
                best = (mae, kind, run.info.run_id)
    assert best is not None
    best_model = fit_all(train, best[1])
    save_model(best_model, "models/v1_model.joblib")
    save_model(best_model, "models/model.joblib")
    model_name = "MP020_Fuel_Station_Model"
    client = MlflowClient()
    try:
        client.get_registered_model(model_name)
    except Exception:
        client.create_registered_model(model_name)
    with mlflow.start_run(run_name="v1_registration") as run:
        mlflow.log_param("model_type", best[1])
        mlflow.log_param("data_sha256", data_hash)
        mlflow.log_metric("mae_validation", best[0])
        result = mlflow.sklearn.log_model(best_model, "model", registered_model_name=model_name, serialization_format="cloudpickle")
        version = result.registered_model_version
        if version is None:
            versions = client.search_model_versions(f"name='{model_name}'")
            version = max(int(v.version) for v in versions)
        client.set_registered_model_alias(model_name, "champion", version)
    print({"best_kind": best[1], "best_mae": best[0], "best_run_id": best[2], "model_name": model_name, "champion_version": version})

if __name__ == "__main__":
    main()
