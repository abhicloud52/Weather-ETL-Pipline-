from datetime import datetime
from src.api_client import WeatherAPIClient

class DummyResp:
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code != 200:
            raise Exception("HTTP error")

    def json(self):
        return self._json

def test_fetch_city_weather_monkeypatched(monkeypatch):
    def fake_get(url, params, timeout):
        return DummyResp(
            {
                "main": {
                    "temp": 22.5,
                    "humidity": 40,
                    "pressure": 1010,
                },
                "wind": {
                    "speed": 2.0
                },
                "weather": [
                    {"description": "clear sky"}
                ],
            }
        )

    monkeypatch.setattr("src.api_client.requests.get", fake_get)

    client = WeatherAPIClient(api_key="TEST", base_url="http://fake")
    data = client.fetch_city_weather("Delhi", "IN")

    assert data["city"] == "Delhi"
    assert data["country"] == "IN"
    assert -80 <= data["temperature"] <= 60
    assert 0 <= data["humidity"] <= 100
    assert "timestamp" in data
