import pytest
from test_data.test_data import place_type_data

from src.place_normaliser import PlaceNameNormaliser
from src.type_detection import resolve_type, type_detection

# initialise instance of normaliser
place_normaliser = PlaceNameNormaliser()
normaliser = place_normaliser.normalise


@pytest.mark.parametrize("normalised_query, expected_type", place_type_data)
def test_type_detection(normalised_query, expected_type):
    assert type_detection(normalised_query) == expected_type


def test_detect_county_abbreviation_after_normalisation():
    normalised_query = normaliser("Co. Dublin")

    assert normalised_query == "county dublin"
    assert type_detection(normalised_query) == "county"


def test_detect_county_suffix_after_normalisation():
    normalised_query = normaliser("Galway Co.")

    assert normalised_query == "galway county"
    assert type_detection(normalised_query) == "county"


def test_council_has_priority_over_city():
    assert type_detection("dublin city council") == "local_authority"


def test_council_has_priority_over_county():
    assert type_detection("dlr county council") == "local_authority"


def test_detect_city_and_county_conflict():
    assert type_detection("dublin city county") is None


def test_passed_entity_type_in_query_overrides_type_detection():
    normalised_query = "county dublin"
    entity_type = "city"
    result = resolve_type(normalised_query, entity_type)

    assert result == "city"


def test_type_detection_used_without_entity_type():
    normalised_query = "county dublin"
    entity_type = None
    result = resolve_type(normalised_query, entity_type)

    assert result == "county"
