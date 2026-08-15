# Nifty100 Financial Intelligence Platform

A complete financial analytics platform developed during the **Bluestock Data Analysis Internship**.

The project analyzes Nifty 100 companies using ETL pipelines, financial ratios, valuation models, cash flow intelligence, clustering, NLP-generated insights, PDF reports, a Streamlit dashboard, and a FastAPI-based Financial Intelligence API.

---

# Features

- ETL Data Pipeline
- SQLite Database
- Financial Ratio Engine
- KMeans Company Clustering
- 8-Page Streamlit Dashboard
- Company Profile
- Stock Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation Dashboard
- Annual Reports Viewer
- Valuation Engine
- Cash Flow Intelligence
- NLP Pros & Cons Generator
- Company Tearsheet PDFs
- Sector Reports
- Portfolio Summary Report
- CSV & Excel Export
- FastAPI Financial Intelligence API
- Health Monitoring API
- Company Search API
- Financial Screener API
- Sector-wise Analysis API
- Automated Testing

---

# Technologies Used

- Python
- Pandas
- NumPy
- Scikit-learn
- SQLite
- FastAPI
- Uvicorn
- Streamlit
- Plotly
- Matplotlib
- ReportLab
- OpenPyXL
- Pytest
- Git & GitHub

---

# Project Structure

```text
Nifty100_Project/
│
├── data/
├── db/
│   └── nifty100.db
│
├── src/
│   ├── analytics/
│   ├── api/
│   │   ├── main.py
│   │   └── routers/
│   ├── dashboard/
│   │   ├── app.py
│   │   └── utils/
│   ├── etl/
│   ├── nlp/
│   └── reports/
│
├── tests/
├── output/
├── reports/
├── requirements.txt
└── README.md
```

---

# Dashboard Modules

- Home Dashboard
- Company Profile
- Stock Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation
- Reports

---

# Analytics Modules

- Financial Ratio Engine
- Valuation Engine
- Cash Flow Intelligence
- Capital Allocation Analysis
- CAGR Analysis
- Company Clustering

---

# FastAPI Modules

The project includes a REST API for accessing financial intelligence data.

Available modules include:

- Health API
- Companies API
- Stock Screener API
- Sector Analysis API
- Sector-wise Company API

Run the API using:

```bash
uvicorn src.api.main:app --reload --port 8000
```

Open the API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# NLP Modules

- Analysis Text Parser
- Auto Pros & Cons Generator

---

# Report Modules

- Company Tearsheet PDF
- Sector Reports
- Portfolio Summary Report

---

# Output Files

- analysis_parsed.csv
- parse_failures.csv
- pros_cons_generated.csv
- valuation_summary.xlsx
- valuation_flags.csv
- cashflow_intelligence.xlsx
- distress_alerts.csv
- pattern_changes.csv
- portfolio_summary.pdf

---

# Run Dashboard

```bash
streamlit run src/dashboard/app.py
```

---

# Run Analytics

```bash
python src/analytics/valuation.py
python src/analytics/cashflow_kpis.py
python src/analytics/clustering.py
```

---

# Run NLP

```bash
python src/nlp/parser.py
python src/nlp/pros_cons_generator.py
```

---

# Run Reports

```bash
python src/reports/tearsheet.py
python src/reports/sector_report.py
python src/reports/portfolio_report.py
```

---

# Run Tests

Run the complete automated test suite:

```bash
python -m pytest tests -v
```

## Test Results

**98 tests passed with 0 failures.**

---

# Project Highlights

- 92 Nifty100 Companies
- Interactive Streamlit Dashboard
- FastAPI Financial Intelligence API
- Financial Ratio Analysis
- Stock Screening
- Company Valuation
- Cash Flow Intelligence
- CAGR Analysis
- KMeans Company Clustering
- Sector-wise Analysis
- NLP-Based Insights
- PDF Report Generation
- SQLite Database
- Automated ETL Pipeline
- Comprehensive Automated Testing
- **98 Tests Passed**

---

# Author

**Pavan Kumar Katkuri**

Bluestock Data Analysis Internship

**Nifty100 Financial Intelligence Platform**