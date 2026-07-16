from typing import Literal, TypeAlias

"""
References:
    - https://typing.python.org/en/latest/spec/aliases.html
"""

EntityType: TypeAlias = Literal["city", "county"]


def type_detection(normalised_query: str) -> EntityType | None:
    """Identify the place type from the cleaned query."""
    if not normalised_query:
        return None

    if "city" in normalised_query:
        return "city"

    if "county" in normalised_query:
        return "county"
