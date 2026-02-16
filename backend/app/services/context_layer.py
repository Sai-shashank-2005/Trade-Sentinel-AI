import numpy as np


def compute_context_adjusted_risk(df):

    df = df.copy()

    df["final_risk"] = df["raw_risk"]

    # -------------------------
    # 1️⃣ Peer Adjustment
    # -------------------------
    # Group by HS code to simulate similar transactions
    peer_mean_risk = df.groupby("hs_code")["raw_risk"].transform("mean")

    # If many peers are risky, reduce impact
    peer_adjustment_factor = 1 - (peer_mean_risk / 200)

    df["final_risk"] = df["final_risk"] * peer_adjustment_factor

    # -------------------------
    # 2️⃣ Stability Adjustment (Exporter frequency proxy)
    # -------------------------
    # Stable exporter (high frequency) → slightly reduce anomaly
    stability_factor = 1 - (df["counterparty_frequency"] * 0.5)

    df["final_risk"] = df["final_risk"] * stability_factor

    # -------------------------
    # 3️⃣ Extreme Protection
    # -------------------------
    df.loc[df["raw_risk"] > 85, "final_risk"] = df["raw_risk"]

    # Ensure bounds
    df["final_risk"] = np.clip(df["final_risk"], 0, 100)

    return df

def compute_confidence_score(df):

    df = df.copy()

    confidence = (
        (1 - df["route_frequency"]) * 40 +
        (1 - df["counterparty_frequency"]) * 30 +
        (df["raw_risk"] / 100) * 30
    )

    df["confidence_score"] = np.clip(confidence, 0, 100)

    return df
