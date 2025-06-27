# Task: Simplify Application Entry Point

## Objective
Replace the current string-based module reference pattern with a standard Python entry point, making the application easier to run and discover.

## Current Issues
- Entry point uses string reference: `uvicorn.run("server:app")`
- Running as script with `if __name__ == "__main__"` is non-standard for packages
- No clear CLI interface
- Difficult to pass configuration options

## Required Changes

### 1. Create Main Module
Create `src/math_agent/main.py`:
```python
import uvicorn
from .api import create_app
from .core.config import get_settings

def main():
    """Main entry point for the application"""
    settings = get_settings()
    app = create_app(settings)
    
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        reload=settings.reload
    )

if __name__ == "__main__":
    main()
```

### 2. Create CLI Entry Point
Update `pyproject.toml`:
```toml
[project.scripts]
math-agent = "math_agent.main:main"
```

### 3. Create App Factory
Create `src/math_agent/api/__init__.py`:
```python
from fastapi import FastAPI
from .routes import register_routes

def create_app(settings) -> FastAPI:
    app = FastAPI(title="Math Agent API")
    
    # Configure app
    app.state.settings = settings
    
    # Register routes
    register_routes(app)
    
    # Add middleware, etc.
    
    return app
```

### 4. Support CLI Arguments
Consider adding CLI argument support:
```python
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8000)
    parser.add_argument("--reload", action="store_true")
    args = parser.parse_args()
    
    # Use args to override settings
```

### 5. Update Documentation
- Document new ways to run the app
- `python -m math_agent`
- `math-agent` (after pip install)
- `uv run math-agent`

## Files to Read First
- `/workspaces/math-agent/src/backend/server.py` (bottom section)
- `/workspaces/math-agent/pyproject.toml`

## Success Criteria
- Can run with `python -m math_agent`
- Can run with `math-agent` command after install
- No string-based module references
- Clear, discoverable entry point
- Easy to pass configuration
- Works with uv run

## Dependencies
- Depends on task 01 (module restructuring)
- Should be done after task 04 (separate concerns)
- Needs task 06 (config management) for settings