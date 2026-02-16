import pandas as pd

from app.services.feature_engineering import engineer_features
from app.services.rule_engine import compute_rule_score
from app.services.model import compute_ai_score
from app.services.scoring import compute_hybrid_risk
from app.services.context_layer import compute_context_adjusted_risk
from app.services.context_layer import compute_confidence_score

print("Loading dataset...")

# 1️⃣ Load dataset
df = pd.read_csv("synthetic_trade_data.csv")

# 2️⃣ Feature Engineering
df = engineer_features(df)

# 3️⃣ Rule Engine
df = compute_rule_score(df)

# 4️⃣ AI Layer
df = compute_ai_score(df)

# 5️⃣ Hybrid Risk
df = compute_hybrid_risk(df)

# 6️⃣ Context Adjustment
df = compute_context_adjusted_risk(df)

# 7️⃣ Confidence Score
df = compute_confidence_score(df)

print("\nFinal Columns:")
print(df.columns)

print("\nFinal Risk Distribution:")
print(df["final_risk"].describe())

print("\nTop 10 Final Risks:")
print(df.sort_values("final_risk", ascending=False)[
    ["final_risk", "raw_risk", "confidence_score", "anomaly_flag"]
].head(10))
