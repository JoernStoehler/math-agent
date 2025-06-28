# Task 02: Fix Test Environment

## Problem
All API tests are skipped because the test environment isn't properly initialized.

## Root Cause
- The app uses module-level initialization
- Job manager starts on first request via middleware
- Tests can't import the app without side effects

## Solution Approach

### 1. Create Test Configuration
```python
# tests/conftest.py
import pytest
from pathlib import Path

@pytest.fixture
def test_dirs(tmp_path):
    """Create test directory structure"""
    data_dir = tmp_path / "data"
    jobs_dir = tmp_path / "jobs"
    static_dir = tmp_path / "static"
    
    # Create dirs
    data_dir.mkdir()
    jobs_dir.mkdir()
    static_dir.mkdir()
    
    return data_dir, jobs_dir, static_dir
```

### 2. Patch Configuration for Tests
```python
@pytest.fixture
def test_app(test_dirs, monkeypatch):
    """Create app with test configuration"""
    data_dir, jobs_dir, static_dir = test_dirs
    
    # Patch the config module
    monkeypatch.setattr("math_agent.config.DATA_DIR", data_dir)
    monkeypatch.setattr("math_agent.config.JOBS_DIR", jobs_dir)
    monkeypatch.setattr("math_agent.config.STATIC_DIR", static_dir)
    
    # Now import app
    from math_agent.main import app
    return app
```

### 3. Fix Basic Tests
```python
def test_root_endpoint(test_app):
    """Test the root endpoint"""
    client = TestClient(test_app)
    # Create a dummy dashboard.html
    (test_app.state.static_dir / "dashboard.html").write_text("<html></html>")
    response = client.get("/")
    assert response.status_code == 200
```

## Success Criteria
- Can import app in tests without side effects
- Basic GET endpoints return 200/404 as expected
- Tests run without skipping
- No need for complex mocking