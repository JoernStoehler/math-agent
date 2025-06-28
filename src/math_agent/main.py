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
from .api.routes import jobs_router, data_router

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

@app.get("/")
async def serve_dashboard():
    """Serve the main dashboard"""
    return FileResponse(STATIC_DIR / "dashboard.html")

@app.get("/submit")
async def serve_submit_page():
    """Serve the job submission page"""
    return FileResponse(STATIC_DIR / "submit.html")

@app.get("/job/{job_name}")
async def serve_job_page(job_name: str):
    """Serve the job details page - same HTML for all jobs"""
    return FileResponse(STATIC_DIR / "job.html")


# Mount static files - these can be accessed directly
# Note: No directory listing, only direct file access
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/data", StaticFiles(directory=DATA_DIR), name="data")
# Use /jobfiles to avoid conflict with /jobs API endpoint
app.mount("/jobfiles", StaticFiles(directory=JOBS_DIR), name="jobfiles")


if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "math_agent.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(JOBS_DIR.parent)]
    )