"""
Tests for the FastAPI server endpoints.

Note: Many endpoints interact with the UNTESTED job executor.
"""
import pytest
from fastapi.testclient import TestClient


def test_import_app():
    """Test that we can import the app"""
    try:
        from math_agent.main import app
        assert app is not None
    except ImportError:
        pytest.fail("Cannot import FastAPI app from math_agent.main")


def test_root_endpoint():
    """Test the root endpoint returns the dashboard"""
    # Skip for now since dependencies aren't initialized in test environment
    pytest.skip("Dependencies not initialized in test environment")


def test_jobs_list_endpoint():
    """Test listing jobs"""
    # Skip for now since dependencies aren't initialized in test environment
    pytest.skip("Dependencies not initialized in test environment")


def test_models_endpoint():
    """Test getting available models"""
    # Skip for now since dependencies aren't initialized in test environment
    pytest.skip("Dependencies not initialized in test environment")


@pytest.mark.skip("Job creation uses UNTESTED job executor")
def test_create_job():
    """TODO: Test job creation - BLOCKED: JobExecutor is untested"""
    pass


@pytest.mark.skip("Mock executor should be behind --dev flag")  
def test_mock_executor_disabled_by_default():
    """TODO: Mock executor should not run in production"""
    pass