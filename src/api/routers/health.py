import os
import sqlite3
import time

from fastapi import APIRouter

router = APIRouter(tags=["Health"])

START_TIME = time.time()

DB = os.path.join(
    os.path.dirname(__file__),
    "..",
    "..",
    "..",
    "db",
    "nifty100.db"
)

DB = os.path.abspath(DB)


@router.get("/health")
def health_check():
    """Check API health and database status."""

    conn = sqlite3.connect(DB)

    cursor = conn.cursor()

    tables = cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        """
    ).fetchall()

    row_counts = {}

    for table in tables:
        table_name = table[0]

        try:
            count = cursor.execute(
                f'SELECT COUNT(*) FROM "{table_name}"'
            ).fetchone()[0]

            row_counts[table_name] = count

        except Exception:
            row_counts[table_name] = 0

    conn.close()

    uptime = round(
        time.time() - START_TIME,
        2
    )

    return {
        "status": "ok",
        "db_row_counts": row_counts,
        "uptime_seconds": uptime,
        "version": "1.0.0"
    }