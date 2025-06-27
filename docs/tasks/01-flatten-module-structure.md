# Task: Flatten Module Structure

## Objective
Reorganize the project structure to follow standard Python practices, eliminating the awkward `src/backend/` nesting and creating a clean, intuitive module hierarchy.

## Current Issues
- The split between `src/backend/` and `src/` creates awkward imports like `from ..models import`
- Models and utils are at root `src/` level while main logic is in `backend/`
- This non-standard structure increases cognitive overhead

## Target Structure
```
src/
└── math_agent/
    ├── __init__.py
    ├── api/
    │   ├── __init__.py
    │   ├── routes/
    │   │   ├── __init__.py
    │   │   ├── jobs.py
    │   │   ├── data.py
    │   │   └── files.py
    │   └── dependencies.py
    ├── core/
    │   ├── __init__.py
    │   ├── models.py
    │   ├── config.py
    │   └── enums.py
    ├── services/
    │   ├── __init__.py
    │   ├── job_manager.py
    │   └── job_executor.py
    ├── storage/
    │   ├── __init__.py
    │   ├── interface.py
    │   └── filesystem.py
    └── main.py
```

## Required Changes
1. Create new directory structure under `src/math_agent/`
2. Move and reorganize files:
   - `src/models.py` → `src/math_agent/core/models.py`
   - `src/utils.py` → `src/math_agent/core/utils.py` (or appropriate location)
   - `src/backend/server.py` → Split into multiple files
   - `src/backend/job_manager.py` → `src/math_agent/services/job_manager.py`
   - `src/backend/job.py` → `src/math_agent/services/job_executor.py`
3. Update all imports throughout the codebase
4. Create proper `__init__.py` files for each package
5. Update `pyproject.toml` if needed

## Files to Read First
- `/workspaces/math-agent/src/backend/server.py`
- `/workspaces/math-agent/src/models.py`
- `/workspaces/math-agent/src/utils.py`
- `/workspaces/math-agent/src/backend/job_manager.py`
- `/workspaces/math-agent/src/backend/job.py`
- `/workspaces/math-agent/pyproject.toml`

## Success Criteria
- Clean module structure following Python standards
- No more `..` imports
- All tests pass (if any exist)
- Server starts and runs correctly
- Clear separation of concerns in module organization