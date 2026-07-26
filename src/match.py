from src.config import GEO_DATA_PATH
from src.data_loader import load_json_file
from src.matcher import Matcher
from src.place_normaliser import PlaceNameNormaliser
from src.similarity_score import SimilarityScore
from src.type_detection import EntityType

"""
References:
    - https://www.geeksforgeeks.org/python/sort-in-python/
"""

# load dataset
DATASET = load_json_file(GEO_DATA_PATH)

# initialise instance of normaliser
place_normaliser = PlaceNameNormaliser()

# initialise instance of similarity score
similarity_score = SimilarityScore()

# initialise instance of matcher
matcher = Matcher(place_normaliser, similarity_score)


# wrapper to run matcher with parameters
def match_data(
    query: str,
    entity_type: EntityType | None = None,
    limit: int = 10,
) -> list[dict]:
    dataset: list[dict] = DATASET

    return matcher.match(query, dataset, entity_type, limit)
