import pandas as pd
from fastapi.testclient import TestClient

from app.main import app
from g196_mp020.data import canonical_ownership, clean_frame, detect_issues


def sample_frame():
    return pd.DataFrame({
        "record_id": ["R1", "R2", "R3"], "date": ["2026-01-01"] * 3,
        "highway_distance_km": [5.0, 6.0, 7.0], "nearby_pumps": [2, 3, 4],
        "price_rs": [100.0, 101.0, 102.0], "trucks_passing": [100, 200, 300],
        "temp_c": [20.0, 21.0, 22.0], "staff": [5, 6, 7],
        "ownership": [" private ", "coo.", "PUBLIC_SECTOR"], "zone": ["City", "Highway", "Industrial"],
        "litres_from_tank_dip_next_day": [10000, 11000, 12000], "litres_per_day": [10100, 10900, 12000],
    })


def test_ownership_normalization():
    assert canonical_ownership(" PUBLIC_SECTOR ") == "public_sector"
    assert canonical_ownership("coo.") == "cooperative"


def test_clean_frame_removes_leak_and_adds_date_features():
    cleaned = clean_frame(sample_frame())
    assert "litres_from_tank_dip_next_day" not in cleaned.columns
    assert {"month", "day_of_week", "day_of_year"}.issubset(cleaned.columns)


def test_api_health_and_validation():
    client = TestClient(app)
    assert client.get("/health").status_code == 200
    bad = {"highway_distance_km": 26, "nearby_pumps": 1, "price_rs": 100, "trucks_passing": 10, "temp_c": 25, "staff": 5, "ownership": "private", "zone": "City"}
    assert client.post("/predict", json=bad).status_code == 422
