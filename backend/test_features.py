import pandas as pd
from app.services.feature_engineering import engineer_features
from app.services.rule_engine import compute_rule_score
from app.services.model import compute_ai_score

print("Loading dataset...")

df = pd.read_csv("synthetic_trade_data.csv")

df = engineer_features(df)
df = compute_rule_score(df)
df = compute_ai_score(df)

print("\nFinal Columns:")
print(df.columns)

print("\nAI Score Distribution:")
print(df["ai_score"].describe())

print("\nTop 10 AI Scores:")
print(df.sort_values("ai_score", ascending=False)[
    ["ai_score", "rule_score", "anomaly_flag"]
].head(10))
