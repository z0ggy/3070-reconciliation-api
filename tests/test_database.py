import sqlite3

from src.db.database import create_database

"""
References:
    - https://stackoverflow.com/questions/947215/how-do-i-get-a-list-of-table-column-names-from-an-sqlite-database
    - How to use temporary directories and files in tests (https://docs.pytest.org/en/7.1.x/how-to/tmp_path.html)
"""


def test_create_database_creates_expected_tables(tmp_path):
    """
    Test migration from JSON to SQLite
    tmp_path: pytest built-in fixture for temporary directory destroyed after tests
    """
    db_path = tmp_path / "test.db"

    create_database(db_path)

    with sqlite3.connect(db_path) as connection:
        """
        sqlite_master: stores metadata about every object in the DB (tables, indexes...)
        """
        tables = connection.execute(
            """
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
            """
        ).fetchall()

    print(f"TABLES: {tables}")

    assert "places" in tables[0]
    assert "aliases" in tables[1]
