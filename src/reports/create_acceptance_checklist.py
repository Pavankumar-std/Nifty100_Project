from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


BASE_DIR = Path(__file__).resolve().parents[2]

DOCS_DIR = BASE_DIR / "docs"
DOCS_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = DOCS_DIR / "acceptance_checklist.pdf"


def create_acceptance_checklist():
    """Create project acceptance checklist PDF."""

    doc = SimpleDocTemplate(
        str(OUTPUT_FILE),
        pagesize=A4
    )

    styles = getSampleStyleSheet()
    story = []

    title = Paragraph(
        "Nifty100 Financial Intelligence Platform",
        styles["Title"]
    )

    subtitle = Paragraph(
        "Project Acceptance Checklist",
        styles["Heading2"]
    )

    story.append(title)
    story.append(Spacer(1, 12))
    story.append(subtitle)
    story.append(Spacer(1, 20))

    data = [
        ["ID", "Deliverable", "Status"],

        ["D-01", "SQLite Database", "Completed"],
        ["D-02", "Data Loading Audit", "Completed"],
        ["D-03", "Data Validation", "Completed"],
        ["D-04", "Exploratory SQL Queries", "Completed"],
        ["D-05", "Financial Ratios", "Completed"],
        ["D-06", "Capital Allocation Analysis", "Completed"],
        ["D-07", "Stock Screener Output", "Completed"],
        ["D-08", "Screener Configuration", "Completed"],
        ["D-09", "Peer Comparison", "Completed"],
        ["D-10", "Radar Charts", "Completed"],
        ["D-11", "Streamlit Dashboard", "Completed"],
        ["D-12", "Valuation Analysis", "Completed"],
        ["D-13", "Cash Flow Intelligence", "Completed"],
        ["D-14", "Pros and Cons Generator", "Completed"],
        ["D-15", "Analysis Text Parser", "Completed"],
        ["D-16", "Company Tearsheets", "Completed"],
        ["D-17", "Sector Reports", "Completed"],
        ["D-18", "Portfolio Summary Report", "Completed"],
        ["D-19", "Cluster Analysis", "Completed"],
        ["D-20", "FastAPI Server", "Completed"],
        ["D-21", "Automated Testing Report", "Completed"],
        ["D-22", "Analyst Guide", "Completed"],
        ["D-23", "Acceptance Checklist", "Completed"],
    ]

    table = Table(
        data,
        colWidths=[60, 320, 100]
    )

    table.setStyle(
        TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

            ("ALIGN", (0, 0), (-1, -1), "CENTER"),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),

            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

            ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ])
    )

    story.append(table)
    story.append(Spacer(1, 20))

    summary = Paragraph(
        "Project Status: ACCEPTED<br/>"
        "All 23 project deliverables have been completed and verified.",
        styles["BodyText"]
    )

    story.append(summary)

    doc.build(story)

    print(f"Acceptance checklist created: {OUTPUT_FILE}")


if __name__ == "__main__":
    create_acceptance_checklist()