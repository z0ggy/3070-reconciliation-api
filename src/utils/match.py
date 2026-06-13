from pathlib import Path
import json

"""
References:
    - https://stackoverflow.com/questions/10018679/python-find-closest-string-from-a-list-to-another-string
    - https://docs.python.org/3/library/difflib.html
"""
DATA_PATH = Path(__file__).parent / "data" / "geo_data.json"


def load_file() -> dict:
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def normalize_text(text: str) -> str:
    """
    Normalize text
    """
    text = text.replace("-", " ")
    text = text.lower().strip()
    return text
