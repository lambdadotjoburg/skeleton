import json
from pathlib import Path
from fastapi import FastAPI
# from pydantic import BaseModel

{{ app }} = FastAPI(
    # name="Backend API Docs",
    root_path="/api", # template var!
    # root_path="/{{ api }}",
    title="{{ title }}",
    description="{{ description }}",
    version="{{ version }}",
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

# simple index page!
@{{ app }}.get(
    ROUTES["index"]["route"],
    summary=ROUTES["index"]["summary"],
    tags=ROUTES["index"]["tags"]
)
async def index():
    return { "message": "running ..." }

@{{ app }}.get(
    ROUTES["status"]["route"],
    summary=ROUTES["status"]["summary"],
    tags=ROUTES["status"]["tags"]
)
async def status():
    return { "status": "OK" }

# html response example!
from fastapi.responses import HTMLResponse
@{{ app }}.get(
    ROUTES["html"]["route"],
    summary=ROUTES["html"]["summary"],
    tags=ROUTES["html"]["tags"],
    response_class=HTMLResponse
)
def html():
    html = "<h1>FastAPI!</h1>"
    return HTMLResponse(content=html)