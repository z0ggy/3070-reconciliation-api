from src.utils.match import load_file, normalize_text, similarity_score


def test_exact_city_match():
    city = "Dublin"
    assert normalize_text(city) == "dublin"


def test_unormalized_exatct_city_match():
    city = "  DUblin  "
    assert normalize_text(city) == "dublin"


def test_extat_dash_match():
    city = "Dún Laoghaire-Rathdown "
    assert normalize_text(city) == "dún laoghaire rathdown"


def test_match_data_from_file():
    data = load_file()
    print(data)


def test_score():
    query = "  Dublin--  "
    candidate = "dUblin  - "
    score = similarity_score(query, candidate)
    assert score == 1.0
