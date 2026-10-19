import json
from pathlib import Path
from fastapi import FastAPI
# from pydantic import BaseModel

app = FastAPI(
    # name="Backend API Docs",
    title="Backend API Docs",
    description="Backend API Docs",
    version="1.0.0",
    # lifespan=lifespan,
    swagger_ui_parameters={
        "docExpansion": "none",
        "displayRequestDuration": True,
        "defaultModelsExpandDepth": -1
    },
)

# dynamically load routes.json to creat
# endpoints or access using json indexing
BASE = Path(__file__).resolve().parents[1]
with open(BASE/"routes.json") as endpoints:
    ROUTES = json.load(endpoints)["routes"]

# html response example!
from fastapi.responses import HTMLResponse
@app.get(
    ROUTES["test"]["route"],
    summary=ROUTES["test"]["summary"],
    tags=ROUTES["test"]["tags"],
    response_class=HTMLResponse
)
def page():
    html = "<h1>FastAPI!</h1>"
    return HTMLResponse(content=html)