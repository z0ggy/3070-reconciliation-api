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

    # Check whole word instead of just substring in normalised_query
    words = normalised_query.split()

    # Prioritise "council" and "local authority" over "city" or "county."
    if "council" in words or ("local" in words and "authority" in words):
        return "local_authority"

    if "city" in words:
        return "city"

    if "county" in words:
        return "county"

    return None
