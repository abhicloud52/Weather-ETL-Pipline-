import os
import yaml

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

def load_config(path: str = None) -> dict:
    if path is None:
        path = os.path.join(BASE_DIR, "config", "config.yaml")
    with open(path, "r") as f:
        return yaml.safe_load(f)
