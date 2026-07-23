import pytest
from test_data.test_data import place_type_data

from src.place_normaliser import PlaceNameNormaliser
from src.type_detection import EntityType, resolve_type, type_detection

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


def test_city_has_priority_over_council():
    assert type_detection("dublin city council") == "city"


def test_county_has_priority_over_council():
    assert type_detection("dlr county council") == "county"


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


@pytest.mark.parametrize(
    ("normalised_query", "expected_type"),
    [
        # Local-authority phrase has the highest precedence.
        ("dublin local authority", "local_authority"),
        ("dublin city local authority", "local_authority"),
        ("dublin county local authority", "local_authority"),
        ("dublin city county local authority", "local_authority"),
        # Conflicting city and county cues.
        ("dublin city county", None),
        # City/county words are stronger than council.
        ("dublin city council", "city"),
        ("dublin county council", "county"),
        # Individual type cues.
        ("dublin city", "city"),
        ("county dublin", "county"),
        # Bare council cue.
        ("dublin council", "local_authority"),
        ("council dublin", "local_authority"),
        # No type context.
        ("dublin", None),
        ("", None),
    ],
)
def test_type_detection_priority(
    normalised_query: str,
    expected_type: EntityType | None,
) -> None:
    assert type_detection(normalised_query) == expected_type


@pytest.mark.parametrize(
    "normalised_query",
    [
        "countywide dublin",
        "councillor dublin",
        "local dublin authority",
        "local authorities dublin",
    ],
)
def test_type_detection_matches_exact_words(
    normalised_query: str,
) -> None:
    """Ensures type detection only matches full words and properly spaced types (local authority)."""
    assert type_detection(normalised_query) is None
