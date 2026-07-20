import pandas as pd
import os

files = [
    "documents.xlsx",
    "stock_prices.xlsx",
    "peer_groups.xlsx",
    "sectors.xlsx"
]

for file in files:
    path = os.path.join("data", file)

    df = pd.read_excel(path, header=1)

    print("\n" + "=" * 50)
    print(file)
    print(df.columns.tolist())