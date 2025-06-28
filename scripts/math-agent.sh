#!/bin/bash

# Math Agent Runner Script
# Handles setup, execution, and lifecycle management for math agent jobs

set -e

# Default values
MODEL="claude-sonnet-4"
MAX_TURNS=100
PROMPT_FILE=""
EXERCISE_FILE=""
JOB_DIR=""
ANTHROPIC_API_KEY="${ANTHROPIC_API_KEY:-}"
TEST_RUN=false

# Function to display usage
usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Math Agent Runner - Executes Claude to solve math problems

Options:
    -j, --job-dir DIR        Job directory (required)
    -e, --exercise FILE      Exercise .tex file (required)
    -p, --prompt FILE        Prompt .md file (required)
    -m, --model MODEL        Model to use (default: claude-sonnet-4)
    -t, --max-turns NUM      Maximum turns (default: 100)
    -k, --api-key KEY        Anthropic API key (or use ANTHROPIC_API_KEY env var)
    --test-run               Use claude-dummy for testing (ignores API key)
    -h, --help               Show this help message

Example:
    $0 -j jobs/test_job -e exercises/addition.tex -p prompts/v2.md

EOF
    exit 1
}

# Function to write status
write_status() {
    local status="$1"
    local job_dir="$2"
    local timestamp=$(date +"%Y%m%d_%H%M%S")
    
    # Create status.json
    if [ "$status" = "scheduled" ]; then
        echo "{\"status\": \"$status\", \"created\": \"$timestamp\"}" > "$job_dir/status.json"
    elif [ "$status" = "failed" ] || [ "$status" = "completed" ]; then
        # Update with completion time
        local created=$(jq -r '.created' "$job_dir/status.json" 2>/dev/null || echo "$timestamp")
        echo "{\"status\": \"$status\", \"created\": \"$created\", \"completed\": \"$timestamp\"}" > "$job_dir/status.json"
    else
        # Just update status
        local created=$(jq -r '.created' "$job_dir/status.json" 2>/dev/null || echo "$timestamp")
        echo "{\"status\": \"$status\", \"created\": \"$created\"}" > "$job_dir/status.json"
    fi
}

# Function to log message
log_message() {
    local message="$1"
    local log_file="$2"
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] $message" >> "$log_file"
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -j|--job-dir)
            JOB_DIR="$2"
            shift 2
            ;;
        -e|--exercise)
            EXERCISE_FILE="$2"
            shift 2
            ;;
        -p|--prompt)
            PROMPT_FILE="$2"
            shift 2
            ;;
        -m|--model)
            MODEL="$2"
            shift 2
            ;;
        -t|--max-turns)
            MAX_TURNS="$2"
            shift 2
            ;;
        -k|--api-key)
            ANTHROPIC_API_KEY="$2"
            shift 2
            ;;
        --test-run)
            TEST_RUN=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            echo "Error: Unknown option $1"
            usage
            ;;
    esac
done

# Validate required arguments
if [ -z "$JOB_DIR" ] || [ -z "$EXERCISE_FILE" ] || [ -z "$PROMPT_FILE" ]; then
    echo "Error: Missing required arguments"
    usage
fi

if [ -z "$ANTHROPIC_API_KEY" ]; then
    echo "Warning: ANTHROPIC_API_KEY not set"
    # Don't exit - we might be using claude-dummy
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

# Create job directory structure
mkdir -p "$JOB_DIR/workspace"
LOG_FILE="$JOB_DIR/log.jsonl"

# Write initial status
write_status "scheduled" "$JOB_DIR"

echo "Starting math agent job in: $JOB_DIR"
echo "Exercise: $EXERCISE_FILE"
echo "Prompt: $PROMPT_FILE"
echo "Model: $MODEL"
echo "Max turns: $MAX_TURNS"
if [ "$TEST_RUN" = true ]; then
    echo "Test run: YES (will use claude-dummy)"
fi

# Copy files to workspace
cp "$EXERCISE_FILE" "$JOB_DIR/workspace/exercise.tex"
cp "$PROMPT_FILE" "$JOB_DIR/workspace/prompt.md"

# Update status to running
write_status "running" "$JOB_DIR"

# Get the absolute path to the script directory before changing directories
if [ -L "$0" ]; then
    SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
else
    SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
fi
CLAUDE_DUMMY="$SCRIPT_DIR/claude-dummy"

# Change to workspace directory
cd "$JOB_DIR/workspace"

# Run Claude with proper error handling
{
    # Log start
    log_message "Starting Claude execution" "$LOG_FILE"
    log_message "Model: $MODEL, Max turns: $MAX_TURNS" "$LOG_FILE"
    
    # Determine which claude command to use
    CLAUDE_CMD=""
    
    if [ "$TEST_RUN" = true ]; then
        # Force use of claude-dummy in test run mode
        if [ -x "$CLAUDE_DUMMY" ]; then
            CLAUDE_CMD="$CLAUDE_DUMMY"
            log_message "Test run mode: Using claude-dummy for debugging" "$LOG_FILE"
        else
            log_message "Error: Test run requested but claude-dummy not found at $CLAUDE_DUMMY" "$LOG_FILE"
            write_status "failed" "$JOB_DIR"
            exit 1
        fi
    elif command -v claude-code >/dev/null 2>&1 && [ -n "$ANTHROPIC_API_KEY" ]; then
        CLAUDE_CMD="claude-code --model $MODEL --max-turns $MAX_TURNS"
        log_message "Using claude-code with model $MODEL" "$LOG_FILE"
    elif [ -x "$CLAUDE_DUMMY" ]; then
        CLAUDE_CMD="$CLAUDE_DUMMY"
        log_message "Warning: Using claude-dummy (simulation mode)" "$LOG_FILE"
    else
        log_message "Error: Neither claude-code nor claude-dummy found (looked for $CLAUDE_DUMMY)" "$LOG_FILE"
        write_status "failed" "$JOB_DIR"
        exit 1
    fi
    
    # Execute Claude
    if $CLAUDE_CMD < prompt.md >> "$LOG_FILE" 2>&1; then
        log_message "Claude execution completed successfully" "$LOG_FILE"
        
        # Check if solution.tex was created
        if [ -f "solution.tex" ]; then
            log_message "Compiling solution.tex to PDF" "$LOG_FILE"
            
            # Compile to PDF (run twice for references)
            if pdflatex -interaction=nonstopmode solution.tex >> "$LOG_FILE" 2>&1 && \
               pdflatex -interaction=nonstopmode solution.tex >> "$LOG_FILE" 2>&1; then
                log_message "PDF compilation successful" "$LOG_FILE"
                write_status "completed" "$JOB_DIR"
            else
                log_message "PDF compilation failed" "$LOG_FILE"
                write_status "failed" "$JOB_DIR"
            fi
        else
            log_message "Warning: solution.tex not found" "$LOG_FILE"
            write_status "completed" "$JOB_DIR"
        fi
    else
        log_message "Claude execution failed" "$LOG_FILE"
        write_status "failed" "$JOB_DIR"
    fi
} || {
    # Catch any unexpected errors
    log_message "Unexpected error occurred" "$LOG_FILE"
    write_status "failed" "$JOB_DIR"
}

echo "Job completed. Status written to $JOB_DIR/status.json"