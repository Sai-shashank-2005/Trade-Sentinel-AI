import pandas as pd
import numpy as np


def compute_zscore(series):
    mean = series.mean()
    std = series.std()
    if std == 0:
        return np.zeros(len(series))
    return (series - mean) / std


def engineer_features(df: pd.DataFrame) -> pd.DataFrame:

    df = df.copy()

    # -----------------------------
    # Original Statistical Features
    # -----------------------------
    df["price_zscore"] = (
        df.groupby("hs_code")["unit_price"]
        .transform(lambda x: compute_zscore(x))
    )

    df["volume_zscore"] = compute_zscore(df["quantity"])

    route_counts = df["route"].value_counts(normalize=True)
    df["route_frequency"] = df["route"].map(route_counts)

    exporter_counts = df["exporter"].value_counts(normalize=True)
    df["counterparty_frequency"] = df["exporter"].map(exporter_counts)

    # -----------------------------
    # NEW Behavioral Features
    # -----------------------------

    # Exporter price deviation
    exporter_avg_price = df.groupby("exporter")["unit_price"].transform("mean")
    df["price_deviation_exporter"] = (
        (df["unit_price"] - exporter_avg_price) /
        exporter_avg_price.replace(0, 1)
    )

    # HS quantity deviation
    hs_avg_qty = df.groupby("hs_code")["quantity"].transform("mean")
    df["quantity_deviation_hs"] = (
        (df["quantity"] - hs_avg_qty) /
        hs_avg_qty.replace(0, 1)
    )

    return df
