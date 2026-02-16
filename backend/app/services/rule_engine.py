import numpy as np


def compute_rule_score(df):

    df = df.copy()
    df["rule_score"] = 0

    # Price Rule
    df.loc[df["price_zscore"] > 3, "rule_score"] += 40
    df.loc[df["price_zscore"] > 5, "rule_score"] += 30

    # Volume Rule
    df.loc[df["volume_zscore"] > 3, "rule_score"] += 30
    df.loc[df["volume_zscore"] > 5, "rule_score"] += 20

    # Rare Route Rule
    df.loc[df["route_frequency"] < 0.01, "rule_score"] += 20

    # Rare Exporter Rule
    df.loc[df["counterparty_frequency"] < 0.01, "rule_score"] += 10

    df["rule_score"] = np.clip(df["rule_score"], 0, 100)

    return df
