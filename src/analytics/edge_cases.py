import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join("db", "nifty100.db")

connection = sqlite3.connect(DB_PATH)

print("Connected to SQLite Database!")

companies = pd.read_sql(
    "SELECT * FROM companies",
    connection
)

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    connection
)

print("Companies :", len(companies))
print("Financial Ratios :", len(ratios))


# --------------------------------
# Merge ROE & ROCE
# --------------------------------

merged = ratios.merge(
    companies[
        [
            "id",
            "company_name",
            "roe_percentage",
            "roce_percentage"
        ]
    ],
    left_on="company_id",
    right_on="id",
    how="left"
)

print("\nComparing ROE and ROCE...\n")
# --------------------------------
# ROE Difference
# --------------------------------

merged["roe_difference"] = (
    merged["roe"] -
    merged["roe_percentage"]
).abs()

# --------------------------------
# ROCE Difference
# --------------------------------

merged["roce_difference"] = (
    merged["roce"] -
    merged["roce_percentage"]
).abs()

# --------------------------------
# Find Edge Cases
# --------------------------------

edge_cases = merged[
    (merged["roe_difference"] > 5) |
    (merged["roce_difference"] > 5)
].copy()

print("Edge Cases Found :", len(edge_cases))

# --------------------------------
# Categorise
# --------------------------------

def category(row):

    if row["roe_difference"] > 5:
        return "Formula Difference"

    if row["roce_difference"] > 5:
        return "Source Difference"

    return "OK"


edge_cases["category"] = edge_cases.apply(
    category,
    axis=1
)

# --------------------------------
# Save Log
# --------------------------------

os.makedirs("output", exist_ok=True)

edge_cases.to_csv(
    "output/ratio_edge_cases.log",
    index=False
)

print("\nEdge Case Log Created Successfully!")

print(edge_cases[
    [
        "company_id",
        "company_name",
        "roe_difference",
        "roce_difference",
        "category"
    ]
].head())

connection.close()

print("\nDatabase Closed Successfully!")
print("Day 13 Completed Successfully!")