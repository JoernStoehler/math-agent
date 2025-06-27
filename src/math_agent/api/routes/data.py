"""Data management routes"""
from pathlib import Path

from fastapi import APIRouter, HTTPException

from ...core.models import PromptSaveRequest
from ..dependencies import ExercisesDir, PromptsDir

router = APIRouter(prefix="/data", tags=["data"])


@router.get("/exercises")
async def list_exercises(exercises_dir: ExercisesDir):
    """List available exercises"""
    exercises = []
    
    if exercises_dir.exists():
        for course_dir in sorted(exercises_dir.iterdir()):
            if course_dir.is_dir():
                for exercise_file in sorted(course_dir.glob("*.tex")):
                    exercises.append(f"{course_dir.name}/{exercise_file.stem}")
    
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
async def list_prompts(prompts_dir: PromptsDir):
    """List saved prompts"""
    prompts = []
    
    if prompts_dir.exists():
        for prompt_file in sorted(prompts_dir.glob("*.md")):
            prompts.append(prompt_file.stem)
    
    return prompts


@router.post("/prompts/save")
async def save_prompt(request: PromptSaveRequest, prompts_dir: PromptsDir):
    """Save a new prompt"""
    if not request.name or "/" in request.name or "\\" in request.name:
        raise HTTPException(status_code=400, detail="Invalid prompt name")
    
    prompt_file = prompts_dir / f"{request.name}.md"
    prompt_file.write_text(request.content)
    
    return {"message": "Prompt saved successfully"}