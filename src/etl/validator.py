import os
import pandas as pd

DATA_FOLDER = "data"
OUTPUT_FOLDER = "output"

validation_results = []


def add_result(rule, status, message):
    validation_results.append({
        "Rule": rule,
        "Status": status,
        "Message": message
    })


def load_excel(file_name):
    path = os.path.join(DATA_FOLDER, file_name)
    return pd.read_excel(path, header=1)


# -----------------------------
# Load Data
# -----------------------------

companies = load_excel("companies.xlsx")
profit = load_excel("profitandloss.xlsx")
balance = load_excel("balancesheet.xlsx")
cashflow = load_excel("cashflow.xlsx")
analysis = load_excel("analysis.xlsx")
documents = load_excel("documents.xlsx")
peer_groups = load_excel("peer_groups.xlsx")
sectors = load_excel("sectors.xlsx")
stock_prices = load_excel("stock_prices.xlsx")


# -----------------------------
# DQ-01 Company PK
# -----------------------------

if companies["id"].duplicated().sum() == 0:
    add_result("DQ-01", "PASS", "Company IDs are unique")
else:
    add_result("DQ-01", "FAIL", "Duplicate Company IDs found")


# -----------------------------
# DQ-02 (company_id, year)
# -----------------------------

duplicate_rows = profit.duplicated(
    subset=["company_id", "year"]
).sum()

if duplicate_rows == 0:
    add_result("DQ-02", "PASS", "Yearly records unique")
else:
    add_result("DQ-02", "FAIL", f"{duplicate_rows} duplicate records")


# -----------------------------
# DQ-03 Foreign Key
# -----------------------------

company_ids = set(companies["id"])

invalid_fk = profit[
    ~profit["company_id"].isin(company_ids)
]

if len(invalid_fk) == 0:
    add_result("DQ-03", "PASS", "Foreign Keys valid")
else:
    add_result("DQ-03", "FAIL", f"{len(invalid_fk)} invalid company IDs")


# -----------------------------
# DQ-04 Positive Sales
# -----------------------------

profit["sales"] = pd.to_numeric(
    profit["sales"],
    errors="coerce"
)

invalid_sales = profit[
    (profit["sales"].isna()) |
    (profit["sales"] <= 0)
]

if len(invalid_sales) == 0:
    add_result("DQ-04", "PASS", "Sales valid")
else:
    add_result("DQ-04", "FAIL", f"{len(invalid_sales)} invalid sales")


# -----------------------------
# DQ-05 Balance Sheet
# -----------------------------

balance["total_assets"] = pd.to_numeric(
    balance["total_assets"],
    errors="coerce"
)

balance["total_liabilities"] = pd.to_numeric(
    balance["total_liabilities"],
    errors="coerce"
)

difference = (
    balance["total_assets"] -
    balance["total_liabilities"]
).abs()

invalid_balance = difference > 1

if invalid_balance.sum() == 0:
    add_result("DQ-05", "PASS", "Balance Sheet matched")
else:
    add_result(
        "DQ-05",
        "FAIL",
        f"{invalid_balance.sum()} mismatched rows"
    )# -----------------------------
# DQ-06 Year Format
# -----------------------------

profit["year"] = pd.to_numeric(
    profit["year"],
    errors="coerce"
)

invalid_year = profit[
    (profit["year"].isna()) |
    (profit["year"] < 2000) |
    (profit["year"] > 2100)
]

if len(invalid_year) == 0:
    add_result("DQ-06", "PASS", "Year format valid")
else:
    add_result("DQ-06", "FAIL", f"{len(invalid_year)} invalid years")


# -----------------------------
# DQ-07 Ticker Format
# -----------------------------

invalid_ticker = companies[
    companies["id"].astype(str).str.strip() == ""
]

if len(invalid_ticker) == 0:
    add_result("DQ-07", "PASS", "Ticker format valid")
else:
    add_result("DQ-07", "FAIL", f"{len(invalid_ticker)} invalid tickers")


# -----------------------------
# DQ-08 Net Cash Flow
# -----------------------------

cashflow["operating_activity"] = pd.to_numeric(
    cashflow["operating_activity"],
    errors="coerce"
)

cashflow["investing_activity"] = pd.to_numeric(
    cashflow["investing_activity"],
    errors="coerce"
)

cashflow["financing_activity"] = pd.to_numeric(
    cashflow["financing_activity"],
    errors="coerce"
)

