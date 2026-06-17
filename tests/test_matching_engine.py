from src.utils.match import normalize_text, similarity_score, match_data


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
    print(f"result: {result}")
    assert result[0] == {
        "id": "IE-CITY-DUBLIN",
        "name": "Dublin City",
        "type": "city",
        "country": "Ireland",
        "score": 1.0,
        "matched_on": "alias",
    }


def test_match_data_by_aliases():
    result = match_data("Baile Átha Cliath")
    print(f"result: {result}")
    assert result[0] == {
        "id": "IE-CITY-DUBLIN",
        "name": "Dublin City",
        "type": "city",
        "country": "Ireland",
        "score": 1.0,
        "matched_on": "alias",
    }


def test_shortcut_name():
    result = match_data("Co. Dublin")
    print(f"result: {result}")
    assert result[0]["name"] == "County Dublin"
