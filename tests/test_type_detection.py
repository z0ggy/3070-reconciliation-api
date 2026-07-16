from src.type_detection import type_detection


def test_type_detection():
    normalised_query = "dublin city"
    assert type_detection(normalised_query) == "city"
    normalised_query = "dublin county"
    assert type_detection(normalised_query) == "county"
