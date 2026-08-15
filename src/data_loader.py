import json
from pathlib import Path

from src.geo_types import PlaceRecord


def load_json_file(path: Path) -> list[PlaceRecord]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)
