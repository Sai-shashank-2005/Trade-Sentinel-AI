import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

np.random.seed(42)
random.seed(42)

NUM_RECORDS = 10000
ANOMALY_PERCENT = 0.06

hs_codes = {
    "1001": 30,   # Agriculture
    "2709": 70,   # Oil
    "3004": 120,  # Pharma
    "7208": 80,   # Steel
    "8501": 150   # Electrical
}

countries = ["USA", "China", "India", "Germany", "UAE", "Brazil"]
importers = [f"Importer_{i}" for i in range(1, 51)]
exporters = [f"Exporter_{i}" for i in range(1, 51)]

data = []
start_date = datetime(2023, 1, 1)

for i in range(NUM_RECORDS):

    date = start_date + timedelta(days=random.randint(0, 365))

    hs = random.choice(list(hs_codes.keys()))
    base_price = hs_codes[hs]

    origin = random.choice(countries)
    dest = random.choice([c for c in countries if c != origin])

    importer = random.choice(importers)
    exporter = random.choice(exporters)

    quantity = np.random.normal(1000, 150)
    unit_price = np.random.normal(base_price, base_price * 0.1)

    quantity = abs(quantity)
    unit_price = abs(unit_price)

    total_value = quantity * unit_price

    route = f"{origin}-{dest}"

    data.append([
        i,
        date,
        importer,
        exporter,
        hs,
        quantity,
        unit_price,
        total_value,
        origin,
        dest,
        route,
        0  # anomaly_flag (initially normal)
    ])

df = pd.DataFrame(data, columns=[
    "transaction_id",
    "date",
    "importer",
    "exporter",
    "hs_code",
    "quantity",
    "unit_price",
    "total_value",
    "origin_country",
    "destination_country",
    "route",
    "anomaly_flag"
])

# Inject anomalies
num_anomalies = int(NUM_RECORDS * ANOMALY_PERCENT)
anomaly_indices = np.random.choice(df.index, num_anomalies, replace=False)

for idx in anomaly_indices:

    anomaly_type = random.choice(["price_spike", "volume_spike", "route_anomaly"])

    if anomaly_type == "price_spike":
        df.loc[idx, "unit_price"] *= random.uniform(3, 5)
        df.loc[idx, "total_value"] = df.loc[idx, "quantity"] * df.loc[idx, "unit_price"]

    elif anomaly_type == "volume_spike":
        df.loc[idx, "quantity"] *= random.uniform(3, 5)
        df.loc[idx, "total_value"] = df.loc[idx, "quantity"] * df.loc[idx, "unit_price"]

    elif anomaly_type == "route_anomaly":
        df.loc[idx, "route"] = "UNKNOWN-ROUTE"

    df.loc[idx, "anomaly_flag"] = 1


df.to_csv("synthetic_trade_data.csv", index=False)

print("Dataset Generated Successfully!")
print(f"Total Records: {len(df)}")
print(f"Anomalies Injected: {num_anomalies}")
