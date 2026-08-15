from src.geo_types import MatchCandidate, PlaceRecord
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
        country_bonus: float = 0.04,
        country_penalty: float = 0.03,
        ambiguity_threshold: float = 0.10,
    ) -> None:
        self.normaliser: PlaceNameNormaliser = normaliser
        self.scorer: SimilarityScore = scorer
        self.min_score: float = min_score
        self.type_bonus: float = type_bonus
        self.type_penalty: float = type_penalty
        self.country_bonus: float = country_bonus
        self.country_penalty: float = country_penalty
        self.ambiguity_threshold: float = ambiguity_threshold

    def match(
        self,
        query: str,
        dataset: list[PlaceRecord],
        entity_type: EntityType | None = None,
        limit: int = 10,
        country: str | None = None,
    ) -> list[MatchCandidate]:
        """Match a query against the dataset and return ranked candidates."""

        # Normalise query, remove country words ("Ireland").
        normalised_query = self.normaliser.normalise(query)

        # Normalise query, keeps country words ("Ireland"), for use as context.
        normalised_context_query = self.normaliser.normalise_with_context(query)

        # Return empty list (input checking) for an empty query
        if not normalised_query:
            return []

        # Inferred type if no explicit type in the query is provided.
        inferred_type = resolve_type(normalised_query) if entity_type is None else None

        # Used as a secondary ranking rule when final scores are equal.
        priority_entity_type = entity_type or inferred_type

        # Explicit country is used as a hard filter.
        explicit_country = self.parse_country(country) if country else None

        # Use country if is in the query for ranking only,
        # Or ignore if an explicit country parameter is already provided.
        detected_country = None

        if explicit_country is None:
            detected_country = self.detect_country_context(
                normalised_context_query,
                dataset,
            )

        candidates: list[MatchCandidate] = []

        for place in dataset:
            # Explicit entity type filters records before scoring.
            if entity_type and place["type"] != entity_type:
                continue

            place_country = place["country"]

            # Explicit country filters records before scoring.
            if (
                explicit_country is not None
                and self.parse_country(place_country) != explicit_country
            ):
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

            # Apply a small country bonus or penalty when country context is in the query
            final_score = self.add_country_adjustment(
                score=final_score,
                place_country=place_country,
                detected_country=detected_country,
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
        place: PlaceRecord,
        names_to_check: list[str],
        normalised_query: str,
    ) -> tuple[float, str, str]:
        """
        Find the highest similarity score considering: place, name and aliases.

        Returns the best score, the source of the match, and the matched value.
        """

        if not place or place == "":
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
        place: PlaceRecord,
        best_score: float,
        matched_on: str,
        matched_value: str,
    ) -> MatchCandidate | None:
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

    def parse_country(self, country: str) -> str:
        """
        Allows 'Ireland' and 'Éire' to represent the same country:
        """
        normalised_country = self.normaliser.normalise_with_context(country)

        country_aliases = {
            "eire": "ireland",
            "ireland": "ireland",
        }

        return country_aliases.get(
            normalised_country,
            normalised_country,
        )

    def contains_phrase(
        self,
        query_words: list[str],
        phrase_words: list[str],
    ) -> bool:
        """
        Detect single word ("Ireland" and multi word ("United States") inputs.
        Example:
            query_words = ["dublin", "united", "states"]
            phrase_words = ["united", "states"]
        return True if detect country or False otherwise.
        """
        if not phrase_words:
            return False

        if len(phrase_words) > len(query_words):
            return False

        number_of_positions = len(query_words) - len(phrase_words) + 1

        for index in range(number_of_positions):
            if query_words[index : index + len(phrase_words)] == phrase_words:
                return True

        return False

    def detect_country_context(
        self,
        normalised_context_query: str,
        dataset: list[PlaceRecord],
    ) -> str | None:
        """
        Detect country in the normalised query.
        Returns a country only when exactly one country is detected.
        """
        query_words = normalised_context_query.split()

        # A set prevents duplicate country values.
        detected_countries: set[str] = set()

        for place in dataset:
            place_country = place["country"]

            # Skip records missing a valid country.
            if not place:
                continue

            canonical_country = self.parse_country(place_country)
            country_words = canonical_country.split()

            # Add the country when name is in the query.
            if self.contains_phrase(query_words, country_words):
                detected_countries.add(canonical_country)

        # Handle Irish country name, "Éire" map to 'ireland'
        if "eire" in query_words:  # "eire" accent removal applied.
            detected_countries.add("ireland")

        # Return None when the query not contains country,
        # or contains conflicting countries.
        if len(detected_countries) != 1:
            return None

        return detected_countries.pop()

    def add_country_adjustment(
        self,
        score: float,
        place_country: str | None,
        detected_country: str | None,
    ) -> float:
        """
        Apply a small score adjustment using country context from the query.
        A matching country get bonus. A different country get penalty.
        """

        # Keep original score without detected country
        if detected_country is None:
            return score

        # Not apply penalty for candidate when its country is missing.
        if not place_country:
            return score

        canonical_place_country = self.parse_country(place_country)

        if canonical_place_country == detected_country:
            score += self.country_bonus
        else:
            score -= self.country_penalty

        return max(0.0, min(1.0, score))

    def detect_ambiguity(
        self,
        candidates: list[MatchCandidate],
    ) -> bool:
        """
        Return True when the two best ranked candidates have similar score.
        Similar score respect the threshold
        """
        if len(candidates) < 2:
            return False

        first_score = candidates[0]["score"]
        second_score = candidates[1]["score"]

        score_difference = first_score - second_score

        return score_difference <= self.ambiguity_threshold
