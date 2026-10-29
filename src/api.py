from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.predict import predict_one, MODEL_PATH

app = FastAPI(title="Customer Churn Prediction API", version="1.0.0",
              description="Predict customer churn with an XGBoost model.")

class CustomerFeatures(BaseModel):
    tenure: int = Field(ge=0, le=100)
    monthly_charges: float = Field(ge=0, le=10000)
    total_charges: float = Field(ge=0, le=1000000)
    contract: str
    internet_service: str
    tech_support: str
    online_security: str
    payment_method: str
    paperless_billing: str
    senior_citizen: int = Field(ge=0, le=1)
    partner: str
    dependents: str

@app.get("/")
def root():
    return {"message": "Customer Churn Prediction API", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok", "model_ready": MODEL_PATH.exists()}

@app.post("/predict")
def predict(customer: CustomerFeatures):
    try:
        return predict_one(customer.model_dump())
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Prediction failed: {exc}") from exc
