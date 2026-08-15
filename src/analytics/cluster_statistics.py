import os
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# CONFIG
# ============================================================

DB = "db/nifty100.db"

OUTPUT_DIR = "output"
REPORTS_DIR = "reports"

os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(REPORTS_DIR, exist_ok=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def clean_columns(df):
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def find_column(df, possible_names):
    for name in possible_names:
        name = name.lower().replace(" ", "_").replace("-", "_")

        if name in df.columns:
            return name

    return None


def to_numeric(series):
    return pd.to_numeric(series, errors="coerce")


# ============================================================
# LOAD DATA
# ============================================================

print("Loading database...")

conn = sqlite3.connect(DB)

companies = pd.read_sql(
    'SELECT * FROM "companies"',
    conn
)

tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table'",
    conn
)

ratio_table = None

for table in tables["name"].tolist():

    if table.lower().replace(" ", "_") == "financial_ratios":
        ratio_table = table
        break


if ratio_table is None:
    raise ValueError("Financial ratios table not found!")


ratios = pd.read_sql(
    f'SELECT * FROM "{ratio_table}"',
    conn
)

conn.close()


# ============================================================
# CLEAN DATA
# ============================================================

companies = clean_columns(companies)
ratios = clean_columns(ratios)

company_id_companies = find_column(
    companies,
    ["company_id", "id"]
)

company_id_ratios = find_column(
    ratios,
    ["company_id", "id"]
)

companies["company_id"] = (
    companies[company_id_companies]
    .astype(str)
    .str.strip()
)

ratios["company_id"] = (
    ratios[company_id_ratios]
    .astype(str)
    .str.strip()
)


# ============================================================
# SECTOR
# ============================================================

sector_col = find_column(
    companies,
    [
        "broad_sector",
        "sector",
        "industry"
    ]
)

if sector_col is None:
    companies["sector"] = "Unknown"
    sector_col = "sector"


# ============================================================
# GET LATEST YEAR
# ============================================================

year_col = find_column(
    ratios,
    ["year"]
)

ratios["_year_sort"] = (
    ratios[year_col]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
)

ratios["_year_sort"] = pd.to_numeric(
    ratios["_year_sort"],
    errors="coerce"
)

latest = (
    ratios
    .sort_values("_year_sort")
    .groupby("company_id", as_index=False)
    .tail(1)
)

print("Latest company records:", len(latest))


# ============================================================
# SELECT KPI COLUMNS
# ============================================================

possible_kpis = {
    "roe": ["roe", "return_on_equity_pct"],
    "roce": ["roce", "return_on_capital_employed"],
    "roa": ["roa", "return_on_assets"],
    "net_profit_margin": [
        "net_profit_margin",
        "net_profit_margin_pct"
    ],
    "operating_profit_margin": [
        "operating_profit_margin",
        "operating_profit_margin_pct",
        "opm"
    ],
    "debt_to_equity": [
        "debt_to_equity",
        "de_ratio"
    ],
    "interest_coverage": [
        "interest_coverage",
        "icr"
    ],
    "net_debt": [
        "net_debt"
    ],
    "asset_turnover": [
        "asset_turnover"
    ],
    "dividend_payout_ratio": [
        "dividend_payout_ratio"
    ]
}


kpi_data = pd.DataFrame()

kpi_data["company_id"] = latest["company_id"]

for output_name, options in possible_kpis.items():

    column = find_column(
        latest,
        options
    )

    if column is not None:

        kpi_data[output_name] = to_numeric(
            latest[column]
        )


# ============================================================
# ADD SECTOR
# ============================================================

sector_data = companies[
    [
        "company_id",
        sector_col
    ]
].copy()

sector_data = sector_data.rename(
    columns={
        sector_col: "sector"
    }
)

sector_data["sector"] = (
    sector_data["sector"]
    .fillna("Unknown")
)

data = kpi_data.merge(
    sector_data,
    on="company_id",
    how="left"
)


# ============================================================
# REMOVE INVALID VALUES
# ============================================================

numeric_columns = [
    col
    for col in data.columns
    if col not in ["company_id", "sector"]
]

for col in numeric_columns:

    data[col] = pd.to_numeric(
        data[col],
        errors="coerce"
    )

    data[col] = data[col].replace(
        [np.inf, -np.inf],
        np.nan
    )


# ============================================================
# FILL MISSING VALUES
# ============================================================

