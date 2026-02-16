import numpy as np


def compute_hybrid_risk(df, ai_weight=0.6, rule_weight=0.4):

    df = df.copy()

    # Weighted combination
    df["raw_risk"] = (
        ai_weight * df["ai_score"] +
        rule_weight * df["rule_score"]
    )

    # Ensure bounds 0–100
    df["raw_risk"] = np.clip(df["raw_risk"], 0, 100)

    return df
