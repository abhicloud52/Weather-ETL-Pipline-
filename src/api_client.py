import os
import requests
from datetime import datetime

class WeatherAPIClient:
    def __init__(self, api_key: str, base_url: str):
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY")
        self.base_url = base_url
        if not self.api_key:
            raise ValueError("OpenWeather API key missing")

    def fetch_city_weather(self, city: str, country: str, units: str = "metric"):
        params = {
            "q": f"{city},{country}",
            "appid": self.api_key,
            "units": units,
        }
        resp = requests.get(self.base_url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return {
            "city": city,
            "country": country,
            "timestamp": datetime.utcnow().isoformat(timespec="seconds"),
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "wind_speed": data["wind"]["speed"],
            "condition": data["weather"][0]["description"],
        }
