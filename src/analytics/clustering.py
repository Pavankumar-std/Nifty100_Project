import os
import sqlite3
import warnings

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

warnings.filterwarnings("ignore")

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
    """
    Clean dataframe column names.
    """
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
    )
    return df


def find_column(df, possible_names):
    """
    Find the first matching column from possible names.
    """
    for name in possible_names:
        name = name.lower().replace(" ", "_").replace("-", "_")
        if name in df.columns:
            return name

    return None


def to_numeric(series):
    """
    Convert values safely to numeric.
    """
    return pd.to_numeric(series, errors="coerce")


# ============================================================
# LOAD DATABASE TABLES
# ============================================================

print("Loading database...")

conn = sqlite3.connect(DB)

tables = pd.read_sql(
    "SELECT name FROM sqlite_master WHERE type='table'",
    conn
)

print("\nAvailable tables:")
print(tables["name"].tolist())

# Load companies
companies = pd.read_sql(
    'SELECT * FROM "companies"',
    conn
)

# Find financial ratios table automatically
ratio_table = None

for table_name in tables["name"].tolist():
    if table_name.lower().replace(" ", "_") == "financial_ratios":
        ratio_table = table_name
        break

if ratio_table is None:
    conn.close()
    raise ValueError("Financial ratios table not found!")

ratios = pd.read_sql(
    f'SELECT * FROM "{ratio_table}"',
    conn
)

# Load CAGR results if available
cagr_table = None

for table_name in tables["name"].tolist():
    if table_name.lower().replace(" ", "_") == "cagr_results":
        cagr_table = table_name
        break

if cagr_table is not None:
    cagr = pd.read_sql(
        f'SELECT * FROM "{cagr_table}"',
        conn
    )
else:
    print("\nWARNING: CAGR results table not found.")
    cagr = pd.DataFrame()

# Load cashflow intelligence if available
cashflow_intelligence_path = "output/cashflow_intelligence.xlsx"

conn.close()


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

companies = clean_columns(companies)
ratios = clean_columns(ratios)

if not cagr.empty:
    cagr = clean_columns(cagr)

print("\nCompanies columns:")
print(companies.columns.tolist())

print("\nFinancial ratios columns:")
print(ratios.columns.tolist())

if not cagr.empty:
    print("\nCAGR columns:")
    print(cagr.columns.tolist())


# ============================================================
# IDENTIFY COMPANY ID COLUMN
# ============================================================

company_id_col_companies = find_column(
    companies,
    ["company_id", "id"]
)

company_id_col_ratios = find_column(
    ratios,
    ["company_id", "id"]
)

if company_id_col_companies is None:
    raise ValueError("Company ID column not found in companies table!")

if company_id_col_ratios is None:
    raise ValueError("Company ID column not found in financial ratios!")

# Standardize company IDs
companies["company_id"] = (
    companies[company_id_col_companies]
    .astype(str)
    .str.strip()
)

ratios["company_id"] = (
    ratios[company_id_col_ratios]
    .astype(str)
    .str.strip()
)


# ============================================================
# FIND SECTOR COLUMN
# ============================================================

sector_col = find_column(
    companies,
    [
        "broad_sector",
        "sector",
        "industry",
        "sub_sector"
    ]
)

if sector_col is None:
    print("\nWARNING: Sector column not found.")
    companies["sector"] = "Unknown"
    sector_col = "sector"

print(f"\nUsing sector column: {sector_col}")


# ============================================================
# GET LATEST YEAR FOR EACH COMPANY
# ============================================================

year_col = find_column(
    ratios,
    ["year", "financial_year"]
)

if year_col is None:
    raise ValueError("Year column not found in financial ratios!")

# Create sortable year value
ratios["_year_sort"] = (
    ratios[year_col]
    .astype(str)
    .str.extract(r"(\d{4})")[0]
)

ratios["_year_sort"] = pd.to_numeric(
    ratios["_year_sort"],
    errors="coerce"
)

# Keep latest valid year per company
latest_ratios = (
    ratios
    .sort_values("_year_sort")
    .groupby("company_id", as_index=False)
    .tail(1)
)

print(f"\nLatest ratio rows: {len(latest_ratios)}")


