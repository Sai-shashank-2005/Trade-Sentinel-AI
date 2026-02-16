import pandas as pd
from app.services.feature_engineering import engineer_features
from app.services.rule_engine import compute_rule_score

print("Loading dataset...")

# Load dataset
df = pd.read_csv("synthetic_trade_data.csv")

print("Original columns:")
print(df.columns)

# Feature Engineering
df = engineer_features(df)

# Rule Engine
df = compute_rule_score(df)

print("\nColumns after processing:")
print(df.columns)

print("\nRule Score Distribution:")
print(df["rule_score"].describe())

print("\nSample High Rule Scores:")
print(df[df["rule_score"] > 50][
    ["price_zscore", "volume_zscore", "rule_score", "anomaly_flag"]
].head())
