import logging
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

from .config import load_config
from .etl_pipeline import WeatherETLPipeline

logger = logging.getLogger(__name__)

class ETLScheduler:
    def __init__(self):
        self.cfg = load_config()
        self.pipeline = WeatherETLPipeline(self.cfg)
        self.scheduler = BackgroundScheduler()

    def _job(self):
        logger.info("Scheduled ETL run started at %s", datetime.utcnow())
        results = self.pipeline.run_for_all_config_cities()
        logger.info("Run results: %s", results)

    def start(self):
        interval = self.cfg["etl"]["schedule_minutes"]
        self.scheduler.add_job(
            self._job,
            "interval",
            minutes=interval,
            id="weather_etl_job",
            replace_existing=True,
        )
        self.scheduler.start()
        logger.info("Scheduler started with %d min interval", interval)

    def stop(self):
        self.scheduler.shutdown()
