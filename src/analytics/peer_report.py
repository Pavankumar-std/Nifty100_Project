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

companies = pd.read_sql(
    "SELECT id, company_name FROM companies",
    conn
)

# Merge Data
report = peer.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

report = report.merge(
    ratios,
    on="company_id",
    how="left"
)

os.makedirs("output", exist_ok=True)

excel_file = "output/peer_comparison.xlsx"

with pd.ExcelWriter(
    excel_file,
    engine="openpyxl"
) as writer:

    groups = report["peer_group"].dropna().unique()

    for group in groups:

        df = report[
            report["peer_group"] == group
        ].copy()

        df.to_excel(
            writer,
            sheet_name=str(group)[:31],
            index=False
        )

        print(f"{group}: {len(df)} rows")

print("\nPeer Comparison Report Generated Successfully!")
print(excel_file)

conn.close()

print("\nDatabase Closed Successfully!")
print("Day 20 Completed Successfully!")