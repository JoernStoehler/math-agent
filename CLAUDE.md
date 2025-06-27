# CLAUDE.md

This file offers essential information about the `math-agent` project.

See our specification @SPECIFICATION.md for a detailed overview of the project.
IMPORTANT: The specification must be kept up-to-date whenever you learn about a new change in vision for the project, or new architecture decisions.

## Environment
We are inside a devcontainer that was setup by the related project @../agent-environment
Said repository also provides useful generally applicable guidelines we want to adhere to:

## Guidelines

### 📁 Core Concepts
- [Development Principles](../agent-environment/docs/development/principles.md) - How to work effectively with Claude Code
- [Environment Setup](../agent-environment/docs/development/environment-setup.md) - DevContainer and tool configuration
- [Testing Guidelines](../agent-environment/docs/development/testing.md) - General testing best practices

### 🔄 Workflows
- [Task Management](../agent-environment/docs/workflows/task-management.md) - Using todos to track complex work
- [Git Worktree Workflow](../agent-environment/docs/workflows/git-worktree.md) - Parallel development with `agent-worktree`
- [Pull Request Process](../agent-environment/docs/workflows/pull-requests.md) - Creating effective PRs

### 🛠️ Tools
- [agent-worktree](../agent-environment/docs/tools/agent-worktree.md) - Git worktree management
- [agent-monitor](../agent-environment/docs/tools/agent-monitor.md) - System monitoring dashboard
- [Claude CLI](../agent-environment/docs/tools/claude.md) - Claude Code assistant
- [Gemini CLI](../agent-environment/docs/tools/gemini-cli.md) - Google's AI assistant

### 🐍 Python Development
- [Python Guide](../agent-environment/docs/python/README.md) - Python-specific documentation index
- [Code Style](../agent-environment/docs/python/code-style.md) - Python coding standards
- [Testing](../agent-environment/docs/python/testing.md) - Comprehensive pytest guide


## Common Commands

```bash
# Git worktree management
agent-worktree add feat/new-feature    # Create feature worktree
agent-worktree remove feat/old-feature # Remove after PR merge
git worktree list                      # List all worktrees

# System monitoring
agent-monitor                          # Live system dashboard
agent-monitor --interval 10            # Update every 10 seconds

# Python development (if applicable)
uv sync                               # Install dependencies
uv run pytest                         # Run tests
uv run ruff check .                   # Lint code
uv run pyright .                      # Type check

# Git workflow
git status                            # Check changes
git add <files>                       # Stage specific files
git commit -m "type: message"         # Conventional commit
gh pr create                          # Create pull request
```

## Working Patterns

### Task Management
- Use the Todo tool for complex multi-step tasks
- Break work into manageable pieces
- Update task status as you progress

### Code Development
- Follow existing patterns in the codebase
- Write tests first (TDD) when possible
- Use type hints and documentation
- Keep commits focused and atomic

### Communication
- Direct communication preferred
- Ask for clarification when needed
- Submit PRs for review
- Document decisions and rationale

## Environment Details

### File Paths
- **Workspace**: `/workspaces/{project-name}`
- **Tools**: `/workspaces/agent-environment/tools`
- **Config**: `~/.claude`, `~/.gemini` (Docker volumes)

### Environment Variables
- GitHub secrets used in Codespaces
- `WORKSPACE_PATH` always points to current workspace

### Telemetry (Optional)
- OTEL collector at `http://otlp:4318`
- Forwards to Honeycomb if configured
- See [Telemetry Setup](../agent-environment/docs/setup/telemetry-configuration.md)

## Getting Help

- **Documentation**: Browse `../agent-environment/docs/` for detailed guides
- **Troubleshooting**: Check specific tool documentation
- **Examples**: Look for existing patterns in the codebase

Remember: This environment is designed for efficient development with AI assistance. Use the tools provided to explore, understand, and modify code effectively.