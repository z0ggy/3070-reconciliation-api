from src.utils.match import normalize_text


def test_exact_city_match():
    city = "Dublin"
    assert normalize_text(city) == "dublin"


def test_unormalized_exatct_city_match():
    city = "  DUblin  "
    assert normalize_text(city) == "dublin"
