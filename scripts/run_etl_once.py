from src.config import load_config
from src.etl_pipeline import WeatherETLPipeline
from src.reporter import generate_daily_report
from src.monitor import generate_alerts

if __name__ == "__main__":
    cfg = load_config()
    pipeline = WeatherETLPipeline(cfg)

    results = pipeline.run_for_all_config_cities()
    print("ETL RUN RESULTS:", results)

    rep = generate_daily_report()
    alt = generate_alerts()
    print("Report generated:", rep)
    print("Alerts generated:", alt)
