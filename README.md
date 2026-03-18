# Weather ETL Pipeline – OpenWeather + SQLite

This repository contains an end‑to‑end **weather data ETL pipeline** that periodically collects current weather data for multiple Indian cities from the OpenWeather API, validates and stores it in a SQLite database, and generates summary reports and alerts. [file:1]

---

## 1. Project Overview

### 1.1 Goal

The goal of this system is to demonstrate a complete, production‑style ETL pipeline in Python:

- Extract weather data for multiple cities from a public API.
- Validate and store the data in a relational database (SQLite).
- Schedule periodic collection using a job scheduler.
- Generate daily summary reports and real‑time alerts based on thresholds.
- Provide clear documentation, tests, and a clean GitHub project structure. [file:1]

### 1.2 Features

- Multiple‑city weather tracking (Delhi, Mumbai, Bangalore, Chennai, Kolkata by default). [file:1]
- SQLite database with normalized schema (`cities`, `weather_data`). [file:1]
- OpenWeather API integration with basic error handling.
- Automated scheduling using APScheduler.
- Data validation with configurable thresholds.
- Text‑based daily summary reports and alert reports.
- Unit and integration tests using `pytest`.
- Modular, easily extendable codebase.

---

## 2. Architecture Overview

The project follows a modular design with clear separation of concerns. [file:1]

```text
weather-etl/
├─ README.md
├─ requirements.txt
├─ config/
│  └─ config.yaml
├─ src/
│  ├─ __init__.py
│  ├─ config.py        # Load YAML configuration
│  ├─ database.py      # SQLite DB, tables, queries
│  ├─ api_client.py    # OpenWeather API integration
│  ├─ validators.py    # Data quality checks
│  ├─ etl_pipeline.py  # Main ETL workflow
│  ├─ scheduler.py     # Automated job scheduling
│  ├─ reporter.py      # Report generation
│  └─ monitor.py       # Alerts and basic monitoring
├─ database/
│  └─ weather_data.db  # Auto-created at runtime
├─ tests/
│  ├─ __init__.py
│  ├─ test_database.py
│  ├─ test_api_client.py
│  ├─ test_validators.py
│  └─ test_etl_pipeline.py
├─ docs/
│  ├─ architecture.md
│  ├─ api_integration.md
│  ├─ database_schema.md
│  ├─ etl_workflow.md
│  └─ deployment_guide.md
├─ scripts/
│  ├─ run_etl_once.py
│  └─ run_scheduler.py
├─ logs/
│  └─ app.log          # Created at runtime
└─ reports/
   ├─ daily_summary.txt
   └─ alerts.txt
