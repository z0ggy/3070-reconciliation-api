from src.config import GEO_DB_PATH
from src.geo_types import MatchCandidate, PlaceRecord
from src.matcher import Matcher
from src.place_normaliser import PlaceNameNormaliser
from src.similarity_score import SimilarityScore
from src.store import PlaceStore
from src.type_detection import EntityType

"""
References:
    - https://www.geeksforgeeks.org/python/sort-in-python/
"""

# load dataset
# DATASET: list[PlaceRecord] = load_json_file(GEO_DATA_PATH)
# Load data from SQLite through.
store: PlaceStore = PlaceStore(GEO_DB_PATH)
DATASET: list[PlaceRecord] = store.get_all_places()

# initialise instance of normaliser
place_normaliser: PlaceNameNormaliser = PlaceNameNormaliser()

# initialise instance of similarity score
similarity_score: SimilarityScore = SimilarityScore()

# initialise instance of matcher
matcher: Matcher = Matcher(place_normaliser, similarity_score)


# wrapper to run matcher with parameters
def match_data(
    query: str,
    entity_type: EntityType | None = None,
    limit: int = 10,
    country: str | None = None,
) -> list[MatchCandidate]:
    dataset: list[PlaceRecord] = DATASET

    return matcher.match(query, dataset, entity_type, limit, country)


def detect_ambiguity(candidates: list[MatchCandidate]) -> bool:
    return matcher.detect_ambiguity(candidates)
