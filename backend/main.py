from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from io import StringIO
from backend.model import predict_risk
from backend.shap_explainer import generate_explanations

app = FastAPI(title="NeuroGuard AI API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

REQUIRED_COLUMNS = [
    "delta_power",
    "theta_power",
    "alpha_power",
    "beta_power",
    "signal_variance",
    "spectral_entropy",
]

@app.get("/health")
def health():
    return {"status": "ok", "service": "NeuroGuard AI API"}

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Please upload a CSV file.")

    content = await file.read()
    try:
        df = pd.read_csv(StringIO(content.decode("utf-8")))
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid CSV format.")

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {missing}"
        )

    patient_vector = df[REQUIRED_COLUMNS].mean().to_dict()

    risk_score, risk_level = predict_risk(patient_vector)
    explanations = generate_explanations(patient_vector, risk_score)

    return {
        "risk_score": round(float(risk_score), 4),
        "risk_level": risk_level,
        "explanations": explanations
    }