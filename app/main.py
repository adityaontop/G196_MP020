from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Literal

import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

from g196_mp020.modeling import load_model, predict

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({"level": record.levelname, "event": record.getMessage()})

logger = logging.getLogger("mp020")
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
handler.setFormatter(JsonFormatter())
logger.handlers.clear(); logger.addHandler(handler)

class PredictionRequest(BaseModel):
    highway_distance_km: float = Field(..., le=25)
    nearby_pumps: int
    price_rs: float
    trucks_passing: int = Field(..., ge=0)
    temp_c: float
    staff: int
    ownership: Literal["public_sector", "private", "cooperative"]
    zone: Literal["Highway", "City", "Industrial"]

class PredictionResponse(BaseModel):
    prediction: float

app = FastAPI(title="MP020 Fuel Station Sales API", version="1.0")
MODEL_PATH = Path("models/model.joblib")
model = load_model(MODEL_PATH) if MODEL_PATH.exists() else None

@app.get("/health")
def health() -> dict:
    return {"status": "ok", "model_loaded": model is not None}

@app.post("/predict", response_model=PredictionResponse)
def predict_endpoint(request: PredictionRequest) -> PredictionResponse:
    global model
    if model is None:
        model = load_model(MODEL_PATH)
    frame = pd.DataFrame([request.model_dump()])
    value = float(predict(model, frame).iloc[0])
    logger.info("prediction_generated")
    return PredictionResponse(prediction=max(0.0, value))
