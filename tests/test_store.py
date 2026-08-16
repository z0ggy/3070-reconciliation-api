import sqlite3
from pathlib import Path

from src.db.database import create_database
from src.geo_types import PlaceRecord
from src.store import PlaceStore

"""
References:
    - How to use temporary directories and files in tests (https://docs.pytest.org/en/7.1.x/how-to/tmp_path.html)
"""


def test_store_records_with_aliases(tmp_path: Path) -> None:
    # tmp_path: pytest built-in fixture for temporary directory destroyed after tests.
    db_path: Path = tmp_path / "test.db"

    create_database(db_path)

    with sqlite3.connect(db_path) as connection:
        _ = connection.execute(
            """
            INSERT INTO places (
                id,
                official_name,
                entity_type,
                country
            )
            VALUES (?, ?, ?, ?)
            """,
            (
                "IE-CITY-DUBLIN",
                "Dublin City",
                "city",
                "Ireland",
            ),
        )

        _ = connection.execute(
            """
            INSERT INTO aliases (
                place_id,
                alias
            )
            VALUES (?, ?)
            """,
            (
                "IE-CITY-DUBLIN",
                "Dublin",
            ),
        )

        _ = connection.execute(
            """
            INSERT INTO aliases (
                place_id,
                alias
            )
            VALUES (?, ?)
            """,
            (
                "IE-CITY-DUBLIN",
                "Baile Átha Cliath",
            ),
        )

    store: PlaceStore = PlaceStore(db_path)

    places: list[PlaceRecord] = store.get_all_places()

    assert len(places) == 1

    assert places[0] == {
        "id": "IE-CITY-DUBLIN",
        "name": "Dublin City",
        "type": "city",
        "country": "Ireland",
        "aliases": [
            "Dublin",
            "Baile Átha Cliath",
        ],
    }


def test_store_returns_empty_alias(tmp_path: Path) -> None:
    # tmp_path: pytest built-in fixture for temporary directory destroyed after tests.
    db_path: Path = tmp_path / "test.db"

    create_database(db_path)

    with sqlite3.connect(db_path) as connection:
        _ = connection.execute(
            """
                INSERT INTO places (
                    id,
                    official_name,
                    entity_type,
                    country
                )
                VALUES (?, ?, ?, ?)
                """,
            (
                "IE-COUNTY-CORK",
                "County Cork",
                "county",
                "Ireland",
            ),
        )

    store: PlaceStore = PlaceStore(db_path)

    places: list[PlaceRecord] = store.get_all_places()

    assert places[0]["aliases"] == []
