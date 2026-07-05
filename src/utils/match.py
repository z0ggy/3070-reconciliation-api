import json
from pathlib import Path

from src.matcher import Matcher
from src.place_normaliser import PlaceNameNormaliser
from src.similarity_score import SimilarityScore

"""
References:
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

# initialise instance of matcher
matcher = Matcher(place_normaliser, similarity_score)


# wrapper to run matcher with parameters
def match_data(
    query: str,
    entity_type: str | None = None,
    limit: int = 10,
) -> list[dict]:
    dataset: list[dict] = load_file()

    return matcher.match(query, dataset, entity_type, limit)
