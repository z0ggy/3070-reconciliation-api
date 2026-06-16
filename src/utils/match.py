from pathlib import Path
from difflib import SequenceMatcher as sm
import json
from icecream import ic

"""
References:
    - https://stackoverflow.com/questions/10018679/python-find-closest-string-from-a-list-to-another-string
    - https://docs.python.org/3/library/difflib.html
    - https://docs.python.org/3/library/difflib.html#sequencematcher-objects
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
    """
    compare two normalized strings and return similarity score.
    query: str represent input query.
    candidate: str represent official name from dataset.
    """
    # normalize strings
    normalized_query = normalize_text(query)
    normalized_candidate = normalize_text(candidate)

    # perfect match
    if normalized_query == normalized_candidate:
        return 1.0

    # nearly perfect matches when string contains string
    elif normalized_query in normalized_candidate:
        return 0.9
    elif normalized_candidate in normalized_query:
        return 0.9

    # similarity score based on how similar query and candidate are
    return sm(None, normalized_query, normalized_candidate).ratio()


def match_data(query: str, type: str | None = None) -> list[dict]:
    """
    Search data set and return best matches.
    """
    # load dataset
    dataset = load_file()

    # store candidates
    candidates = []

    for match in dataset:
        # if one type requested skip rest of the type
        if type and match["type"] != type:
            continue

        # store name and aliases
        names_to_check = [match["name"]] + match.get("aliases", "")
        ic(names_to_check)

        # store strongest match (name or aliases)
        best_score = 0.0

        # represnt a match 'source' (name or alias)
        matched_on = "name"

        for i, candidate_name in enumerate(names_to_check):
            score = similarity_score(query, candidate_name)
            ic(score)

            if score > best_score:
                best_score = score
                matched_on = "name" if i == 0 else "alias"
                ic(matched_on)

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
                }
            )
    # return a list of candidates
    return candidates
