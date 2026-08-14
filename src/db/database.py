import json
import sqlite3
from pathlib import Path

"""
References:
    -https://stackoverflow.com/questions/8811783/convert-json-to-sqlite-table
    -https://dev.to/kamranakhan/python-convert-json-to-sqlite-4a5n
    -https://www.iditect.com/faq/python/convert-json-to-sqlite-in-python--how-to-map-json-keys-to-database-columns-properly.html
"""


def create_database(db_path: Path) -> None:

    # Open connection and open/create database file if not exists.
    with sqlite3.connect(db_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        # Store the official record for each place.
        # CHECK: constraint restricts values to (city, county, local_authority)
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS places (
                id TEXT PRIMARY KEY,
                official_name TEXT NOT NULL,
                entity_type TEXT NOT NULL
                    CHECK (
                        entity_type IN (
                            'city',
                            'county',
                            'local_authority'
                        )
                    ),
                country TEXT NOT NULL
            )
            """
        )

        # Store the aliases for each place.
        #  UNIQUE: prevents duplicate aliases for one place..
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS aliases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                place_id TEXT NOT NULL,
                alias TEXT NOT NULL,

                FOREIGN KEY (place_id)
                    REFERENCES places(id)
                    ON DELETE CASCADE,

                UNIQUE (place_id, alias)
            )
            """
        )

        connection.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_aliases_place_id
            ON aliases(place_id)
            """
        )


def import_json_data(
    json_path: Path,
    db_path: Path,
) -> None:
    with json_path.open("r", encoding="utf-8") as file:
        records = json.load(file)

    with sqlite3.connect(db_path) as connection:
        connection.execute("PRAGMA foreign_keys = ON")

        for record in records:
            connection.execute(
                """
                INSERT OR REPLACE INTO places (
                    id,
                    official_name,
                    entity_type,
                    country
                )
                VALUES (?, ?, ?, ?)
                """,
                (
                    record["id"],
                    record["name"],
                    record["type"],
                    record["country"],
                ),
            )

            for alias in record.get("aliases", []):
                connection.execute(
                    """
                    INSERT OR IGNORE INTO aliases (
                        place_id,
                        alias
                    )
                    VALUES (?, ?)
                    """,
                    (
                        record["id"],
                        alias,
                    ),
                )


def initialise_database(
    json_path: Path,
    db_path: Path,
) -> None:
    create_database(db_path)
    import_json_data(json_path, db_path)
