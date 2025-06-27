# Task: Add Basic Tests That Actually Matter

## Objective
Add simple tests for the parts that actually break. No complex fixtures, no 100% coverage goals.

## What to Test
1. **Job executor command building** - this is critical and untested
2. **API endpoints** - basic smoke tests
3. **File operations** - ensure atomic writes work

## Test Structure
Keep it dead simple:
```python
def test_job_executor_builds_correct_command():
    # Test that we build the right CLI command
    executor = JobExecutor(Path("/tmp/test"))
    cmd = executor._build_command("claude", "my_prompt.md")
    assert "claude" in cmd
    assert "my_prompt.md" in cmd

def test_api_endpoints_dont_crash():
    # Just make sure endpoints return 200 or 404
    client = TestClient(app)
    assert client.get("/").status_code == 200
    assert client.get("/jobs").status_code == 200
```

## What NOT to Do
- Don't mock everything
- Don't aim for 100% coverage
- Don't create complex test utilities
- Don't test obvious things

## Success Criteria
- Critical paths have basic tests
- Tests run in < 10 seconds
- Any developer can read and understand tests
- Tests actually catch real bugs