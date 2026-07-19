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


def test_exact_official_name_outranks_fuzzy_alternative():
    """Exact official name match should ranks above a longer fuzzy match."""
    dataset = [
        {
            "id": "IE-CITY-DUBLIN",
            "name": "Dublin City",
            "type": "city",
            "country": "Ireland",
            "aliases": [],
        },
        {
            "id": "IE-CITY-DUBLIN-SOUTH",
            "name": "Dublin City South",
            "type": "city",
            "country": "Ireland",
            "aliases": [],
        },
    ]

    results = matcher.match("Dublin City", dataset)

    assert results[0]["id"] == "IE-CITY-DUBLIN"
    assert results[0]["matched_on"] == "name"


def test_exact_alias_outranks_weak_official_name_similarity():
    """Aliases are should be included in ranking."""
    dataset = [
        {
            "id": "IE-CITY-DUBLIN",
            "name": "Dublin City",
            "type": "city",
            "country": "Ireland",
            "aliases": ["Baile Átha Cliath"],
        },
        {
            "id": "IE-CITY-GALWAY",
            "name": "Galway City",
            "type": "city",
            "country": "Ireland",
            "aliases": [],
        },
    ]

    results = matcher.match("Baile Atha Cliath", dataset)

    assert results[0]["id"] == "IE-CITY-DUBLIN"
    assert results[0]["matched_on"] == "alias"


def test_correctly_spelled_candidate_outranks_close_typo_candidate():
    """The exact correctly spelled value should receive the highest score."""
    dataset = [
        {
            "id": "IE-CITY-GALWAY",
            "name": "Galway",
            "type": "city",
            "country": "Ireland",
            "aliases": [],
        },
        {
            "id": "TEST-CITY-GALLWAY",
            "name": "Gallway",
            "type": "city",
            "country": "Ireland",
            "aliases": [],
        },
    ]

    results = matcher.match("Galway", dataset)

    assert results[0]["id"] == "IE-CITY-GALWAY"


def test_county_query_ranks_county_above_city():
    dataset = [
        {
            "id": "IE-CITY-DUBLIN",
            "name": "Dublin",
            "type": "city",
            "country": "Ireland",
            "aliases": [],
        },
        {
            "id": "IE-COUNTY-DUBLIN",
            "name": "Dublin",
            "type": "county",
            "country": "Ireland",
            "aliases": [],
        },
    ]

    results = matcher.match("County Dublin", dataset)

    assert results[0]["id"] == "IE-COUNTY-DUBLIN"
    assert results[0]["score"] > results[1]["score"]


def test_city_query_ranks_city_above_county():
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

    assert results[0]["id"] == "IE-CITY-DUBLIN"
    assert results[0]["score"] > results[1]["score"]


def test_council_query_ranks_local_authority_above_city_and_county():
    dataset = [
        {
            "id": "TEST-CITY-DUBLIN",
            "name": "Dublin",
            "type": "city",
            "country": "Ireland",
            "aliases": [],
        },
        {
            "id": "TEST-COUNTY-DUBLIN",
            "name": "Dublin",
            "type": "county",
            "country": "Ireland",
            "aliases": [],
        },
        {
            "id": "TEST-LA-DUBLIN",
            "name": "Dublin",
            "type": "local_authority",
            "country": "Ireland",
            "aliases": [],
        },
    ]

    results = matcher.match("Dublin Council", dataset)

    assert results[0]["id"] == "TEST-LA-DUBLIN"
    assert results[0]["score"] > results[1]["score"]
    assert results[0]["score"] > results[2]["score"]


def test_equal_scores_are_sorted_deterministically():
    dataset = [
        {
            "id": "B-ID",
            "name": "B-test",
            "type": "city",
            "country": "Ireland",
            "aliases": ["Dublin"],
        },
        {
            "id": "A-ID",
            "name": "A-test",
            "type": "city",
            "country": "Ireland",
            "aliases": ["Dublin"],
        },
    ]

    results = matcher.match("Dublin", dataset)

    assert results[0]["id"] == "A-ID"
    assert results[1]["id"] == "B-ID"


def test_record_is_not_duplicated_when_multiple_aliases_match():
    """Record appears only once"""
    dataset = [
        {
            "id": "IE-CITY-DUBLIN",
            "name": "Dublin City",
            "type": "city",
            "country": "Ireland",
            "aliases": [
                "Dublin",
                "Dublin City",
                "City of Dublin",
            ],
        }
    ]

    results = matcher.match("Dublin City", dataset)

    assert len(results) == 1
    assert results[0]["id"] == "IE-CITY-DUBLIN"


def test_limit_is_applied_after_ranking():
    """Limit is passed as argument default is set to 10"""
    dataset = [
        {
            "id": "A-ID",
            "name": "Dublin Place",
            "type": "city",
            "country": "Ireland",
            "aliases": [],
        },
        {
            "id": "B-ID",
            "name": "Dublin City",
            "type": "city",
            "country": "Ireland",
            "aliases": [],
        },
    ]

    results = matcher.match(
        "Dublin City",
        dataset,
        limit=1,
    )

    assert len(results) == 1
    assert results[0]["id"] == "B-ID"
