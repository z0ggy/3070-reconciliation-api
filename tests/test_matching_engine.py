from src.utils.match import match_data, normalize_text, similarity_score


def test_exact_city_match():
    city = "Dublin"
    assert normalize_text(city) == "dublin"


def test_unormalized_exatct_city_match():
    city = "  DUblin  "
    assert normalize_text(city) == "dublin"


def test_extat_dash_match():
    city = "Dún Laoghaire-Rathdown "
    assert normalize_text(city) == "dún laoghaire rathdown"


def test_basic_score():
    query = "  Dublin--  "
    candidate = "dUblin  - "
    score = similarity_score(query, candidate)
    assert score == 1.0


def test_city_with_county():
    query = "County Dublin -- "
    candidate = "dUblin  - "
    score = similarity_score(query, candidate)
    assert score == 0.9


def test_city():
    query = "City"
    candidate = "dUblin  - "
    score = similarity_score(query, candidate)
    print(score)


def test_match_data_perfect_match_by_name():
    result = match_data("Dublin")
    assert result[0]["name"] == "Dublin City"
    assert result[0]["type"] == "city"


def test_match_data_by_aliases_dublin():
    result = match_data("Baile Átha Cliath")
    assert result[0]["name"] == "Dublin City"
    assert result[0]["type"] == "city"
    assert result[0]["matched_on"] == "alias"


def test_match_data_by_aliases_dun():
    result = match_data("Dun Laoghaire Rathdown")
    assert result[0]["name"] == "Dún Laoghaire-Rathdown"
    assert result[0]["type"] == "local_authority"
    assert result[0]["matched_on"] == "alias"


def test_county_name():
    result = match_data("Co. Dublin")
    assert result[0]["name"] == "County Dublin"


def test_type_filter():
    result = match_data("Dublin", entity_type="city")
    assert result[0]["type"] == "city"
    assert result[0]["name"] == "Dublin City"


def test_multiple_candidates_city_county_match():
    results = match_data("Dublin")
    names = [result["name"] for result in results]
    assert "Dublin City" in names
    assert "County Dublin" in names


def test_misspeling_city():
    results = match_data("Dubln")
    names = [result["name"] for result in results]
    assert "Dublin City" in names
    assert "County Dublin" in names


def test_no_score():
    results = match_data("Paris")
    assert len(results) == 0
