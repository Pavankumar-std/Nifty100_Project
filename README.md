# Nifty100 Financial Intelligence Platform

A financial analytics platform developed as part of the **Bluestock Data Analysis Internship**. The project analyzes Nifty 100 companies using ETL pipelines, financial ratios, screening engines, peer comparisons, valuation analysis, and an interactive Streamlit dashboard.

---

## Features

- ETL pipeline for loading and validating financial datasets
- SQLite database integration
- Financial ratio calculation and analysis
- Interactive Streamlit dashboard (8 modules)
- Financial screener with custom filters
- Company profile and trend analysis
- Peer comparison dashboard
- Sector analysis
- Capital allocation analysis
- Valuation module
- CSV and Excel report generation
- Automated testing using Pytest

---

## Project Structure

```text
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
│   ├── screener/
│   └── utils/
├── tests/
├── requirements.txt
├── README.md
└── Makefile
```

---

## Technologies Used

- Python
- Streamlit
- Pandas
- NumPy
- SQLite
- Plotly
- Matplotlib
- OpenPyXL
- Pytest
- Git & GitHub

---

## Dashboard Modules

- 🏠 Home Dashboard
- 🏢 Company Profile
- 📊 Stock Screener
- 👥 Peer Comparison
- 📈 Trend Analysis
- 🏭 Sector Analysis
- 💰 Capital Allocation
- 📑 Reports

---

## Outputs

- `output/screener_output.csv`
- `output/valuation_summary.xlsx`
- `output/valuation_flags.csv`
- SQLite Database: `db/nifty100.db`

---

## Run the Dashboard

```bash
streamlit run app.py
```

---

## Run Valuation Module

```bash
python src/analytics/valuation.py
```

---

## Run Tests

```bash
python -m pytest
```

---

## Sprint 4 Deliverables

- ✅ Multi-page Streamlit Dashboard
- ✅ SQLite Database Integration
- ✅ Financial Ratio Analytics
- ✅ Company Profile Dashboard
- ✅ Stock Screener
- ✅ Peer Comparison
- ✅ Trend Analysis
- ✅ Sector Analysis
- ✅ Capital Allocation Dashboard
- ✅ Reports Dashboard
- ✅ Valuation Module
- ✅ README Documentation

---

## Author

**Pavan Kumar Katkuri**

Bluestock Data Analysis Internship  
Nifty100 Financial Intelligence Platform