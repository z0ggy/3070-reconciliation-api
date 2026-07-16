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
    if "council" in words or "local authority" in words:
        return "local_authority"

    if "city" in words:
        return "city"

    if "county" in words:
        return "county"

    return None


def resolve_type(
    normalised_query: str,
    entity_type: str | None = None,
) -> str | None:
    """
    Use the specified type if provided. Otherwise, get it from the query.
    """

    if entity_type is not None:
        return entity_type

    return type_detection(normalised_query)
