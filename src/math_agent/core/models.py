"""
Pydantic models for the math agent system.
"""
from typing import Dict, Optional
from pydantic import BaseModel


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
    status: str  # TODO: Should be an Enum (setup, running, completed, error, cancelled)
    createdAt: str
    startedAt: Optional[str] = None
    completedAt: Optional[str] = None
    model: Optional[str] = None
    exercise: Optional[str] = None
    disallowedTools: Optional[str] = None
    error: Optional[str] = None
    solutionTexCreated: Optional[bool] = False
    solutionPdfCreated: Optional[bool] = False