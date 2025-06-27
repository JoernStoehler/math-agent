"""
Tests for the FastAPI server endpoints.

Note: Many endpoints interact with the UNTESTED job executor.
"""
import pytest
from fastapi.testclient import TestClient


def test_import_app():
    """Test that we can import the app"""
    try:
        from src.backend.server import app
        assert app is not None
    except ImportError:
        pytest.fail("Cannot import FastAPI app from src.backend.server")


def test_root_endpoint():
    """Test the root endpoint returns the dashboard"""
    from src.backend.server import app
    client = TestClient(app)
    
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_jobs_list_endpoint():
    """Test listing jobs"""
    from src.backend.server import app
    client = TestClient(app)
    
    response = client.get("/jobs")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_models_endpoint():
    """Test getting available models"""
    from src.backend.server import app
    client = TestClient(app)
    
    response = client.get("/data/models")
    assert response.status_code == 200
    models = response.json()
    assert isinstance(models, list)
    assert "claude-opus-4" in models


@pytest.mark.skip("Job creation uses UNTESTED job executor")
def test_create_job():
    """TODO: Test job creation - BLOCKED: JobExecutor is untested"""
    pass


@pytest.mark.skip("Mock executor should be behind --dev flag")  
def test_mock_executor_disabled_by_default():
    """TODO: Mock executor should not run in production"""
    pass