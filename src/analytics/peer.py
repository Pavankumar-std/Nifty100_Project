import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join("db", "nifty100.db")

conn = sqlite3.connect(DB_PATH)

print("Connected to SQLite Database!")

peer = pd.read_sql(
    "SELECT * FROM peer_groups",
    conn
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

print("Peer Groups :", len(peer))
print("Financial Ratios :", len(ratios))

# -------------------------
# Merge Tables
# -------------------------

df = ratios.merge(
    peer,
    on="company_id",
    how="left"
)

# -------------------------
# Metrics
# -------------------------

metrics = [
    "roe",
    "roce",
    "net_profit_margin",
    "debt_to_equity",
    "interest_coverage",
    "asset_turnover"
]

records = []

for metric in metrics:

    if metric not in df.columns:
        continue

    temp = df.copy()

    # Lower Debt is Better
    ascending = True if metric == "debt_to_equity" else False

    temp["percentile_rank"] = (
        temp.groupby("peer_group")[metric]
        .rank(
            pct=True,
            ascending=ascending
        ) * 100
    )

    for _, row in temp.iterrows():

        records.append({

            "company_id": row["company_id"],

            "peer_group": row["peer_group"],

            "metric": metric,

            "value": row[metric],

            "percentile_rank": row["percentile_rank"],

            "year": row["year"]

        })

peer_percentiles = pd.DataFrame(records)

peer_percentiles.to_sql(
    "peer_percentiles",
    conn,
    if_exists="replace",
    index=False
)

print()

print("Peer Percentiles Generated Successfully!")

print(peer_percentiles.head())

print()

count = pd.read_sql(
    "SELECT COUNT(*) AS total_rows FROM peer_percentiles",
    conn
)

print(count)

conn.close()

print()

print("Database Closed Successfully!")

print("Day 18 Completed Successfully!")