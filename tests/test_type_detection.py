def test_type_detection():
    normalised_query = "dublin city"
    assert type_detection(normalised_query) == "city"
