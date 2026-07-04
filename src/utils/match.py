import json
from pathlib import Path

from src.matcher import Matcher
from src.place_normaliser import PlaceNameNormaliser
from src.similarity_score import SimilarityScore

"""
References:
    - https://stackoverflow.com/questions/10018679/python-find-closest-string-from-a-list-to-another-string
    - https://stackoverflow.com/questions/51710082/what-does-unicodedata-normalize-do-in-python
    - https://docs.python.org/3/library/difflib.html
    - https://docs.python.org/3/library/difflib.html#sequencematcher-objects
    - https://www.geeksforgeeks.org/python/sort-in-python/
"""
DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "geo_data.json"


def load_file() -> list[dict]:
    with DATA_PATH.open("r", encoding="utf-8") as file:
        return json.load(file)


# initialise instance of normaliser
place_normaliser = PlaceNameNormaliser()

# initialise instance of similarity score
similarity_score = SimilarityScore()

matcher = Matcher(place_normaliser, similarity_score)


def match_data(
    query: str,
    entity_type: str | None = None,
    limit: int = 10,
) -> list[dict]:
    dataset: list[dict] = load_file()

    return matcher.match(query, dataset, entity_type, limit)
