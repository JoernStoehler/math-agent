# Task 03: Simple Error Handling - COMPLETED

## Summary of Changes

Successfully added simple, obvious error handling throughout the codebase:

### 1. **File Operations** - Added try/except blocks for:
   - JSON loading in `jobs.py` route (status files, log files)
   - File writing operations (exercise copy, prompt save)
   - Directory creation in job setup
   - Status file reading in `job_manager.py`
   - Prompt file writing in `data.py`

### 2. **JSON Parsing** - Protected against:
   - Malformed JSON in status files
   - Corrupt log entries (already had some handling)
   - Added fallback behavior instead of crashing

### 3. **Directory Listing** - Added error handling for:
   - Exercise directory iteration
   - Prompt directory listing
   - Returns empty lists on errors instead of crashing

### 4. **Job Executor** - Enhanced error handling:
   - Already had comprehensive try/except for process execution
   - Added error handling to `_load_status()` method
   - Returns error status if files are missing/corrupt

## Implementation Approach

Followed the simple pattern recommended:
```python
try:
    with open(file) as f:
        data = json.load(f)
except (FileNotFoundError, json.JSONDecodeError) as e:
    logger.error(f"Failed to read {file}: {e}")
    # Either return default value or raise HTTPException
```

## Result

The application is now much more robust:
- Won't crash on missing/corrupt files
- Provides clear error messages in logs
- Returns meaningful HTTP error codes to users
- Continues operating even if individual jobs have issues
- No custom exception classes - just standard Python exceptions

## Testing

Verified the server starts successfully with all error handling in place. The error handling is straightforward and obvious - any developer can understand what's happening.