from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import numpy as np

from app.services.feature_engineering import engineer_features
from app.services.rule_engine import compute_rule_score
from app.services.model import compute_ai_score
from app.services.scoring import compute_hybrid_risk
from app.services.context_layer import compute_context_adjusted_risk
from app.services.context_layer import compute_confidence_score

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Trade Sentinel AI Backend Running"}


@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))

    # ================= PIPELINE =================
    df = engineer_features(df)
    df = compute_rule_score(df)
    df = compute_ai_score(df)
    df = compute_hybrid_risk(df)
    df = compute_context_adjusted_risk(df)
    df = compute_confidence_score(df)

    # ================= ABSOLUTE RISK THRESHOLDS =================
    df["risk_level"] = "Low"

    df.loc[df["final_risk"] >= 75, "risk_level"] = "High"
    df.loc[
        (df["final_risk"] >= 50) & (df["final_risk"] < 75),
        "risk_level"
    ] = "Medium"

    # ================= CONTEXT DELTA =================
    df["context_adjustment"] = df["final_risk"] - df["raw_risk"]

    # ================= RULE BREAKDOWN FLAGS =================
    df["price_rule_triggered"] = np.where(df["price_zscore"] > 3, 1, 0)
    df["volume_rule_triggered"] = np.where(df["volume_zscore"] > 3, 1, 0)
    df["route_rule_triggered"] = np.where(df["route_frequency"] < 0.01, 1, 0)
    df["exporter_rule_triggered"] = np.where(df["counterparty_frequency"] < 0.01, 1, 0)

    # ================= MODEL VALIDATION (REAL PERFORMANCE) =================
    if "anomaly_flag" in df.columns:

        df["predicted_flag"] = np.where(df["risk_level"] == "High", 1, 0)

        true_positives = ((df["predicted_flag"] == 1) & (df["anomaly_flag"] == 1)).sum()
        false_positives = ((df["predicted_flag"] == 1) & (df["anomaly_flag"] == 0)).sum()
        false_negatives = ((df["predicted_flag"] == 0) & (df["anomaly_flag"] == 1)).sum()

        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0 else 0
        )

        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0 else 0
        )

        print("\n===== MODEL VALIDATION =====")
        print("True Positives:", true_positives)
        print("False Positives:", false_positives)
        print("False Negatives:", false_negatives)
        print("Precision:", round(precision, 3))
        print("Recall:", round(recall, 3))
        print("============================\n")

    # ================= FINAL RESULT =================
    result = df[[
        "transaction_id",
        "raw_risk",
        "final_risk",
        "confidence_score",
        "risk_level",

        # AI
        "ai_score",

        # Context
        "context_adjustment",

        # Feature Signals
        "price_zscore",
        "volume_zscore",
        "route_frequency",
        "counterparty_frequency",

        # Rule Flags
        "price_rule_triggered",
        "volume_rule_triggered",
        "route_rule_triggered",
        "exporter_rule_triggered"
    ]]

    return result.to_dict(orient="records")
