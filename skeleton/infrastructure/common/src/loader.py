import json
from pathlib import Path

# json.load wrapper utility!
def load(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as config:
        data = json.load(config)
    return data