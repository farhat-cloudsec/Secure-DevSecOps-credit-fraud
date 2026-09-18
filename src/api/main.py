from fastapi import FastAPI
import joblib
import numpy as np
from pydantic import BaseModel
from typing import List

app = FastAPI()

model = joblib.load('fraud_model.pkl')
scaler = joblib.load('scaler.pkl')

class Transaction(BaseModel):
    features: List[float]


@app.post("/predict")
def predict(transaction: Transaction):
    data = np.array(transaction.features).reshape(1, -1)
    data_scaled = scaler.transform(data)
    prediction = model.predict(data_scaled)
    probability = model.predict_proba(data_scaled)

    result = "Fraud" if prediction[0] == 1 else "Not Fraud"

    return {
        "prediction": result,
        "fraud_probability": float(probability[0][1])
    }