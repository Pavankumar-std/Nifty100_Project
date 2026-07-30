# 📈 Nifty100 Financial Intelligence Platform

A complete financial analytics platform developed as part of the **Bluestock Data Analysis Internship**.

The project analyzes Nifty 100 companies using ETL pipelines, financial ratios, valuation analytics, cash flow intelligence, NLP-based insights, PDF report generation, and an interactive Streamlit dashboard.

---

# 🚀 Features

- ETL Pipeline
- SQLite Database
- Financial Ratio Engine
- Interactive Streamlit Dashboard
- Company Profile Analysis
- Stock Screener
- Peer Comparison
- Trend Analysis
- Sector Analysis
- Capital Allocation Analysis
- Valuation Module
- Cash Flow Intelligence
- NLP-Based Pros & Cons Generator
- PDF Company Tearsheets
- Sector Reports
- Portfolio Summary Report
- CSV & Excel Export
- Automated Testing

---

# 🛠 Technologies Used

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

# 📁 Project Structure

```text
src/
├── analytics/
├── dashboard/
│   ├── app.py
│   └── utils/
├── etl/
├── nlp/
├── reports/

pages/
├── 01_home.py
├── 02_profile.py
├── 03_screener.py
├── 04_peers.py
├── 05_trends.py
├── 06_sectors.py
├── 07_capital.py
└── 08_reports.py

output/
reports/
db/
```

---

# 📊 Dashboard Modules

- 🏠 Home Dashboard
- 📋 Company Profile
- 🔍 Stock Screener
- 👥 Peer Comparison
- 📈 Trend Analysis
- 🏭 Sector Analysis
- 💰 Capital Allocation
- 📄 Reports

---

# 🤖 NLP Modules

- Analysis Text Parser
- Auto Pros & Cons Generator

---

# 📉 Analytics Modules

- Financial Ratio Engine
- Valuation Engine
- Cash Flow Intelligence
- Capital Allocation Analysis

---

# 📄 Report Generation

- Company Tearsheets (92 PDFs)
- Sector Reports (11 PDFs)
- Portfolio Summary PDF

---

# 📦 Generated Outputs

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

# ▶️ Run Dashboard

```bash
streamlit run src/dashboard/app.py
```

---

# 📈 Run Analytics

```bash
python src/analytics/valuation.py
python src/analytics/cashflow_kpis.py
python src/analytics/capital_allocation_report.py
```

---

# 🤖 Run NLP

```bash
python src/nlp/parser.py
python src/nlp/pros_cons_generator.py
```

---

# 📄 Generate Reports

```bash
python src/reports/tearsheet.py
python src/reports/sector_report.py
python src/reports/portfolio_report.py
```

---

# ✅ Run Tests

```bash
python -m pytest
```

---

# 👨‍💻 Author

**Pavan Kumar Katkuri**

Bluestock Data Analysis Internship

Nifty100 Financial Intelligence Platform