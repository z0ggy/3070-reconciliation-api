from fastapi import FastAPI

from src.utils.match import match_data

"""
References:
    - https://pypi.org/project/fastapi/
    - https://fastapi.tiangolo.com/
"""
app = FastAPI(
    title="Reconciliation API prototype",
    description="Prototype API for matching messy geographic names standarised Irish geographic entities.",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/reconcile")
def reconcile(q: str, t: str | None = None):
    candidates = match_data(query=q, entity_type=t)
    return {"query": q, "type": t, "candidates": candidates}
