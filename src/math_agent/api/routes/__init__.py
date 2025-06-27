"""API routes for the math agent system"""
from .data import router as data_router
from .files import router as files_router
from .jobs import router as jobs_router

__all__ = ["data_router", "files_router", "jobs_router"]