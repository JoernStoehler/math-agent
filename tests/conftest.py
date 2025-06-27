"""
Pytest configuration and shared fixtures for the math agent system.
"""

import asyncio
import json
import tempfile
from datetime import datetime
from pathlib import Path
from typing import AsyncGenerator, Generator, Dict, Any
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from src.backend.job import JobExecutor
from src.backend.job_manager import JobManager


@pytest.fixture
def temp_data_dir() -> Generator[Path, None, None]:
    """Provide a temporary directory for test data."""
    with tempfile.TemporaryDirectory() as tmpdir:
        data_path = Path(tmpdir)
        
        # Create basic structure
        (data_path / "exercises").mkdir(parents=True)
        (data_path / "prompts").mkdir(parents=True)
        (data_path / "jobs").mkdir(parents=True)
        
        # Create sample exercise
        exercise_dir = data_path / "exercises" / "test_course"
        exercise_dir.mkdir(parents=True)
        (exercise_dir / "test_exercise.tex").write_text(
            "\\begin{problem}\nProve that 1 + 1 = 2\n\\end{problem}"
        )
        
        # Create sample prompt
        (data_path / "prompts" / "test_prompt.md").write_text(
            "Solve the following math problem step by step."
        )
        
        yield data_path


@pytest.fixture
def temp_job_dir(temp_data_dir: Path) -> Generator[Path, None, None]:
    """Provide a temporary job directory."""
    job_dir = temp_data_dir / "jobs" / "test_job"
    job_dir.mkdir(parents=True)
    
    # Create workspace
    workspace = job_dir / "workspace"
    workspace.mkdir(parents=True)
    
    # Create initial status
    status = {
        "status": "setup",
        "createdAt": datetime.utcnow().isoformat() + "Z",
        "model": "claude-opus-4",
        "exercise": "test_course/test_exercise",
        "disallowedTools": ""
    }
    (job_dir / "status.json").write_text(json.dumps(status))
    
    # Create empty log
    (job_dir / "log.jsonl").touch()
    
    yield job_dir


@pytest.fixture
def mock_subprocess() -> Generator[AsyncMock, None, None]:
    """Mock subprocess for testing command execution."""
    mock_process = AsyncMock()
    mock_process.returncode = 0
    mock_process.stdout = AsyncMock()
    mock_process.stderr = AsyncMock()
    
    # Mock readline to return empty (EOF)
    mock_process.stdout.readline = AsyncMock(return_value=b"")
    mock_process.wait = AsyncMock(return_value=0)
    mock_process.communicate = AsyncMock(return_value=(b"", b""))
    
    yield mock_process


@pytest.fixture
def job_executor(temp_job_dir: Path) -> JobExecutor:
    """Create a JobExecutor instance with test directory."""
    return JobExecutor(temp_job_dir)


@pytest.fixture
async def job_manager(temp_data_dir: Path) -> AsyncGenerator[JobManager, None]:
    """Create a JobManager instance for testing."""
    jobs_dir = temp_data_dir / "jobs"
    manager = JobManager(jobs_dir, max_concurrent_jobs=1)
    
    # Start the manager
    await manager.start()
    
    yield manager
    
    # Stop the manager
    await manager.stop()


@pytest.fixture
def sample_job_request() -> Dict[str, Any]:
    """Sample job creation request."""
    return {
        "name": "test-job",
        "model": "claude-opus-4",
        "exercise": "test_course/test_exercise",
        "prompt": "Solve the following math problem step by step.",
        "disallowedTools": "",
        "additionalFiles": {}
    }


@pytest.fixture
def mock_claude_output() -> list[bytes]:
    """Mock output from Claude CLI in stream-json format."""
    return [
        b'{"type": "message", "content": "Starting to solve the problem..."}\n',
        b'{"type": "tool_use", "name": "Write", "params": {"file_path": "solution.tex", "content": "Solution content"}}\n',
        b'{"type": "message", "content": "Solution written to solution.tex"}\n'
    ]


@pytest.fixture
def mock_time(freezegun):
    """Mock time using freezegun."""
    with freezegun.freeze_time("2024-01-01T00:00:00Z") as frozen_time:
        yield frozen_time


@pytest.fixture
def test_client(temp_data_dir: Path, monkeypatch) -> TestClient:
    """Create a test client with mocked dependencies."""
    # Set environment variables
    monkeypatch.setenv("DEV_MODE", "true")  # Use mock executor
    
    # Patch the global path variables before importing
    import src.backend.server as server_module
    monkeypatch.setattr(server_module, "DATA_DIR", temp_data_dir)
    monkeypatch.setattr(server_module, "JOBS_DIR", temp_data_dir / "jobs")
    monkeypatch.setattr(server_module, "STATIC_DIR", Path(__file__).parent.parent / "static")
    monkeypatch.setattr(server_module, "EXERCISES_DIR", temp_data_dir / "exercises")
    monkeypatch.setattr(server_module, "PROMPTS_DIR", temp_data_dir / "prompts")
    
    # Create directories
    (temp_data_dir / "jobs").mkdir(exist_ok=True)
    (temp_data_dir / "exercises").mkdir(exist_ok=True)
    (temp_data_dir / "prompts").mkdir(exist_ok=True)
    
    # Import app after paths are patched
    from src.backend.server import app
    
    return TestClient(app)


@pytest.fixture
def mock_job_manager() -> MagicMock:
    """Mock JobManager for testing routes."""
    mock = MagicMock(spec=JobManager)
    mock.submit_job = AsyncMock()
    mock.cancel_job = AsyncMock()
    mock.get_running_jobs = MagicMock(return_value={})
    return mock