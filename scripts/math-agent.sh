#!/bin/bash
# Math Agent Runner - Simplified version
set -e

# Default values
MODEL="claude-sonnet-4"
MAX_TURNS=100

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -j|--job-dir) JOB_DIR="$2"; shift 2 ;;
        -e|--exercise) EXERCISE_FILE="$2"; shift 2 ;;
        -p|--prompt) PROMPT_FILE="$2"; shift 2 ;;
        -m|--model) MODEL="$2"; shift 2 ;;
        -t|--max-turns) MAX_TURNS="$2"; shift 2 ;;
        -k|--api-key) shift 2 ;; # Ignored for compatibility
        --test-run) echo "Test run not implemented"; exit 1 ;;
        -h|--help)
            echo "Usage: $0 -j JOB_DIR -e EXERCISE -p PROMPT [-m MODEL] [-t MAX_TURNS]"
            echo "Models: claude-opus-4, claude-sonnet-4, gemini-2.5-pro, gemini-2.5-flash"
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# Validate required arguments
if [ -z "$JOB_DIR" ] || [ -z "$EXERCISE_FILE" ] || [ -z "$PROMPT_FILE" ]; then
    echo "Error: Missing required arguments"
    exit 1
fi

# Convert to absolute paths
JOB_DIR=$(realpath "$JOB_DIR")
EXERCISE_FILE=$(realpath "$EXERCISE_FILE")
PROMPT_FILE=$(realpath "$PROMPT_FILE")

# Validate files exist
if [ ! -f "$EXERCISE_FILE" ]; then
    echo "Error: Exercise file not found: $EXERCISE_FILE"
    exit 1
fi

if [ ! -f "$PROMPT_FILE" ]; then
    echo "Error: Prompt file not found: $PROMPT_FILE"
    exit 1
fi

# Setup workspace
mkdir -p "$JOB_DIR/workspace"
LOG_FILE="$JOB_DIR/log.jsonl"

# Initial status
echo "{\"status\": \"scheduled\", \"created\": \"$(date +%Y%m%d_%H%M%S)\"}" > "$JOB_DIR/status.json"

echo "Starting job in: $JOB_DIR"
echo "Model: $MODEL"

# Copy files to workspace
cp "$EXERCISE_FILE" "$JOB_DIR/workspace/exercise.tex"
cp "$PROMPT_FILE" "$JOB_DIR/workspace/prompt.md"

# Update status
echo "{\"status\": \"running\", \"created\": \"$(date +%Y%m%d_%H%M%S)\"}" > "$JOB_DIR/status.json"

# Change to workspace
cd "$JOB_DIR/workspace"

# Log function
log() {
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] $1" >> "$LOG_FILE"
}

# Start execution
log "Starting execution with model: $MODEL"

# Build and execute command based on model type
if [[ "$MODEL" == gemini-* ]]; then
    # Gemini command
    if ! command -v gemini >/dev/null 2>&1; then
        log "Error: gemini command not found"
        echo "{\"status\": \"failed\"}" > "$JOB_DIR/status.json"
        exit 1
    fi
    
    log "Executing: gemini -m $MODEL -y -p @prompt.md"
    if gemini -m "$MODEL" -y -p "@prompt.md" >> "$LOG_FILE" 2>&1; then
        log "Gemini execution completed"
    else
        log "Gemini execution failed"
        echo "{\"status\": \"failed\"}" > "$JOB_DIR/status.json"
        exit 1
    fi
else
    # Claude command
    if ! command -v claude >/dev/null 2>&1; then
        log "Error: claude command not found"
        echo "{\"status\": \"failed\"}" > "$JOB_DIR/status.json"
        exit 1
    fi
    
    # Map model names
    case "$MODEL" in
        claude-opus-4) CLAUDE_MODEL="opus" ;;
        claude-sonnet-4) CLAUDE_MODEL="sonnet" ;;
        *) CLAUDE_MODEL="$MODEL" ;;
    esac
    
    log "Executing: claude with model $CLAUDE_MODEL"
    if claude --dangerously-skip-permissions --print --verbose --output-format stream-json \
              --model "$CLAUDE_MODEL" --max-turns "$MAX_TURNS" < prompt.md >> "$LOG_FILE" 2>&1; then
        log "Claude execution completed"
    else
        log "Claude execution failed"
        echo "{\"status\": \"failed\"}" > "$JOB_DIR/status.json"
        exit 1
    fi
fi

# Check for solution and compile PDF
if [ -f "solution.tex" ]; then
    log "Compiling solution.tex to PDF"
    if pdflatex -interaction=nonstopmode solution.tex >> "$LOG_FILE" 2>&1 && \
       pdflatex -interaction=nonstopmode solution.tex >> "$LOG_FILE" 2>&1; then
        log "PDF compilation successful"
    else
        log "PDF compilation failed"
    fi
else
    log "Warning: solution.tex not found"
fi

# Final status
echo "{\"status\": \"completed\", \"created\": \"$(date +%Y%m%d_%H%M%S)\"}" > "$JOB_DIR/status.json"
echo "Job completed"