cashflow["net_cash_flow"] = pd.to_numeric(
    cashflow["net_cash_flow"],
    errors="coerce"
)

expected_cash = (
    cashflow["operating_activity"] +
    cashflow["investing_activity"] +
    cashflow["financing_activity"]
)

invalid_cash = (
    expected_cash -
    cashflow["net_cash_flow"]
).abs() > 1

if invalid_cash.sum() == 0:
    add_result("DQ-08", "PASS", "Net cash flow matched")
else:
    add_result("DQ-08", "FAIL", f"{invalid_cash.sum()} mismatched rows")


# -----------------------------
# DQ-09 Fixed Assets
# -----------------------------

balance["fixed_assets"] = pd.to_numeric(
    balance["fixed_assets"],
    errors="coerce"
)

invalid_assets = balance[
    balance["fixed_assets"] < 0
]

if len(invalid_assets) == 0:
    add_result("DQ-09", "PASS", "Fixed assets valid")
else:
    add_result("DQ-09", "FAIL", f"{len(invalid_assets)} negative assets")


# -----------------------------
# DQ-10 Tax Percentage
# -----------------------------

profit["tax_percentage"] = pd.to_numeric(
    profit["tax_percentage"],
    errors="coerce"
)

invalid_tax = profit[
    (profit["tax_percentage"] < 0) |
    (profit["tax_percentage"] > 100)
]

if len(invalid_tax) == 0:
    add_result("DQ-10", "PASS", "Tax percentage valid")
else:
    add_result("DQ-10", "FAIL", f"{len(invalid_tax)} invalid tax values")

    # -----------------------------
# DQ-11 Dividend Payout
# -----------------------------

profit["dividend_payout"] = pd.to_numeric(
    profit["dividend_payout"],
    errors="coerce"
)

invalid_dividend = profit[
    (profit["dividend_payout"] < 0) |
    (profit["dividend_payout"] > 100)
]

if len(invalid_dividend) == 0:
    add_result("DQ-11", "PASS", "Dividend payout valid")
else:
    add_result("DQ-11", "FAIL", f"{len(invalid_dividend)} invalid dividend values")


# -----------------------------
# DQ-12 EPS
# -----------------------------

profit["eps"] = pd.to_numeric(
    profit["eps"],
    errors="coerce"
)

invalid_eps = profit[
    profit["eps"].isna()
]

if len(invalid_eps) == 0:
    add_result("DQ-12", "PASS", "EPS values valid")
else:
    add_result("DQ-12", "FAIL", f"{len(invalid_eps)} invalid EPS values")


# -----------------------------
# DQ-13 Website URL
# -----------------------------

invalid_url = companies[
    ~companies["website"].fillna("").astype(str).str.startswith(("http://", "https://"))
]

if len(invalid_url) == 0:
    add_result("DQ-13", "PASS", "Website URLs valid")
else:
    add_result("DQ-13", "FAIL", f"{len(invalid_url)} invalid URLs")


# -----------------------------
# DQ-14 Documents URL
# -----------------------------

if "annual_report" in documents.columns:
    invalid_docs = documents[
        ~documents["annual_report"].fillna("").astype(str).str.startswith(("http://", "https://"))
    ]

    if len(invalid_docs) == 0:
        add_result("DQ-14", "PASS", "Document URLs valid")
    else:
        add_result("DQ-14", "FAIL", f"{len(invalid_docs)} invalid document URLs")
else:
    add_result("DQ-14", "SKIP", "annual_report column not found")


# -----------------------------
# DQ-15 Null Company Names
# -----------------------------

invalid_names = companies[
    companies["company_name"].isna()
]

if len(invalid_names) == 0:
    add_result("DQ-15", "PASS", "Company names available")
else:
    add_result("DQ-15", "FAIL", f"{len(invalid_names)} missing company names")


# -----------------------------
# DQ-16 Duplicate Companies
# -----------------------------

duplicate_names = companies["company_name"].duplicated().sum()

if duplicate_names == 0:
    add_result("DQ-16", "PASS", "No duplicate company names")
else:
    add_result("DQ-16", "FAIL", f"{duplicate_names} duplicate company names")


# -----------------------------
# Save Validation Report
# -----------------------------

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

results = pd.DataFrame(validation_results)

results.to_csv(
    os.path.join(OUTPUT_FOLDER, "validation_failures.csv"),
    index=False
)

print("\n========== VALIDATION REPORT ==========\n")
print(results)
print("\nValidation Completed Successfully!")
