import json
import sys
from pathlib import Path

"""
Replace the manually created prototype dataset with official Irish source data.
References:
    - https://www.pythontutorials.net/blog/how-to-use-to-find-files-recursively/
"""


BASE_DIR: Path = Path(__file__).resolve().parents[1]

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
    print(f"BASE_DIR: {BASE_DIR}")
    print(f"LOGAINM_DIR: {LOGAINM_DIR}")

    files: list[Path] = sorted(LOGAINM_DIR.glob("counties*.json"))
    print(f"FILES: {files}")

    if not files:
        raise FileNotFoundError(f"No files found in: {LOGAINM_DIR}")

    pages: dict[int, dict] = {}  # pyright: ignore[reportMissingTypeArgument, reportUnknownVariableType]

    for file_path in files:
        with file_path.open(encoding="utf-8") as file:
            data = json.load(file)  # pyright: ignore[reportAny]

        page_number: int = int(data["currentPage"])  # pyright: ignore[reportAny]

        print(page_number)

        # Assign data to pages dict
        pages[page_number] = data


def main() -> None:
    counties = load_logainm_counties()  # pyright: ignore[reportUnknownVariableType]
    print(f" COUNTY-REC: {counties}")


if __name__ == "__main__":
    main()
