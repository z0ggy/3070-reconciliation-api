import json
from pathlib import Path

import pytest

from src.match import match_data

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "sprint3_ranking_cases.json"


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
