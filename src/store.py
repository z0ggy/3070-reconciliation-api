import sqlite3
from pathlib import Path
from typing import cast

from src.geo_types import PlaceRecord
from src.type_detection import EntityType

"""
References:
    - https://www.zetcode.com/python/sqlite3-connection-row-factory/
    - https://docs.python.org/3/library/sqlite3.html#sqlite3.Row
"""


class PlaceStore:
    """
    A wrapper that fetches place records from SQLite and formats for matcher as dictionary.
    This keeps SQL code separate from matcher.py logic.
    """

    def __init__(self, db_path: Path):
        self.db_path: Path = db_path

    def get_all_places(self) -> list[PlaceRecord]:
        with sqlite3.connect(self.db_path) as connection:
            # Read columns by name instead of index.
            connection.row_factory = sqlite3.Row

            place_rows: list[sqlite3.Row] = connection.execute(
                """
                SELECT
                    id,
                    official_name,
                    entity_type,
                    country
                FROM places
                ORDER BY id
                """
            ).fetchall()

            places: list[PlaceRecord] = []

            for row in place_rows:
                # For Basedpyright row type Any is too broad need to cast for explicit type.
                place_id: str = cast(str, row["id"])
                place_name: str = cast(str, row["official_name"])
                place_type: EntityType = cast(EntityType, row["entity_type"])
                place_country: str = cast(str, row["country"])
                aliases: list[str] = self.get_aliases(
                    connection,
                    place_id,
                )

                places.append(
                    {
                        "id": place_id,
                        "name": place_name,
                        "type": place_type,
                        "country": place_country,
                        "aliases": aliases,
                    }
                )

            return places

    def get_aliases(
        self,
        connection: sqlite3.Connection,
        place_id: str,
    ) -> list[str]:
        """Returns the alias names for a place"""
        rows: list[sqlite3.Row] = connection.execute(
            """
            SELECT alias
            FROM aliases
            WHERE place_id = ?
            ORDER BY id
            """,
            (place_id,),
        ).fetchall()

        return [cast(str, row["alias"]) for row in rows]
