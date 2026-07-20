import os
import sqlite3
import pandas as pd

# ----------------------------
# Paths
# ----------------------------

DATA_FOLDER = "data"
DB_FOLDER = "db"
OUTPUT_FOLDER = "output"

DB_NAME = "nifty100.db"
SCHEMA_FILE = "schema.sql"

os.makedirs(DB_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

db_path = os.path.join(DB_FOLDER, DB_NAME)
schema_path = os.path.join(DB_FOLDER, SCHEMA_FILE)

# ----------------------------
# Excel Files
# ----------------------------

excel_files = [
    "companies.xlsx",
    "analysis.xlsx",
    "balancesheet.xlsx",
    "cashflow.xlsx",
    "documents.xlsx",
    "profitandloss.xlsx",
    "prosandcons.xlsx",
    "financial_ratios.xlsx",
    "market_cap.xlsx",
    "peer_groups.xlsx",
    "sectors.xlsx",
    "stock_prices.xlsx"
]

# ----------------------------
# Create Database
# ----------------------------

if os.path.exists(db_path):
    os.remove(db_path)

connection = sqlite3.connect(db_path)

print("SQLite Database Created Successfully!")

# ----------------------------
# Execute Schema
# ----------------------------

with open(schema_path, "r", encoding="utf-8") as f:
    connection.executescript(f.read())

print("Database Schema Created Successfully!")

load_audit = []

# ----------------------------
# Load All Excel Files
# ----------------------------

print("\nLoading Excel Files...\n")

for file in excel_files:

    file_path = os.path.join(DATA_FOLDER, file)

    if not os.path.exists(file_path):
        print(f"{file} : NOT FOUND")

        load_audit.append({
            "File": file,
            "Status": "FAIL",
            "Rows": 0,
            "Message": "File Not Found"
        })
        continue

    try:
        df = pd.read_excel(file_path, header=1)

        # Table name
        table_name = file.replace(".xlsx", "")

        # Remove empty rows
        df = df.dropna(how="all")

        # Clean column names
        df.columns = [str(col).strip().lower().replace(" ", "_") for col in df.columns]

        # Remove unnamed columns
        df = df.loc[:, ~df.columns.str.contains("^unnamed", case=False)]

        # Remove duplicate columns
        df = df.loc[:, ~df.columns.duplicated()]

        # Load into SQLite
        df.to_sql(
            table_name,
            connection,
            if_exists="replace",
            index=False
        )

        print(f"{table_name} loaded successfully ({len(df)} rows)")

        load_audit.append({
            "File": file,
            "Status": "PASS",
            "Rows": len(df),
            "Message": "Loaded Successfully"
        })

    except Exception as e:
        print(f"{file} FAILED : {e}")

        load_audit.append({
            "File": file,
            "Status": "FAIL",
            "Rows": 0,
            "Message": str(e)
        })

# ----------------------------
# Save Load Audit
# ----------------------------

audit_df = pd.DataFrame(load_audit)

audit_df.to_csv(
    os.path.join(OUTPUT_FOLDER, "load_audit.csv"),
    index=False
)

print("\n========== LOAD SUMMARY ==========")
print(audit_df)

print("\nTotal Files :", len(audit_df))
print("Passed      :", len(audit_df[audit_df["Status"] == "PASS"]))
print("Failed      :", len(audit_df[audit_df["Status"] == "FAIL"]))

connection.close()

print("\nDatabase Closed Successfully!")
print("Day 5 Completed Successfully!")