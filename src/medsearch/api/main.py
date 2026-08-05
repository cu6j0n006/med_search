from fastapi import FastAPI

app = FastAPI()


@app.get("/search?q={query}")
def search_query(query: str | None = None):
    return {"query": query}
