import os
import sqlite3
import pandas as pd

os.makedirs("output", exist_ok=True)

conn = sqlite3.connect("db/nifty100.db")

cf = pd.read_sql("SELECT * FROM cashflow", conn)

conn.close()

cf.columns = (
    cf.columns.str.strip()
              .str.lower()
              .str.replace(" ", "_")
)

patterns = []

for company in cf["company_id"].unique():

    df = cf[
        cf["company_id"] == company
    ].sort_values("year")

    latest = df.iloc[-1]

    cfo = latest["operating_activity"]
    cfi = latest["investing_activity"]
    cff = latest["financing_activity"]

    if cfo > 0 and cfi < 0:
        pattern = "Reinvestor"

    elif cfo > 0 and cff < 0:
        pattern = "Deleveraging"

    elif cfo < 0 and cff > 0:
        pattern = "Distress"

    else:
        pattern = "Stable"

    patterns.append({
        "company_id": company,
        "capital_allocation_label": pattern
    })

result = pd.DataFrame(patterns)

result.to_csv(
    "output/pattern_changes.csv",
    index=False
)

print(result.head())
print("Capital Allocation Report Generated")
