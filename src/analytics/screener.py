import os
import sqlite3
import pandas as pd

DB_PATH = os.path.join("db", "nifty100.db")

connection = sqlite3.connect(DB_PATH)

print("Connected to SQLite Database!")

query = """
SELECT
company_id,
year,
roe,
debt_to_equity
FROM financial_ratios
WHERE roe > 15
AND debt_to_equity < 1
ORDER BY roe DESC
"""
companies = pd.read_sql(query, connection)

print("\nTop Companies (ROCE > 20)\n")
print(companies)

connection.close()

print("\nDatabase Closed Successfully!")