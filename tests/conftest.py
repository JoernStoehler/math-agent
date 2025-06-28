"""Test configuration and fixtures for math agent tests"""
import sys
import pytest
from unittest.mock import AsyncMock
from fastapi.testclient import TestClient


@pytest.fixture
def test_dirs(tmp_path):
    """Create test directory structure"""
    data_dir = tmp_path / "data"
    jobs_dir = tmp_path / "jobs"
    static_dir = tmp_path / "static"
    exercises_dir = data_dir / "exercises"
    prompts_dir = data_dir / "prompts"
    
    # Create all directories
    data_dir.mkdir()
    jobs_dir.mkdir()
    static_dir.mkdir()
    exercises_dir.mkdir()
    prompts_dir.mkdir()
    
    # Create test data
    # Add a test exercise
    test_course = exercises_dir / "test_course"
    test_course.mkdir()
    (test_course / "test_ex_01.tex").write_text("\\documentclass{article}\\begin{document}Test\\end{document}")
    
    # Add a test prompt
    (prompts_dir / "test_prompt.md").write_text("Test prompt content")
    
    # Add dashboard.html for root endpoint
    (static_dir / "dashboard.html").write_text("<html><body>Dashboard</body></html>")
    
    return {
        "data": data_dir,
        "jobs": jobs_dir,
        "static": static_dir,
        "exercises": exercises_dir,
        "prompts": prompts_dir
    }


@pytest.fixture
def mock_job_manager():
    """Create a mock job manager"""
    manager = AsyncMock()
    manager.submit_job = AsyncMock(return_value=None)
    manager.cancel_job = AsyncMock(return_value=True)
    manager.start = AsyncMock(return_value=None)
    manager.stop = AsyncMock(return_value=None)
    return manager


@pytest.fixture
def test_app(test_dirs, mock_job_manager, monkeypatch):
    """Create FastAPI app with test configuration"""
    # Remove the modules from sys.modules to force reimport
    modules_to_remove = [
        'math_agent.main',
        'math_agent.config', 
        'math_agent.app_state',
        'math_agent.api.routes.jobs',
        'math_agent.api.routes.data',
        'math_agent.api.routes.files',
        'math_agent.api.routes'
    ]
    for module in modules_to_remove:
        if module in sys.modules:
            del sys.modules[module]
    
    # Patch the config module BEFORE it's imported
    import math_agent.config
    monkeypatch.setattr(math_agent.config, "DATA_DIR", test_dirs["data"])
    monkeypatch.setattr(math_agent.config, "JOBS_DIR", test_dirs["jobs"])
    monkeypatch.setattr(math_agent.config, "STATIC_DIR", test_dirs["static"])
    monkeypatch.setattr(math_agent.config, "EXERCISES_DIR", test_dirs["exercises"])
    monkeypatch.setattr(math_agent.config, "PROMPTS_DIR", test_dirs["prompts"])
    
    # Patch job manager in app_state BEFORE it's imported
    import math_agent.app_state
    monkeypatch.setattr(math_agent.app_state, "job_manager", mock_job_manager)
    
    # Now import the app
    from math_agent.main import app
    
    # Skip the middleware that starts job manager
    app.user_middleware = []
    
    return app


@pytest.fixture
def client(test_app):
    """Create test client"""
    return TestClient(test_app)