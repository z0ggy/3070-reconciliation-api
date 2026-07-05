from src.matcher import Matcher
from src.place_normaliser import PlaceNameNormaliser
from src.similarity_score import SimilarityScore

"""
References:
    - https://docs.pytest.org/en/stable/
"""
normaliser = PlaceNameNormaliser()
scorer = SimilarityScore()
matcher = Matcher(normaliser, scorer)


def test_matcher_returns_ranked_candidates():
    dataset = [
        {
            "id": "IE-DUBLIN",
            "name": "Dublin",
            "type": "city",
            "country": "Ireland",
            "aliases": ["Baile Átha Cliath"],
        },
        {
            "id": "IE-CORK",
            "name": "Cork",
            "type": "city",
            "country": "Ireland",
            "aliases": [],
        },
    ]

    results = matcher.match("Dublinn", dataset)

    assert results[0]["name"] == "Dublin"
    assert results[0]["score"] > 0.7
