"""
Integration tests for API endpoints.
"""
import json
import base64
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock

import pytest
from fastapi.testclient import TestClient

from tests.utils import (
    create_job_status,
    write_job_files,
    create_log_entry,
    create_sample_exercise,
    read_job_status
)


class TestAPIEndpoints:
    """Test API endpoints with mocked dependencies."""
    
    def test_root_endpoint(self, test_client):
        """Test root endpoint returns dashboard HTML."""
        response = test_client.get("/")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Math Agent Dashboard" in response.text
    
    def test_submit_page(self, test_client):
        """Test submit page is served correctly."""
        response = test_client.get("/submit")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "Submit New Job" in response.text
    
    def test_job_page(self, test_client):
        """Test job page is served correctly."""
        response = test_client.get("/job/test-job")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "test-job" in response.text
    
    def test_get_jobs_empty(self, test_client):
        """Test getting jobs when none exist."""
        response = test_client.get("/jobs")
        assert response.status_code == 200
        assert response.json() == {}
    
    def test_get_jobs_with_data(self, test_client, temp_data_dir):
        """Test getting jobs with existing data."""
        # Create test jobs
        jobs_dir = temp_data_dir / "jobs"
        write_job_files(
            jobs_dir / "job1",
            status=create_job_status("running", model="claude-opus-4")
        )
        write_job_files(
            jobs_dir / "job2",
            status=create_job_status("completed", model="gemini-2.5-pro")
        )
        
        response = test_client.get("/jobs")
        assert response.status_code == 200
        
        jobs = response.json()
        assert len(jobs) == 2
        assert "job1" in jobs
        assert "job2" in jobs
        assert jobs["job1"]["status"] == "running"
        assert jobs["job2"]["status"] == "completed"
    
    def test_get_single_job(self, test_client, temp_data_dir):
        """Test getting a single job's data."""
        # Create test job
        job_name = "test-job"
        jobs_dir = temp_data_dir / "jobs"
        job_dir = jobs_dir / job_name
        
        # Write status and log
        write_job_files(
            job_dir,
            status=create_job_status("running"),
            log_entries=[
                create_log_entry("message", "Starting solution"),
                create_log_entry("tool_use", "", name="Write", params={"file": "test.tex"})
            ]
        )
        
        response = test_client.get(f"/jobs/{job_name}")
        assert response.status_code == 200
        
        data = response.json()
        assert "status" in data
        assert "log" in data
        assert data["status"]["status"] == "running"
        assert len(data["log"]) == 2
    
    def test_get_nonexistent_job(self, test_client):
        """Test getting a job that doesn't exist."""
        response = test_client.get("/jobs/nonexistent")
        assert response.status_code == 404
        assert response.json()["detail"] == "Job not found"
    
    def test_get_models(self, test_client):
        """Test getting available models."""
        response = test_client.get("/data/models")
        assert response.status_code == 200
        
        models = response.json()
        assert isinstance(models, list)
        assert "claude-opus-4" in models
        assert "claude-sonnet-4" in models
        assert "gemini-2.5-pro" in models
        assert "gemini-2.5-flash" in models
    
    def test_get_exercises(self, test_client, temp_data_dir):
        """Test getting available exercises."""
        # Create test exercises
        exercises_dir = temp_data_dir / "exercises"
        course_dir = exercises_dir / "test_course"
        course_dir.mkdir(parents=True)
        (course_dir / "ex1.tex").write_text("Exercise 1")
        (course_dir / "ex2.tex").write_text("Exercise 2")
        
        response = test_client.get("/data/exercises")
        assert response.status_code == 200
        
        exercises = response.json()
        assert isinstance(exercises, list)
        assert "test_course/ex1" in exercises
        assert "test_course/ex2" in exercises
    
    def test_get_prompts(self, test_client, temp_data_dir):
        """Test getting saved prompts."""
        # Create test prompts
        prompts_dir = temp_data_dir / "prompts"
        (prompts_dir / "prompt1.md").write_text("Test prompt 1")
        (prompts_dir / "prompt2.md").write_text("Test prompt 2")
        
        response = test_client.get("/data/prompts")
        assert response.status_code == 200
        
        prompts = response.json()
        assert isinstance(prompts, list)
        assert "prompt1" in prompts
        assert "prompt2" in prompts
    
    def test_save_prompt(self, test_client, temp_data_dir):
        """Test saving a new prompt."""
        request_data = {
            "name": "new_prompt",
            "content": "This is a new prompt template"
        }
        
        response = test_client.post("/data/prompts/save", json=request_data)
        assert response.status_code == 200
        assert response.json() == {"status": "saved"}
        
        # Verify file was created
        prompt_file = temp_data_dir / "prompts" / "new_prompt.md"
        assert prompt_file.exists()
        assert prompt_file.read_text() == "This is a new prompt template"
    
    def test_save_prompt_invalid_name(self, test_client):
        """Test saving prompt with invalid name."""
        request_data = {
            "name": "../../../etc/passwd",
            "content": "malicious"
        }
        
        response = test_client.post("/data/prompts/save", json=request_data)
        assert response.status_code == 400
        assert "Invalid prompt name" in response.json()["detail"]
    
    @patch('src.backend.server.job_manager')
    def test_create_job_success(self, mock_manager, test_client, temp_data_dir):
        """Test successful job creation."""
        # Setup mock
        mock_manager.submit_job = AsyncMock()
        
        # Create test exercise
        exercises_dir = temp_data_dir / "exercises"
        course_dir = exercises_dir / "test_course"
        course_dir.mkdir(parents=True)
        (course_dir / "test.tex").write_text(create_sample_exercise())
        
        request_data = {
            "name": "new-job",
            "model": "claude-opus-4",
            "exercise": "test_course/test",
            "prompt": "Solve this problem",
            "disallowedTools": "Bash",
            "additionalFiles": {}
        }
        
        response = test_client.post("/jobs/create", json=request_data)
        assert response.status_code == 200
        assert response.json() == {"status": "created", "name": "new-job"}
        
        # Verify job was added to queue
        mock_manager.submit_job.assert_called_once_with("new-job")
        
        # Verify job directory was created
        job_dir = temp_data_dir / "jobs" / "new-job"
        assert job_dir.exists()
        assert (job_dir / "workspace").exists()
        assert (job_dir / "status.json").exists()
    
    def test_create_job_duplicate_name(self, test_client, temp_data_dir):
        """Test creating job with duplicate name."""
        # Create existing job
        jobs_dir = temp_data_dir / "jobs"
        (jobs_dir / "existing-job").mkdir(parents=True)
        
        request_data = {
            "name": "existing-job",
            "model": "claude-opus-4",
            "exercise": "test/test",
            "prompt": "Test"
        }
        
        response = test_client.post("/jobs/create", json=request_data)
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]
    
    def test_create_job_invalid_exercise(self, test_client):
        """Test creating job with non-existent exercise."""
        request_data = {
            "name": "test-job",
            "model": "claude-opus-4",
            "exercise": "nonexistent/exercise",
            "prompt": "Test"
        }
        
        response = test_client.post("/jobs/create", json=request_data)
        assert response.status_code == 400
        assert "Exercise not found" in response.json()["detail"]
    
    def test_create_job_with_saved_prompt(self, test_client, temp_data_dir):
        """Test creating job with saved prompt reference."""
        # Create saved prompt
        prompts_dir = temp_data_dir / "prompts"
        (prompts_dir / "saved_prompt.md").write_text("Saved prompt content")
        
        # Create exercise
        exercises_dir = temp_data_dir / "exercises"
        (exercises_dir / "test").mkdir(parents=True)
        (exercises_dir / "test" / "ex.tex").write_text("Exercise")
        
        request_data = {
            "name": "test-job",
            "model": "claude-opus-4",
            "exercise": "test/ex",
            "prompt": "@saved_prompt"
        }
        
        with patch('src.backend.server.job_manager') as mock_manager:
            mock_manager.submit_job = AsyncMock()
            
            response = test_client.post("/jobs/create", json=request_data)
            assert response.status_code == 200
            
            # Verify prompt was loaded
            job_dir = temp_data_dir / "jobs" / "test-job"
            prompt_content = (job_dir / "workspace" / "prompt.md").read_text()
            assert prompt_content == "Saved prompt content"
    
    def test_create_job_with_additional_files(self, test_client, temp_data_dir):
        """Test creating job with additional files."""
        # Create exercise
        exercises_dir = temp_data_dir / "exercises"
        (exercises_dir / "test").mkdir(parents=True)
        (exercises_dir / "test" / "ex.tex").write_text("Exercise")
        
        # Encode file content
        file_content = "Additional notes"
        encoded_content = base64.b64encode(file_content.encode()).decode()
        
        request_data = {
            "name": "test-job",
            "model": "claude-opus-4",
            "exercise": "test/ex",
            "prompt": "Test",
            "additionalFiles": {
                "notes.txt": encoded_content
            }
        }
        
        with patch('src.backend.server.job_manager') as mock_manager:
            mock_manager.submit_job = AsyncMock()
            
            response = test_client.post("/jobs/create", json=request_data)
            assert response.status_code == 200
            
            # Verify additional file was created
            job_dir = temp_data_dir / "jobs" / "test-job"
            notes_file = job_dir / "workspace" / "notes.txt"
            assert notes_file.exists()
            assert notes_file.read_text() == "Additional notes"
    
    @patch('src.backend.server.job_manager')
    def test_cancel_job_success(self, mock_manager, test_client):
        """Test successful job cancellation."""
        mock_manager.cancel_job = AsyncMock(return_value=True)
        
        response = test_client.post("/jobs/test-job/cancel")
        assert response.status_code == 200
        assert response.json() == {"status": "cancelled"}
        
        mock_manager.cancel_job.assert_called_once_with("test-job")
    
    @patch('src.backend.server.job_manager')
    def test_cancel_job_not_found(self, mock_manager, test_client):
        """Test cancelling non-existent job."""
        mock_manager.cancel_job = AsyncMock(return_value=False)
        
        response = test_client.post("/jobs/nonexistent/cancel")
        assert response.status_code == 404
        assert "not found or not running" in response.json()["detail"]
    
    def test_file_server_data_files(self, test_client, temp_data_dir):
        """Test file server for data directory."""
        # Create test file
        test_file = temp_data_dir / "exercises" / "test.tex"
        test_file.parent.mkdir(parents=True)
        test_file.write_text("Test content")
        
        response = test_client.get("/files/data/exercises/test.tex")
        assert response.status_code == 200
        assert response.content == b"Test content"
    
    def test_file_server_job_files(self, test_client, temp_data_dir):
        """Test file server for jobs directory."""
        # Create test file
        job_file = temp_data_dir / "jobs" / "test-job" / "workspace" / "solution.tex"
        job_file.parent.mkdir(parents=True)
        job_file.write_text("Solution content")
        
        response = test_client.get("/files/jobs/test-job/workspace/solution.tex")
        assert response.status_code == 200
        assert response.content == b"Solution content"
    
    def test_file_server_directory_listing(self, test_client, temp_data_dir):
        """Test file server directory listing."""
        # Create test directory with files
        test_dir = temp_data_dir / "exercises" / "course1"
        test_dir.mkdir(parents=True)
        (test_dir / "ex1.tex").write_text("Ex 1")
        (test_dir / "ex2.tex").write_text("Ex 2")
        
        response = test_client.get("/files/data/exercises/course1")
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        assert "ex1.tex" in response.text
        assert "ex2.tex" in response.text
    
    def test_file_server_nonexistent(self, test_client):
        """Test file server for non-existent file."""
        response = test_client.get("/files/data/nonexistent.txt")
        assert response.status_code == 404
    
    def test_file_server_path_traversal(self, test_client):
        """Test file server blocks path traversal attempts."""
        response = test_client.get("/files/data/../../../etc/passwd")
        assert response.status_code == 400
        assert "Invalid path" in response.json()["detail"]
    
    def test_styles_endpoint(self, test_client):
        """Test styles.css is served correctly."""
        response = test_client.get("/styles.css")
        assert response.status_code == 200
        assert "text/css" in response.headers["content-type"]