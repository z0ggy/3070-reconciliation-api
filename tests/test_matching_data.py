from src.match import match_data


def test_match_data_perfect_match_by_name():
    result = match_data("Dublin")
    assert result[0]["name"] == "Dublin City"
    assert result[0]["type"] == "city"


def test_match_data_by_aliases_dublin():
    result = match_data("Baile Átha Cliath")
    assert result[0]["name"] == "Dublin City"
    assert result[0]["type"] == "city"
    assert result[0]["matched_on"] == "alias"


def test_match_data_by_normalized_official_name():
    result = match_data("Dun Laoghaire Rathdown")
    assert result[0]["name"] == "Dún Laoghaire-Rathdown"
    assert result[0]["type"] == "local_authority"
    assert result[0]["matched_on"] == "name"


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


def test_no_score():
    results = match_data("Paris")
    assert len(results) == 0
