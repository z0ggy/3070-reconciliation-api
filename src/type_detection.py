from typing import Literal, TypeAlias

"""
References:
    - https://typing.python.org/en/latest/spec/aliases.html
    - https://www.w3schools.com/python/ref_set_issubset.asp
"""

EntityType: TypeAlias = Literal["city", "county", "local_authority"]


def type_detection(normalised_query: str) -> EntityType | None:
    """Identify the place type from the cleaned/normalised query."""
    if not normalised_query:
        return None

    # Check whole word instead of just substring in normalised_query
    words = set(normalised_query.split())

    # Return True/False if all items in set x are present in set y
    is_local_authority = {"local", "authority"}.issubset(words)

    # Prioritise "council" and "local authority" over "city" or "county."
    # if "council" in words or ("local" in words and "authority" in words):
    if is_local_authority:
        return "local_authority"

    # Handle conflicted type like "dublin city county"
    if "city" in words and "county" in words:
        return None

    if "city" in words:
        return "city"

    if "county" in words:
        return "county"

    # Council without city or county context.
    if "council" in words:
        return "local_authority"

    return None


def resolve_type(
    normalised_query: str,
    explicit_entity_type: EntityType | None = None,
) -> EntityType | None:
    """
    Use the specified type if provided. Otherwise, get it from the query.
    """

    if explicit_entity_type is not None:
        return explicit_entity_type

    return type_detection(normalised_query)
