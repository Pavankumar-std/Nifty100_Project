# Nifty100 Financial Intelligence Platform

A complete financial analytics platform developed during the **Bluestock Data Analysis Internship**.

The project analyzes Nifty 100 companies using ETL pipelines, financial ratios, valuation models, cash flow intelligence, NLP-generated insights, PDF reports, and an interactive Streamlit dashboard.

---

# Features

- ETL Data Pipeline
- SQLite Database
- Financial Ratio Engine
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
- Automated Testing

---

# Technologies Used

- Python
- Pandas
- NumPy
- SQLite
- Streamlit
- Plotly
- Matplotlib
- ReportLab
- OpenPyXL
- Pytest
- Git & GitHub

---

# Project Structure

```
src/
│
├── analytics/
├── dashboard/
│   ├── app.py
│   └── utils/
├── etl/
├── nlp/
├── reports/
│
pages/
│
output/
│
db/
│
reports/
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

```bash
python -m pytest
```

---

# Project Highlights

- Interactive Streamlit Dashboard
- 92 Nifty100 Companies
- Financial Ratio Analysis
- Stock Screening
- Company Valuation
- Cash Flow Intelligence
- NLP-Based Insights
- PDF Report Generation
- SQLite Database
- Automated Analytics Pipeline

---

# Author

**Pavan Kumar Katkuri**

Bluestock Data Analysis Internship

Nifty100 Financial Intelligence Platform
