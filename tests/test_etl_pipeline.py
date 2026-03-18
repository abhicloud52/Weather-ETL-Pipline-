from src.etl_pipeline import WeatherETLPipeline
from src.config import load_config

class DummyClient:
    def __init__(self, *args, **kwargs):
        pass

    def fetch_city_weather(self, city, country, units="metric"):
        return {
            "city": city,
            "country": country,
            "timestamp": "2026-03-18T10:00:00",
            "temperature": 25.0,
            "humidity": 60,
            "pressure": 1012,
            "wind_speed": 2.5,
            "condition": "clear sky",
        }

def test_run_for_all_cities_monkeypatched(monkeypatch, tmp_path):
    cfg = load_config()
    # point DB to tmp path
    db_path = tmp_path / "etl_test.db"
    monkeypatch.setattr("src.database.DB_PATH", str(db_path))

    # patch Database to use new path and patch client
    from src import database as db_module
    monkeypatch.setattr(
        "src.etl_pipeline.Database",
        lambda: db_module.Database(str(db_path))
    )
    monkeypatch.setattr("src.etl_pipeline.WeatherAPIClient", DummyClient)

    pipeline = WeatherETLPipeline(cfg)
    results = pipeline.run_for_all_config_cities()

    assert isinstance(results, dict)
    # at least one city should be True
    assert any(results.values())
