from src.utils.match import match_engine


def test_exact_city_match():
    city = "Dublin"
    assert match_engine(city) == "Dublin"
