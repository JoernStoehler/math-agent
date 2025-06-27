# Task: Remove Unnecessary Complexity

## Objective
Strip out all the over-engineered patterns and make the codebase dead simple. Any developer should understand it in 5 minutes.

## Current Problems
1. **Dependency injection for simple things** - paths don't need DI!
2. **Global state hidden behind functions** - just use a simple global or pass parameters
3. **Complex lifespan management** - just initialize things at startup
4. **Mock executor mixed with production** - should be a separate script
5. **Type aliases for paths** - unnecessarily clever

## Changes Required

### 1. Create Simple Config Module
`src/math_agent/config.py`:
```python
from pathlib import Path

# Just simple constants
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
JOBS_DIR = PROJECT_ROOT / "jobs"
STATIC_DIR = PROJECT_ROOT / "static"
EXERCISES_DIR = DATA_DIR / "exercises"
PROMPTS_DIR = DATA_DIR / "prompts"

# Ensure directories exist
JOBS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
PROMPTS_DIR.mkdir(exist_ok=True)
```

### 2. Simplify main.py
- Remove lifespan context manager
- Just create job_manager at module level
- Remove all the factory functions
- Direct, simple initialization

### 3. Remove dependencies.py
- Delete the entire file
- Routes should just import from config
- Pass job_manager as a simple parameter where needed

### 4. Extract Mock Executor
- Move to `scripts/mock_executor.py`
- Run separately when needed for demos
- Not part of the main application

### 5. Update Routes
- Import paths directly from config
- Accept job_manager as a regular parameter
- No type annotations for simple things

## Success Criteria
- No dependency injection
- No global state functions
- Simple module-level constants
- Can understand entire app flow in 5 minutes
- Any Python developer can maintain it

## Files to Modify
- Delete: `src/math_agent/api/dependencies.py`
- Create: `src/math_agent/config.py`
- Simplify: `src/math_agent/main.py`
- Update: All route files to use simple imports
- Create: `scripts/mock_executor.py`