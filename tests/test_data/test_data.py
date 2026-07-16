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
    ("dublin city council", "local_authority"),
    ("galway county council", "local_authority"),
    ("dublin local authority", "local_authority"),
    ("dublin", None),
    ("baile atha cliath", None),
]
