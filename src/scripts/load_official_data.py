import json
import sys
from pathlib import Path
from typing import cast

from typing_extensions import TypedDict

from src.config import BASE_DIR

"""
Replace the manually created prototype dataset with official Irish source data.
Module can be run with: uv run -m src.scripts.load_official_data
References:
    - https://www.pythontutorials.net/blog/how-to-use-to-find-files-recursively/
"""

sys.path.insert(0, str(BASE_DIR))

LOGAINM_DIR: Path = BASE_DIR / "data" / "official" / "logainm"

# ---------------------------------------------------------
# Logainm official Irish dataset (counties, cities)
# ---------------------------------------------------------


def load_logainm_counties() -> list[dict]:  # pyright: ignore[reportUnknownParameterType, reportReturnType, reportMissingTypeArgument]
    """
    load counties from 4 files/pages counties*.json
    "totalCount": 32,
    "totalPages": 4,
    "currentPage": 1,
    "countPerPage": 10,
    "results": [
    """

    class LogainmType(TypedDict):
        totalCount: int
        totalPages: int
        currentPage: int
        countPerPage: int
        results: list[dict[str, object]]

    files: list[Path] = sorted(LOGAINM_DIR.glob("counties*.json"))

    if not files:
        raise FileNotFoundError(f"No files found in: {LOGAINM_DIR}")

    pages: dict[int, LogainmType] = {}

    for file_path in files:
        with file_path.open(encoding="utf-8") as file:
            data: LogainmType = cast(LogainmType, json.load(file))

        page_number: int = int(data["currentPage"])

        print(page_number)

        # Assign data to pages dict
        pages[page_number] = data


def main() -> None:
    counties = load_logainm_counties()  # pyright: ignore[reportUnknownVariableType]
    print(f" COUNTY-REC: {counties}")


if __name__ == "__main__":
    main()
