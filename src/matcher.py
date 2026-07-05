from typing import Any

from src.place_normaliser import PlaceNameNormaliser
from src.similarity_score import SimilarityScore

"""
References:
    - https://www.geeksforgeeks.org/python/sort-in-python/
"""


class Matcher:
    """Match a user query against a dataset, and return ranked candidates."""

    def __init__(
        self,
        normaliser: PlaceNameNormaliser,
        scorer: SimilarityScore,
        min_score: float = 0.45,
    ) -> None:
        self.normaliser = normaliser
        self.scorer = scorer
        self.min_score = min_score

    def match(
        self,
        query: str,
        dataset: list[dict],
        entity_type: str | None = None,
        limit: int = 10,
    ) -> list:

        # normalise query
        normalised_query = self.normaliser.normalise(query)

        # Return empty list (input checking)
        if not normalised_query:
            return []

        candidates: list[dict[str, Any]] = []

        for place in dataset:
            # if one type requested skip rest of the type
            if entity_type and place["type"] != entity_type:
                continue

            # store name and aliases
            names_to_check = [place["name"]] + place.get("aliases", [])

            # find best score
            best_score, matched_on, matched_value = self.find_best_score(
                place, names_to_check, normalised_query
            )
            # assign and filter weak candidates
            candidate = self.filter_weak_candidate(
                place, best_score, matched_on, matched_value
            )
            if candidate:
                candidates.append(candidate)

        # sort candidates descending (highest first)
        candidates.sort(key=lambda item: item["score"], reverse=True)

        # return a list of candidates highest first up to limit
        return candidates[:limit]

    def find_best_score(self, place: dict, names_to_check: list, normalised_query: str):
        """Find the best score for place using calculate_score logic
        place
        """
        if not place:
            raise ValueError("Place should be not empty")

        if not names_to_check:
            raise ValueError("Names to check should be not empty")

        if not normalised_query:
            raise ValueError("Normalised query should be not empty")

        # store strongest match (name or aliases)
        best_score = 0.0

        # represent a match 'source' (name or alias)
        matched_on = "name"

        # actual name or alias (what was matched)
        matched_value = place["name"]

        for i, candidate_name in enumerate(names_to_check):
            # normalise each candidate
            normalised_candidate = self.normaliser.normalise(candidate_name)

            # calculate score
            score = self.scorer.calculate_score(normalised_query, normalised_candidate)

            # logic for score result
            if score > best_score:
                best_score = score
                matched_on = "name" if i == 0 else "alias"
                matched_value = candidate_name

        return best_score, matched_on, matched_value

    def filter_weak_candidate(
        self,
        place: dict[str, Any],
        best_score: float,
        matched_on: str,
        matched_value: str,
    ) -> dict[str, Any] | None:
        """Build a candidate result only if the score passes the minimum threshold."""

        if best_score <= self.min_score:
            return None

        return {
            "id": place["id"],
            "name": place["name"],
            "type": place["type"],
            "country": place["country"],
            "score": round(best_score, 3),
            "matched_on": matched_on,
            "matched_value": matched_value,
        }
