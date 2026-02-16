import pandas as pd
from app.services.feature_engineering import engineer_features
from app.services.rule_engine import compute_rule_score
from app.services.model import compute_ai_score
from app.services.scoring import compute_hybrid_risk

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

print("\nFinal Columns:")
print(df.columns)

print("\nHybrid Risk Distribution:")
print(df["raw_risk"].describe())

print("\nTop 10 Hybrid Risks:")
print(df.sort_values("raw_risk", ascending=False)[
    ["raw_risk", "ai_score", "rule_score", "anomaly_flag"]
].head(10))
