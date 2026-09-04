from src.match import match_data


def test_match_data_perfect_match_by_name():
    candidates = match_data("Dublin")
    top_ids = [candidate["id"] for candidate in candidates[:2]]

    assert "IE-CITY-DUBLIN" in top_ids
    assert "IE-COUNTY-DUBLIN" in top_ids


def test_match_data_by_aliases_dublin():
    candidates = match_data("Baile Átha Cliath")
    top_candidates = candidates[:2]
    top_ids = [candidate["id"] for candidate in top_candidates]

    assert "IE-CITY-DUBLIN" in top_ids
    assert "IE-COUNTY-DUBLIN" in top_ids
    assert all(candidate["matched_on"] == "alias" for candidate in top_candidates)


def test_match_data_by_normalized_official_name():
    results = match_data("Dun Laoghaire Rathdown")

    assert results
    assert results[0]["id"] == "IE-LA-DLR"
    assert results[0]["type"] == "local_authority"


def test_county_name():
    result = match_data("Co. Dublin")
    assert result[0]["name"] == "County Dublin"


def test_type_filter():
    result = match_data("Dublin", entity_type="city")
    assert result[0]["type"] == "city"
    assert result[0]["name"] == "Dublin City"
    assert result[0]["score"] == 1.0


def test_multiple_candidates_city_county_match():
    results = match_data("Dublin")
    names = [result["name"] for result in results]
    assert "Dublin City" in names
    assert "County Dublin" in names


def test_misspelling_city():
    results = match_data("Dubln")
    names = [result["name"] for result in results]
    assert "Dublin City" in names
    assert "County Dublin" in names


##############SPRINT2 tests
def test_match_data_by_extended_aliases_dublin():
    result = match_data("City of Dublin")
    assert result[0]["name"] == "Dublin City"
    assert result[0]["type"] == "city"
    assert result[0]["matched_on"] == "alias"
