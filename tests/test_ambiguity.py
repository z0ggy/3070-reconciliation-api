from src.match import DATASET
from src.matcher import Matcher
from src.place_normaliser import PlaceNameNormaliser
from src.similarity_score import SimilarityScore

normaliser = PlaceNameNormaliser()
scorer = SimilarityScore()
matcher = Matcher(normaliser, scorer)


def test_detected_ambiguity() -> None:
    candidates = matcher.match(
        query="Dublin",
        dataset=DATASET,
    )

    candidate_ids = [candidate["id"] for candidate in candidates]

    assert "IE-CITY-DUBLIN" in candidate_ids
    assert "IE-COUNTY-DUBLIN" in candidate_ids

    assert matcher.detect_ambiguity(candidates) is True


def test_ambiguity_not_detected():
    """
    Candidates_with_large_score_difference_are_not_ambiguous
    """
    candidates = [
        {
            "id": "IE-CITY-DUBLIN",
            "type": "city",
            "score": 1.0,
        },
        {
            "id": "IE-COUNTY-DUBLIN",
            "type": "county",
            "score": 0.75,
        },
    ]

    assert matcher.detect_ambiguity(candidates) is False
