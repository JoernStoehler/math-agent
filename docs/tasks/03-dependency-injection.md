# Task: Replace Global State with Dependency Injection

## Objective
Eliminate the global `job_manager` variable and implement proper dependency injection using FastAPI's built-in DI system, improving testability and removing hidden dependencies.

## Current Issues
- `job_manager` is declared as a global variable in the lifespan context (server.py:80-81)
- This creates hidden dependencies and makes testing difficult
- The pattern violates dependency injection principles
- Mock job executor is also tangled in the lifespan logic

## Required Changes

### 1. Create Dependencies Module
Create `src/math_agent/api/dependencies.py`:
```python
from fastapi import Depends
from typing import Annotated

async def get_job_manager() -> JobManager:
    # Return the job manager instance
    pass

JobManagerDep = Annotated[JobManager, Depends(get_job_manager)]
```

### 2. Refactor Lifespan Management
- Separate startup/shutdown logic from dependency creation
- Store instances in app.state instead of global variables
- Clean separation between production and dev mode

### 3. Update Route Handlers
Replace global access with dependency injection:
```python
@app.post("/jobs/create")
async def create_job(
    request: JobCreateRequest,
    job_manager: JobManagerDep
):
    # Use injected job_manager
```

### 4. Create Proper App Factory
- Move app creation to a factory function
- Allow configuration injection
- Separate dev mode logic

### 5. Improve Testing Support
- Create test fixtures for dependencies
- Allow easy mocking of services
- Document testing patterns

## Files to Read First
- `/workspaces/math-agent/src/backend/server.py` (especially lifespan function)
- `/workspaces/math-agent/src/backend/job_manager.py`
- FastAPI dependency injection documentation

## Key Areas to Refactor
1. Lifespan context manager (lines 66-95)
2. All route handlers that use `job_manager`
3. Mock job executor integration
4. App initialization

## Success Criteria
- No global variables for service instances
- All dependencies injected properly
- Easy to test with mock dependencies
- Clear separation of concerns
- Dev mode cleanly separated

## Dependencies
This task depends on task 01 (module restructuring) to have the proper structure in place.