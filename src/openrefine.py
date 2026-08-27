from typing import NotRequired, TypedDict

from src.geo_types import MatchCandidate
from src.match import match_data
from src.type_detection import EntityType

"""
Align the matcher to the OpenRefine reconciliation API.

References:
    - https://www.w3.org/community/reports/reconciliation/CG-FINAL-specs-0.2-20230410/
    - https://github.com/OpenRefine/reconciliation_service_skeleton/blob/master/reconciliation_service.py
    - https://github.com/opensanctions/nomenklatura/tree/main
    - https://stackoverflow.com/questions/72326834/how-to-have-optional-keys-in-typeddict
"""


# OpenRefine types
TYPE_NAMES: dict[EntityType, str] = {
    "city": "City",
    "county": "County",
    "local_authority": "Local Authority",
}


class OpenRefineType(TypedDict):
    id: str
    name: str


class OpenRefineCandidateType(TypedDict):
    id: str
    name: str
    score: float
    type: list[OpenRefineType]


class ResultType(TypedDict):
    result: list[OpenRefineCandidateType]


class QueryType(TypedDict):
    query: str
    type: NotRequired[str | list[str] | None]
    limit: NotRequired[int]


def get_entity_type(query_type: str | list[str] | None) -> EntityType | None:
    """Return the entity type from query"""

    if isinstance(query_type, str) and query_type in TYPE_NAMES:
        return query_type

    # Process single type only.
    if isinstance(query_type, list) and len(query_type) == 1:
        entity_type = query_type[0]

        if entity_type in TYPE_NAMES:
            return entity_type

    return None


def candidate_to_openrefine(candidate: MatchCandidate) -> OpenRefineCandidateType:
    """Matcher candidate conversion to an OpenRefine candidate type."""

    entity_type: EntityType = candidate["type"]

    return {
        "id": candidate["id"],
        "name": candidate["name"],
        "score": candidate["score"],
        "type": [
            {
                "id": entity_type,
                "name": TYPE_NAMES.get(entity_type, entity_type),
            }
        ],
    }


def multiple_reconciliation(
    queries: dict[str, QueryType],
) -> dict[str, ResultType]:
    """
    Run each query of an OpenRefine with ("q0", "q1"...) ids.
    """

    response: dict[str, ResultType] = {}

    for query_id, reconciliation_query in queries.items():
        query = reconciliation_query.get("query", "")

        # If no match return empty list as result.
        if not query:
            response[query_id] = {"result": []}
            continue

        entity_type = get_entity_type(reconciliation_query.get("type"))

        limit = reconciliation_query.get("limit", 10)

        candidates = match_data(
            query=query,
            entity_type=entity_type,
            limit=limit,
        )

        response[query_id] = {
            "result": [candidate_to_openrefine(candidate) for candidate in candidates]
        }

    return response
