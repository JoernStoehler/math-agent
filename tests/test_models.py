"""
Unit tests for Pydantic models.
"""
import pytest
from pydantic import ValidationError

from src.models import JobCreateRequest, PromptSaveRequest, JobStatus


class TestJobCreateRequest:
    """Test JobCreateRequest model."""
    
    def test_valid_job_create_minimal(self):
        """Test creating job with minimal required fields."""
        job = JobCreateRequest(
            name="test-job",
            model="claude-opus-4",
            exercise="analysis_1/sheet_01_ex_01",
            prompt="Solve this problem"
        )
        assert job.name == "test-job"
        assert job.model == "claude-opus-4"
        assert job.exercise == "analysis_1/sheet_01_ex_01"
        assert job.prompt == "Solve this problem"
        assert job.disallowedTools == ""
        assert job.additionalFiles == {}
    
    def test_valid_job_create_full(self):
        """Test creating job with all fields."""
        job = JobCreateRequest(
            name="test-job",
            model="gemini-2.5-pro",
            exercise="linear_algebra/sheet_02_ex_03",
            prompt="@saved_prompt",
            disallowedTools="Bash,WebSearch",
            additionalFiles={"notes.tex": "base64content"}
        )
        assert job.disallowedTools == "Bash,WebSearch"
        assert job.additionalFiles == {"notes.tex": "base64content"}
    
    def test_missing_required_fields(self):
        """Test validation errors for missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            JobCreateRequest(name="test")
        
        errors = exc_info.value.errors()
        assert len(errors) == 3  # model, exercise, prompt missing
        assert all(e['type'] == 'missing' for e in errors)
    
    def test_empty_name(self):
        """Test that empty name is allowed."""
        # Empty name is actually allowed by the model
        job = JobCreateRequest(
            name="",
            model="claude-opus-4",
            exercise="test",
            prompt="test"
        )
        assert job.name == ""
    
    def test_none_optional_fields(self):
        """Test None values for optional fields."""
        job = JobCreateRequest(
            name="test",
            model="claude-opus-4",
            exercise="test",
            prompt="test",
            disallowedTools=None,
            additionalFiles=None
        )
        # When None is provided, it overrides the default
        assert job.disallowedTools is None
        assert job.additionalFiles is None


class TestPromptSaveRequest:
    """Test PromptSaveRequest model."""
    
    def test_valid_prompt_save(self):
        """Test creating valid prompt save request."""
        prompt = PromptSaveRequest(
            name="math_solver",
            content="Solve the following problem step by step..."
        )
        assert prompt.name == "math_solver"
        assert prompt.content == "Solve the following problem step by step..."
    
    def test_missing_fields(self):
        """Test validation errors for missing fields."""
        with pytest.raises(ValidationError) as exc_info:
            PromptSaveRequest(name="test")
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]['loc'] == ('content',)
        assert errors[0]['type'] == 'missing'
    
    def test_empty_values(self):
        """Test empty string values."""
        # Empty strings should be allowed
        prompt = PromptSaveRequest(name="", content="")
        assert prompt.name == ""
        assert prompt.content == ""


class TestJobStatus:
    """Test JobStatus model."""
    
    def test_minimal_job_status(self):
        """Test creating job status with minimal fields."""
        status = JobStatus(
            status="setup",
            createdAt="2024-01-01T00:00:00Z"
        )
        assert status.status == "setup"
        assert status.createdAt == "2024-01-01T00:00:00Z"
        assert status.startedAt is None
        assert status.completedAt is None
        assert status.error is None
        assert status.solutionTexCreated is False
        assert status.solutionPdfCreated is False
    
    def test_full_job_status(self):
        """Test creating job status with all fields."""
        status = JobStatus(
            status="completed",
            createdAt="2024-01-01T00:00:00Z",
            startedAt="2024-01-01T00:01:00Z",
            completedAt="2024-01-01T00:05:00Z",
            model="claude-opus-4",
            exercise="test_exercise",
            disallowedTools="Bash",
            error=None,
            solutionTexCreated=True,
            solutionPdfCreated=True
        )
        assert status.status == "completed"
        assert status.solutionTexCreated is True
        assert status.solutionPdfCreated is True
    
    def test_error_status(self):
        """Test job status with error."""
        status = JobStatus(
            status="error",
            createdAt="2024-01-01T00:00:00Z",
            error="Command not found: claude"
        )
        assert status.status == "error"
        assert status.error == "Command not found: claude"
    
    def test_status_values(self):
        """Test various status values (should accept any string currently)."""
        # TODO: Once status becomes an Enum, this test should verify only valid values
        valid_statuses = ["setup", "running", "completed", "error", "cancelled"]
        
        for status_value in valid_statuses:
            status = JobStatus(
                status=status_value,
                createdAt="2024-01-01T00:00:00Z"
            )
            assert status.status == status_value
        
        # Currently accepts any string (should be fixed with Enum)
        status = JobStatus(
            status="invalid_status",
            createdAt="2024-01-01T00:00:00Z"
        )
        assert status.status == "invalid_status"
    
    def test_optional_fields_none(self):
        """Test that optional fields can be None."""
        status = JobStatus(
            status="running",
            createdAt="2024-01-01T00:00:00Z",
            startedAt=None,
            completedAt=None,
            model=None,
            exercise=None,
            disallowedTools=None,
            error=None,
            solutionTexCreated=None,
            solutionPdfCreated=None
        )
        assert status.startedAt is None
        # When None is provided, it overrides the default
        assert status.solutionTexCreated is None
        assert status.solutionPdfCreated is None
    
    def test_missing_required_fields(self):
        """Test validation errors for missing required fields."""
        with pytest.raises(ValidationError) as exc_info:
            JobStatus(status="setup")
        
        errors = exc_info.value.errors()
        assert len(errors) == 1
        assert errors[0]['loc'] == ('createdAt',)
        assert errors[0]['type'] == 'missing'
    
    def test_dict_export(self):
        """Test exporting model to dict."""
        status = JobStatus(
            status="running",
            createdAt="2024-01-01T00:00:00Z",
            startedAt="2024-01-01T00:01:00Z"
        )
        data = status.model_dump()
        assert data["status"] == "running"
        assert data["createdAt"] == "2024-01-01T00:00:00Z"
        assert data["startedAt"] == "2024-01-01T00:01:00Z"
        assert data["completedAt"] is None
    
    def test_json_export(self):
        """Test exporting model to JSON."""
        status = JobStatus(
            status="completed",
            createdAt="2024-01-01T00:00:00Z",
            solutionTexCreated=True
        )
        json_str = status.model_dump_json()
        assert '"status":"completed"' in json_str
        assert '"solutionTexCreated":true' in json_str