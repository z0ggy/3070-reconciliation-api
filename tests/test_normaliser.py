import pytest
from test_data.test_data import (
    accent_data,
    country_context_data,
    country_suffix_data,
    county_data,
    dash_data,
    punctuation_data,
    space_data,
)

from src.place_normaliser import PlaceNameNormaliser

"""
References:
    - https://docs.pytest.org/en/7.1.x/example/parametrize.html
    - https://docs.pytest.org/en/stable/
"""


# initialise instance of normaliser
place_normaliser = PlaceNameNormaliser()
normaliser = place_normaliser.normalise
normaliser_base = place_normaliser.normalise_base
normaliser_with_context = place_normaliser.normalise_with_context


def test_sprint2():
    assert normaliser("Co. Dublin") == "county dublin"
    assert normaliser("Co Dublin") == "county dublin"
    assert normaliser("Dublin Co.") == "dublin county"

    assert normaliser("County of Dublin") == "county dublin"

    assert normaliser("Baile Átha Cliath") == "baile atha cliath"
    assert normaliser("Dún Laoghaire-Rathdown") == "dun laoghaire rathdown"

    assert normaliser("D.L.R.") == "dlr"
    assert normaliser("D L R") == "dlr"

    assert normaliser("Dublin, Ireland") == "dublin"
    assert normaliser("Dublin / Ireland") == "dublin"


@pytest.mark.parametrize("city, expected", punctuation_data)
def test_punctuation(city, expected):
    assert normaliser(city) == expected


@pytest.mark.parametrize("city, expected", accent_data)
def test_remove_accent(city, expected):
    assert normaliser(city) == expected


@pytest.mark.parametrize("city, expected", dash_data)
def test_dash_replace(city, expected):
    # found bug "Galway-Co." become "galway co" instead "galway county"
    # fixed by re-arrange normalisation pipeline
    assert normaliser(city) == expected


@pytest.mark.parametrize("city, expected", space_data)
def test_remove_extra_spaces(city, expected):
    assert normaliser(city) == expected


@pytest.mark.parametrize("city, expected", county_data)
def test_convert_county(city, expected):
    assert normaliser(city) == expected


@pytest.mark.parametrize("city, expected", country_suffix_data)
def test_remove_country_suffix(city, expected):
    """Obsolete remove country is replaced with context normaliser"""
    assert normaliser(city) == expected


@pytest.mark.parametrize("query, expected", country_context_data)
def test_normalise_with_context_retains_country(
    query: str,
    expected: str,
) -> None:
    assert normaliser_with_context(query) == expected


def test_normalise_base_preserve_country_context() -> None:
    result = normaliser_base(" Co. Dún-Laoghaire / Éire ")

    assert result == "county dun laoghaire eire"


def test_normalise_methods_return_empty_string() -> None:
    assert normaliser_base("") == ""
    assert normaliser("") == ""
    assert normaliser_with_context("") == ""
