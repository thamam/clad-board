import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.database import init_db
from backend.routes import bots, ingest, register


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Ensure data directory exists
    os.makedirs("data", exist_ok=True)
    init_db()
    yield


app = FastAPI(title="Bot Monitoring Dashboard", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(register.router)
app.include_router(ingest.router)
app.include_router(bots.router)

# Serve frontend static files (built React app)
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/", StaticFiles(directory=str(static_dir), html=True), name="static")
