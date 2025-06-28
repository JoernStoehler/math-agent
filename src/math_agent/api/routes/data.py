"""Data management routes"""
import logging

from fastapi import APIRouter, HTTPException

from ...core.models import PromptSaveRequest
from ...config import EXERCISES_DIR, PROMPTS_DIR

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/data", tags=["data"])


@router.get("/exercises")
async def list_exercises():
    """List available exercises"""
    exercises = []
    
    if EXERCISES_DIR.exists():
        try:
            for course_dir in sorted(EXERCISES_DIR.iterdir()):
                if course_dir.is_dir():
                    for exercise_file in sorted(course_dir.glob("*.tex")):
                        exercises.append(f"{course_dir.name}/{exercise_file.stem}")
        except Exception as e:
            logger.error(f"Failed to list exercises: {e}")
            # Return what we have so far instead of crashing
    
    return exercises


@router.get("/models")
async def get_models():
    """Get list of available models"""
    return [
        "claude-opus-4",
        "claude-sonnet-4", 
        "gemini-2.5-pro",
        "gemini-2.5-flash"
    ]


@router.get("/prompts")
async def list_prompts():
    """List saved prompts"""
    prompts = []
    
    if PROMPTS_DIR.exists():
        try:
            for prompt_file in sorted(PROMPTS_DIR.glob("*.md")):
                prompts.append(prompt_file.stem)
        except Exception as e:
            logger.error(f"Failed to list prompts: {e}")
            # Return what we have so far instead of crashing
    
    return prompts


@router.post("/prompts/save")
async def save_prompt(request: PromptSaveRequest):
    """Save a new prompt"""
    if not request.name or "/" in request.name or "\\" in request.name:
        raise HTTPException(status_code=400, detail="Invalid prompt name")
    
    prompt_file = PROMPTS_DIR / f"{request.name}.md"
    try:
        prompt_file.write_text(request.content)
    except Exception as e:
        logger.error(f"Failed to save prompt: {e}")
        raise HTTPException(status_code=500, detail="Failed to save prompt")
    
    return {"message": "Prompt saved successfully"}