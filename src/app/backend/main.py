from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
from starlette.routing import Route
from typing import Optional

from onboarding import tracker, Status
from mcp_server import mcp

mcp_app = mcp.streamable_http_app()


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with mcp.session_manager.run():
        yield


app = FastAPI(title="Foundry Agents Essentials - Client Onboarding Tracker", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["mcp-session-id"],
)

mcp_route = mcp_app.routes[0]
app.router.routes.insert(0, Route("/mcp", endpoint=mcp_route.endpoint))


class StatusRequest(BaseModel):
    status: str


class NoteRequest(BaseModel):
    text: str


class CreateRequest(BaseModel):
    client_name: str
    engagement_type: str
    description: str
    contact_email: Optional[str] = ""


@app.get("/api/onboardings")
async def list_onboardings():
    return tracker.list_all()


@app.get("/api/onboardings/{onboarding_id}")
async def get_onboarding(onboarding_id: str):
    result = tracker.get(onboarding_id)
    if result is None:
        return {"error": "Not found"}
    return result


@app.post("/api/onboardings")
async def create_onboarding(request: CreateRequest):
    return tracker.create(request.client_name, request.engagement_type, request.description, request.contact_email)


@app.patch("/api/onboardings/{onboarding_id}/status")
async def update_onboarding_status(onboarding_id: str, request: StatusRequest):
    result = tracker.update_status(onboarding_id, request.status)
    if result is None:
        return {"error": "Not found"}
    return result


@app.post("/api/onboardings/{onboarding_id}/notes")
async def add_onboarding_note(onboarding_id: str, request: NoteRequest):
    result = tracker.add_note(onboarding_id, request.text)
    if result is None:
        return {"error": "Not found"}
    return result


# Serve React static files if the build exists
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/assets", StaticFiles(directory=static_dir / "assets"), name="assets")

    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        file_path = static_dir / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(static_dir / "index.html")
