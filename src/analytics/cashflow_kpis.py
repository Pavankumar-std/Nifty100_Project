import os
import sqlite3
import pandas as pd

DB = "db/nifty100.db"

os.makedirs("output", exist_ok=True)

conn = sqlite3.connect(DB)

cf = pd.read_sql("SELECT * FROM cashflow", conn)
pl = pd.read_sql("SELECT * FROM profitandloss", conn)
companies = pd.read_sql("SELECT * FROM companies", conn)

conn.close()

# Normalize column names
cf.columns = cf.columns.str.strip().str.lower().str.replace(" ", "_")
pl.columns = pl.columns.str.strip().str.lower().str.replace(" ", "_")
companies.columns = companies.columns.str.strip().str.lower().str.replace(" ", "_")

data = cf.merge(
    pl,
    on=["company_id", "year"],
    how="left"
)

results = []

for company in data["company_id"].unique():

    df = data[data["company_id"] == company].sort_values("year")

    latest = df.iloc[-1]

    cfo = latest["operating_activity"]
    cff = latest["financing_activity"]
    sales = latest["sales"]
    profit = latest["net_profit"]

    if profit != 0:
        cfo_quality = cfo / profit
    else:
        cfo_quality = 0

    if cfo_quality > 1:
        quality = "High Quality"
    elif cfo_quality >= 0.5:
        quality = "Moderate"
    else:
        quality = "Accrual Risk"

    capex = abs(latest["investing_activity"])

    if sales != 0:
        capex_pct = capex / sales * 100
    else:
        capex_pct = 0

    if capex_pct < 3:
        capex_label = "Asset Light"
    elif capex_pct <= 8:
        capex_label = "Moderate"
    else:
        capex_label = "Capital Intensive"

    distress = (
        cfo < 0 and
        cff > 0
    )

    results.append({
        "company_id": company,
        "cfo_quality_score": round(cfo_quality, 2),
        "cfo_quality_label": quality,
        "capex_intensity_pct": round(capex_pct, 2),
        "capex_label": capex_label,
        "distress_flag": distress
    })

result = pd.DataFrame(results)

result.to_excel(
    "output/cashflow_intelligence.xlsx",
    index=False
)

result[result["distress_flag"]].to_csv(
    "output/distress_alerts.csv",
    index=False
)

print("Cash Flow Intelligence Generated")
print(result.head())