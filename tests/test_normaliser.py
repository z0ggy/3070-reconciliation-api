from src.normalisation import PlaceNameNormaliser

# initialise instance of normaliser
place_normaliser = PlaceNameNormaliser()
normaliser = place_normaliser.normalise


def test_remove_punctuation():
    city = "Dublin, Ireland"
    assert normaliser(city) == "dublin ireland"


def test_remove_accent():
    city = "Dún-Laoghaire"
    assert normaliser(city) == "dun laoghaire"


def test_dash_replace():
    city = "Dublin-City"
    assert normaliser(city) == "dublin city"


def test_remove_extra_spaces():
    city = "   Dublin   !!!"
    assert normaliser(city) == "dublin"


def test_convert_county():
    city = "Co. Dublin"
    assert normaliser(city) == "county dublin"
