# Nifty100 Financial Intelligence Platform

A financial analytics platform developed as part of the **Bluestock Data Analysis Internship**. The project analyzes Nifty 100 companies using ETL pipelines, financial ratios, screening engines, peer comparisons, valuation analysis, and an interactive Streamlit dashboard.

---

## Features

- ETL pipeline for loading and validating financial datasets
- SQLite database integration
- Financial ratio calculation and analysis
- Interactive Streamlit dashboard (8 modules)
- Financial screener with preset and custom filters
- Company profile and trend analysis
- Peer comparison dashboard
- Sector analysis
- Capital allocation analysis
- Valuation module with valuation flags
- CSV and Excel report generation
- Automated testing using Pytest

---

## Project Structure

```
Nifty100_Project/
│
├── config/
├── data/
├── db/
├── docs/
├── notebook/
├── output/
├── reports/
├── src/
│   ├── analytics/
│   ├── dashboard/
│   ├── etl/
│   └── screener/
├── tests/
├── requirements.txt
├── README.md
└── Makefile
```

---

## Technologies Used

- Python
- Pandas
- NumPy
- SQLite
- Streamlit
- Plotly
- Matplotlib
- OpenPyXL
- Pytest
- Git & GitHub

---

## Dashboard Modules

- Home Dashboard
- Company Profile
- Stock Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation
- Reports

---

## Outputs Generated

- `output/screener_output.xlsx`
- `output/peer_comparison.xlsx`
- `output/valuation_summary.xlsx`
- `output/valuation_flags.csv`
- SQLite database (`db/nifty100.db`)

---

## Run the Dashboard

```bash
streamlit run app.py
```

---

## Run the Valuation Module

```bash
python src/analytics/valuation.py
```

---

## Run Tests

```bash
python -m pytest
```

---

## Author

**Pavan Kumar Katkuri**


Bluestock Data Analysis Internship – Nifty100 Financial Intelligence Platform

