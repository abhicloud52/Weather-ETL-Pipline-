import time
from src.scheduler import ETLScheduler
from src.reporter import generate_daily_report
from src.monitor import generate_alerts

if __name__ == "__main__":
    sched = ETLScheduler()
    sched.start()
    print("Scheduler running. Press Ctrl+C to stop.")
    try:
        while True:
            time.sleep(3600)
            generate_daily_report()
            generate_alerts()
    except KeyboardInterrupt:
        sched.stop()
