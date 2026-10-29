from pathlib import Path
import json
import joblib
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, classification_report
from xgboost import XGBClassifier
from src.data.load_data import load_data
from src.features import FEATURES, build_preprocessor

ROOT = Path(__file__).resolve().parents[1]
MODEL_DIR = ROOT / "models"
REPORT_DIR = ROOT / "reports"

def train_model():
    df = load_data()
    X, y = df[FEATURES], df["churn"].astype(int)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=.2, random_state=42, stratify=y
    )
    model = Pipeline([
        ("preprocessor", build_preprocessor()),
        ("classifier", XGBClassifier(
            n_estimators=180, max_depth=4, learning_rate=.05,
            subsample=.9, colsample_bytree=.9, eval_metric="logloss",
            random_state=42, n_jobs=4
        ))
    ])
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    prob = model.predict_proba(X_test)[:, 1]
    metrics = {
        "accuracy": round(float(accuracy_score(y_test, pred)), 4),
        "precision": round(float(precision_score(y_test, pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_test, pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_test, pred, zero_division=0)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, prob)), 4)
    }
    MODEL_DIR.mkdir(exist_ok=True)
    REPORT_DIR.mkdir(exist_ok=True)
    joblib.dump(model, MODEL_DIR / "churn_model.joblib")
    (MODEL_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    (REPORT_DIR / "classification_report.txt").write_text(
        classification_report(y_test, pred, zero_division=0), encoding="utf-8"
    )
    print("Training complete. Test metrics:")
    print(json.dumps(metrics, indent=2))
    print(f"Saved model: {MODEL_DIR / 'churn_model.joblib'}")
    return model, metrics

if __name__ == "__main__":
    train_model()
