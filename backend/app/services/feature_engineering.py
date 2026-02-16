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

    # Price Z-Score per HS code
    df["price_zscore"] = (
        df.groupby("hs_code")["unit_price"]
        .transform(lambda x: compute_zscore(x))
    )

    # Volume Z-Score
    df["volume_zscore"] = compute_zscore(df["quantity"])

    # Route Frequency
    route_counts = df["route"].value_counts(normalize=True)
    df["route_frequency"] = df["route"].map(route_counts)

    # Exporter Frequency
    exporter_counts = df["exporter"].value_counts(normalize=True)
    df["counterparty_frequency"] = df["exporter"].map(exporter_counts)

    return df
