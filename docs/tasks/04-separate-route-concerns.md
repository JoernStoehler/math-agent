# Task: Separate Route Concerns

## Objective
Break up the monolithic `server.py` file by separating routes into logical modules, reducing the 380-line file to focused, single-responsibility modules.

## Current Issues
- `server.py` contains all routes mixed together
- File handles multiple unrelated concerns
- Difficult to navigate and maintain
- HTML generation mixed with API logic
- Mock executor mixed with production code

## Required Changes

### 1. Create Route Modules
Split routes into logical groups:

#### `src/math_agent/api/routes/jobs.py`
- `POST /jobs/create`
- `GET /jobs`
- `GET /jobs/{job_name}`
- `POST /jobs/{job_name}/cancel`

#### `src/math_agent/api/routes/data.py`
- `GET /data/exercises`
- `GET /data/models`
- `GET /data/prompts`
- `POST /data/prompts/save`

#### `src/math_agent/api/routes/files.py`
- `GET /files/`
- Static file mounting for `/files/data` and `/files/jobs`

#### `src/math_agent/api/routes/root.py`
- `GET /` (dashboard)
- Other root-level routes

### 2. Create Router Registration
In `src/math_agent/api/routes/__init__.py`:
```python
from fastapi import APIRouter
from .jobs import router as jobs_router
from .data import router as data_router
# etc...

def register_routes(app: FastAPI):
    app.include_router(jobs_router, prefix="/jobs", tags=["jobs"])
    app.include_router(data_router, prefix="/data", tags=["data"])
    # etc...
```

### 3. Extract Mock Executor
Move mock job executor to separate module:
- `src/math_agent/dev/mock_executor.py`
- Only loaded when DEV_MODE is enabled

### 4. Simplify Main Server File
The main server file should only:
- Create the FastAPI app
- Register routes
- Configure middleware
- Start the server

### 5. Extract HTML Generation
- Consider using templates or dedicated functions
- Move inline HTML to separate files or functions

## Files to Read First
- `/workspaces/math-agent/src/backend/server.py` (all 380 lines)
- FastAPI router documentation

## Migration Strategy
1. Create new route modules with routers
2. Move routes one by one, testing each
3. Update imports and dependencies
4. Remove old code from server.py
5. Test all endpoints still work

## Success Criteria
- `server.py` reduced to <100 lines
- Clear separation of route concerns
- Each route module focused on one domain
- Mock executor cleanly separated
- All endpoints still functional
- Easier to find and modify specific routes

## Dependencies
- Depends on task 01 (module restructuring)
- Should be done with or after task 03 (dependency injection)