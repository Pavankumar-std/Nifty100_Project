import sqlite3
import pandas as pd
import os

# ----------------------------
# Connect Database
# ----------------------------
conn = sqlite3.connect("db/nifty100.db")

market = pd.read_sql("SELECT * FROM market_cap", conn)

conn.close()

# ----------------------------
# Fix Broken Headers
# ----------------------------
market.columns = [
    "id",
    "company_id",
    "year",
    "market_cap",
    "enterprise_value",
    "pe_ratio",
    "pb_ratio",
    "ev_ebitda",
    "dividend_yield"
][:len(market.columns)]

# ----------------------------
# Convert Numeric Columns
# ----------------------------
numeric_cols = [
    "market_cap",
    "enterprise_value",
    "pe_ratio",
    "pb_ratio",
    "ev_ebitda",
    "dividend_yield"
]

for col in numeric_cols:
    market[col] = pd.to_numeric(market[col], errors="coerce")

# ----------------------------
# Simple Valuation Flag
# ----------------------------
market["valuation_flag"] = "Fair"

market.loc[
    market["pe_ratio"] > market["pe_ratio"].median() * 1.5,
    "valuation_flag"
] = "Caution"

market.loc[
    market["pe_ratio"] < market["pe_ratio"].median() * 0.7,
    "valuation_flag"
] = "Discount"

# ----------------------------
# Create Output Folder
# ----------------------------
os.makedirs("output", exist_ok=True)

# ----------------------------
# Export Files
# ----------------------------
market.to_excel(
    "output/valuation_summary.xlsx",
    index=False
)

market[
    market["valuation_flag"] != "Fair"
].to_csv(
    "output/valuation_flags.csv",
    index=False
)

print("\n✅ valuation_summary.xlsx Created")

print("✅ valuation_flags.csv Created")