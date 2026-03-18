import os
import sqlite3
from datetime import datetime, timedelta

from .database import DB_PATH
from .config import load_config

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
REPORT_DIR = os.path.join(BASE_DIR, "reports")
os.makedirs(REPORT_DIR, exist_ok=True)

def generate_alerts():
    cfg = load_config()
    t_thr = cfg["etl"]["temp_high_threshold"]
    h_thr = cfg["etl"]["humidity_high_threshold"]

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
      SELECT c.city_name, w.temperature_c, w.humidity, w.timestamp
      FROM weather_data w
      JOIN cities c ON c.city_id = w.city_id
      WHERE w.timestamp >= datetime('now', '-1 hour')
    """)

    rows = cur.fetchall()
    conn.close()

    alerts = []
    for city, temp, hum, ts in rows:
        if temp > t_thr:
            alerts.append(
                f"High temperature alert: {city} ({temp:.1f}°C > {t_thr}°C) at {ts}"
            )
        if hum > h_thr:
            alerts.append(
                f"High humidity alert: {city} ({hum}% > {h_thr}%) at {ts}"
            )

    path = os.path.join(REPORT_DIR, "alerts.txt")
    with open(path, "w") as f:
        f.write("TODAY'S ALERTS\n")
        f.write("==============\n")
        if not alerts:
            f.write("No alerts in the last hour.\n")
        else:
            for a in alerts:
                f.write(f"• {a}\n")

    return path
