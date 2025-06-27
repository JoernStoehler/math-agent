# Task: Create Storage Abstraction Layer

## Objective
Replace direct file operations scattered throughout the codebase with a clean abstraction layer, improving testability and future flexibility.

## Current Issues
- Direct file operations scattered across multiple files
- Difficult to test without actual filesystem
- Path construction logic duplicated
- No consistent error handling for I/O operations
- Hard to switch storage backends in the future

## Required Changes

### 1. Define Storage Interface
Create `src/math_agent/storage/interface.py`:
```python
from abc import ABC, abstractmethod
from typing import Protocol

class JobStorage(Protocol):
    async def create_job(self, name: str) -> Path:
        ...
    
    async def get_job_status(self, name: str) -> dict:
        ...
    
    async def update_job_status(self, name: str, status: dict) -> None:
        ...
    
    async def append_log_entry(self, name: str, entry: dict) -> None:
        ...
    
    # etc...
```

### 2. Implement Filesystem Storage
Create `src/math_agent/storage/filesystem.py`:
- Implement the storage interface
- Centralize all file operations
- Add proper error handling
- Use the existing `atomic_write_json` utility

### 3. Create Storage Factory
- Configure storage based on settings
- Allow easy swapping for tests
- Document how to add new storage backends

### 4. Update All File Operations
Replace direct file access with storage methods:
- Job creation and management
- Status file operations
- Log file operations
- Exercise file access
- Prompt file management

### 5. Add Proper Error Handling
- Define storage-specific exceptions
- Consistent error messages
- Proper cleanup on failures

## Files to Read First
- `/workspaces/math-agent/src/backend/server.py` (all file operations)
- `/workspaces/math-agent/src/backend/job_manager.py`
- `/workspaces/math-agent/src/backend/job.py`
- `/workspaces/math-agent/src/utils.py` (atomic_write_json)

## Migration Strategy
1. Identify all file operations in the codebase
2. Design the storage interface based on actual usage
3. Implement filesystem storage
4. Replace operations one by one
5. Add tests with mock storage

## Success Criteria
- No direct file operations outside storage module
- Easy to test with mock storage
- Clear error handling
- All existing functionality preserved
- Documentation on adding new storage backends
- Potential for future S3/database storage

## Dependencies
- Should be done after task 01 (module restructuring)
- Can be done in parallel with tasks 02-04