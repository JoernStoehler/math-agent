"""
Testing utilities for the math agent system.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional


def create_job_status(
    status: str = "setup",
    created_at: Optional[str] = None,
    model: str = "claude-opus-4",
    exercise: str = "test_course/test_exercise",
    **kwargs
) -> Dict[str, Any]:
    """Create a job status dictionary for testing."""
    if created_at is None:
        created_at = datetime.utcnow().isoformat() + "Z"
    
    base_status = {
        "status": status,
        "createdAt": created_at,
        "model": model,
        "exercise": exercise
    }
    base_status.update(kwargs)
    return base_status


def create_log_entry(
    entry_type: str,
    content: str,
    timestamp: Optional[str] = None,
    **kwargs
) -> Dict[str, Any]:
    """Create a log entry for testing."""
    if timestamp is None:
        timestamp = datetime.utcnow().isoformat() + "Z"
    
    entry = {
        "type": entry_type,
        "content": content,
        "timestamp": timestamp
    }
    entry.update(kwargs)
    return entry


def write_job_files(
    job_dir: Path,
    status: Optional[Dict[str, Any]] = None,
    log_entries: Optional[List[Dict[str, Any]]] = None,
    workspace_files: Optional[Dict[str, str]] = None
) -> None:
    """Write job files for testing."""
    # Ensure directories exist
    job_dir.mkdir(parents=True, exist_ok=True)
    workspace_dir = job_dir / "workspace"
    workspace_dir.mkdir(exist_ok=True)
    
    # Write status
    if status:
        (job_dir / "status.json").write_text(json.dumps(status, indent=2))
    
    # Write log entries
    if log_entries:
        with open(job_dir / "log.jsonl", "w") as f:
            for entry in log_entries:
                f.write(json.dumps(entry) + "\n")
    
    # Write workspace files
    if workspace_files:
        for filename, content in workspace_files.items():
            (workspace_dir / filename).write_text(content)


def read_job_status(job_dir: Path) -> Dict[str, Any]:
    """Read job status from file."""
    status_file = job_dir / "status.json"
    if status_file.exists():
        return json.loads(status_file.read_text())
    return {}


def read_job_log(job_dir: Path) -> List[Dict[str, Any]]:
    """Read job log entries from file."""
    log_file = job_dir / "log.jsonl"
    entries = []
    if log_file.exists():
        with open(log_file) as f:
            for line in f:
                if line.strip():
                    entries.append(json.loads(line))
    return entries


def assert_status_valid(status: Dict[str, Any]) -> None:
    """Assert that a job status is valid."""
    assert "status" in status
    assert status["status"] in ["setup", "running", "completed", "error", "cancelled"]
    assert "createdAt" in status
    assert status["createdAt"].endswith("Z")  # ISO format with Z suffix
    
    if status["status"] == "running":
        assert "startedAt" in status
    
    if status["status"] in ["completed", "error", "cancelled"]:
        assert "completedAt" in status


def assert_log_entry_valid(entry: Dict[str, Any]) -> None:
    """Assert that a log entry is valid."""
    assert "type" in entry
    assert "content" in entry
    assert "timestamp" in entry
    assert entry["timestamp"].endswith("Z")


def create_mock_claude_stream(messages: List[str]) -> List[bytes]:
    """Create mock Claude CLI output stream."""
    stream = []
    for msg in messages:
        entry = create_log_entry("message", msg)
        stream.append((json.dumps(entry) + "\n").encode())
    return stream


def create_mock_tool_use(
    tool_name: str,
    params: Dict[str, Any],
    result: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Create mock tool use entries."""
    entries = [
        {
            "type": "tool_use",
            "name": tool_name,
            "params": params,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
    ]
    
    if result:
        entries.append({
            "type": "tool_result",
            "content": result,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        })
    
    return entries


def create_sample_exercise(content: str = "Prove that 1 + 1 = 2") -> str:
    """Create a sample LaTeX exercise."""
    return f"""\\documentclass{{article}}
\\begin{{document}}
\\section{{Exercise}}
{content}
\\end{{document}}"""


def create_sample_solution(content: str = "1 + 1 = 2 by Peano axioms") -> str:
    """Create a sample LaTeX solution."""
    return f"""\\documentclass{{article}}
\\begin{{document}}
\\section{{Solution}}
{content}
\\end{{document}}"""


class JobStatusMatcher:
    """Custom matcher for job status comparisons."""
    
    def __init__(self, expected_status: str, **expected_fields):
        self.expected_status = expected_status
        self.expected_fields = expected_fields
    
    def __eq__(self, other: Dict[str, Any]) -> bool:
        if not isinstance(other, dict):
            return False
        
        if other.get("status") != self.expected_status:
            return False
        
        for key, value in self.expected_fields.items():
            if other.get(key) != value:
                return False
        
        return True
    
    def __repr__(self) -> str:
        fields = ", ".join(f"{k}={v!r}" for k, v in self.expected_fields.items())
        return f"JobStatusMatcher(status={self.expected_status!r}, {fields})"