# Task 01: Test Job Executor Core Functions

## 🚨 CRITICAL: The job executor is completely untested!

## Objective
Add basic tests for the JobExecutor class - the heart of the system that actually runs AI agents.

## What to Test

### 1. Command Building
```python
def test_executor_builds_claude_command():
    # Test the actual command that gets built
    executor = JobExecutor(tmp_path / "test_job")
    executor.workspace_dir.mkdir(parents=True)
    
    # Create mock status file
    status = {"model": "claude-opus-4", "disallowedTools": "WebSearch"}
    (tmp_path / "test_job" / "status.json").write_text(json.dumps(status))
    
    # The executor builds command in execute(), but we need to extract that logic
    # Check the actual command building code in job_executor.py lines 43-53
```

### 2. Status Updates
```python
def test_executor_updates_status():
    # Test that status transitions work
    executor = JobExecutor(tmp_path / "test_job") 
    # Test status goes from setup -> running -> completed
```

### 3. Log Streaming
```python
def test_executor_streams_logs():
    # Mock the subprocess to test log streaming
    # Verify JSON lines are written correctly
```

## What NOT to Test
- ❌ Actual claude/gemini execution (requires API keys)
- ❌ PDF compilation (external dependency)
- ❌ Full integration (keep it simple)

## Implementation Notes

1. Extract command building logic to a testable method
2. Use pytest tmp_path for test directories
3. Mock subprocess for testing process interaction
4. Focus on the critical paths only

## Success Criteria
- Can verify correct commands are built
- Can verify status updates work
- Can verify log streaming works
- Tests run fast (< 5 seconds)
- No external dependencies required