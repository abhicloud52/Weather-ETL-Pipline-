def validate_weather_record(record: dict) -> bool:
    req_keys = [
        "city", "country", "timestamp",
        "temperature", "humidity", "pressure", "wind_speed", "condition",
    ]
    for k in req_keys:
        if k not in record:
            return False
    # basic range checks
    if not (-80 <= record["temperature"] <= 60):
        return False
    if not (0 <= record["humidity"] <= 100):
        return False
    if not (800 <= record["pressure"] <= 1100):
        return False
    if record["wind_speed"] < 0:
        return False
    return True
