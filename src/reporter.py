import os
from datetime import datetime, timedelta
import sqlite3

from .database import DB_PATH

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
REPORT_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

def generate_daily_report():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
      SELECT c.city_name,
             AVG(w.temperature_c),
             MIN(w.temperature_c),
             MAX(w.temperature_c),
             COUNT(*)
      FROM weather_data w
      JOIN cities c ON c.city_id = w.city_id
      WHERE w.timestamp >= datetime('now', '-1 day')
      GROUP BY c.city_id
    """)

    rows = cur.fetchall()
    conn.close()

    path = os.path.join(REPORT_DIR, "daily_summary.txt")
    with open(path, "w") as f:
        f.write("WEATHER DATA PIPELINE SYSTEM\n")
        f.write("=============================\n\n")
        f.write(f"Last Run: {datetime.utcnow()}\n")
        f.write(f"Records Processed (24h): {sum(r[4] for r in rows)}\n\n")
        f.write("CITY STATS (last 24h):\n")
        f.write("----------------------\n")
        for city, avg_t, min_t, max_t, cnt in rows:
            f.write(
                f"{city}: avg={avg_t:.1f}°C, min={min_t:.1f}°C, "
                f"max={max_t:.1f}°C, records={cnt}\n"
            )

    return path
