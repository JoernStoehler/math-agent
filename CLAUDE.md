# Math Agent Development Guidelines

This is the entry point for Claude Code. This file is automatically read at the start of each session.

## Quick Start

You are working in the math-agent development setup:
- **Current directory**: `/workspaces/math-agent`
- **Python**: Standard Python 3 with pip, Flask for web server
- **Tools available**: `claude`, `gemini`, `pdflatex`, `cloudflared`, `gh`, `git`
- **Main scripts**: Located in `src/` directory

## Environment Overview

### Architecture
- **DevContainer**: Docker Compose with two services
  - Main development container with LaTeX and tools
  - OTLP collector for telemetry (optional)
- **Persistence**: Docker named volumes for CLI credentials
- **Auto-setup**: Post-create script configures environment

### Key Tools
- **claude/gemini**: AI assistant CLIs for solving math exercises
- **pdflatex**: LaTeX compiler for generating PDF solutions
- **cloudflared**: Tunnel service for exposing local server
- **math-agent-simple.sh**: Script to process single exercises
- **server.py**: Web dashboard for batch processing

## Folder Structure

```
/workspaces/math-agent/
├── .devcontainer/          # DevContainer configuration
│   ├── devcontainer.json   # VS Code dev container settings
│   ├── docker-compose.yml  # Multi-container setup
│   ├── Dockerfile          # Custom container image
│   └── postCreateCommand.sh # Setup script
├── exercises/              # LaTeX exercise files
├── prompts/                # System prompts for AI agents
├── jobs/                   # Job outputs and logs
├── src/                    # Source code and scripts
│   ├── math-agent.sh       # Main batch processing script
│   ├── math-agent-simple.sh # Simple single-job script
│   ├── server.py           # Web dashboard server
│   └── start-cloudflare.sh # Cloudflare tunnel starter
├── .env.example            # Environment variables template
├── CLAUDE.md               # This file (developer guide)
└── README.md               # End-user documentation
```

## Common Commands

```bash
# Process a single exercise
./src/math-agent-simple.sh -j jobs/test -e exercises/example.tex -p prompts/v6.md -m claude-sonnet-4

# Start web dashboard
python src/server.py

# Expose server via Cloudflare tunnel
./src/start-cloudflare.sh

# Run with different models
# Claude models: claude-opus-4, claude-sonnet-4
# Gemini models: gemini-2.5-pro, gemini-2.5-flash

# Compile LaTeX manually
pdflatex solution.tex
```

## Working with Math Exercises

### Exercise Format
Exercises are LaTeX files in the `exercises/` directory. They typically contain:
- Problem statement
- Mathematical notation
- Sometimes hints or structure

### Solution Process
1. The AI reads the exercise file
2. Uses the prompt to understand solving approach
3. Generates a LaTeX solution
4. Compiles to PDF automatically

### Prompt Engineering
Prompts in `prompts/` directory control:
- Problem-solving approach
- Output format
- Level of detail
- Self-correction behavior

## Server Features

The web dashboard (`server.py`) provides:
- Job submission interface
- Real-time status monitoring
- Log viewing
- Process monitoring
- Batch processing with queue management

### Server Endpoints
- `/` - Main dashboard
- `/submit` - Job submission form
- `/logs/<job_id>` - View job logs
- `/processes` - Monitor running processes
- `/files/` - Browse output files

## Development Workflow

### Adding New Exercises
1. Create `.tex` file in `exercises/`
2. Follow existing naming convention
3. Test with simple script first

### Creating New Prompts
1. Copy existing prompt as template
2. Modify instructions as needed
3. Test effectiveness on sample exercises

### Debugging Jobs
1. Check job status in web dashboard
2. View logs at `/logs/<job_id>`
3. Examine workspace in `jobs/<job_id>/workspace/`

## Environment Variables

Optional configuration via `.env` file:
- `HONEYCOMB_API_KEY` - For telemetry (optional)
- `HONEYCOMB_DATASET` - Dataset name (default: math-agent)
- `CLAUDE_API_KEY` - If not using CLI auth
- `GEMINI_API_KEY` - If not using CLI auth

## Tips

- Use `git worktree` for parallel development branches
- Monitor system resources during batch processing
- Set appropriate `MAX_CONCURRENT_JOBS` in server.py
- Use test mode with smaller max_turns for debugging

## Troubleshooting

### LaTeX Compilation Errors
- Check for missing packages in Dockerfile
- Verify exercise.tex is valid LaTeX
- Look for encoding issues

### AI Model Issues
- Ensure CLI tools are authenticated
- Check API rate limits
- Verify model names are correct

### Server Problems
- Check port 5001 is not in use
- Verify file permissions
- Look for Python dependency issues

Remember: This environment is optimized for mathematical problem-solving with AI assistance. The tools and structure are designed to make batch processing of exercises efficient and trackable.