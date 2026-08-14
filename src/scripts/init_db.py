from src.config import GEO_DATA_PATH, GEO_DB_PATH
from src.db.database import initialise_database

initialise_database(
    json_path=GEO_DATA_PATH,
    db_path=GEO_DB_PATH,
)

print(f"Database created: {GEO_DB_PATH}")
