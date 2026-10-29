from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PATH = ROOT / "data" / "customer_churn.csv"

def load_data(path=DEFAULT_PATH):
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError("Dataset missing. Run: python -m src.data.generate_data")
    df = pd.read_csv(path)
    if "churn" not in df.columns:
        raise ValueError("Dataset must include target column 'churn'.")
    return df
