import os
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

DB = "db/nifty100.db"

conn = sqlite3.connect(DB)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

os.makedirs("reports/radar_charts", exist_ok=True)

metrics = [
    "roe",
    "roce",
    "net_profit_margin",
    "asset_turnover"
]

companies = ratios["company_id"].unique()

for company in companies[:20]:

    df = ratios[ratios["company_id"] == company]

    if df.empty:
        continue

    latest = df.iloc[-1]

    values = []

    labels = []

    for m in metrics:

        if m in latest.index:

            values.append(
                0 if pd.isna(latest[m]) else latest[m]
            )

            labels.append(m)

    values += values[:1]

    angles = np.linspace(
        0,
        2*np.pi,
        len(labels),
        endpoint=False
    ).tolist()

    angles += angles[:1]

    fig = plt.figure(figsize=(5,5))

    ax = plt.subplot(111, polar=True)

    ax.plot(
        angles,
        values,
        linewidth=2
    )

    ax.fill(
        angles,
        values,
        alpha=0.25
    )

    ax.set_xticks(angles[:-1])

    ax.set_xticklabels(labels)

    plt.title(company)

    plt.savefig(
        f"reports/radar_charts/{company}_radar.png"
    )

    plt.close()

print("Radar Charts Generated Successfully!")

conn.close()