for col in numeric_columns:

    sector_median = (
        data
        .groupby("sector")[col]
        .transform("median")
    )

    data[col] = data[col].fillna(
        sector_median
    )

    data[col] = data[col].fillna(
        data[col].median()
    )

    data[col] = data[col].fillna(0)


print("\nData ready for analysis.")
print(data.head())


# ============================================================
# 1. CORRELATION HEATMAP
# ============================================================

print("\nGenerating correlation heatmap...")

correlation_data = data[
    numeric_columns
].copy()

correlation = correlation_data.corr(
    method="pearson"
)

plt.figure(
    figsize=(12, 9)
)

sns.heatmap(
    correlation,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    square=True
)

plt.title(
    "Financial KPI Correlation Matrix"
)

plt.tight_layout()

plt.savefig(
    os.path.join(
        REPORTS_DIR,
        "correlation_heatmap.png"
    ),
    dpi=300
)

plt.close()

print(
    "Saved: reports/correlation_heatmap.png"
)


# ============================================================
# 2. OUTLIER DETECTION
# ============================================================

print("\nDetecting outliers...")

outliers = []

for sector in data["sector"].unique():

    sector_df = data[
        data["sector"] == sector
    ].copy()

    for col in numeric_columns:

        mean = sector_df[col].mean()

        std = sector_df[col].std()

        if std == 0 or pd.isna(std):
            continue

        sector_df[f"{col}_zscore"] = (
            sector_df[col] - mean
        ) / std

        flagged = sector_df[
            sector_df[f"{col}_zscore"].abs() > 3
        ]

        for _, row in flagged.iterrows():

            outliers.append(
                {
                    "company_id": row["company_id"],
                    "sector": sector,
                    "metric": col,
                    "value": row[col],
                    "z_score": round(
                        row[f"{col}_zscore"],
                        2
                    )
                }
            )


outlier_df = pd.DataFrame(outliers)

if outlier_df.empty:

    outlier_df = pd.DataFrame(
        columns=[
            "company_id",
            "sector",
            "metric",
            "value",
            "z_score"
        ]
    )


outlier_df.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "outlier_report.csv"
    ),
    index=False
)

print(
    "Saved: output/outlier_report.csv"
)

print(
    "Total outliers found:",
    len(outlier_df)
)


# ============================================================
# 3. PORTFOLIO STATISTICS
# ============================================================

print("\nGenerating portfolio statistics...")

statistics = []

for col in numeric_columns:

    values = data[col].dropna()

    statistics.append(
        {
            "metric": col,
            "P10": values.quantile(0.10),
            "P25": values.quantile(0.25),
            "P50": values.quantile(0.50),
            "P75": values.quantile(0.75),
            "P90": values.quantile(0.90),
            "Mean": values.mean(),
            "Std": values.std()
        }
    )


portfolio_stats = pd.DataFrame(
    statistics
)

portfolio_stats = portfolio_stats.round(2)

portfolio_stats.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "portfolio_stats.csv"
    ),
    index=False
)

print(
    "Saved: output/portfolio_stats.csv"
)

print(portfolio_stats)


# ============================================================
# 4. CLUSTER PROFILE
# ============================================================

print("\nGenerating cluster profile...")

cluster_file = os.path.join(
    OUTPUT_DIR,
    "cluster_labels.csv"
)

if os.path.exists(cluster_file):

    clusters = pd.read_csv(
        cluster_file
    )

    clusters["company_id"] = (
        clusters["company_id"]
        .astype(str)
        .str.strip()
    )

    cluster_data = data.merge(
        clusters[
            [
                "company_id",
                "cluster_id",
                "cluster_name"
            ]
        ],
        on="company_id",
        how="left"
    )

    cluster_profile = (
        cluster_data
        .groupby(
            [
                "cluster_id",
                "cluster_name"
            ]
        )[numeric_columns]
        .agg(
            ["mean", "median"]
        )
    )

    cluster_profile.to_csv(
        os.path.join(
            OUTPUT_DIR,
            "cluster_profile.csv"
        )
    )

    print(
        "Saved: output/cluster_profile.csv"
    )

else:

    print(
        "WARNING: cluster_labels.csv not found."
    )


# ============================================================
# COMPLETE
# ============================================================

print("\n===================================")
print("DAY 37 COMPLETED SUCCESSFULLY")
print("===================================")

print("\nGenerated files:")

print(
    "1. reports/correlation_heatmap.png"
)

print(
    "2. output/outlier_report.csv"
)

print(
    "3. output/portfolio_stats.csv"
)

print(
    "4. output/cluster_profile.csv"
)