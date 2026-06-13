from src.utils.match import normalize_text


def test_exact_city_match():
    city = "Dublin"
    assert normalize_text(city) == "dublin"


def test_unormalized_exatct_city_match():
    city = "  DUblin  "
    assert normalize_text(city) == "dublin"


def test_extat_dash_match():
    city = "Dún Laoghaire-Rathdown "
    assert normalize_text(city) == "dún laoghaire rathdown"
