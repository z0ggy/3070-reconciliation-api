punctuation_data = [
    ("Dublin!!!", "dublin"),
    ("Cork???", "cork"),
    ("Galway, City", "galway city"),
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

country_suffix_data = [
    ("Dublin, Ireland", "dublin"),
    ("Dublin. Ireland!?", "dublin"),
    ("Dublin Ireland", "dublin"),
    ("Dublin / Ireland", "dublin"),
]

place_type_data = [
    ("dublin city", "city"),
    ("city of dublin", "city"),
    ("county dublin", "county"),
    ("dublin county", "county"),
    ("dublin city council", "city"),
    ("galway county council", "county"),
    ("dublin local authority", "local_authority"),
    ("dublin", None),
    ("baile atha cliath", None),
]


country_context_data = [
    ("Dublin, Ireland", "dublin ireland"),
    ("Dublin / Ireland", "dublin ireland"),
    ("Dublin, Éire", "dublin eire"),
    ("County Cork, Ireland", "county cork ireland"),
    (
        "Dún Laoghaire-Rathdown / Ireland",
        "dun laoghaire rathdown ireland",
    ),
]

country_context_two_identical_records_dataset = [
    {
        "id": "IE-CITY-DUBLIN",
        "name": "Dublin",
        "type": "city",
        "country": "Ireland",
        "aliases": ["Dublin City"],
    },
    {
        "id": "US-CITY-DUBLIN",
        "name": "Dublin",
        "type": "city",
        "country": "USA",
        "aliases": ["Dublin Ohio"],
    },
]
