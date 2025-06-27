#!/usr/bin/env python3
"""
Math Agent Backend Server

FastAPI server providing API endpoints for the math agent system.
"""
import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

from math_agent.api.dependencies import init_paths, set_job_manager, StaticDir
from math_agent.api.routes import jobs_router, data_router, files_router
from math_agent.services.job_manager import JobManager
from math_agent.core.utils import atomic_write_json

logger = logging.getLogger(__name__)


# Mock job execution (DEV MODE ONLY - Enable with DEV_MODE=true)
async def mock_job_executor(jobs_dir: Path):
    """Simulate job execution for demo"""
    while True:
        await asyncio.sleep(5)
        
        # Check for jobs in setup state
        if jobs_dir.exists():
            for job_dir in jobs_dir.iterdir():
                if job_dir.is_dir():
                    status_file = job_dir / "status.json"
                    if status_file.exists():
                        with open(status_file, 'r') as f:
                            status = json.load(f)
                        
                        # Simulate starting setup jobs
                        if status["status"] == "setup":
                            status["status"] = "running"
                            status["startedAt"] = datetime.utcnow().isoformat() + "Z"
                            
                            atomic_write_json(status_file, status)
                            
                            # Add log entry
                            log_file = job_dir / "log.jsonl"
                            log_entry = {
                                "timestamp": status["startedAt"],
                                "type": "message",
                                "role": "assistant",
                                "content": "Starting to work on the problem..."
                            }
                            with open(log_file, 'a') as f:
                                f.write(json.dumps(log_entry) + "\n")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Initialize paths
    project_root = Path(__file__).parent.parent.parent
    init_paths(project_root)
    
    # Get paths for this context
    jobs_dir = project_root / "jobs"
    
    # Check if dev mode is enabled
    dev_mode = os.getenv("DEV_MODE", "").lower() == "true"
    
    # Startup
    task = None
    if dev_mode:
        print("WARNING: Running in DEV_MODE with mock job executor")
        task = asyncio.create_task(mock_job_executor(jobs_dir))
    
    # Initialize job manager
    job_manager = JobManager(jobs_dir)
    set_job_manager(job_manager)
    await job_manager.start()
    
    yield
    
    # Shutdown
    await job_manager.stop()
    
    if task:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


def create_app() -> FastAPI:
    """Create and configure the FastAPI application"""
    app = FastAPI(title="Math Agent API", lifespan=lifespan)
    
    # Include routers with dependency injection
    app.include_router(jobs_router, dependencies=[])
    app.include_router(data_router, dependencies=[])
    app.include_router(files_router, dependencies=[])
    
    @app.get("/")
    async def serve_dashboard(static_dir: StaticDir):
        """Serve the main dashboard"""
        return FileResponse(static_dir / "dashboard.html")
    
    # Mount static files right away since paths are already initialized in lifespan
    project_root = Path(__file__).parent.parent.parent
    static_dir = project_root / "static"
    data_dir = project_root / "data"
    jobs_dir = project_root / "jobs"
    
    # Mount static files
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    
    # Mount file directories with browsing enabled
    app.mount("/files/data", StaticFiles(directory=data_dir, html=True), name="data_files")
    app.mount("/files/jobs", StaticFiles(directory=jobs_dir, html=True), name="jobs_files")
    
    return app


# Create the app instance
app = create_app()


if __name__ == "__main__":
    # Run the server
    project_root = Path(__file__).parent.parent.parent
    uvicorn.run(
        "math_agent.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(project_root)]
    )