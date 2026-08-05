import pytest
from test_data.test_data import (
    accent_data,
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
    assert normaliser(city) == expected
