import os
import sqlite3
from src.database import Database, DB_PATH

def test_db_file_created(tmp_path, monkeypatch):
    # use temp DB so we don't touch real file
    db_path = tmp_path / "test_weather.db"
    monkeypatch.setattr("src.database.DB_PATH", str(db_path))
    db = Database(str(db_path))

    assert db_path.exists()
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = {row[0] for row in cur.fetchall()}
    conn.close()

    assert "cities" in tables
    assert "weather_data" in tables

def test_insert_city_and_weather(tmp_path, monkeypatch):
    db_path = tmp_path / "test_weather.db"
    monkeypatch.setattr("src.database.DB_PATH", str(db_path))
    db = Database(str(db_path))

    city_id = db.upsert_city("TestCity", "TC")
    assert isinstance(city_id, int)

    rid = db.insert_weather(
        city_id,
        {
            "timestamp": "2026-03-18T10:00:00",
            "temperature": 25.0,
            "humidity": 50,
            "pressure": 1013,
            "wind_speed": 3.5,
            "condition": "clear sky",
        },
    )
    assert isinstance(rid, int)
