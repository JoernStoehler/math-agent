#!/bin/bash
# Simplified Math Agent Runner
set -e

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -j) JOB_DIR="$2"; shift 2 ;;
        -e) EXERCISE_FILE="$2"; shift 2 ;;
        -p) PROMPT_FILE="$2"; shift 2 ;;
        -m) MODEL="$2"; shift 2 ;;
        -t) MAX_TURNS="$2"; shift 2 ;;
        *) echo "Usage: $0 -j JOB_DIR -e EXERCISE -p PROMPT [-m MODEL] [-t MAX_TURNS]"; exit 1 ;;
    esac
done

# Defaults
MODEL="${MODEL:-claude-sonnet-4}"
MAX_TURNS="${MAX_TURNS:-100}"

# Validate required args
if [ -z "$JOB_DIR" ] || [ -z "$EXERCISE_FILE" ] || [ -z "$PROMPT_FILE" ]; then
    echo "Error: Missing required arguments"
    exit 1
fi

# Setup
mkdir -p "$JOB_DIR/workspace"
cp "$EXERCISE_FILE" "$JOB_DIR/workspace/exercise.tex"
cp "$PROMPT_FILE" "$JOB_DIR/workspace/prompt.md"
cd "$JOB_DIR/workspace"

# Log file
LOG="$JOB_DIR/log.jsonl"
echo "{\"status\": \"running\", \"time\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" > "$JOB_DIR/status.json"

# Build command based on model
if [[ "$MODEL" == gemini-* ]]; then
    # Gemini models
    if ! command -v gemini >/dev/null 2>&1; then
        echo "Error: gemini CLI not found"
        echo "{\"status\": \"failed\", \"error\": \"gemini not found\"}" > "$JOB_DIR/status.json"
        exit 1
    fi
    CMD="gemini -m $MODEL -y -p @prompt.md"
else
    # Claude models
    if ! command -v claude >/dev/null 2>&1; then
        echo "Error: claude CLI not found"
        echo "{\"status\": \"failed\", \"error\": \"claude not found\"}" > "$JOB_DIR/status.json"
        exit 1
    fi
    # Map model names for Claude
    case "$MODEL" in
        claude-opus-4) CLAUDE_MODEL="opus" ;;
        claude-sonnet-4) CLAUDE_MODEL="sonnet" ;;
        *) CLAUDE_MODEL="$MODEL" ;;
    esac
    CMD="claude --dangerously-skip-permissions --print --verbose --output-format stream-json --model $CLAUDE_MODEL --max-turns $MAX_TURNS < prompt.md"
fi

# Execute
echo "[$(date)] Executing: $CMD" >> "$LOG"
if eval "$CMD" >> "$LOG" 2>&1; then
    echo "[$(date)] Execution completed" >> "$LOG"
    
    # Compile PDF if solution exists
    if [ -f "solution.tex" ]; then
        pdflatex -interaction=nonstopmode solution.tex >> "$LOG" 2>&1
        pdflatex -interaction=nonstopmode solution.tex >> "$LOG" 2>&1
    fi
    
    echo "{\"status\": \"completed\", \"time\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" > "$JOB_DIR/status.json"
else
    echo "[$(date)] Execution failed" >> "$LOG"
    echo "{\"status\": \"failed\", \"time\": \"$(date -u +%Y-%m-%dT%H:%M:%SZ)\"}" > "$JOB_DIR/status.json"
fi