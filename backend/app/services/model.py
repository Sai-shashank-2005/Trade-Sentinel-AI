import numpy as np
from sklearn.ensemble import IsolationForest


def compute_ai_score(df):

    df = df.copy()

    feature_columns = [
        "price_zscore",
        "volume_zscore",
        "route_frequency",
        "counterparty_frequency"
    ]

    X = df[feature_columns].values

    # Initialize Isolation Forest
    model = IsolationForest(
        n_estimators=100,
        contamination=0.06,   # 6% anomalies injected
        random_state=42
    )

    model.fit(X)

    # decision_function gives anomaly score
    anomaly_scores = model.decision_function(X)

    # Normalize to 0–100
    normalized_scores = (anomaly_scores - anomaly_scores.min()) / (
        anomaly_scores.max() - anomaly_scores.min()
    )

    df["ai_score"] = (1 - normalized_scores) * 100

    return df
