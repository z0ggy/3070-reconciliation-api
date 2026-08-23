import json
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import NotRequired, cast

import pandas as pd
from typing_extensions import TypedDict

from src.config import BASE_DIR

"""
Replace the manually created prototype dataset with official Irish source data.
Module can be run with: uv run -m src.scripts.load_official_data
References:
    - https://www.pythontutorials.net/blog/how-to-use-to-find-files-recursively/
    - https://runebook.dev/en/docs/python/library/typing/typing.NotRequired
    - https://stackoverflow.com/questions/51710082/what-does-unicodedata-normalize-do-in-python
    - https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.iterrows.html
"""

sys.path.insert(0, str(BASE_DIR))

LOGAINM_DIR: Path = BASE_DIR / "data" / "official" / "logainm"
TAILTE_FILE: Path = BASE_DIR / "data" / "official" / "tailte" / "local_authorities.csv"


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

    id: str
    official_name: str
    entity_type: str
    country: str
    aliases: list[str]


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


def generate_postfix_id(value: str) -> str:
    """Convert a place name to uppercase part for an id."""

    # Strip accents for eg. "Dún" and "Dun" are the same id part.
    value = unicodedata.normalize("NFKD", value)
    value = value.encode("ascii", "ignore").decode("ascii")
    value = value.upper()

    cleaned: list[str] = []

    # Non letters and digits replace with a separator.
    for char in value:
        if char.isalnum():
            cleaned.append(char)
        else:
            cleaned.append("-")

    postfix: str = "".join(cleaned)

    # Replace leftover double dashes
    while "--" in postfix:
        postfix = postfix.replace("--", "-")

    # Remove edge dashes
    return postfix.strip("-")


def get_main_placename(
    record: LogainmRecord,
    language: str,
) -> str | None:
    for placename in record.get("placenames", []):
        if placename.get("language") == language and placename.get("main") is True:
            return placename.get("wording")

    return None


def clear_aliases(values: list[str | None]) -> list[str]:
    """
    Drop empty and duplicate aliases,
    Return list of unique aliases.
    """
    aliases: list[str] = []

    for value in values:
        if not value:
            continue

        value = value.strip()

        if value and value not in aliases:
            aliases.append(value)

    return aliases


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

        irish_name = get_main_placename(
            record,
            "ga",
        )

        if not english_name:
            continue

        # Append PlaceImport
        places.append(
            PlaceImport(
                id=(f"IE-COUNTY-{generate_postfix_id(english_name)}"),
                official_name=(f"County {english_name}"),
                entity_type="county",
                country="IRELAND",
                aliases=clear_aliases(
                    [
                        english_name,
                        irish_name,
                    ]
                ),
            )
        )
    # Check 26 ROI counties
    if len(places) != 26:
        raise RuntimeError(f"Expected 26 ROI counties: {len(places)}.")

    return places


# ---------------------------------------------------------
# Tailte Éireann official Irish dataset (local_authorities)
# ---------------------------------------------------------
def load_local_authorities() -> pd.DataFrame:
    """Load local_authorities.csv as DataFrame"""
    df: pd.DataFrame = pd.read_csv(
        TAILTE_FILE,
        encoding="utf-8-sig",
    )
    for column in df.columns:
        print(column)
    loc_auth = (
        df[
            [
                "BDY_ID",
                "ENG_NAME_VALUE",
                "GLE_NAME_VALUE",
                "BDY_TYPE_VALUE",
            ]
        ]
        .drop_duplicates(subset=["BDY_ID"])
        .copy()
    )

    if len(loc_auth) != 31:
        raise RuntimeError(f"Expected 31 local authorities: {len(loc_auth)}.")

    return loc_auth


def transform_local_authorities(
    local_authorities: pd.DataFrame,
) -> list[PlaceImport]:
    """
    Build local authority places from the Tailte DataFrame.
    The Irish name is uses as an alias.
    """
    places: list[PlaceImport] = []

    for _, row in local_authorities.iterrows():
        eng_name_value = cast(str, row["ENG_NAME_VALUE"]).strip()
        irish_name_value = cast(str, row["GLE_NAME_VALUE"]).strip()

        internal_id = f"IE-LA-{generate_postfix_id(eng_name_value)}"

        aliases: list[str | None] = []

        aliases.append(irish_name_value)

        places.append(
            PlaceImport(
                id=internal_id,
                official_name=eng_name_value,
                entity_type=("local_authority"),
                country="IRELAND",
                aliases=clear_aliases(aliases),
            )
        )

    return places


def main() -> None:
    counties: list[LogainmRecord] = load_logainm_counties()
    cities: list[LogainmRecord] = load_logainm_cities()
    places: list[PlaceImport] = transform_counties(counties)
    local_authorities = load_local_authorities()
    local_authorities_1 = transform_local_authorities(local_authorities)
    # print(f" COUNTY-REC: {counties}")
    # print(f" CITIES-REC: {cities}")
    # print(f"PLACES-REC: {places}")
    print(f"AUTHORITIES-TRANSFORM: {local_authorities_1}")
    for auth in local_authorities_1:
        print(auth.id)


if __name__ == "__main__":
    main()
