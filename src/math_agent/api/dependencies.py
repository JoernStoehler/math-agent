"""API dependencies for dependency injection"""
from pathlib import Path
from typing import Annotated

from fastapi import Depends


# Project paths - these will be initialized in main.py
_PROJECT_ROOT: Path = None
_DATA_DIR: Path = None
_JOBS_DIR: Path = None
_EXERCISES_DIR: Path = None
_PROMPTS_DIR: Path = None
_STATIC_DIR: Path = None
_JOB_MANAGER = None


def init_paths(project_root: Path):
    """Initialize project paths"""
    global _PROJECT_ROOT, _DATA_DIR, _JOBS_DIR, _EXERCISES_DIR, _PROMPTS_DIR, _STATIC_DIR
    _PROJECT_ROOT = project_root
    _DATA_DIR = project_root / "data"
    _JOBS_DIR = project_root / "jobs"
    _EXERCISES_DIR = _DATA_DIR / "exercises"
    _PROMPTS_DIR = _DATA_DIR / "prompts"
    _STATIC_DIR = project_root / "static"
    
    # Ensure directories exist
    _JOBS_DIR.mkdir(exist_ok=True)
    _DATA_DIR.mkdir(exist_ok=True)
    _PROMPTS_DIR.mkdir(exist_ok=True)


def set_job_manager(job_manager):
    """Set the job manager instance"""
    global _JOB_MANAGER
    _JOB_MANAGER = job_manager


# Dependency functions
def get_jobs_dir() -> Path:
    return _JOBS_DIR


def get_data_dir() -> Path:
    return _DATA_DIR


def get_exercises_dir() -> Path:
    return _EXERCISES_DIR


def get_prompts_dir() -> Path:
    return _PROMPTS_DIR


def get_static_dir() -> Path:
    return _STATIC_DIR


def get_job_manager():
    return _JOB_MANAGER


# Type aliases for cleaner signatures
JobsDir = Annotated[Path, Depends(get_jobs_dir)]
DataDir = Annotated[Path, Depends(get_data_dir)]
ExercisesDir = Annotated[Path, Depends(get_exercises_dir)]
PromptsDir = Annotated[Path, Depends(get_prompts_dir)]
StaticDir = Annotated[Path, Depends(get_static_dir)]
JobManager = Annotated[object, Depends(get_job_manager)]