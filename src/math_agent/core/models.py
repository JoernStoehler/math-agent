"""
Pydantic models for the math agent system.
"""
from typing import Dict, Optional
from enum import Enum
from pydantic import BaseModel


class JobStatusEnum(str, Enum):
    """Enumeration of valid job statuses"""
    SETUP = "setup"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    CANCELLED = "cancelled"


class JobCreateRequest(BaseModel):
    """Request model for creating a new job"""
    name: str
    model: str
    exercise: str
    prompt: str
    disallowedTools: Optional[str] = ""
    additionalFiles: Optional[Dict[str, str]] = {}


class PromptSaveRequest(BaseModel):
    """Request model for saving a prompt"""
    name: str
    content: str


class JobStatus(BaseModel):
    """Status information for a job"""
    status: JobStatusEnum
    createdAt: str
    startedAt: Optional[str] = None
    completedAt: Optional[str] = None
    model: Optional[str] = None
    exercise: Optional[str] = None
    disallowedTools: Optional[str] = None
    error: Optional[str] = None
    solutionTexCreated: Optional[bool] = False
    solutionPdfCreated: Optional[bool] = False