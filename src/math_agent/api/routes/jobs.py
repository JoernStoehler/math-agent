"""Job management routes"""
import json
import logging
from datetime import datetime, timezone
from base64 import b64decode

from fastapi import APIRouter, HTTPException

from ...core.models import JobCreateRequest, JobStatusEnum
from ...core.utils import atomic_write_json
from ...config import JOBS_DIR, DATA_DIR, PROMPTS_DIR
from ...app_state import job_manager

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("")
async def list_jobs():
    """List all jobs with their status"""
    jobs = {}
    
    if JOBS_DIR.exists():
        for job_dir in JOBS_DIR.iterdir():
            if job_dir.is_dir():
                status_file = job_dir / "status.json"
                if status_file.exists():
                    try:
                        with open(status_file, 'r') as f:
                            jobs[job_dir.name] = json.load(f)
                    except (FileNotFoundError, json.JSONDecodeError) as e:
                        logger.error(f"Failed to read status for {job_dir.name}: {e}")
                        # Skip this job instead of crashing
    
    return jobs


@router.get("/{job_name}")
async def get_job_details(job_name: str):
    """Get job status and log"""
    job_dir = JOBS_DIR / job_name
    
    if not job_dir.exists():
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Read status
    status_file = job_dir / "status.json"
    if not status_file.exists():
        raise HTTPException(status_code=404, detail="Job status not found")
    
    try:
        with open(status_file, 'r') as f:
            status = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Failed to read status for {job_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to read job status")
    
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
    try:
        job_dir.mkdir(parents=True)
        workspace_dir = job_dir / "workspace"
        workspace_dir.mkdir()
    except Exception as e:
        logger.error(f"Failed to create job directory: {e}")
        raise HTTPException(status_code=500, detail="Failed to create job directory")
    
    # Copy exercise file
    exercise_parts = request.exercise.split("/")
    if len(exercise_parts) != 2:
        raise HTTPException(status_code=400, detail="Invalid exercise format")
    
    course, exercise_name = exercise_parts
    exercises_dir = DATA_DIR / "exercises"
    exercise_file = exercises_dir / course / f"{exercise_name}.tex"
    
    if not exercise_file.exists():
        raise HTTPException(status_code=404, detail="Exercise not found")
    
    # Copy exercise to workspace
    try:
        (workspace_dir / f"{exercise_name}.tex").write_text(exercise_file.read_text())
    except Exception as e:
        logger.error(f"Failed to copy exercise file: {e}")
        raise HTTPException(status_code=500, detail="Failed to copy exercise file")
    
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
    try:
        (workspace_dir / "prompt.md").write_text(prompt_content)
    except Exception as e:
        logger.error(f"Failed to save prompt: {e}")
        raise HTTPException(status_code=500, detail="Failed to save prompt")
    
    # Save additional files
    if request.additionalFiles:
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
        "status": JobStatusEnum.SETUP.value,
        "createdAt": datetime.now(timezone.utc).isoformat() + "Z",
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
async def cancel_job(job_name: str):
    """Cancel a running job"""
    job_dir = JOBS_DIR / job_name
    
    if not job_dir.exists():
        raise HTTPException(status_code=404, detail="Job not found")
    
    # Check current status
    status_file = job_dir / "status.json"
    if not status_file.exists():
        raise HTTPException(status_code=404, detail="Job status not found")
    
    try:
        with open(status_file, 'r') as f:
            status = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logger.error(f"Failed to read status for {job_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to read job status")
    
    if status["status"] not in [JobStatusEnum.SETUP.value, JobStatusEnum.RUNNING.value]:
        raise HTTPException(status_code=400, detail=f"Cannot cancel job in {status['status']} state")
    
    # Cancel via job manager
    success = await job_manager.cancel_job(job_name)
    if not success:
        # Fallback: update status directly
        status["status"] = JobStatusEnum.CANCELLED.value
        status["completedAt"] = datetime.now(timezone.utc).isoformat() + "Z"
        atomic_write_json(status_file, status)
    
    return {"message": "Job cancelled successfully"}