from fastapi import FastAPI

from src.match import match_data

"""
References:
    - https://pypi.org/project/fastapi/
    - https://fastapi.tiangolo.com/
"""
app = FastAPI(
    title="Reconciliation API prototype",
    description="Prototype API for matching messy geographic names standardise Irish geographic entities.",
    version="0.1.0",
)


@app.get("/")
def check_server():
    return {"server_status": "works"}


@app.get("/reconcile")
#  entity type default = None
def reconcile(q: str, entity_type: str | None = None):
    candidates = match_data(query=q, entity_type=entity_type)
    return {"query": q, "entity_type": entity_type, "candidates": candidates}
