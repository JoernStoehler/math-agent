# Math Agent System

A benchmarking system for evaluating AI agents on mathematical problems from University of Augsburg lectures.

## What Is This?

This system allows you to submit mathematical problems to AI agents (Claude or Gemini), track their execution, and review the generated solutions through a web interface. It's designed for benchmarking how well different AI models can solve university-level mathematics problems.

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- Claude CLI or Gemini CLI installed and configured with API keys

### Installation & Running

```bash
# Clone the repository
git clone <repository-url>
cd math-agent

# Install dependencies
uv sync

# Start the server
PYTHONPATH=src uv run python -m math_agent.main

# Open your browser to http://localhost:8000
```

## How to Submit a Job

1. **Open the Dashboard**: Navigate to http://localhost:8000
2. **Click "New Job"**: This opens the job submission form
3. **Fill out the form**:
   - **Job Name**: A unique identifier (e.g., "analysis-problem-5")
   - **Model**: Select from available models:
     - claude-opus-4
     - claude-sonnet-4
     - gemini-2.5-pro
     - gemini-2.5-flash
   - **Exercise**: Choose from dropdown of available exercises
   - **Prompt**: Either select an existing prompt template or create a new one
   - **Disallowed Tools** (optional): Comma-separated list of tools to disable (e.g., "WebSearch,Bash")
4. **Submit**: The job will be queued and executed
5. **Monitor Progress**: Click on the job in the dashboard to see real-time logs

## For Testing/Demos

If you don't have API keys or want to test the system without calling real AI models:

```bash
# In a separate terminal, run the mock executor
python scripts/mock_executor.py

# This simulates job execution by:
# - Changing job status from "setup" → "running" → "completed"
# - Creating mock solution files
# - Adding fake log entries
```

## Project Structure

```
math-agent/
├── data/                    # Data files
│   ├── exercises/          # Math problems organized by course
│   │   └── <course>/      # e.g., analysis_1, linear_algebra
│   │       └── *.tex      # LaTeX exercise files
│   └── prompts/           # Saved prompt templates
│       └── *.md          # Markdown prompt files
├── jobs/                   # Job execution results (gitignored)
│   └── <job-name>/        # Each job gets its own directory
│       ├── workspace/     # Working directory for the AI agent
│       ├── status.json    # Job status and metadata
│       └── log.jsonl      # Execution log entries
├── src/math_agent/        # Source code
│   ├── api/              # API routes
│   ├── services/         # Core services (job executor, manager)
│   ├── config.py         # Simple configuration
│   └── main.py           # FastAPI application
├── static/               # Web UI files
│   ├── dashboard.html    # Main job listing
│   ├── job.html         # Job details view
│   └── submit.html      # Job submission form
└── tests/               # Comprehensive test suite
```

## Key Features

- **Simple Architecture**: No complex abstractions or unnecessary patterns
- **Real-time Monitoring**: Watch job execution logs in real-time
- **Multiple AI Models**: Support for both Claude and Gemini models
- **Error Handling**: Graceful handling of failures with clear error messages
- **File Browser**: Browse job outputs and data files through the web UI

## API Endpoints

- `GET /` - Dashboard showing all jobs
- `GET /jobs` - JSON list of all jobs
- `POST /jobs/create` - Create a new job
- `GET /jobs/{name}` - Get job details and logs
- `POST /jobs/{name}/cancel` - Cancel a running job
- `GET /data/exercises` - List available exercises
- `GET /data/models` - List available AI models
- `GET /data/prompts` - List saved prompts
- `POST /data/prompts/save` - Save a new prompt
- `GET /files/...` - Browse files (data and jobs)

## Development

### Running Tests

```bash
# Run all tests
PYTHONPATH=src uv run pytest -v

# Run specific test file
PYTHONPATH=src uv run pytest tests/test_job_executor.py -v
```

All critical components are tested:
- Job executor command building and execution flow
- API endpoints and error handling
- Status updates and log streaming

### Code Quality

```bash
# Run linter
uv run ruff check .

# Format code
uv run ruff format .
```

### Adding New Features

1. Keep it simple - avoid unnecessary abstractions
2. Add tests for critical functionality
3. Use clear, descriptive names
4. Follow existing patterns in the codebase

## Troubleshooting

### Common Issues

**Server won't start**: Make sure you're using `PYTHONPATH=src` when running the server

**Jobs stuck in "setup"**: Check that either:
- The Claude/Gemini CLI is properly installed and configured
- The mock executor is running for testing

**Can't find exercises**: Ensure the `data/exercises/` directory contains `.tex` files organized by course

**Import errors**: Install dependencies with `uv sync` (not pip)

### Logs

- **Server logs**: Check the terminal where you started the server
- **Job logs**: View in the web UI or check `jobs/<job-name>/log.jsonl`
- **Error details**: Found in `jobs/<job-name>/status.json`

## Architecture Notes

This codebase follows the principle of "boring is good":
- Simple module-level configuration
- Direct imports instead of dependency injection  
- Standard FastAPI patterns
- File-based storage (no database needed)
- Clear separation between API, services, and data

The goal is code that any Python developer can understand and modify in minutes, not hours.