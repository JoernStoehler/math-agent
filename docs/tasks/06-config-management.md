# Task: Implement Proper Configuration Management

## Objective
Replace hardcoded paths and configuration with a proper configuration system using environment variables and/or config files, making the application more flexible and deployment-ready.

## Current Issues
- Paths computed relative to `__file__` (fragile and location-dependent)
- No centralized configuration
- Hardcoded values scattered throughout code
- No environment-based configuration
- Difficult to deploy in different environments

## Required Changes

### 1. Create Configuration Module
Create `src/math_agent/core/config.py`:
```python
from pydantic import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Paths
    data_dir: Path = Path("data")
    jobs_dir: Path = Path("jobs")
    static_dir: Path = Path("static")
    
    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    reload: bool = False
    
    # Features
    dev_mode: bool = False
    
    # Models
    available_models: list[str] = [
        "claude-opus-4",
        "claude-sonnet-4",
        "gemini-2.5-pro",
        "gemini-2.5-flash"
    ]
    
    class Config:
        env_file = ".env"
        env_prefix = "MATH_AGENT_"
```

### 2. Remove Hardcoded Paths
Replace all instances of:
- `Path(__file__).parent.parent.parent`
- Direct path construction
- Hardcoded directory names

### 3. Create Settings Dependency
```python
from functools import lru_cache

@lru_cache()
def get_settings() -> Settings:
    return Settings()

SettingsDep = Annotated[Settings, Depends(get_settings)]
```

### 4. Update Directory Creation
- Move directory creation to startup
- Make it configurable
- Add validation

### 5. Environment Variable Documentation
Create clear documentation for all configuration options:
- `MATH_AGENT_DATA_DIR`
- `MATH_AGENT_JOBS_DIR`
- `MATH_AGENT_DEV_MODE`
- etc.

### 6. Add Config Validation
- Validate paths exist or can be created
- Check permissions
- Validate model names

## Files to Read First
- `/workspaces/math-agent/src/backend/server.py` (lines 100-112 for paths)
- `/workspaces/math-agent/src/backend/job.py`
- Look for all hardcoded values

## Migration Strategy
1. Create settings class with defaults
2. Replace path calculations
3. Replace hardcoded values
4. Add environment variable support
5. Document all settings
6. Add validation

## Success Criteria
- No hardcoded paths in code
- All configuration in one place
- Easy to configure via environment
- Works regardless of where it's run from
- Clear documentation of all settings
- Validation prevents misconfiguration

## Dependencies
- Should be done after task 01 (module restructuring)
- Can be done in parallel with other tasks