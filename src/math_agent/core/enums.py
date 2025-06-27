"""
Enumerations for the math agent system.
"""
from enum import Enum


class JobStatus(str, Enum):
    """Job status enumeration."""
    SETUP = "setup"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    CANCELLED = "cancelled"