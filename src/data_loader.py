import json
from pathlib import Path
from typing import cast

from src.geo_types import PlaceRecord

"""
References:
    - https://stackoverflow.com/questions/51457563/what-does-typing-cast-do-in-python
    - https://stackoverflow.com/questions/75010631/python-typing-cast-vs-built-in-casting
"""


def load_json_file(path: Path) -> list[PlaceRecord]:
    with path.open("r", encoding="utf-8") as file:
        return cast(list[PlaceRecord], json.load(file))
