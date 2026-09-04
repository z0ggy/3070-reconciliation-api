import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.match import match_data

client = TestClient(app)

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "final_context_cases.json"


with FIXTURE_PATH.open(encoding="utf-8") as file:
    ranking_cases = json.load(file)


@pytest.mark.parametrize(
    "case",
    ranking_cases,
    ids=lambda case: case["case_id"],
)
def test_expected_candidate_is_ranked_first(case):
    results = match_data(
        query=case["query"],
        entity_type=case["entity_type"],
        limit=10,
    )

    expected_id = case["expected_id"]

    if expected_id is None:
        assert results == []
        return

    assert results
    assert results[0]["id"] == expected_id
    assert results[0]["type"] == case["expected_type"]


def test_dublin_is_ambiguous():
    response = client.get("/reconcile?q=Dublin")

    body = response.json()

    assert body["ambiguous"] is True

    ids = [candidate["id"] for candidate in body["candidates"][:2]]

    assert "IE-CITY-DUBLIN" in ids
    assert "IE-COUNTY-DUBLIN" in ids
