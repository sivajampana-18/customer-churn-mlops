# Customer Churn Prediction System
**XGBoost + automated MLOps pipeline**

This educational project trains an XGBoost model to predict whether a customer may churn, saves evaluation metrics, exposes predictions through FastAPI, includes tests, Docker, and GitHub Actions CI.

The project generates a **synthetic telecom-style dataset** so it works without downloading private or external data. Synthetic model performance is only for demonstrating the workflow, not real business use.

## Architecture
1. Generate sample data.
2. Preprocess numeric and categorical features.
3. Train and evaluate XGBoost.
4. Save model and metrics.
5. Serve predictions through a REST API.
6. Run training/tests automatically in GitHub Actions.

## Setup (Windows PowerShell)
```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python -m src.data.generate_data
python -m src.train
uvicorn src.api:app --reload
```
If activation is blocked, run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` in that PowerShell window, then activate again.

Open **http://127.0.0.1:8000/docs** to test the API.

## Test
```powershell
pytest -q
```

## Example `POST /predict` JSON
```json
{
  "tenure": 12,
  "monthly_charges": 79.5,
  "total_charges": 954.0,
  "contract": "Month-to-month",
  "internet_service": "Fiber optic",
  "tech_support": "No",
  "online_security": "No",
  "payment_method": "Electronic check",
  "paperless_billing": "Yes",
  "senior_citizen": 0,
  "partner": "No",
  "dependents": "No"
}
```
Response contains `churn_prediction`, `churn_probability`, and `risk_level`.

## Files
- `src/data/generate_data.py`: creates demo CSV.
- `src/data/load_data.py`: loads and validates data.
- `src/features.py`: preprocessing pipeline.
- `src/train.py`: model training, evaluation, and artifact saving.
- `src/predict.py`: prediction helper.
- `src/api.py`: FastAPI endpoints.
- `tests/test_api.py`: API tests.
- `.github/workflows/ci.yml`: automated training and test workflow.
- `Dockerfile` and `docker-compose.yml`: container deployment.

## MLOps improvements for a production version
Add MLflow experiment tracking/model registry, data and model drift monitoring, scheduled retraining, model-quality gates, deployment approvals, secrets management, and cloud hosting. Review privacy and fairness before using customer data.
