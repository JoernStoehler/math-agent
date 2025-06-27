# Task: Keep Status as Simple Strings

## Objective
Keep the status field as simple strings. No enums needed for 5 values that rarely change.

## Why This is Better
1. **Already works** - the current string-based system is fine
2. **No imports needed** - just use "running", "completed", etc.
3. **JSON-friendly** - strings serialize naturally
4. **Less code** - no enum class to maintain

## Changes Required

### 1. Document Valid Values
Add a comment in models.py:
```python
class JobStatus(BaseModel):
    """Status information for a job"""
    status: str  # Valid values: "setup", "running", "completed", "error", "cancelled"
```

### 2. Maybe Add Validation
If we really need validation, use Pydantic's Literal:
```python
from typing import Literal

status: Literal["setup", "running", "completed", "error", "cancelled"]
```

But honestly, even this might be overkill.

## Success Criteria
- No enum imports
- Status remains simple strings
- Code is shorter and clearer
- No behavior changes

## Note
This "task" might be to do nothing - if the strings work fine, leave them alone!