# Task 03: Basic Usage Documentation

## Objective
Create a simple, practical README that explains how to actually use the system.

## Required Sections

### 1. What Is This?
- One paragraph explaining the math agent benchmarking system
- What problem it solves

### 2. Quick Start
```bash
# Install dependencies
uv sync

# Start the server
uv run python -m math_agent.main

# Open browser to http://localhost:8000
```

### 3. How to Submit a Job
1. Click "New Job" on dashboard
2. Fill out the form:
   - Job name: unique identifier
   - Model: claude-opus-4 or gemini-2.5-pro
   - Exercise: select from dropdown
   - Prompt: choose existing or create new
3. Submit and monitor progress

### 4. For Testing/Demos
```bash
# Run the mock executor in another terminal
python scripts/mock_executor.py

# This simulates job execution without calling real AI
```

### 5. Project Structure
Brief explanation of key directories:
- `data/exercises/` - Math problems
- `data/prompts/` - Saved prompts  
- `jobs/` - Job results
- `static/` - Web UI

### 6. Configuration
- No configuration needed for basic usage
- Runs on port 8000 by default

## What NOT to Include
- Complex architecture diagrams
- Detailed API documentation
- Development philosophy
- Future roadmap

## Success Criteria
- Someone can run the system in 2 minutes
- Clear explanation of what it does
- Simple troubleshooting section
- Links to task documentation for developers