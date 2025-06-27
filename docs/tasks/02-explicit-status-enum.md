# Task: Make Job Status Explicit with Enum

## Objective
Replace string-based job status with a proper Enum to make valid status values explicit and type-safe, preventing typos and improving code clarity.

## Current Issues
- Job status is defined as a string with a TODO comment (models.py line 26)
- Status values are hardcoded strings throughout the codebase
- No compile-time or runtime validation of status values
- Easy to introduce typos or inconsistent status values

## Required Changes

### 1. Create Status Enum
Create `src/math_agent/core/enums.py`:
```python
from enum import Enum

class JobStatus(str, Enum):
    SETUP = "setup"
    RUNNING = "running"
    COMPLETED = "completed"
    ERROR = "error"
    CANCELLED = "cancelled"
```

### 2. Update Models
- Update `JobStatus` model to use the enum
- Ensure backward compatibility with existing JSON data

### 3. Update All Status References
Search and replace all hardcoded status strings:
- `"setup"` → `JobStatus.SETUP`
- `"running"` → `JobStatus.RUNNING`
- `"completed"` → `JobStatus.COMPLETED`
- `"error"` → `JobStatus.ERROR`
- `"cancelled"` → `JobStatus.CANCELLED`

### 4. Add Validation
- Ensure status transitions are valid
- Add helper methods for status checks if needed

## Files to Read First
- `/workspaces/math-agent/src/models.py`
- `/workspaces/math-agent/src/backend/server.py`
- `/workspaces/math-agent/src/backend/job_manager.py`
- `/workspaces/math-agent/src/backend/job.py`

## Files to Search
Use grep to find all status string occurrences:
```bash
grep -r '"setup"\|"running"\|"completed"\|"error"\|"cancelled"' src/
```

## Success Criteria
- No hardcoded status strings remain in the codebase
- All status values use the enum
- Existing JSON data still loads correctly
- Type checking catches invalid status values
- Code is more maintainable and self-documenting

## Dependencies
This task should be done after or in parallel with task 01 (module restructuring) to place the enum in the correct location.