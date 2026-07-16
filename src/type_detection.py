from typing import Literal, TypeAlias

"""
References:
    - https://typing.python.org/en/latest/spec/aliases.html
"""

EntityType: TypeAlias = Literal["city", "county", "local_authority"]


def type_detection(normalised_query: str) -> EntityType | None:
    """Identify the place type from the cleaned/normalised query."""
    if not normalised_query:
        return None

    # Prioritise "council" and "local authority" over "city" or "county."
    if "council" in normalised_query or "local authority" in normalised_query:
        return "local_authority"

    if "city" in normalised_query:
        return "city"

    if "county" in normalised_query:
        return "county"
