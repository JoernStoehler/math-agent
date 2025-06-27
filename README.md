# Math Agent System

A benchmarking system for evaluating AI agents on mathematical problems from University of Augsburg lectures.

## ⚠️ WARNING: UNTESTED CODE

**The job executor component is COMPLETELY UNTESTED and should not be used in production.** See [tests/test_job_executor.py](tests/test_job_executor.py) for details on what needs testing.

## Overview

This system allows you to:
- Submit math problems to AI agents (Claude, Gemini)
- Track job execution and results
- Browse solutions through a web interface

## Quick Start

### Prerequisites

- Python 3.12+
- [uv](https://github.com/astral-sh/uv) package manager
- Claude CLI or Gemini CLI installed and configured

### Setup

```bash
# Clone the repository
git clone <repository-url>
cd math-agent

# Install dependencies with uv
uv sync

# Run the server
uv run python src/backend/server.py
```

The server will start at http://localhost:8000

### Development Mode

To enable the mock job executor for testing (without actually running AI agents):

```bash
DEV_MODE=true uv run python src/backend/server.py
```

## Project Structure

```
math-agent/
├── src/                    # Source code
│   ├── backend/           # Backend implementation
│   │   ├── server.py      # FastAPI server
│   │   ├── job.py         # Job executor (UNTESTED!)
│   │   └── job_manager.py # Job queue management
│   └── models.py          # Pydantic models
├── static/                # Frontend HTML files
├── data/                  # Exercise files and prompts
│   ├── exercises/         # Math problems (.tex files)
│   └── prompts/          # Prompt templates
├── jobs/                  # Job execution artifacts (gitignored)
└── tests/                 # Test files (with warnings!)
```

## API Endpoints

- `GET /` - Main dashboard
- `GET /jobs` - List all jobs
- `POST /jobs/create` - Create a new job
- `GET /jobs/{name}` - Get job details
- `POST /jobs/{name}/cancel` - Cancel a running job
- `GET /files/{path}` - Browse files

## Running Tests

```bash
# Install dev dependencies
uv sync --dev

# Run tests (will show warnings about untested code)
uv run pytest
```

## Configuration

The system uses environment variables for configuration:

- `DEV_MODE=true` - Enable mock job executor
- `PORT=8000` - Server port (default: 8000)
- `HOST=0.0.0.0` - Server host (default: 0.0.0.0)

## Known Issues

1. **Job Executor is Untested** - The core job execution logic has not been tested with real AI agents
2. **No Production Safeguards** - Missing rate limiting, authentication, and error recovery
3. **File-based Storage** - Uses JSON files instead of a proper database

## Development

This project uses:
- **FastAPI** for the web framework
- **uv** for package management
- **pytest** for testing
- **ruff** for linting

### Adding a New AI Model

1. Add the model to the allowed list in `src/backend/server.py`
2. Ensure the corresponding CLI tool is installed
3. Test the integration (currently no tests exist!)

## Contributing

Before contributing:
1. Run the existing tests: `uv run pytest`
2. Add tests for any new functionality
3. Use `uv run ruff check .` for linting

## License

[Add license information]