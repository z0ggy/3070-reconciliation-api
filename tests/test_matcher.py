from test_data.test_data import country_context_two_identical_records_dataset

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


def test_matching_type_get_bonus():
    """
    Both records have the same name.
    adding a county to the query, record with county is ranked first.
    """
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

    results = matcher.match("County Dublin", dataset)

    assert results[0]["id"] == "IE-COUNTY-DUBLIN"
    assert results[0]["type"] == "county"
    assert results[0]["score"] > results[1]["score"]


def test_matching_type_get_penalty():
    """
    Both records have the same name.
    adding a city to the query, record with city get bonus,
    record with count get penalty score.
    """
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

    city_result = None
    county_result = None

    for result in results:
        if result["type"] == "city":
            city_result = result
        elif result["type"] == "county":
            county_result = result

    assert city_result is not None
    assert county_result is not None
    assert city_result["score"] > county_result["score"]


def test_no_explicit_type_skip_adjust_scores():
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

    results = matcher.match("Dublin", dataset)

    assert results[0]["score"] == results[1]["score"]


def test_type_bonus_is_not_bigger_than_one():
    """Adding `0.05` to perfect match (1.0) must return `1.0`."""
    dataset = [
        {
            "id": "IE-COUNTY-DUBLIN",
            "name": "County Dublin",
            "type": "county",
            "country": "Ireland",
            "aliases": [],
        },
    ]

    results = matcher.match("County Dublin", dataset)

    assert results[0]["score"] == 1.0


def test_type_adjustment_favourite_exact_name_match():
    """
    Query detect "local_authority", city gets penalty,
    "local_authority" gets bonus. Exact match rank should be above
    unrelated "Cork" candidate.
    """
    dataset = [
        {
            "id": "IE-CITY-DUBLIN",
            "name": "Dublin City Council",
            "type": "city",
            "country": "Ireland",
            "aliases": [],
        },
        {
            "id": "IE-LA-CORK",
            "name": "Cork County Council",
            "type": "local_authority",
            "country": "Ireland",
            "aliases": [],
        },
    ]

    results = matcher.match("Dublin City Council", dataset)

    assert results[0]["id"] == "IE-CITY-DUBLIN"


def test_explicit_type_filter_skip_conflicting_names():
    """
    The query contain word "city", entity_type="county".
    The county should win.
    """
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
    assert results[0]["id"] == "IE-COUNTY-DUBLIN"


def test_explicit_country_filters_candidates():
    # Two identically named records
    dataset = country_context_two_identical_records_dataset
    results = matcher.match(
        query="Dublin",
        dataset=dataset,
        country="Ireland",
    )

    assert len(results) == 1
    assert results[0]["id"] == "IE-CITY-DUBLIN"


def test_unknown_explicit_country_returns_no_candidates():
    dataset = country_context_two_identical_records_dataset
    results = matcher.match(
        query="Dublin",
        dataset=dataset,
        country="France",
    )

    assert results == []


def test_country_in_query_score_top():
    """Query country get bonus"""
    dataset = country_context_two_identical_records_dataset
    results = matcher.match(
        query="Dublin, Ireland",
        dataset=dataset,
    )

    assert len(results) == 2
    assert results[0]["id"] == "IE-CITY-DUBLIN"
    assert results[1]["id"] == "US-CITY-DUBLIN"
    assert results[0]["score"] > results[1]["score"]


def test_eire_context_matches_ireland():
    """Éire (Irish name) maps to Ireland"""
    dataset = country_context_two_identical_records_dataset
    results = matcher.match(
        query="Dublin, Éire",
        dataset=dataset,
    )

    assert results[0]["id"] == "IE-CITY-DUBLIN"


def test_explicit_country_overrides_detected_country():
    """Explicit country overrides query context"""
    dataset = country_context_two_identical_records_dataset
    results = matcher.match(
        query="Dublin, Ireland",
        dataset=dataset,
        country="USA",
    )

    assert len(results) == 1
    assert results[0]["id"] == "US-CITY-DUBLIN"
