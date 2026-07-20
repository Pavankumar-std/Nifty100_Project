import math


def calculate_cagr(start_value, end_value, years):
    """
    Calculate CAGR with edge-case handling.
    Returns:
        (value, flag)
    """

    if years <= 0:
        return None, "INVALID_PERIOD"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value > 0 and end_value > 0:
        cagr = (
            (end_value / start_value) ** (1 / years) - 1
        ) * 100

        return round(cagr, 2), "NORMAL"

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    return None, "UNKNOWN"
import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join("db", "nifty100.db")

connection = sqlite3.connect(DB_PATH)

print("Connected to SQLite Database!")

profit = pd.read_sql(
    "SELECT company_id, year, sales, net_profit, eps FROM profitandloss",
    connection
)

print("Profit & Loss Loaded :", len(profit))
print("\nCalculating CAGR Metrics...\n")

results = []

for company in profit["company_id"].unique():

    company_data = (
        profit[profit["company_id"] == company]
        .sort_values("year")
        .reset_index(drop=True)
    )

    if len(company_data) < 2:
        continue

    start_row = company_data.iloc[0]
    end_row = company_data.iloc[-1]

    years = len(company_data) - 1

    # -------------------------
    # Revenue CAGR
    # -------------------------

    revenue_cagr, revenue_flag = calculate_cagr(
        start_row["sales"],
        end_row["sales"],
        years
    )

    # -------------------------
    # PAT CAGR
    # -------------------------

    pat_cagr, pat_flag = calculate_cagr(
        start_row["net_profit"],
        end_row["net_profit"],
        years
    )

    # -------------------------
    # EPS CAGR
    # -------------------------

    eps_cagr, eps_flag = calculate_cagr(
        start_row["eps"],
        end_row["eps"],
        years
    )

    results.append({
        "company_id": company,
        "years": years,

        "revenue_cagr": revenue_cagr,
        "revenue_flag": revenue_flag,

        "pat_cagr": pat_cagr,
        "pat_flag": pat_flag,

        "eps_cagr": eps_cagr,
        "eps_flag": eps_flag
    })

cagr_df = pd.DataFrame(results)

print(cagr_df.head(10))

print("\nTotal Companies Processed :", len(cagr_df))
cagr_df.to_sql(
    "cagr_results",
    connection,
    if_exists="replace",
    index=False
)

print("\nCAGR Results saved successfully!")
connection.close()

print("\nDatabase Closed Successfully!")
print("\nDay 10 CAGR Engine Completed Successfully!")