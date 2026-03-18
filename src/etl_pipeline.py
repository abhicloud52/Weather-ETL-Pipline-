import logging
from typing import List, Tuple

from .config import load_config
from .database import Database
from .api_client import WeatherAPIClient
from .validators import validate_weather_record

logger = logging.getLogger(__name__)

class WeatherETLPipeline:
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.db = Database()
        self.client = WeatherAPIClient(
            api_key=cfg["openweather"]["api_key"],
            base_url=cfg["openweather"]["base_url"],
        )

    def run_for_city(self, city: str, country: str) -> bool:
        try:
            raw = self.client.fetch_city_weather(
                city, country, self.cfg["openweather"]["units"]
            )
            if not validate_weather_record(raw):
                logger.error("Validation failed for %s", city)
                return False

            city_id = self.db.upsert_city(city, country)
            self.db.insert_weather(city_id, raw)
            logger.info("ETL success for %s", city)
            return True
        except Exception as e:
            logger.exception("ETL failed for %s: %s", city, e)
            return False

    def run_for_all_config_cities(self) -> dict:
        results = {}
        for c in self.cfg["cities"]:
            name, country = c["name"], c["country"]
            results[name] = self.run_for_city(name, country)
        return results
