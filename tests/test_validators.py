from src.validators import validate_weather_record

def test_validate_weather_record_ok():
    record = {
        "city": "Delhi",
        "country": "IN",
        "timestamp": "2026-03-18T10:00:00",
        "temperature": 30.0,
        "humidity": 70,
        "pressure": 1010,
        "wind_speed": 3.0,
        "condition": "clear sky",
    }
    assert validate_weather_record(record) is True

def test_validate_weather_record_missing_field():
    record = {
        "city": "Delhi",
        "country": "IN",
        "timestamp": "2026-03-18T10:00:00",
        # "temperature" missing
        "humidity": 70,
        "pressure": 1010,
        "wind_speed": 3.0,
        "condition": "clear sky",
    }
    assert validate_weather_record(record) is False

def test_validate_weather_record_out_of_range():
    bad_temp = {
        "city": "Delhi",
        "country": "IN",
        "timestamp": "2026-03-18T10:00:00",
        "temperature": 100.0,  # too high
        "humidity": 70,
        "pressure": 1010,
        "wind_speed": 3.0,
        "condition": "clear sky",
    }
    assert validate_weather_record(bad_temp) is False
