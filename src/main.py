import json
from typing import Annotated, cast

from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from src.geo_types import MatchCandidate
from src.match import detect_ambiguity, match_data
from src.openrefine import QueryType, ResultType, multiple_reconciliation
from src.service_manifest import get_service_metadata
from src.type_detection import EntityType

"""
FastAPI runner: uv run uvicorn src.main:app --reload
References:
    - https://pypi.org/project/fastapi/
    - https://fastapi.tiangolo.com/
    - https://fastapi.tiangolo.com/tutorial/request-forms/#define-form-parameters
    - https://www.slingacademy.com/article/python-typing-annotated-examples/
"""
app: FastAPI = FastAPI(
    title="Reconciliation API",
    description="API for matching messy geographic names standardise Irish geographic entities.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3333",
        "http://localhost:3333",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.get("/")
def check_server() -> dict[str, str]:
    return {"server_status": "works"}


@app.get("/reconcile")
#  entity type default = None
def reconcile(
    q: str,
    entity_type: EntityType | None = None,
    country: str | None = None,
) -> dict[str, str | bool | list[MatchCandidate] | None]:
    candidates: list[MatchCandidate] = match_data(
        query=q,
        entity_type=entity_type,
        country=country,
    )
    return {
        "query": q,
        "entity_type": entity_type,
        "country": country,
        "ambiguous": detect_ambiguity(candidates),
        "candidates": candidates,
    }


@app.get("/openrefine/reconcile")
def openrefine_reconcile_get(
    queries: str | None = None,
):
    """
    GET endpoint:
    when no query param it returns the service manifest,
    with query returns multiple reconciliation
    """
    # No queries
    if queries is None:
        return get_service_metadata()

    try:
        query_batch: dict[str, QueryType] = cast(
            dict[str, QueryType], json.loads(queries)
        )
    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid reconciliation query JSON",
        )

    return multiple_reconciliation(query_batch)


@app.post("/openrefine/reconcile")
def openrefine_reconcile_post(
    queries: Annotated[str, Form()],
) -> dict[str, ResultType]:
    """
    POST endpoint
    OpenRefine use it to reconcile column.
    """
    try:
        query_batch: dict[str, QueryType] = cast(
            dict[str, QueryType], json.loads(queries)
        )

    except json.JSONDecodeError:
        raise HTTPException(
            status_code=400,
            detail="Invalid reconciliation query JSON",
        )

    return multiple_reconciliation(query_batch)
