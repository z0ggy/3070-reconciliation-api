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


def test_detection_type_prioritise_score():
    """Same name different type query contains 'city'"""
    dataset = [
        {
            "id": "IE-COUNTY-DUBLIN",
            "name": "Dublin",
            "type": "county",
            "country": "Ireland",
            "aliases": [],
        },
        {
            "id": "IE-CITY-DUBLIN",
            "name": "Dublin",
            "type": "city",
            "country": "Ireland",
            "aliases": [],
        },
    ]

    results = matcher.match("Dublin City", dataset)

    assert results[0]["type"] == "city"
    assert results[0]["id"] == "IE-CITY-DUBLIN"


def test_explicit_type_filter_overrides_type_detection():
    """Query contains 'entity_type="county'"""
    dataset = [
        {
            "id": "IE-COUNTY-DUBLIN",
            "name": "Dublin",
            "type": "county",
            "country": "Ireland",
            "aliases": [],
        },
        {
            "id": "IE-CITY-DUBLIN",
            "name": "Dublin",
            "type": "city",
            "country": "Ireland",
            "aliases": [],
        },
    ]

    results = matcher.match(
        "Dublin City",
        dataset,
        entity_type="county",
    )

    assert len(results) == 1
    assert results[0]["type"] == "county"
    assert results[0]["id"] == "IE-COUNTY-DUBLIN"
