import os
import sqlite3
import pandas as pd
import yaml

from openpyxl import load_workbook
# -----------------------------
# Database
# -----------------------------

DB_PATH = os.path.join("db", "nifty100.db")

connection = sqlite3.connect(DB_PATH)

print("Connected to SQLite Database!")

# -----------------------------
# Load Config
# -----------------------------

with open("config/screener_config.yaml", "r") as file:
    config = yaml.safe_load(file)

print("Screener Config Loaded!")

# -----------------------------
# Load Financial Ratios
# -----------------------------

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    connection
)

print("Financial Ratios Loaded :", len(ratios))

# -----------------------------
# Composite Quality Score
# -----------------------------

score_columns = []

for col in [
    "roe",
    "roce",
    "net_profit_margin",
    "asset_turnover"
]:
    if col in ratios.columns:
        score_columns.append(col)

if score_columns:
    ratios["composite_quality_score"] = (
        ratios[score_columns]
        .fillna(0)
        .mean(axis=1)
    )
else:
    ratios["composite_quality_score"] = 0

# -----------------------------
# Filter Function
# -----------------------------

def apply_filters(df, rules):

    result = df.copy()

    if "roe_min" in rules and "roe" in result.columns:
        result = result[result["roe"] >= rules["roe_min"]]

    if "debt_to_equity_max" in rules and "debt_to_equity" in result.columns:
        result = result[
            result["debt_to_equity"] <= rules["debt_to_equity_max"]
        ]

    if "revenue_cagr_min" in rules and "revenue_cagr" in result.columns:
        result = result[
            result["revenue_cagr"] >= rules["revenue_cagr_min"]
        ]

    if "pat_cagr_min" in rules and "pat_cagr" in result.columns:
        result = result[
            result["pat_cagr"] >= rules["pat_cagr_min"]
        ]

    if "free_cash_flow_min" in rules and "free_cash_flow" in result.columns:
        result = result[
            result["free_cash_flow"] >= rules["free_cash_flow_min"]
        ]

    return result.sort_values(
        by="composite_quality_score",
        ascending=False
    )

# -----------------------------
# Test One Screener
# -----------------------------

# -----------------------------
# Run All Screeners
# -----------------------------

presets = [
    "quality_compounder",
    "value_pick",
    "growth_accelerator",
    "dividend_champion",
    "debt_free_bluechip",
    "turnaround_watch"
]

# ------------------------------------
# Export All Screeners to Excel
# ------------------------------------

os.makedirs("output", exist_ok=True)

excel_file = "output/screener_output.xlsx"

with pd.ExcelWriter(
    excel_file,
    engine="openpyxl"
) as writer:

    for preset in presets:

        print("\nRunning:", preset)

        result = apply_filters(
            ratios,
            config[preset]
        )

        result = result.sort_values(
            "composite_quality_score",
            ascending=False
        )

        result.to_excel(
            writer,
            sheet_name=preset[:31],
            index=False
        )

        print("Companies:", len(result))

print("\nExcel Report Generated Successfully!")

print(excel_file)

connection.close()

print("\nDatabase Closed Successfully!")