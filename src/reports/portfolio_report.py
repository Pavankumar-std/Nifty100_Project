import os
import sqlite3
import pandas as pd

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph
)

from reportlab.lib.styles import getSampleStyleSheet

os.makedirs(
    "reports/portfolio",
    exist_ok=True
)

conn = sqlite3.connect(
    "db/nifty100.db"
)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

conn.close()

companies.columns = (
    companies.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

styles = getSampleStyleSheet()

pdf = SimpleDocTemplate(
    "reports/portfolio/portfolio_summary.pdf"
)

story = []

story.append(
    Paragraph(
        "<b>Nifty100 Portfolio Summary</b>",
        styles["Title"]
    )
)

for _, row in companies.iterrows():

    story.append(
        Paragraph(
            f"{row['id']} - {row['company_name']}",
            styles["BodyText"]
        )
    )

pdf.build(story)

print("Portfolio Summary Generated")