# ============================================================
# CREATE BASE DATASET
# ============================================================

features = companies[
    ["company_id", sector_col]
].copy()

features = features.rename(
    columns={
        sector_col: "sector"
    }
)

features["sector"] = features["sector"].fillna("Unknown").astype(str)


# ============================================================
# GET ROE
# ============================================================

roe_col = find_column(
    latest_ratios,
    [
        "return_on_equity_pct",
        "roe",
        "roe_pct"
    ]
)

if roe_col is None:
    raise ValueError("ROE column not found!")

latest_ratios["roe_feature"] = to_numeric(
    latest_ratios[roe_col]
)


# ============================================================
# GET DEBT TO EQUITY
# ============================================================

de_col = find_column(
    latest_ratios,
    [
        "debt_to_equity",
        "debt_to_equity_ratio",
        "de_ratio",
        "d_e"
    ]
)

if de_col is None:
    raise ValueError("Debt to Equity column not found!")

latest_ratios["de_feature"] = to_numeric(
    latest_ratios[de_col]
)


# ============================================================
# GET OPERATING PROFIT MARGIN
# ============================================================

opm_col = find_column(
    latest_ratios,
    [
        "operating_profit_margin_pct",
        "operating_profit_margin",
        "opm",
        "opm_pct"
    ]
)

if opm_col is None:
    raise ValueError("Operating Profit Margin column not found!")

latest_ratios["opm_feature"] = to_numeric(
    latest_ratios[opm_col]
)


# ============================================================
# MERGE RATIO FEATURES
# ============================================================

ratio_features = latest_ratios[
    [
        "company_id",
        "roe_feature",
        "de_feature",
        "opm_feature"
    ]
].copy()

features = features.merge(
    ratio_features,
    on="company_id",
    how="left"
)


# ============================================================
# REVENUE CAGR AND FCF CAGR
# ============================================================

features["revenue_cagr_5yr"] = np.nan
features["fcf_cagr_5yr"] = np.nan


# ============================================================
# LOAD CAGR RESULTS IF AVAILABLE
# ============================================================

if not cagr.empty:

    cagr_company_col = find_column(
        cagr,
        ["company_id", "id"]
    )

    if cagr_company_col is not None:

        cagr["company_id"] = (
            cagr[cagr_company_col]
            .astype(str)
            .str.strip()
        )

        revenue_cagr_col = find_column(
            cagr,
            [
                "revenue_cagr_5yr",
                "sales_cagr_5yr",
                "sales_cagr",
                "revenue_cagr"
            ]
        )

        fcf_cagr_col = find_column(
            cagr,
            [
                "fcf_cagr_5yr",
                "free_cash_flow_cagr_5yr",
                "fcf_cagr"
            ]
        )

        if revenue_cagr_col is not None:

            revenue_data = cagr[
                ["company_id", revenue_cagr_col]
            ].copy()

            revenue_data = revenue_data.rename(
                columns={
                    revenue_cagr_col: "revenue_cagr_from_table"
                }
            )

            revenue_data[
                "revenue_cagr_from_table"
            ] = to_numeric(
                revenue_data[
                    "revenue_cagr_from_table"
                ]
            )

            features = features.merge(
                revenue_data,
                on="company_id",
                how="left"
            )

            features["revenue_cagr_5yr"] = (
                features[
                    "revenue_cagr_from_table"
                ]
            )

            features.drop(
                columns=["revenue_cagr_from_table"],
                inplace=True
            )

        if fcf_cagr_col is not None:

            fcf_data = cagr[
                ["company_id", fcf_cagr_col]
            ].copy()

            fcf_data = fcf_data.rename(
                columns={
                    fcf_cagr_col: "fcf_cagr_from_table"
                }
            )

            fcf_data[
                "fcf_cagr_from_table"
            ] = to_numeric(
                fcf_data[
                    "fcf_cagr_from_table"
                ]
            )

            features = features.merge(
                fcf_data,
                on="company_id",
                how="left"
            )

            features["fcf_cagr_5yr"] = (
                features[
                    "fcf_cagr_from_table"
                ]
            )

            features.drop(
                columns=["fcf_cagr_from_table"],
                inplace=True
            )


