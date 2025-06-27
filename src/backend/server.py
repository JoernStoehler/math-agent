#!/usr/bin/env python3
"""
Math Agent Backend Server

FastAPI server providing API endpoints for the math agent system.
Includes job management, file serving, and mock data for development.
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from pathlib import Path
from typing import List
from base64 import b64decode
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

logger = logging.getLogger(__name__)


# Import models from separate file
from ..models import JobCreateRequest, PromptSaveRequest, JobStatus
from ..utils import atomic_write_json


# Mock job execution (DEV MODE ONLY - Enable with DEV_MODE=true)
async def mock_job_executor():
    """Simulate job execution for demo"""
    while True:
        await asyncio.sleep(5)
        
        # Check for jobs in setup state
        if JOBS_DIR.exists():
            for job_dir in JOBS_DIR.iterdir():
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
    # Check if dev mode is enabled
    dev_mode = os.getenv("DEV_MODE", "").lower() == "true"
    
    # Startup
    task = None
    if dev_mode:
        print("WARNING: Running in DEV_MODE with mock job executor")
        task = asyncio.create_task(mock_job_executor())
    
    # Import job manager
    from .job_manager import JobManager
    global job_manager
    job_manager = JobManager(JOBS_DIR)
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


# Initialize FastAPI app
app = FastAPI(title="Math Agent API", lifespan=lifespan)

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
JOBS_DIR = PROJECT_ROOT / "jobs"
STATIC_DIR = PROJECT_ROOT / "static"
EXERCISES_DIR = DATA_DIR / "exercises"
PROMPTS_DIR = DATA_DIR / "prompts"

# Ensure directories exist
JOBS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
PROMPTS_DIR.mkdir(exist_ok=True)


# Mount static files
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# Mount file directories with browsing enabled
app.mount("/files/data", StaticFiles(directory=DATA_DIR, html=True), name="data_files")
app.mount("/files/jobs", StaticFiles(directory=JOBS_DIR, html=True), name="jobs_files")


@app.get("/")
async def serve_dashboard():
    """Serve the main dashboard"""
    return FileResponse(STATIC_DIR / "dashboard.html")


# Job management endpoints
@app.get("/jobs")
async def list_jobs():
    """List all jobs with their status"""
    jobs = {}
    
    if JOBS_DIR.exists():
        for job_dir in JOBS_DIR.iterdir():
            if job_dir.is_dir():
                status_file = job_dir / "status.json"
                if status_file.exists():
                    with open(status_file, 'r') as f:
                        jobs[job_dir.name] = json.load(f)
    
    return jobs


@app.get("/jobs/{job_name}")
async def get_job_details(job_name: str):
    """Get job status and log"""
    job_dir = JOBS_DIR / job_name
    
    if not job_dir.exists():
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Read status
    status_file = job_dir / "status.json"
    if not status_file.exists():
        raise HTTPException(status_code=404, detail="Job status not found")
    
    with open(status_file, 'r') as f:
        status = json.load(f)
    
    # Read log entries
    log_file = job_dir / "log.jsonl"
    log_entries = []
    
    if log_file.exists():
        with open(log_file, 'r') as f:
            for line in f:
                if line.strip():
                    try:
                        log_entries.append(json.loads(line))
                    except json.JSONDecodeError:
                        # Handle malformed log entries
                        log_entries.append({
                            "type": "system",
                            "content": f"Malformed log entry: {line[:100]}..."
                        })
    
    return {
        "status": status,
        "log": log_entries
    }


@app.post("/jobs/create")
async def create_job(request: JobCreateRequest):
    """Create a new job"""
    # Validate job name
    if not request.name or "/" in request.name or "\\" in request.name:
        raise HTTPException(status_code=400, detail="Invalid job name")
    
    # Check if job already exists
    job_dir = JOBS_DIR / request.name
    if job_dir.exists():
        raise HTTPException(status_code=409, detail="Job already exists")
    
    # Create job directory
    job_dir.mkdir(parents=True)
    workspace_dir = job_dir / "workspace"
    workspace_dir.mkdir()
    
    # Copy exercise file
    exercise_parts = request.exercise.split("/")
    if len(exercise_parts) != 2:
        raise HTTPException(status_code=400, detail="Invalid exercise format")
    
    course, exercise_name = exercise_parts
    exercise_file = EXERCISES_DIR / course / f"{exercise_name}.tex"
    
    if not exercise_file.exists():
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    # Copy exercise to workspace
    (workspace_dir / f"{exercise_name}.tex").write_text(exercise_file.read_text())
    
    # Handle prompt
    prompt_content = request.prompt
    if prompt_content.startswith("@"):
        # Load saved prompt
        prompt_name = prompt_content[1:]
        prompt_file = PROMPTS_DIR / f"{prompt_name}.md"
        if not prompt_file.exists():
            raise HTTPException(status_code=404, detail="Prompt not found")
        prompt_content = prompt_file.read_text()
    
    # Save prompt to workspace
    (workspace_dir / "prompt.md").write_text(prompt_content)
    
    # Save additional files
    for filename, content_b64 in request.additionalFiles.items():
        try:
            content = b64decode(content_b64)
            (workspace_dir / filename).write_bytes(content)
        except Exception as e:
            # Log error properly instead of print
            logger.error(f"Failed to save file {filename}: {e}")
            # Continue processing other files
    
    # Create initial status
    status = {
        "status": "setup",
        "createdAt": datetime.utcnow().isoformat() + "Z",
        "model": request.model,
        "exercise": request.exercise,
        "disallowedTools": request.disallowedTools
    }
    
    atomic_write_json(job_dir / "status.json", status)
    
    # Create initial log entry
    log_entry = {
        "timestamp": status["createdAt"],
        "type": "system",
        "content": f"Job created with model {request.model} for exercise {request.exercise}"
    }
    
    with open(job_dir / "log.jsonl", 'w') as f:
        f.write(json.dumps(log_entry) + "\n")
    
    # Queue the job for execution
    await job_manager.queue_job(request.name)
    
    return {"message": "Job created successfully", "job_name": request.name}


@app.post("/jobs/{job_name}/cancel")
async def cancel_job(job_name: str):
    """Cancel a running job"""
    job_dir = JOBS_DIR / job_name
    
    if not job_dir.exists():
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Check current status
    status_file = job_dir / "status.json"
    if not status_file.exists():
        raise HTTPException(status_code=404, detail="Job status not found")
    
    with open(status_file, 'r') as f:
        status = json.load(f)
    
    if status["status"] not in ["setup", "running"]:
        raise HTTPException(status_code=400, detail=f"Cannot cancel job in {status['status']} state")
    
    # Cancel via job manager
    success = await job_manager.cancel_job(job_name)
    if not success:
        # Fallback: update status directly
        status["status"] = "cancelled"
        status["completedAt"] = datetime.utcnow().isoformat() + "Z"
        atomic_write_json(status_file, status)
    
    return {"message": "Job cancelled successfully"}


# Data endpoints
@app.get("/data/exercises")
async def list_exercises():
    """List available exercises"""
    exercises = []
    
    if EXERCISES_DIR.exists():
        for course_dir in sorted(EXERCISES_DIR.iterdir()):
            if course_dir.is_dir():
                for exercise_file in sorted(course_dir.glob("*.tex")):
                    exercises.append(f"{course_dir.name}/{exercise_file.stem}")
    
    return exercises


@app.get("/data/models")
async def get_models():
    """Get list of available models"""
    return [
        "claude-opus-4",
        "claude-sonnet-4", 
        "gemini-2.5-pro",
        "gemini-2.5-flash"
    ]


@app.get("/data/prompts")
async def list_prompts():
    """List saved prompts"""
    prompts = []
    
    if PROMPTS_DIR.exists():
        for prompt_file in sorted(PROMPTS_DIR.glob("*.md")):
            prompts.append(prompt_file.stem)
    
    return prompts


@app.post("/data/prompts/save")
async def save_prompt(request: PromptSaveRequest):
    """Save a new prompt"""
    if not request.name or "/" in request.name or "\\" in request.name:
        raise HTTPException(status_code=400, detail="Invalid prompt name")
    
    prompt_file = PROMPTS_DIR / f"{request.name}.md"
    prompt_file.write_text(request.content)
    
    return {"message": "Prompt saved successfully"}


# Simple index page for /files/
@app.get("/files/")
async def files_index():
    """Simple index page for file browsing"""
    html = """
    <html>
    <head>
        <title>File Browser</title>
        <style>
            body { font-family: monospace; margin: 20px; }
            a { text-decoration: none; color: blue; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>File Browser</h1>
        <hr>
        <pre>
<a href="/files/data/">data/</a>
<a href="/files/jobs/">jobs/</a>
        </pre>
        <hr>
    </body>
    </html>"""
    return Response(content=html, media_type="text/html")


if __name__ == "__main__":
    # Run the server
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        reload_dirs=[str(PROJECT_ROOT)]
    )