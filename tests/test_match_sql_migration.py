from src.config import GEO_DATA_PATH, GEO_DB_PATH
from src.data_loader import load_json_file
from src.geo_types import PlaceRecord
from src.store import PlaceStore


def test_sqlite_refers_to_same_place() -> None:
    """Compare old json data to new sql migration"""

    store: PlaceStore = PlaceStore(GEO_DB_PATH)

    # Load JSON data
    json_places: list[PlaceRecord] = load_json_file(GEO_DATA_PATH)

    # Load SQL data
    sqlite_places: list[PlaceRecord] = store.get_all_places()

    json_id: dict[str, PlaceRecord] = {place["id"]: place for place in json_places}

    sqlite_id: dict[str, PlaceRecord] = {place["id"]: place for place in sqlite_places}

    assert sqlite_id == json_id