# ============================================================
# TRY CASHFLOW INTELLIGENCE FOR FCF CAGR
# ============================================================

if os.path.exists(cashflow_intelligence_path):

    try:

        cashflow_intelligence = pd.read_excel(
            cashflow_intelligence_path
        )

        cashflow_intelligence = clean_columns(
            cashflow_intelligence
        )

        cf_company_col = find_column(
            cashflow_intelligence,
            ["company_id", "id"]
        )

        fcf_cagr_col = find_column(
            cashflow_intelligence,
            [
                "fcf_cagr_5yr",
                "free_cash_flow_cagr_5yr"
            ]
        )

        if (
            cf_company_col is not None
            and fcf_cagr_col is not None
        ):

            cf_data = cashflow_intelligence[
                [
                    cf_company_col,
                    fcf_cagr_col
                ]
            ].copy()

            cf_data.columns = [
                "company_id",
                "fcf_cagr_from_cashflow"
            ]

            cf_data["company_id"] = (
                cf_data["company_id"]
                .astype(str)
                .str.strip()
            )

            cf_data[
                "fcf_cagr_from_cashflow"
            ] = to_numeric(
                cf_data[
                    "fcf_cagr_from_cashflow"
                ]
            )

            features = features.merge(
                cf_data,
                on="company_id",
                how="left"
            )

            features["fcf_cagr_5yr"] = (
                features[
                    "fcf_cagr_5yr"
                ]
                .fillna(
                    features[
                        "fcf_cagr_from_cashflow"
                    ]
                )
            )

            features.drop(
                columns=[
                    "fcf_cagr_from_cashflow"
                ],
                inplace=True
            )

    except Exception as e:
        print(
            "\nCould not load cashflow intelligence:",
            e
        )


# ============================================================
# FINAL FEATURE COLUMNS
# ============================================================

feature_columns = [
    "roe_feature",
    "de_feature",
    "revenue_cagr_5yr",
    "fcf_cagr_5yr",
    "opm_feature"
]


# ============================================================
# CLEAN ALL FEATURES
# ============================================================

print("\nMissing values BEFORE cleaning:")

print(
    features[
        feature_columns
    ].isna().sum()
)

# Replace infinite values
features[
    feature_columns
] = features[
    feature_columns
].replace(
    [np.inf, -np.inf],
    np.nan
)

# Convert everything to numeric again
for col in feature_columns:

    features[col] = pd.to_numeric(
        features[col],
        errors="coerce"
    )


# ============================================================
# SECTOR MEDIAN IMPUTATION
# ============================================================

for col in feature_columns:

    sector_median = (
        features
        .groupby("sector")[col]
        .transform("median")
    )

    features[col] = (
        features[col]
        .fillna(sector_median)
    )


# ============================================================
# OVERALL MEDIAN IMPUTATION
# ============================================================

for col in feature_columns:

    overall_median = (
        features[col].median()
    )

    features[col] = (
        features[col]
        .fillna(overall_median)
    )


# ============================================================
# FINAL SAFETY: FILL ANY REMAINING NAN WITH ZERO
# ============================================================

features[
    feature_columns
] = features[
    feature_columns
].fillna(0)

# Replace infinity again just to be safe
features[
    feature_columns
] = features[
    feature_columns
].replace(
    [np.inf, -np.inf],
    0
)


# ============================================================
# VERIFY DATA
# ============================================================

print("\nMissing values AFTER cleaning:")

print(
    features[
        feature_columns
    ].isna().sum()
)

print("\nFeature preview:")

print(
    features[
        [
            "company_id",
            "sector"
        ] + feature_columns
    ].head()
)

# Final check
if features[
    feature_columns
].isna().any().any():

    raise ValueError(
        "NaN values still exist in clustering data!"
    )


# ============================================================
# STANDARD SCALING
# ============================================================

X = features[
    feature_columns
].copy()

scaler = StandardScaler()

X_scaled = scaler.fit_transform(X)

# Safety check
if np.isnan(X_scaled).any():

    raise ValueError(
        "NaN values found after scaling!"
    )

