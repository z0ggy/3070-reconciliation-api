import json
from pathlib import Path

import pytest

from src.match import match_data

"""
References:
    - https://docs.pytest.org/en/stable/how-to/skipping.html

"""

FIXTURE_PATH = Path(__file__).parent / "fixtures" / "final_ranking_cases.json"


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


@pytest.mark.xfail(
    reason="Limitation: false positive(fuzzy matching) exceeds minimum threshold",
    strict=True,
)
@pytest.mark.parametrize("query", ["Berlin", "Paris"])
@pytest.mark.xfail(
    reason="Limitation: false positive(fuzzy matching) exceeds minimum threshold",
    strict=True,
)
def test_no_matching(query):
    """
    Unrelated candidates like non-Irish places are rejected
    """
    assert match_data(query, entity_type=None, limit=10) == []
