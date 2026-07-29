import os
import sqlite3
import pandas as pd

DB = "db/nifty100.db"

OUTPUT = "output/pros_cons_generated.csv"

os.makedirs("output", exist_ok=True)

conn = sqlite3.connect(DB)

ratios = pd.read_sql("SELECT * FROM financial_ratios", conn)
companies = pd.read_sql("SELECT * FROM companies", conn)

conn.close()

results = []

latest = (
    ratios.sort_values("year")
    .groupby("company_id")
    .tail(1)
)

for _, row in latest.iterrows():

    company = row["company_id"]

    # -----------------------
    # PRO RULES
    # -----------------------

    if row["roe"] > 20:
        results.append({
            "company_id": company,
            "type": "Pro",
            "rule_id": "P1",
            "text": "High Return on Equity",
            "confidence_pct": 90
        })

    if row["debt_to_equity"] == 0:
        results.append({
            "company_id": company,
            "type": "Pro",
            "rule_id": "P2",
            "text": "Debt Free Company",
            "confidence_pct": 95
        })

    if row["roce"] > 20:
        results.append({
            "company_id": company,
            "type": "Pro",
            "rule_id": "P3",
            "text": "Strong Capital Efficiency",
            "confidence_pct": 85
        })

    # -----------------------
    # CON RULES
    # -----------------------

    if row["debt_to_equity"] > 2:
        results.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "C1",
            "text": "High Debt",
            "confidence_pct": 90
        })

    if row["roe"] < 10:
        results.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "C2",
            "text": "Low Return on Equity",
            "confidence_pct": 80
        })

    if row["roce"] < 10:
        results.append({
            "company_id": company,
            "type": "Con",
            "rule_id": "C3",
            "text": "Low Capital Efficiency",
            "confidence_pct": 80
        })


proscons = pd.DataFrame(results)

proscons.to_csv(
    OUTPUT,
    index=False
)

print("Generated", len(proscons), "Pros/Cons")