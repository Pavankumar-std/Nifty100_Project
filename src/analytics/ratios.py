import os
import sqlite3
import pandas as pd

# ----------------------------
# Database Path
# ----------------------------

DB_PATH = os.path.join("db", "nifty100.db")

# ----------------------------
# Connect SQLite
# ----------------------------

connection = sqlite3.connect(DB_PATH)

print("Connected to SQLite Database!")

# ----------------------------
# Load Tables
# ----------------------------

companies = pd.read_sql(
    "SELECT * FROM companies",
    connection
)


profit = pd.read_sql(
    "SELECT * FROM profitandloss",
    connection
)

balance = pd.read_sql(
    "SELECT * FROM balancesheet",
    connection
)

cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
    connection
)

print("\nTables Loaded Successfully!\n")

print("Companies :", len(companies))
print("Profit & Loss :", len(profit))
print("Balance Sheet :", len(balance))
print("Cash Flow :", len(cashflow))

# ----------------------------
# Merge Profit + Balance
# ----------------------------

ratios = pd.merge(
    profit,
    balance,
    on=["company_id", "year"],
    how="left"
)

# ----------------------------
# Merge Companies
# ----------------------------
ratios = pd.merge(
    ratios,
    companies[
        [
            "id",
            "roe_percentage",
            "roce_percentage"
        ]
    ],
    left_on="company_id",
    right_on="id",
    how="left"
)
print("\nCalculating Financial Ratios...\n")

# ----------------------------
# Net Profit Margin
# ----------------------------

ratios["net_profit_margin"] = ratios.apply(
    lambda x: None
    if pd.isna(x["sales"]) or x["sales"] == 0
    else (x["net_profit"] / x["sales"]) * 100,
    axis=1
)

# ----------------------------
# Operating Profit Margin
# ----------------------------

ratios["operating_profit_margin"] = ratios.apply(
    lambda x: None
    if pd.isna(x["sales"]) or x["sales"] == 0
    else (x["operating_profit"] / x["sales"]) * 100,
    axis=1
)

# ----------------------------
# Return On Equity (ROE)
# ----------------------------

ratios["roe"] = ratios.apply(
    lambda x: None
    if pd.isna(x["equity_capital"])
    or pd.isna(x["reserves"])
    or (x["equity_capital"] + x["reserves"]) <= 0
    else (
        x["net_profit"] /
        (x["equity_capital"] + x["reserves"])
    ) * 100,
    axis=1
)

# ----------------------------
# Return On Capital Employed (ROCE)
# ----------------------------

ratios["roce"] = ratios.apply(
    lambda x: None
    if pd.isna(x["borrowings"])
    or pd.isna(x["equity_capital"])
    or pd.isna(x["reserves"])
    or (x["equity_capital"] + x["reserves"] + x["borrowings"]) <= 0
    else (
        x["operating_profit"] /
        (x["equity_capital"] + x["reserves"] + x["borrowings"])
    ) * 100,
    axis=1
)

# ----------------------------
# Return On Assets (ROA)
# ----------------------------

ratios["roa"] = ratios.apply(
    lambda x: None
    if pd.isna(x["total_assets"])
    or x["total_assets"] == 0
    else (x["net_profit"] / x["total_assets"]) * 100,
    axis=1
)

# ----------------------------
# ROE / ROCE Difference
# ----------------------------

ratios["roe_difference"] = (
    ratios["roe"] - ratios["roe_percentage"]
).abs()

ratios["roce_difference"] = (
    ratios["roce"] - ratios["roce_percentage"]
).abs()

ratios["roe_warning"] = ratios["roe_difference"] > 5
ratios["roce_warning"] = ratios["roce_difference"] > 5
# ----------------------------
# Existing KPIs
# ----------------------------

ratios["eps_ratio"] = ratios["eps"]
ratios["dividend_payout_ratio"] = ratios["dividend_payout"]

# ----------------------------
# Debt To Equity
# ----------------------------

ratios["debt_to_equity"] = ratios.apply(
    lambda x: 0
    if x["borrowings"] == 0
    else (
        x["borrowings"] /
        (x["equity_capital"] + x["reserves"])
    )
    if (x["equity_capital"] + x["reserves"]) > 0
    else None,
    axis=1
)

# ----------------------------
# High Leverage Flag
# ----------------------------

ratios["high_leverage_flag"] = (
    ratios["debt_to_equity"] > 5
)

# ----------------------------
# Interest Coverage Ratio
# ----------------------------

ratios["interest_coverage"] = ratios.apply(
    lambda x: None
    if x["interest"] == 0
    else (
        (x["operating_profit"] + x["other_income"]) /
        x["interest"]
    ),
    axis=1
)

# ----------------------------
# Debt Free Label
# ----------------------------

ratios["icr_label"] = ratios["interest"].apply(
    lambda x: "Debt Free"
    if x == 0
    else ""
)

# ----------------------------
# ICR Warning
# ----------------------------

ratios["icr_warning"] = ratios["interest_coverage"].apply(
    lambda x: False
    if pd.isna(x)
    else x < 1.5
)

# ----------------------------
# Net Debt
# ----------------------------

ratios["net_debt"] = (
    ratios["borrowings"] -
    ratios["investments"]
)

# ----------------------------
# Asset Turnover
# ----------------------------

ratios["asset_turnover"] = ratios.apply(
    lambda x: None
    if x["total_assets"] == 0
    else (
        x["sales"] /
        x["total_assets"]
    ),
    axis=1
)

print("Financial Ratios Calculated Successfully!")

print(
    ratios[
        [
            "company_id",
            "year",
            "net_profit_margin",
            "operating_profit_margin",
            "roe",
            "roce",
            "roa",
            "debt_to_equity",
            "interest_coverage",
            "net_debt",
            "asset_turnover"
        ]
    ].head()
)
# ----------------------------
# Save Financial Ratios
# ----------------------------

ratios_to_save = ratios[
    [
        "company_id",
        "year",
        "net_profit_margin",
        "operating_profit_margin",
        "roe",
        "roce",
        "roa",
        "debt_to_equity",
        "interest_coverage",
        "icr_label",
        "icr_warning",
        "high_leverage_flag",
        "net_debt",
        "asset_turnover",
        "eps_ratio",
        "dividend_payout_ratio"
    ]
]

# ----------------------------
# Columns to Save
# ----------------------------

ratios_to_save = ratios[
    [
        "company_id",
        "year",

        # Day 8
        "net_profit_margin",
        "operating_profit_margin",
        "roe",
        "roce",
        "roa",

        # Day 9
        "debt_to_equity",
        "high_leverage_flag",
        "interest_coverage",
        "icr_label",
        "icr_warning",
        "net_debt",
        "asset_turnover",

        # Existing
        "eps_ratio",
        "dividend_payout_ratio"
    ]
]
ratios_to_save.to_sql(
    "financial_ratios",
    connection,
    if_exists="replace",
    index=False
)

print("\nFinancial Ratios saved successfully!")

print("\nFinancial Ratios saved successfully!")

# ----------------------------
# Row Count
# ----------------------------

count = pd.read_sql(
    "SELECT COUNT(*) AS total_rows FROM financial_ratios",
    connection
)

print("\nRows in financial_ratios table:")
print(count)

# ----------------------------
# Close Database
# ----------------------------
rows = pd.read_sql(
    """
    SELECT COUNT(*) AS total_rows
    FROM financial_ratios
    """,
    connection
)

print("\nRows in financial_ratios table:")
print(rows)
connection.close()

print("\nDatabase Closed Successfully!")
print("\nDay 9 Leverage & Efficiency Ratios Completed Successfully!")