# Math Agent System Specification

## Overview

A benchmarking system for evaluating AI agents on mathematical problems from University of Augsburg lectures. The system manages job execution, tracks agent performance, and provides a web interface for monitoring.

## Technology Stack

- **Backend**: Python 3.12+, FastAPI, asyncio
- **Frontend**: Vanilla HTML/CSS/JavaScript  
- **Agent**: Claude CLI tool
- **Package Management**: uv
- **Code Quality**: ruff

## Project Structure

```
math-agent/
├── data/                                    # Experiment data
│   ├── exercises/                          # Math exercises by course
│   │   └── <course>/<exercise>.tex
│   └── prompts/                            # Saved prompts (text files)
│       └── <prompt_name>.md
├── jobs/                                   # Job execution artifacts
│   └── <job_name>/
│       ├── workspace/                      # Agent working directory
│       │   ├── prompt.md                  # Job prompt
│       │   ├── <exercise>.tex             # Exercise file
│       │   ├── solution.tex              # Agent output (generated)
│       │   └── solution.pdf              # Compiled solution (generated)
│       ├── status.json                    # Job status metadata
│       └── log.jsonl                      # Agent execution log
├── src/backend/                           # Backend implementation
│   ├── job.py                            # Job execution logic
│   ├── job_manager.py                    # Job queue management
│   └── server.py                        # API server & routing
└── static/                               # Frontend assets
    ├── dashboard.html                    # Main dashboard
    ├── job.html                          # Job details page
    └── submit.html                       # Job submission form
```

## Web Interface

### Dashboard (/)
- Table of jobs with columns: Name, Status, Model, Exercise, Created, Actions
- Click row → job page
- Buttons: "New Job" → submit page, "File Server" → file browser
- Direct links in Actions column: solution.pdf, solution.tex, workspace (if available)

### Job Submission (/submit)

**Step 1: Job Configuration**
- **Job Name**: Text input (must be unique)
- **Model**: Dropdown (claude-opus-4, claude-sonnet-4, gemini-2.5-pro, gemini-2.5-flash)
- **Disallowed Tools**: Text input (optional, e.g., "Bash(git:*),WebSearch")
- **Exercise**: Dropdown to select from data/exercises/

**Step 2: Prompt Selection**
- Radio buttons:
  - Use existing prompt: Dropdown of saved prompts
  - Create new prompt: Text input for new prompt name

**Step 3: Prompt Content** (if creating new)
- Large textarea for prompt content
- Can include markdown + LaTeX code blocks for templates
- No syntax highlighting (too complex)

**Step 4: Additional Files** (optional)
- File upload for supplementary materials (lecture notes, etc.)
- Rarely used

**Step 5: Review**
- Compact summary showing:
  - Job name, model, exercise
  - Prompt name (existing or new)
  - List of uploaded files
  - Disallowed tools
- "Submit" button → creates job and redirects to job page

### Job Page (/job/<job_name>)
- **Status**: Current job status (prominently displayed)
- **Chat View**: Scrollable message list
  - First message: The prompt content
  - Following messages: Log entries formatted as chat
- **Buttons**:
  - "Solution.tex" (disabled until available)
  - "Solution.pdf" (disabled until available)  
  - "View Workspace" → file server
  - "Cancel" (red, only if job is running)
- **Auto-refresh**: Pull status + log every 2 seconds via single endpoint
- **Notifications**: Alert user on status change (tab title + notification)

### File Server (/files/...)
- Browse and download files from data/ and jobs/
- Standard file listing interface

## API Endpoints

### Job Management

**GET /jobs**
- Returns: Map of job_name → status.json content

**GET /jobs/<name>**
- Returns: Combined status + log data
- Used for 2-second polling on job page

**POST /jobs/create**
```json
{
  "name": "unique-job-name",
  "model": "claude-opus-4",
  "exercise": "analysis_1/sheet_01_ex_04",
  "prompt": "prompt content or @saved_prompt_name",
  "disallowedTools": "Bash(git:*),WebSearch",
  "additionalFiles": {
    "filename.tex": "<base64 content>"
  }
}
```

**POST /jobs/<name>/cancel**
- Cancels running job

### Data Access

**GET /data/exercises**
- Returns: List of available exercises

**GET /data/models**
- Returns: ["claude-opus-4", "claude-sonnet-4", "gemini-2.5-pro", "gemini-2.5-flash"]

**GET /data/prompts**
- Returns: List of saved prompt names

**POST /data/prompts/save**
```json
{
  "name": "prompt_name",
  "content": "prompt content"
}
```

### File Server

**GET /files/<path>**
- Serves files from data/ and jobs/ directories only

## Job Execution

### Job Creation
1. Validate unique job name
2. Create job directory: `jobs/<name>/`
3. Setup workspace with:
   - prompt.md (from request or saved prompt)
   - exercise file
   - additional uploaded files
4. Initialize status.json

### Job Execution

#### Automatic Job Scanning
The job manager continuously scans the `jobs/` directory every 5 seconds for jobs in "setup" status and automatically submits them for execution. This allows jobs to be created either through the API or by directly creating the appropriate directory structure.

#### Command Execution
```bash
claude --print "@prompt.md" \
       --verbose \
       --output-format stream-json \
       --disallowedTools <tools> \
       --model <model>
```

Note: The CLI tool is selected based on the model prefix:
- Models starting with "claude" use the `claude` CLI
- All other models use the `gemini` CLI

### Status Updates
- Stream log entries to log.jsonl
- Update status.json on state changes
- After completion: Check for solution.tex/pdf

#### Automatic PDF Compilation
If `solution.tex` exists but `solution.pdf` does not, the system automatically runs:
```bash
pdflatex -interaction=nonstopmode solution.tex
# Runs twice to resolve references
```

### Status Schema
```typescript
{
  status: "setup" | "running" | "completed" | "error" | "cancelled",
  createdAt: string,
  startedAt?: string,
  completedAt?: string,
  error?: string,
  solutionTexCreated?: boolean,
  solutionPdfCreated?: boolean
}
```

## External Evaluation

Evaluations will be done externally (e.g., Google Sheets) since they need to be available when the backend is offline. Future consideration: Read-only Google Sheet updated on status changes for offline dashboard access.

## Development

### Setup
```bash
# Install dependencies
uv sync

# Run server
uv run python src/backend/server.py

# Run with mock executor (for testing)
DEV_MODE=true uv run python src/backend/server.py
```

### Testing
```bash
# Install dev dependencies
uv sync --dev

# Run tests
uv run pytest
```


### Project Structure
- `src/math_agent/main.py` - FastAPI application
- `src/math_agent/services/job_executor.py` - Job executor with comprehensive tests
- `src/math_agent/services/job_manager.py` - Job queue management
- `src/math_agent/core/models.py` - Pydantic models
- `tests/` - Comprehensive test suite

Single Python process running FastAPI + job manager with asyncio.

## Limitations

- No authentication (keep URLs private)
- No job resume capability
- No built-in grading
- File-based storage only
- No database