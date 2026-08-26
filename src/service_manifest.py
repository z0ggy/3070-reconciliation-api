from typing import TypedDict

"""
Based on w3c documentation the API0.2 requires at least:
versions name, API 0.2
identifierSpace (The URI namespace for the identifiers of an entity returned by the reconciliation service),
schemaSpace (https://schema.org/Thing.)
References:
    - https://w3c.github.io/cg-reports/reconciliation/CG-FINAL-specs-0.2-20230410/
"""


class ReconciliationType(TypedDict):
    id: str
    name: str


class ReconciliationMetadata(TypedDict):
    versions: list[str]
    name: str
    identifierSpace: str
    schemaSpace: str
    defaultTypes: list[ReconciliationType]
    batchSize: int


def get_service_metadata() -> ReconciliationMetadata:
    return {
        "versions": ["0.2"],
        "name": "Irish Geographic Reconciliation Service",
        "identifierSpace": "http://localhost:8000/entity/",
        "schemaSpace": "https://schema.org/Place",
        "defaultTypes": [
            {
                "id": "city",
                "name": "City",
            },
            {
                "id": "county",
                "name": "County",
            },
            {
                "id": "local_authority",
                "name": "Local Authority",
            },
        ],
        "batchSize": 10,
    }
