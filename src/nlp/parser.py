import pandas as pd
import re
import os


INPUT = "data/analysis.xlsx"

OUTPUT = "output/analysis_parsed.csv"
FAIL = "output/parse_failures.csv"


def parse_text(value):

    pattern = r"(\d+)\s*Years?:?\s*([\d.]+)%"

    match = re.search(pattern, str(value))

    if match:
        return int(match.group(1)), float(match.group(2))

    return None, None


def main():

    os.makedirs("output", exist_ok=True)

    df = pd.read_excel(INPUT)

    results = []
    failures = []


    for _, row in df.iterrows():

        company = row.iloc[0]

        for col in df.columns[1:]:

            years, value = parse_text(row[col])

            if value:

                results.append({
                    "company_id": company,
                    "metric_type": col,
                    "period_years": years,
                    "value_pct": value
                })

            else:

                failures.append({
                    "company_id": company,
                    "metric_type": col,
                    "text": row[col]
                })


    pd.DataFrame(results).to_csv(
        OUTPUT,
        index=False
    )

    pd.DataFrame(failures).to_csv(
        FAIL,
        index=False
    )


    print("Parser completed")
    print("Parsed:",len(results))


if __name__=="__main__":
    main()