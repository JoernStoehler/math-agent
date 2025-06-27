# Task: Add Proper Testing Infrastructure

## Objective
Replace the current placeholder tests with a comprehensive testing suite, including unit tests, integration tests, and testing utilities.

## Current Issues
- Tests only contain skip statements warning about untested code
- No actual test coverage
- Difficult to test due to global state and file operations
- No testing utilities or fixtures
- Critical job executor is completely untested

## Required Changes

### 1. Set Up Testing Infrastructure
- Configure pytest properly
- Add test dependencies to pyproject.toml
- Create testing utilities module
- Set up coverage reporting

### 2. Create Test Fixtures
Create `tests/conftest.py`:
```python
import pytest
from pathlib import Path
import tempfile

@pytest.fixture
def temp_data_dir():
    """Temporary data directory for tests"""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def mock_storage():
    """Mock storage implementation"""
    # Return mock storage instance

@pytest.fixture
def test_client():
    """FastAPI test client"""
    # Return test client with mock dependencies
```

### 3. Unit Tests for Core Components
- `tests/unit/test_models.py` - Model validation
- `tests/unit/test_job_executor.py` - Job execution logic (CRITICAL)
- `tests/unit/test_job_manager.py` - Queue management
- `tests/unit/test_storage.py` - Storage operations

### 4. Integration Tests
- `tests/integration/test_api.py` - API endpoint tests
- `tests/integration/test_job_flow.py` - Full job lifecycle
- `tests/integration/test_file_operations.py` - File handling

### 5. Testing Utilities
Create `tests/utils.py`:
- Helper functions for creating test data
- Assertion helpers
- Mock builders

### 6. Test the Job Executor
**Priority**: The job executor is marked as COMPLETELY UNTESTED
- Test command construction
- Test process management
- Test output parsing
- Test error handling
- Test cancellation

### 7. Add CI/CD Testing
- GitHub Actions workflow
- Run tests on every PR
- Coverage requirements

## Files to Read First
- `/workspaces/math-agent/tests/test_job_executor.py` (see warnings)
- `/workspaces/math-agent/src/backend/job.py` (needs testing)
- `/workspaces/math-agent/src/backend/job_manager.py`
- `/workspaces/math-agent/pyproject.toml` (test dependencies)

## Testing Strategy
1. Start with unit tests for pure functions
2. Add integration tests for API endpoints
3. Test critical paths (job execution)
4. Add edge case tests
5. Set up continuous testing

## Success Criteria
- >80% code coverage
- All critical paths tested
- Tests run quickly (<30 seconds)
- Easy to add new tests
- Mock dependencies properly
- CI/CD pipeline running tests
- Job executor fully tested

## Dependencies
- Benefits from all other refactoring tasks
- Especially tasks 03 (DI) and 05 (storage abstraction)
- Can start immediately for existing code