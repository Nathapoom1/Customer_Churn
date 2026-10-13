from pathlib import Path
from typing import Literal

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


MODEL_PATH = Path(__file__).parent / "model" / "churn_pipeline.joblib"
app = FastAPI(title="Customer Churn Prediction API", version="1.0.0")
model = joblib.load(MODEL_PATH) if MODEL_PATH.exists() else None


class Customer(BaseModel):
    months_member: int = Field(ge=0)
    monthly_fee: float = Field(ge=0)
    support_calls: int = Field(ge=0)
    usage_hours_month: float = Field(ge=0)
    late_payments: int = Field(ge=0)
    contract_type: Literal["Monthly", "Annual", "Two-Year", "Unknown"]


@app.get("/health")
def health():
    if model is None:
        raise HTTPException(status_code=503, detail="Model file not found")
    return {"status": "ready"}


@app.post("/predict")
def predict(customer: Customer):
    if model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not found. Run the Customer_Churn.ipynb export section first.",
        )
    row = pd.DataFrame([customer.model_dump()])
    prediction = int(model.predict(row)[0])
    probability = float(model.predict_proba(row)[0, 1]) if hasattr(model, "predict_proba") else None
    return {"churn_prediction": prediction, "churn_probability": probability}
