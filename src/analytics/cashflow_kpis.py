import os
import sqlite3
import pandas as pd

# ----------------------------
# Database
# ----------------------------

DB_PATH = os.path.join("db", "nifty100.db")

connection = sqlite3.connect(DB_PATH)

print("Connected to SQLite Database!")

# ----------------------------
# Load Tables
# ----------------------------

profit = pd.read_sql(
    "SELECT * FROM profitandloss",
    connection
)

cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
    connection
)

print("\nTables Loaded Successfully!")

print("Profit & Loss :", len(profit))
print("Cash Flow :", len(cashflow))

# ----------------------------
# Merge Tables
# ----------------------------

df = profit.merge(
    cashflow,
    on=["company_id", "year"],
    how="left"
)

print("\nCalculating Cash Flow KPIs...\n")
# ----------------------------
# Free Cash Flow
# ----------------------------

df["free_cash_flow"] = (
    df["operating_activity"] +
    df["investing_activity"]
)

# ----------------------------
# CFO Quality
# ----------------------------

df["cfo_quality"] = df.apply(
    lambda x: None
    if x["net_profit"] == 0
    else round(
        x["operating_activity"] / x["net_profit"],
        2
    ),
    axis=1
)

# ----------------------------
# CFO Quality Label
# ----------------------------

def quality_label(value):

    if pd.isna(value):
        return None

    if value > 1:
        return "High Quality"

    elif value >= 0.5:
        return "Moderate"

    else:
        return "Accrual Risk"


df["cfo_quality_label"] = df["cfo_quality"].apply(
    quality_label
)

# ----------------------------
# CapEx Intensity
# ----------------------------

df["capex_intensity"] = df.apply(
    lambda x: None
    if x["sales"] == 0
    else abs(x["investing_activity"]) /
         x["sales"] * 100,
    axis=1
)

# ----------------------------
# FCF Conversion
# ----------------------------

df["fcf_conversion"] = df.apply(
    lambda x: None
    if x["operating_profit"] == 0
    else (
        x["free_cash_flow"] /
        x["operating_profit"]
    ) * 100,
    axis=1
)

# ----------------------------
# Capital Allocation Pattern
# ----------------------------

def sign(v):
    if pd.isna(v):
        return "0"
    return "+" if v >= 0 else "-"


def pattern(row):

    cfo = sign(row["operating_activity"])
    cfi = sign(row["investing_activity"])
    cff = sign(row["financing_activity"])

    key = (cfo, cfi, cff)

    patterns = {
        ("+", "-", "-"): "Reinvestor",
        ("+", "+", "-"): "Liquidating Assets",
        ("-", "+", "+"): "Distress Signal",
        ("-", "-", "+"): "Growth Funded by Debt",
        ("+", "+", "+"): "Cash Accumulator",
        ("-", "-", "-"): "Pre-Revenue",
        ("+", "-", "+"): "Mixed"
    }

    return patterns.get(key, "Other")


df["capital_pattern"] = df.apply(
    pattern,
    axis=1
)

# ----------------------------
# Save CSV
# ----------------------------

os.makedirs("output", exist_ok=True)

df[
    [
        "company_id",
        "year",
        "free_cash_flow",
        "cfo_quality",
        "cfo_quality_label",
        "capex_intensity",
        "fcf_conversion",
        "capital_pattern"
    ]
].to_csv(
    "output/capital_allocation.csv",
    index=False
)

print(df[
    [
        "company_id",
        "year",
        "free_cash_flow",
        "capital_pattern"
    ]
].head())

connection.close()

print("\ncapital_allocation.csv created successfully!")
print("Day 11 Completed Successfully!")