from typing import cast

from fastapi.testclient import TestClient

from src.main import app
from src.service_manifest import ReconciliationMetadata

"""
References:
    - https://fastapi.tiangolo.com/reference/testclient/
"""


client = TestClient(app)


def test_openrefine_metadata_contains_required_fields():
    response = client.get("/openrefine/reconcile")

    assert response.status_code == 200

    metadata: ReconciliationMetadata = cast(ReconciliationMetadata, response.json())

    assert metadata["versions"] == ["0.2"]
    assert metadata["name"] == "Irish Geographic Reconciliation Service"
    assert metadata["identifierSpace"] == "http://localhost:8000/entity/"
    assert metadata["schemaSpace"] == "https://schema.org/Place"


def test_openrefine_metadata_contains_default_types():
    response = client.get("/openrefine/reconcile")

    metadata: ReconciliationMetadata = cast(ReconciliationMetadata, response.json())

    assert metadata["defaultTypes"] == [
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
    ]
