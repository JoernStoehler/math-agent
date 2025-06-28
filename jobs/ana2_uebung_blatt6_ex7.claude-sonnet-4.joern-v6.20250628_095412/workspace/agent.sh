#!/bin/bash

# Agent script - runs Claude with the prompt using streaming JSON output

set -e

# Check if prompt.md exists
if [ ! -f "prompt.md" ]; then
    echo "Error: prompt.md not found in current directory"
    exit 1
fi

# Run Claude with streaming JSON output and max 100 turns
# Note: stream-json with --print requires --verbose
echo "Starting Claude agent (v2 - streaming JSON)..."
claude --dangerously-skip-permissions --print --verbose --output-format stream-json --max-turns 100 -p "@prompt.md"