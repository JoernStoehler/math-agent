"""Job management routes"""
import json
import logging
from datetime import datetime
from pathlib import Path
from base64 import b64decode

from fastapi import APIRouter, HTTPException

from ...core.models import JobCreateRequest
from ...core.utils import atomic_write_json
from ..dependencies import JobsDir, DataDir, PromptsDir, JobManager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("")
async def list_jobs(jobs_dir: JobsDir):
    """List all jobs with their status"""
    jobs = {}
    
    if jobs_dir.exists():
        for job_dir in jobs_dir.iterdir():
            if job_dir.is_dir():
                status_file = job_dir / "status.json"
                if status_file.exists():
                    with open(status_file, 'r') as f:
                        jobs[job_dir.name] = json.load(f)
    
    return jobs


@router.get("/{job_name}")
async def get_job_details(job_name: str, jobs_dir: JobsDir):
    """Get job status and log"""
    job_dir = jobs_dir / job_name
    
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


@router.post("/create")
async def create_job(request: JobCreateRequest, jobs_dir: JobsDir, data_dir: DataDir, 
                    prompts_dir: PromptsDir, job_manager: JobManager):
    """Create a new job"""
    # Validate job name
    if not request.name or "/" in request.name or "\\" in request.name:
        raise HTTPException(status_code=400, detail="Invalid job name")
    
    # Check if job already exists
    job_dir = jobs_dir / request.name
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
    exercises_dir = data_dir / "exercises"
    exercise_file = exercises_dir / course / f"{exercise_name}.tex"
    
    if not exercise_file.exists():
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    # Copy exercise to workspace
    (workspace_dir / f"{exercise_name}.tex").write_text(exercise_file.read_text())
    
    # Handle prompt
    prompt_content = request.prompt
    if prompt_content.startswith("@"):
        # Load saved prompt
        prompt_name = prompt_content[1:]
        prompt_file = prompts_dir / f"{prompt_name}.md"
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
    await job_manager.submit_job(request.name)
    
    return {"message": "Job created successfully", "job_name": request.name}


@router.post("/{job_name}/cancel")
async def cancel_job(job_name: str, jobs_dir: JobsDir, job_manager: JobManager):
    """Cancel a running job"""
    job_dir = jobs_dir / job_name
    
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