if np.isinf(X_scaled).any():

    raise ValueError(
        "Infinite values found after scaling!"
    )


# ============================================================
# ELBOW PLOT
# ============================================================

print("\nGenerating elbow plot...")

inertias = []

k_values = range(2, 11)

for k in k_values:

    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    model.fit(X_scaled)

    inertias.append(
        model.inertia_
    )


plt.figure(figsize=(8, 5))

plt.plot(
    list(k_values),
    inertias,
    marker="o"
)

plt.title(
    "KMeans Elbow Plot"
)

plt.xlabel(
    "Number of Clusters (K)"
)

plt.ylabel(
    "Inertia"
)

plt.xticks(
    list(k_values)
)

plt.grid(True)

plt.tight_layout()

plt.savefig(
    os.path.join(
        REPORTS_DIR,
        "elbow_plot.png"
    ),
    dpi=300
)

plt.close()

print(
    "Saved: reports/elbow_plot.png"
)


# ============================================================
# KMEANS CLUSTERING
# ============================================================

print("\nRunning KMeans clustering...")

model = KMeans(
    n_clusters=5,
    random_state=42,
    n_init=10
)

features["cluster_id"] = model.fit_predict(
    X_scaled
)


# ============================================================
# DISTANCE FROM CENTROID
# ============================================================

centers = model.cluster_centers_

distances = []

for i in range(len(X_scaled)):

    cluster = features.iloc[i]["cluster_id"]

    centroid = centers[int(cluster)]

    distance = np.linalg.norm(
        X_scaled[i] - centroid
    )

    distances.append(
        round(float(distance), 4)
    )

features[
    "distance_from_centroid"
] = distances


# ============================================================
# CLUSTER PROFILING
# ============================================================

profile = (
    features
    .groupby("cluster_id")[
        feature_columns
    ]
    .mean()
)

print("\nCluster Profile:")

print(profile)


# ============================================================
# ASSIGN CLUSTER NAMES
# ============================================================

cluster_scores = {}

for cluster_id, row in profile.iterrows():

    score = (
        row["roe_feature"]
        + row["revenue_cagr_5yr"]
        + row["fcf_cagr_5yr"]
        + row["opm_feature"]
        - row["de_feature"]
    )

    cluster_scores[
        cluster_id
    ] = score


sorted_clusters = sorted(
    cluster_scores,
    key=cluster_scores.get,
    reverse=True
)

cluster_names = {}

if len(sorted_clusters) >= 5:

    cluster_names[
        sorted_clusters[0]
    ] = "High-Quality Compounders"

    cluster_names[
        sorted_clusters[1]
    ] = "Emerging Growth"

    cluster_names[
        sorted_clusters[2]
    ] = "Defensive Dividend Payers"

    cluster_names[
        sorted_clusters[3]
    ] = "Value Cyclicals"

    cluster_names[
        sorted_clusters[4]
    ] = "Distressed or Turnaround"


features[
    "cluster_name"
] = features[
    "cluster_id"
].map(cluster_names)


# ============================================================
# GET COMPANY NAMES
# ============================================================

company_name_col = find_column(
    companies,
    [
        "company_name",
        "name"
    ]
)

if company_name_col is not None:

    names = companies[
        [
            "company_id",
            company_name_col
        ]
    ].copy()

    names = names.rename(
        columns={
            company_name_col:
            "company_name"
        }
    )

    features = features.merge(
        names,
        on="company_id",
        how="left"
    )

else:

    features[
        "company_name"
    ] = features[
        "company_id"
    ]


# ============================================================
# SAVE CLUSTER LABELS
# ============================================================

output = features[
    [
        "company_id",
        "company_name",
        "cluster_id",
        "cluster_name",
        "distance_from_centroid"
    ]
].copy()

output.to_csv(
    os.path.join(
        OUTPUT_DIR,
        "cluster_labels.csv"
    ),
    index=False
)

print(
    "\nSaved: output/cluster_labels.csv"
)

print(
    f"Total companies clustered: {len(output)}"
)

print("\nCluster distribution:")

print(
    output[
        "cluster_name"
    ].value_counts()
)

print(
    "\nKMeans clustering completed successfully!"
)