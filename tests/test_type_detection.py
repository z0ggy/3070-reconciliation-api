import pytest
from test_data.test_data import place_type_data

from src.place_normaliser import PlaceNameNormaliser
from src.type_detection import type_detection

# initialise instance of normaliser
place_normaliser = PlaceNameNormaliser()
normaliser = place_normaliser.normalise


@pytest.mark.parametrize("normalised_query, expected_type", place_type_data)
def test_type_detection(normalised_query, expected_type):
    assert type_detection(normalised_query) == expected_type
