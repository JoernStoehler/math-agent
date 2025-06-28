"""Tests for the FastAPI server endpoints"""
import json
import pytest


def test_import_app():
    """Test that we can import the app"""
    try:
        from math_agent.main import app
        assert app is not None
    except ImportError:
        pytest.fail("Cannot import FastAPI app from math_agent.main")


def test_root_endpoint(client):
    """Test the root endpoint returns the dashboard"""
    response = client.get("/")
    assert response.status_code == 200
    assert "Dashboard" in response.text


def test_jobs_list_endpoint(client, test_dirs):
    """Test listing jobs"""
    # Create a test job
    job_dir = test_dirs["jobs"] / "test-job"
    job_dir.mkdir()
    status_data = {
        "status": "completed",
        "model": "claude-opus-4",
        "createdAt": "2024-01-01T00:00:00Z"
    }
    (job_dir / "status.json").write_text(json.dumps(status_data))
    
    response = client.get("/jobs")
    assert response.status_code == 200
    
    jobs = response.json()
    assert "test-job" in jobs
    assert jobs["test-job"]["status"] == "completed"


def test_models_endpoint(client):
    """Test getting available models"""
    response = client.get("/data/models")
    assert response.status_code == 200
    
    models = response.json()
    assert "claude-opus-4" in models
    assert "gemini-2.5-pro" in models
    assert len(models) == 4


def test_exercises_endpoint(client):
    """Test listing exercises"""
    response = client.get("/data/exercises")
    assert response.status_code == 200
    
    exercises = response.json()
    assert "test_course/test_ex_01" in exercises


def test_prompts_endpoint(client):
    """Test listing prompts"""
    response = client.get("/data/prompts")
    assert response.status_code == 200
    
    prompts = response.json()
    assert "test_prompt" in prompts


def test_get_job_details(client, test_dirs):
    """Test getting job details"""
    # Create a test job with log
    job_dir = test_dirs["jobs"] / "test-job"
    job_dir.mkdir()
    
    status_data = {
        "status": "running",
        "model": "claude-opus-4",
        "createdAt": "2024-01-01T00:00:00Z"
    }
    (job_dir / "status.json").write_text(json.dumps(status_data))
    
    # Create log file
    log_entries = [
        {"type": "system", "content": "Job started"},
        {"type": "message", "content": "Working on problem"}
    ]
    with open(job_dir / "log.jsonl", "w") as f:
        for entry in log_entries:
            f.write(json.dumps(entry) + "\n")
    
    response = client.get("/jobs/test-job")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"]["status"] == "running"
    assert len(data["log"]) == 2
    assert data["log"][0]["content"] == "Job started"


def test_get_nonexistent_job(client):
    """Test getting details for a job that doesn't exist"""
    response = client.get("/jobs/nonexistent")
    assert response.status_code == 404
    assert "Job not found" in response.json()["detail"]


def test_save_prompt(client):
    """Test saving a new prompt"""
    prompt_data = {
        "name": "new_prompt",
        "content": "This is a new prompt"
    }
    
    response = client.post("/data/prompts/save", json=prompt_data)
    assert response.status_code == 200
    assert response.json()["message"] == "Prompt saved successfully"
    
    # Verify prompt was saved
    response = client.get("/data/prompts")
    prompts = response.json()
    assert "new_prompt" in prompts


def test_save_prompt_invalid_name(client):
    """Test saving a prompt with invalid name"""
    prompt_data = {
        "name": "invalid/name",
        "content": "This is a prompt"
    }
    
    response = client.post("/data/prompts/save", json=prompt_data)
    assert response.status_code == 400
    assert "Invalid prompt name" in response.json()["detail"]


def test_create_job(client, mock_job_manager):
    """Test job creation"""
    job_data = {
        "name": "test-new-job",
        "model": "claude-opus-4",
        "exercise": "test_course/test_ex_01",
        "prompt": "Test prompt content",
        "disallowedTools": "WebSearch",
        "additionalFiles": {}
    }
    
    response = client.post("/jobs/create", json=job_data)
    assert response.status_code == 200
    assert response.json()["job_name"] == "test-new-job"
    
    # Verify job manager was called
    mock_job_manager.submit_job.assert_called_once_with("test-new-job")


def test_create_job_duplicate_name(client, test_dirs):
    """Test creating a job with duplicate name"""
    # Create existing job
    job_dir = test_dirs["jobs"] / "existing-job"
    job_dir.mkdir()
    
    job_data = {
        "name": "existing-job",
        "model": "claude-opus-4",
        "exercise": "test_course/test_ex_01",
        "prompt": "Test prompt",
        "disallowedTools": "",
        "additionalFiles": {}
    }
    
    response = client.post("/jobs/create", json=job_data)
    assert response.status_code == 409
    assert "Job already exists" in response.json()["detail"]


def test_cancel_job(client, test_dirs, mock_job_manager):
    """Test cancelling a running job"""
    # Create a running job
    job_dir = test_dirs["jobs"] / "running-job"
    job_dir.mkdir()
    
    status_data = {
        "status": "running",
        "model": "claude-opus-4"
    }
    (job_dir / "status.json").write_text(json.dumps(status_data))
    
    response = client.post("/jobs/running-job/cancel")
    assert response.status_code == 200
    assert "cancelled successfully" in response.json()["message"]
    
    # Verify job manager was called
    mock_job_manager.cancel_job.assert_called_once_with("running-job")


def test_cancel_completed_job(client, test_dirs):
    """Test that completed jobs cannot be cancelled"""
    # Create a completed job
    job_dir = test_dirs["jobs"] / "completed-job"
    job_dir.mkdir()
    
    status_data = {
        "status": "completed",
        "model": "claude-opus-4"
    }
    (job_dir / "status.json").write_text(json.dumps(status_data))
    
    response = client.post("/jobs/completed-job/cancel")
    assert response.status_code == 400
    assert "Cannot cancel job in completed state" in response.json()["detail"]