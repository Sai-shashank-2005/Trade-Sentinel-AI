from fastapi import FastAPI, UploadFile, File
import pandas as pd
import io

from app.services.feature_engineering import engineer_features
from app.services.rule_engine import compute_rule_score
from app.services.model import compute_ai_score
from app.services.scoring import compute_hybrid_risk
from app.services.context_layer import compute_context_adjusted_risk
from app.services.context_layer import compute_confidence_score

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Trade Sentinel AI Backend Running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))

    # Pipeline
    df = engineer_features(df)
    df = compute_rule_score(df)
    df = compute_ai_score(df)
    df = compute_hybrid_risk(df)
    df = compute_context_adjusted_risk(df)
    df = compute_confidence_score(df)

    result = df[[
        "transaction_id",
        "raw_risk",
        "final_risk",
        "confidence_score"
    ]]

    return result.to_dict(orient="records")
