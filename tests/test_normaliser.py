import pytest

from src.place_normaliser import PlaceNameNormaliser

"""
References:
    - https://docs.pytest.org/en/7.1.x/example/parametrize.html
    - https://docs.pytest.org/en/stable/
"""

punctuation_data = [
    ("Dublin, Ireland", "dublin ireland"),
    ("Dublin. Ireland!?", "dublin ireland"),
]

accent_data = [
    ("Dún-Laoghaire", "dun laoghaire"),
    ("Cill Chomáin Mhór Theas ", "cill chomain mhor theas"),
]

dash_data = [
    ("Dublin-City", "dublin city"),
    ("Galway-Co.", "galway county"),
]

space_data = [
    ("   Dublin   !!!", "dublin"),
    ("!!@    Cork ", "cork"),
]

county_data = [
    ("Co.!!! Dublin city", "county dublin city"),
    ("Galway  !!! Co.", "galway county"),
]

# initialise instance of normaliser
place_normaliser = PlaceNameNormaliser()
normaliser = place_normaliser.normalise


@pytest.mark.parametrize("city, expected", punctuation_data)
def test_punctuation(city, expected):
    assert normaliser(city) == expected


@pytest.mark.parametrize("city, expected", accent_data)
def test_remove_accent(city, expected):
    assert normaliser(city) == expected


@pytest.mark.parametrize("city, expected", dash_data)
def test_dash_replace(city, expected):
    # found bug "Galway-Co." become "galway co" instead "galway county"
    # fix by re-arrange normalisation pipeline
    assert normaliser(city) == expected


@pytest.mark.parametrize("city, expected", space_data)
def test_remove_extra_spaces(city, expected):
    assert normaliser(city) == expected


@pytest.mark.parametrize("city, expected", county_data)
def test_convert_county(city, expected):
    assert normaliser(city) == expected
