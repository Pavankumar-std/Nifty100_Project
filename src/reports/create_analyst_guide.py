from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer


BASE_DIR = Path(__file__).resolve().parents[2]
OUTPUT_DIR = BASE_DIR / "docs"
OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = OUTPUT_DIR / "analyst_guide.pdf"


def create_analyst_guide():
    styles = getSampleStyleSheet()

    story = []

    story.append(
        Paragraph(
            "Nifty100 Financial Intelligence Platform - Analyst Guide",
            styles["Title"]
        )
    )

    story.append(Spacer(1, 20))

    sections = [
        (
            "1. Project Overview",
            "The Nifty100 Financial Intelligence Platform provides financial analysis, "
            "stock screening, company comparison, valuation analysis, cash flow intelligence, "
            "sector analysis, NLP-based insights, PDF reports, and an interactive dashboard."
        ),
        (
            "2. Company Analysis",
            "Use the Company Profile module to review company information, financial metrics, "
            "ratios, performance indicators, and other available analytical data."
        ),
        (
            "3. Stock Screener",
            "Use the Stock Screener to filter companies using metrics such as Return on Equity "
            "(ROE), Debt-to-Equity ratio, and sector-based filters."
        ),
        (
            "4. Peer Comparison",
            "Use Peer Comparison to compare companies with other companies in their peer group "
            "using available financial and performance metrics."
        ),
        (
            "5. Sector Analysis",
            "Use Sector Analysis to review sector-level company information and aggregated "
            "financial metrics."
        ),
        (
            "6. Valuation Analysis",
            "The Valuation Engine generates valuation outputs and identifies companies that "
            "may require further analyst review."
        ),
        (
            "7. Cash Flow Intelligence",
            "Cash Flow Intelligence analyzes financial cash flow information and generates "
            "patterns, alerts, and analytical outputs."
        ),
        (
            "8. Reports",
            "The platform can generate company tearsheets, sector reports, portfolio summary "
            "reports, and other analytical outputs."
        ),
        (
            "9. API Usage",
            "FastAPI endpoints provide access to company, screener, sector, and health-related "
            "data for programmatic use."
        ),
        (
            "10. Testing",
            "Run the automated test suite before submitting or deploying changes. "
            "The project test suite validates ETL, data quality, KPI calculations, and API functionality."
        ),
    ]

    for heading, content in sections:
        story.append(Paragraph(heading, styles["Heading2"]))
        story.append(Spacer(1, 6))
        story.append(Paragraph(content, styles["BodyText"]))
        story.append(Spacer(1, 14))

    doc = SimpleDocTemplate(
        str(OUTPUT_FILE),
        pagesize=A4
    )

    doc.build(story)

    print(f"Analyst guide created: {OUTPUT_FILE}")


if __name__ == "__main__":
    create_analyst_guide()