import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import NotRequired, cast

from typing_extensions import TypedDict

from src.config import BASE_DIR

"""
Replace the manually created prototype dataset with official Irish source data.
Module can be run with: uv run -m src.scripts.load_official_data
References:
    - https://www.pythontutorials.net/blog/how-to-use-to-find-files-recursively/
    - https://runebook.dev/en/docs/python/library/typing/typing.NotRequired
"""

sys.path.insert(0, str(BASE_DIR))

LOGAINM_DIR: Path = BASE_DIR / "data" / "official" / "logainm"


# ---------------------------------------------------------
# Logainm official Irish dataset (counties, cities)
# ---------------------------------------------------------


class Placename(TypedDict):
    """
    Represents a place in one language in records.
    English ("en")
    Irish ("ga")
    "main" is optional because is the official.
    """

    language: str
    wording: str
    main: NotRequired[bool]


class LogainmRecord(TypedDict):
    """
    A single place from Logainm records.
    """

    id: int
    placenames: list[Placename]
    northernIreland: NotRequired[dict[str, str] | None]


class LogainmType(TypedDict):
    """One page of results from Logainm dataset."""

    totalCount: int
    totalPages: int
    currentPage: int
    countPerPage: int
    results: list[LogainmRecord]


@dataclass
class PlaceImport:
    """Database schema, place with aliases."""

    official_name: str
    entity_type: str
    country: str


def load_logainm_counties() -> list[LogainmRecord]:
    """
    load counties from 4 files/pages counties*.json
    "totalCount": 32,
    "totalPages": 4,
    "currentPage": 1,
    "countPerPage": 10,
    "results": [
    """

    files: list[Path] = sorted(LOGAINM_DIR.glob("counties*.json"))

    if not files:
        raise FileNotFoundError(f"No files found in: {LOGAINM_DIR}")

    pages: dict[int, LogainmType] = {}

    for file_path in files:
        with file_path.open(encoding="utf-8") as file:
            data: LogainmType = cast(LogainmType, json.load(file))

        page_number: int = int(data["currentPage"])

        # Assign data to pages dict
        pages[page_number] = data

    records: list[LogainmRecord] = []

    for page_number in sorted(pages):
        records.extend(pages[page_number]["results"])

    return records


def load_logainm_cities() -> list[LogainmRecord]:
    path: Path = LOGAINM_DIR / "cities.json"

    with path.open(encoding="utf-8") as file:
        data: LogainmType = cast(LogainmType, json.load(file))

    return data["results"]


def get_main_placename(
    record: LogainmRecord,
    language: str,
) -> str | None:
    for placename in record.get("placenames", []):
        if placename.get("language") == language and placename.get("main") is True:
            return placename.get("wording")

    return None


def transform_counties(records: list[LogainmRecord]) -> list[PlaceImport]:
    """
    Build county places from load_logainm_counties().
    Dataset contains records for all 32 counties on the island(Northern Ireland and Republic)
    extract only Republic.
    """
    places: list[PlaceImport] = []

    for record in records:
        northern_ireland: dict[str, str] = record.get("northernIreland") or {}

        if northern_ireland.get("extent") == "all":
            continue

        english_name = get_main_placename(
            record,
            "en",
        )
        if not english_name:
            continue

        places.append(
            PlaceImport(
                official_name=(f"County {english_name}"),
                entity_type="county",
                country="IRELAND",
            ),
        )
    print("LEN-PLACES: ", len(places) == 26)

    return places


def main() -> None:
    counties: list[LogainmRecord] = load_logainm_counties()
    cities: list[LogainmRecord] = load_logainm_cities()
    places: list[PlaceImport] = transform_counties(counties)
    # print(f" COUNTY-REC: {counties}")
    # print(f" CITIES-REC: {cities}")
    print(f"PLACES-REC: {places}")


if __name__ == "__main__":
    main()
