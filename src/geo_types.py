from typing import TypedDict

from src.type_detection import EntityType


class PlaceRecord(TypedDict):
    """A single record loaded from the geo dataset."""

    id: str
    name: str
    type: EntityType
    country: str
    aliases: list[str]


class MatchCandidate(TypedDict):
    """A scored, ranked candidate returned by the matcher."""

    id: str
    name: str
    type: EntityType
    country: str
    score: float
    matched_on: str
    matched_value: str
