import json

from fastapi.testclient import TestClient

from src.main import app

"""
References:
    - https://fastapi.tiangolo.com/reference/testclient/
"""

client = TestClient(app)


def test_openrefine_candidates():
    queries = {
        "q0": {
            "query": "Dublin",
            "limit": 3,
        }
    }

    response = client.post(
        "/openrefine/reconcile",
        data={"queries": json.dumps(queries)},
    )

    assert response.status_code == 200

    body = response.json()

    assert "q0" in body
    assert "result" in body["q0"]
    assert len(body["q0"]["result"]) > 0

    candidate = body["q0"]["result"][0]

    assert "id" in candidate
    assert "name" in candidate
    assert "score" in candidate
    assert "type" in candidate


def test_openrefine_multiple_queries():
    queries = {
        "q0": {
            "query": "Dublin",
            "limit": 3,
        },
        "q1": {
            "query": "Cork",
            "limit": 3,
        },
    }

    response = client.post(
        "/openrefine/reconcile",
        data={"queries": json.dumps(queries)},
    )

    assert response.status_code == 200

    body = response.json()

    assert "q0" in body
    assert "q1" in body

    assert "result" in body["q0"]
    assert "result" in body["q1"]


def test_openrefine_filter_by_type():
    queries = {
        "q0": {
            "query": "Dublin",
            "type": "county",
            "limit": 3,
        }
    }

    response = client.post(
        "/openrefine/reconcile",
        data={"queries": json.dumps(queries)},
    )

    assert response.status_code == 200

    results = response.json()["q0"]["result"]

    assert len(results) > 0

    for candidate in results:
        assert candidate["type"][0]["id"] == "county"
