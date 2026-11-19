# G196 MP020 — Fuel Station Daily Sales (Lucknow)

SCSE3040 MLOps mini project. Group **G196**, problem **MP020**.

Members:
- S24CSEU1447 — AdityaSaxena
- S24CSEU1453 — NamanGarg
- S24CSEU0953 — AYUSHAGUPTA

## Setup

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export PYTHONPATH="$PWD/src"
```

Keep the original CSV files unchanged. The project code reads them from `data/raw/`.

## Run data findings

```bash
PYTHONPATH=src python -m g196_mp020.findings
cat reports/findings.yaml
```

## Train v1 and create MLflow database

```bash
PYTHONPATH=src python src/train.py
mlflow ui --backend-store-uri sqlite:///mlflow.db --host 127.0.0.1 --port 5000
```

This makes three candidate runs, registers the selected model, and sets the `champion` alias.

## Monitor, retrain, and create holdout predictions

```bash
PYTHONPATH=src python src/monitor.py
cat artifacts/monitoring.json
head predictions/holdout_predictions.csv
```

Copy the verified values from the generated outputs into `reports/findings.yaml`.

## Test and run API

```bash
PYTHONPATH=src pytest -q
PYTHONPATH=src uvicorn app.main:app --reload --port 8000
curl http://127.0.0.1:8000/health
```

## Docker and Kubernetes

```bash
docker build -t mp020-api:1.0 .
docker run --rm -p 8000:8000 mp020-api:1.0
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

## DVC

After installing DVC, initialize and track the raw files. Do not commit the CSV files to GitHub:

```bash
dvc init
dvc add data/raw/train.csv data/raw/later.csv data/raw/holdout_features.csv
git add .dvc .dvcignore data/raw/*.dvc
git commit -m "Configure DVC data tracking"
```
