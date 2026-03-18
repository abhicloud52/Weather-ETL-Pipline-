import os
import sqlite3
from datetime import datetime
from typing import List, Dict, Optional

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "weather_data.db")

class Database:
    def __init__(self, db_path: str = DB_PATH):
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_path = db_path
        self._setup()

    def _conn(self):
        return sqlite3.connect(self.db_path)

    def _setup(self):
        conn = self._conn()
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS cities (
            city_id     INTEGER PRIMARY KEY,
            city_name   TEXT NOT NULL,
            country     TEXT,
            latitude    REAL,
            longitude   REAL,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        cur.execute("""
        CREATE TABLE IF NOT EXISTS weather_data (
            record_id        INTEGER PRIMARY KEY,
            city_id          INTEGER,
            timestamp        TIMESTAMP,
            temperature_c    REAL,
            humidity         INTEGER,
            pressure_hpa     REAL,
            wind_speed_mps   REAL,
            weather_condition TEXT,
            rain_1h          REAL,
            FOREIGN KEY (city_id) REFERENCES cities (city_id)
        )
        """)

        cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_weather_city_time
        ON weather_data(city_id, timestamp)
        """)

        conn.commit()
        conn.close()

    def get_city_id(self, name: str, country: str) -> Optional[int]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute(
            "SELECT city_id FROM cities WHERE city_name=? AND country=?",
            (name, country),
        )
        row = cur.fetchone()
        conn.close()
        return row[0] if row else None

    def insert_city(self, name: str, country: str,
                    lat: float = None, lon: float = None) -> int:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO cities (city_name, country, latitude, longitude) "
            "VALUES (?, ?, ?, ?)",
            (name, country, lat, lon),
        )
        cid = cur.lastrowid
        conn.commit()
        conn.close()
        return cid

    def upsert_city(self, name: str, country: str,
                    lat: float = None, lon: float = None) -> int:
        cid = self.get_city_id(name, country)
        if cid is not None:
            return cid
        return self.insert_city(name, country, lat, lon)

    def insert_weather(self, city_id: int, data: dict) -> int:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO weather_data (
              city_id, timestamp, temperature_c, humidity,
              pressure_hpa, wind_speed_mps, weather_condition, rain_1h
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                city_id,
                data["timestamp"],
                data["temperature"],
                data["humidity"],
                data["pressure"],
                data["wind_speed"],
                data["condition"],
            ),
        )
        rid = cur.lastrowid
        conn.commit()
        conn.close()
        return rid

    def fetch_last_n_days(self, days: int = 30) -> List[Dict]:
        conn = self._conn()
        cur = conn.cursor()
        cur.execute(
            """
            SELECT c.city_name, c.country, w.timestamp,
                   w.temperature_c, w.humidity,
                   w.pressure_hpa, w.weather_condition
            FROM weather_data w
            JOIN cities c ON c.city_id = w.city_id
            WHERE w.timestamp >= datetime('now', ?)
            """,
            (f"-{days} days",),
        )
        cols = [d[0] for d in cur.description]
        rows = [dict(zip(cols, r)) for r in cur.fetchall()]
        conn.close()
        return rows
