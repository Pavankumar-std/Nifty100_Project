import os
import sqlite3
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    PageBreak,
)

DB = "db/nifty100.db"

styles = getSampleStyleSheet()

title_style = styles["Heading1"]
title_style.alignment = TA_CENTER

heading_style = styles["Heading2"]
normal_style = styles["BodyText"]

os.makedirs("reports/tearsheets", exist_ok=True)


# --------------------------------------------------
# Database Loader
# --------------------------------------------------

def load_table(table):
    conn = sqlite3.connect(DB)

    df = pd.read_sql(
        f'SELECT * FROM "{table}"',
        conn
    )

    conn.close()

    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


# --------------------------------------------------
# Load Tables
# --------------------------------------------------

companies = load_table("companies")
ratios = load_table("financial_ratios")
pl = load_table("profitandloss")
bs = load_table("balancesheet")
cf = load_table("cashflow")
pros = load_table("prosandcons")


# --------------------------------------------------
# Create One Company PDF
# --------------------------------------------------

def create_tearsheet(company):

    company_name = (
        str(company["company_name"])
        .replace("\n", " ")
        .replace("/", "-")
        .strip()
    )

    pdf = f"reports/tearsheets/{company_name}_tearsheet.pdf"

    doc = SimpleDocTemplate(pdf)

    story = []

    # -----------------------------
    # Company Header
    # -----------------------------

    story.append(
        Paragraph(
            company_name,
            title_style,
        )
    )

    story.append(
        Paragraph(
            f"Ticker : {company['id']}",
            heading_style,
        )
    )

    story.append(Spacer(1, 0.30 * inch))

    if "about_company" in company.index:

        story.append(
            Paragraph(
                str(company["about_company"]),
                normal_style,
            )
        )

    story.append(Spacer(1, 0.25 * inch))

    # -----------------------------
    # Latest Financial Ratios
    # -----------------------------

    company_ratio = ratios[
        ratios["company_id"] == company["id"]
    ]

    if not company_ratio.empty:

        latest = company_ratio.sort_values(
            "year"
        ).iloc[-1]

        data = [
            ["Metric", "Value"],
            ["ROE", f"{latest['roe']:.2f}%"],
            ["ROCE", f"{latest['roce']:.2f}%"],
            ["ROA", f"{latest['roa']:.2f}%"],
            ["Debt / Equity", f"{latest['debt_to_equity']:.2f}"],
            ["Net Profit Margin", f"{latest['net_profit_margin']:.2f}%"],
            ["Interest Coverage", f"{latest['interest_coverage']:.2f}"],
        ]

        table = Table(
            data,
            colWidths=[220, 120]
        )

        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
            ])
        )

        story.append(table)

    story.append(Spacer(1, 0.30 * inch))

    story.append(
        Paragraph(
            "Revenue History",
            heading_style,
        )
    )

    company_pl = pl[
        pl["company_id"] == company["id"]
    ].sort_values("year")
        # -----------------------------
    # Revenue Table
    # -----------------------------

    if not company_pl.empty:

        revenue = [["Year", "Revenue", "Net Profit"]]

        for _, row in company_pl.iterrows():

            revenue.append([
                str(row["year"]),
                f"{row['sales']:,.0f}",
                f"{row['net_profit']:,.0f}",
            ])

        revenue_table = Table(revenue)

        revenue_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.darkgreen),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                ("GRID", (0, 0), (-1, -1), 1, colors.grey),
                ("BACKGROUND", (0, 1), (-1, -1), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ])
        )

        story.append(revenue_table)

    story.append(PageBreak())

    # -----------------------------
    # Pros & Cons
    # -----------------------------

    story.append(
        Paragraph(
            "Pros & Cons",
            heading_style,
        )
    )

    company_pros = pros[
        pros["company_id"] == company["id"]
    ]

    if not company_pros.empty:

        row = company_pros.iloc[0]

        story.append(
            Paragraph(
                "<b>Pros</b>",
                heading_style,
            )
        )

        for col in company_pros.columns:

            value = row[col]

            if pd.isna(value):
                continue

            if "pro" in col.lower():

                story.append(
                    Paragraph(
                        f"• {value}",
                        normal_style,
                    )
                )

        story.append(Spacer(1, 0.20 * inch))

        story.append(
            Paragraph(
                "<b>Cons</b>",
                heading_style,
            )
        )

        for col in company_pros.columns:

            value = row[col]

            if pd.isna(value):
                continue

            if "con" in col.lower():

                story.append(
                    Paragraph(
                        f"• {value}",
                        normal_style,
                    )
                )

    else:

        story.append(
            Paragraph(
                "No Pros & Cons available.",
                normal_style,
            )
        )

    doc.build(story)


# --------------------------------------------------
# Generate PDFs
# --------------------------------------------------

for _, company in companies.iterrows():

    try:

        create_tearsheet(company)

        print(f"Generated: {company['company_name']}")

    except Exception as e:

        print("=" * 60)
        print(f"FAILED : {company['company_name']}")
        print(f"ERROR  : {e}")
        print("=" * 60)

print("\nAll Company Tearsheet PDFs Generated Successfully.")