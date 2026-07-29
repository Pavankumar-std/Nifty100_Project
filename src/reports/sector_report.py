import os
import sqlite3
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

os.makedirs("reports/sector", exist_ok=True)

conn = sqlite3.connect("db/nifty100.db")

companies = pd.read_sql("SELECT * FROM companies", conn)
sectors = pd.read_sql("SELECT * FROM sectors", conn)

conn.close()

companies.columns = companies.columns.str.strip().str.lower().str.replace(" ", "_")
sectors.columns = sectors.columns.str.strip().str.lower().str.replace(" ", "_")

styles = getSampleStyleSheet()

sector_col = sectors.columns[2]

for sector in sorted(sectors[sector_col].dropna().unique()):

    pdf = SimpleDocTemplate(
        f"reports/sector/{sector}.pdf"
    )

    story = []

    story.append(
        Paragraph(
            f"<b>{sector}</b>",
            styles["Title"]
        )
    )

    members = sectors[
        sectors[sector_col] == sector
    ]

    story.append(
        Paragraph(
            f"Companies : {len(members)}",
            styles["Heading2"]
        )
    )

    pdf.build(story)

print("Sector Reports Generated")