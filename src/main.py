from fastapi import FastAPI

from src.utils.match import match_data

app = FastAPI(
    title="Reconciliation API prototype",
    description="Prototype API for matching messy geographic names standarised Irish geographics entities.",
    version="0.1.0",
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}
