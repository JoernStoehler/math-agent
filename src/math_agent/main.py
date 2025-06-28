#!/usr/bin/env python3
"""
Math Agent Backend Server

FastAPI server providing API endpoints for the math agent system.
"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from .config import STATIC_DIR, DATA_DIR, JOBS_DIR
from .app_state import job_manager
from .api.routes import jobs_router, data_router, files_router

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifecycle"""
    # Startup
    logger.info("Starting job manager...")
    await job_manager.start()
    logger.info("Job manager started successfully")
    yield
    # Shutdown (if needed in future)
    # await job_manager.stop()


# Create FastAPI app
app = FastAPI(title="Math Agent API", lifespan=lifespan)

# Include routers
app.include_router(jobs_router)
app.include_router(data_router)
app.include_router(files_router)

@app.get("/")
async def serve_dashboard():
    """Serve the main dashboard"""
    return FileResponse(STATIC_DIR / "dashboard.html")

# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Mount file directories with browsing enabled
app.mount("/files/data", StaticFiles(directory=DATA_DIR, html=True), name="data_files")
app.mount("/files/jobs", StaticFiles(directory=JOBS_DIR, html=True), name="jobs_files")


if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "math_agent.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(JOBS_DIR.parent)]
    )