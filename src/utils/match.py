import json
from pathlib import Path

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

# create shortcut for normaliser
normaliser = place_normaliser.normalise

# initialise instance of similarity score
similarity_score = SimilarityScore()


def match_data(
    query: str, entity_type: str | None = None, limit: int = 10
) -> list[dict]:
    """
    Search data set and return best matches.
    """
    # load dataset
    dataset = load_file()

    # store candidates
    candidates = []

    # normalise query
    normalised_query = normaliser(query)

    # Return empty list (input checking)
    if not normalised_query:
        return []

    for match in dataset:
        # if one type requested skip rest of the type
        if entity_type and match["type"] != entity_type:
            continue

        # store name and aliases
        names_to_check = [match["name"]] + match.get("aliases", [])

        # store strongest match (name or aliases)
        best_score = 0.0

        # represent a match 'source' (name or alias)
        matched_on = "name"

        # actual name or alias (what was matched)
        matched_value = match["name"]

        for i, candidate_name in enumerate(names_to_check):
            # score = similarity_score(query, candidate_name)

            normalised_candidate = normaliser(candidate_name)

            score = similarity_score.calculate_score(
                normalised_query, normalised_candidate
            )

            if score > best_score:
                best_score = score
                matched_on = "name" if i == 0 else "alias"
                matched_value = candidate_name

        # filter for weak candidates
        if best_score > 0.45:
            candidates.append(
                {
                    "id": match["id"],
                    "name": match["name"],
                    "type": match["type"],
                    "country": match["country"],
                    "score": round(best_score, 3),
                    "matched_on": matched_on,
                    "matched_value": matched_value,
                }
            )
    # sort candidates descending (highest first)
    candidates.sort(key=lambda item: item["score"], reverse=True)

    # return a list of candidates highest first up to limit
    return candidates[:limit]
