# Task: Add Simple, Obvious Error Handling

## Objective
Add basic error handling where it's missing, but keep it simple and obvious.

## Current Issues
1. File operations with no try/except
2. JSON parsing without error handling
3. Process execution without catching failures

## Changes Required

### 1. Wrap File Operations
```python
# Instead of
with open(file) as f:
    data = json.load(f)

# Use
try:
    with open(file) as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    logger.error(f"Failed to read {file}: {e}")
    return None  # or raise HTTPException
```

### 2. Handle Missing Directories
- Check if directories exist before listing them
- Return empty lists/dicts instead of crashing

### 3. Process Execution
- Catch subprocess errors in job executor
- Log failures clearly
- Update job status to "error" with error message

## What NOT to Do
- Don't create custom exception classes
- Don't build complex error hierarchies
- Don't over-abstract error handling

## Success Criteria
- App doesn't crash on missing files
- Clear error messages in logs
- User gets meaningful HTTP errors
- Code remains simple and obvious