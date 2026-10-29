from pathlib import Path
import joblib
import pandas as pd
from src.features import FEATURES

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "churn_model.joblib"

def load_model():
    if not MODEL_PATH.exists():
        raise FileNotFoundError("Model not found. Run `python -m src.train` first.")
    return joblib.load(MODEL_PATH)

def predict_one(payload, model=None):
    model = model or load_model()
    row = pd.DataFrame([{key: payload[key] for key in FEATURES}])
    probability = float(model.predict_proba(row)[0, 1])
    risk = "High" if probability >= .70 else "Medium" if probability >= .40 else "Low"
    return {
        "churn_prediction": "Yes" if probability >= .5 else "No",
        "churn_probability": round(probability, 4),
        "risk_level": risk
    }
