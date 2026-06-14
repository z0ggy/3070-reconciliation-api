from pathlib import Path
import json

"""
References:
    - https://stackoverflow.com/questions/10018679/python-find-closest-string-from-a-list-to-another-string
    - https://docs.python.org/3/library/difflib.html
"""
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "geo_data.json"


def load_file() -> list[dict]:
    with DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


def normalize_text(text: str) -> str:
    """
    Normalize text
    """
    text = text.replace("-", " ")
    text = text.lower().strip()
    return text


def similarity_score(query: str, candidate: str) -> float:
    normalized_query = normalize_text(query)
    normalized_candidate = normalize_text(candidate)

    if normalized_query == normalized_candidate:
        return 1.0

    return 0
