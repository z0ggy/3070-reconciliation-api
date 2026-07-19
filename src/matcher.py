from typing import Any

from src.place_normaliser import PlaceNameNormaliser
from src.similarity_score import SimilarityScore
from src.type_detection import EntityType, resolve_type

"""
References:
    - https://www.geeksforgeeks.org/python/sort-in-python/
    - https://www.w3schools.com/python/ref_string_casefold.asp
    - https://stackoverflow.com/questions/45745661/lower-vs-casefold-in-string-matching-and-converting-to-lowercase
"""


class Matcher:
    """Match a user query against a dataset, and return ranked candidates."""

    def __init__(
        self,
        normaliser: PlaceNameNormaliser,
        scorer: SimilarityScore,
        min_score: float = 0.45,
        type_bonus: float = 0.05,
        type_penalty: float = 0.04,
    ) -> None:
        self.normaliser = normaliser
        self.scorer = scorer
        self.min_score = min_score
        self.type_bonus = type_bonus
        self.type_penalty = type_penalty

    def match(
        self,
        query: str,
        dataset: list[dict],
        entity_type: EntityType | None = None,
        limit: int = 10,
    ) -> list:

        # normalise query
        normalised_query = self.normaliser.normalise(query)

        # Return empty list (input checking) for an empty query
        if not normalised_query:
            return []

        # Infer type only without an explicit type in the query.
        inferred_type = resolve_type(normalised_query) if entity_type is None else None

        # Used as a secondary ranking rule when final scores are equal.
        priority_entity_type = entity_type or inferred_type

        candidates: list[dict[str, Any]] = []

        for place in dataset:
            # If one type requested skip rest of the type
            if entity_type and place["type"] != entity_type:
                continue

            # Check and store name and aliases
            names_to_check = [place["name"]] + place.get("aliases", [])

            # Find best score
            best_score, matched_on, matched_value = self.find_best_score(
                place, names_to_check, normalised_query
            )

            # Apply an inferred type bonus or penalty to the best text score.
            final_score = self.apply_type_updater(
                base_score=best_score,
                candidate_type=place["type"],
                detection_type=inferred_type,
            )

            # Filter weak candidates.
            candidate = self.filter_weak_candidate(
                place,
                final_score,
                matched_on,
                matched_value,
            )
            if candidate:
                candidates.append(candidate)

        # sort candidates descending (highest first)
        # candidates.sort(key=lambda item: item["score"], reverse=True)
        candidates.sort(
            key=lambda item: (
                # Preferred entity type first when scores are equal
                -item["score"],  # Highest score first
                0  # Candidate matches the preferred type
                if (
                    priority_entity_type is not None
                    and item["type"] == priority_entity_type
                )
                else 1,  # candidate does not match the preferred type
                # Sort equal candidates alphabetically by name
                item["name"].casefold(),
                # If candidate have the same: score, type priority, name finally sort by 'id'
                item["id"],
            )
        )

        # return a list of candidates highest first up to limit
        return candidates[:limit]

    def find_best_score(
        self,
        place: dict[str, Any],
        names_to_check: list[str],
        normalised_query: str,
    ) -> tuple[float, str, str]:
        """
        Find the highest similarity score considering: place, name and aliases.

        Returns the best score, the source of the match, and the matched value.
        """

        if not place:
            raise ValueError("Place should not be empty")

        if not names_to_check:
            raise ValueError("Names to check should not be empty")

        if not normalised_query:
            raise ValueError("Normalised query should not be empty")

        best_score = 0.0
        matched_on = "name"
        matched_value = place["name"]

        # Loops through the official name and aliases and update best_score
        for index, candidate_name in enumerate(names_to_check):
            normalised_candidate = self.normaliser.normalise(candidate_name)

            score = self.scorer.calculate_score(
                normalised_query,
                normalised_candidate,
            )

            if score > best_score:
                best_score = score
                matched_on = "name" if index == 0 else "alias"
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

    def apply_type_updater(
        self,
        base_score: float,
        candidate_type: str,
        detection_type: EntityType | None,
    ) -> float:
        """
        Adjust a similarity score using a detection type.
        returns the updated final score between 0.0 and 1.0
        """

        if detection_type is None:
            return base_score

        if candidate_type == detection_type:
            updated_score = base_score + self.type_bonus
        else:
            updated_score = base_score - self.type_penalty

        # Keep the final score within the (0.0, 1.0) range.
        return max(0.0, min(1.0, updated_score))
