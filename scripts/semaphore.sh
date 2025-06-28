#!/bin/bash
# Semaphore-based concurrency control for Claude processes
# Uses file-based locks with flock for atomic operations

SEMAPHORE_DIR="/tmp/math-agent-semaphores"
MAX_CONCURRENT=5
LOCK_TIMEOUT=3600  # 1 hour timeout to prevent stuck locks

# Create semaphore directory if it doesn't exist
mkdir -p "$SEMAPHORE_DIR"

# Function to acquire a semaphore lock
acquire_lock() {
    local job_id="$1"
    local wait_time=0
    
    # Try to acquire any available lock (1 through MAX_CONCURRENT)
    while true; do
        for i in $(seq 1 $MAX_CONCURRENT); do
            lock_file="$SEMAPHORE_DIR/lock.$i"
            
            # Try to acquire lock with timeout
            if flock -n -x "$lock_file" -c "echo $job_id > $lock_file && sleep infinity" & then
                lock_pid=$!
                echo "$i:$lock_pid"  # Return lock number and PID
                return 0
            fi
        done
        
        # No lock available, wait and retry
        if [ $wait_time -eq 0 ]; then
            echo "All $MAX_CONCURRENT slots are busy, waiting for available slot..." >&2
        fi
        
        sleep 5
        wait_time=$((wait_time + 5))
        
        # Log every minute
        if [ $((wait_time % 60)) -eq 0 ]; then
            echo "Still waiting for available slot (${wait_time}s elapsed)..." >&2
        fi
    done
}

# Function to release a semaphore lock
release_lock() {
    local lock_info="$1"
    local lock_num="${lock_info%%:*}"
    local lock_pid="${lock_info##*:}"
    
    # Kill the lock holder process
    if [ -n "$lock_pid" ] && kill -0 "$lock_pid" 2>/dev/null; then
        kill "$lock_pid" 2>/dev/null
    fi
    
    # Clean up lock file
    lock_file="$SEMAPHORE_DIR/lock.$lock_num"
    rm -f "$lock_file"
    
    echo "Released lock $lock_num" >&2
}

# Function to check current queue status
check_status() {
    echo "Current semaphore status:" >&2
    local active=0
    
    for i in $(seq 1 $MAX_CONCURRENT); do
        lock_file="$SEMAPHORE_DIR/lock.$i"
        if [ -f "$lock_file" ] && flock -n -x "$lock_file" -c true 2>/dev/null; then
            echo "  Slot $i: available" >&2
        else
            if [ -f "$lock_file" ]; then
                job_id=$(cat "$lock_file" 2>/dev/null || echo "unknown")
                echo "  Slot $i: occupied by $job_id" >&2
                active=$((active + 1))
            else
                echo "  Slot $i: available" >&2
            fi
        fi
    done
    
    echo "Active jobs: $active/$MAX_CONCURRENT" >&2
}

# Function to clean up stale locks
cleanup_locks() {
    echo "Cleaning up stale locks..." >&2
    
    for i in $(seq 1 $MAX_CONCURRENT); do
        lock_file="$SEMAPHORE_DIR/lock.$i"
        if [ -f "$lock_file" ]; then
            # Check if lock is stale (can be acquired)
            if flock -n -x "$lock_file" -c true 2>/dev/null; then
                rm -f "$lock_file"
                echo "  Removed stale lock $i" >&2
            fi
        fi
    done
}

# Main command processing
case "${1:-}" in
    acquire)
        acquire_lock "${2:-unknown}"
        ;;
    release)
        release_lock "$2"
        ;;
    status)
        check_status
        ;;
    cleanup)
        cleanup_locks
        ;;
    *)
        echo "Usage: $0 {acquire|release|status|cleanup} [args]" >&2
        echo "  acquire <job_id>  - Acquire a semaphore lock (blocks until available)" >&2
        echo "  release <lock_info> - Release a previously acquired lock" >&2
        echo "  status           - Show current semaphore status" >&2
        echo "  cleanup          - Clean up stale locks" >&2
        exit 1
        ;;
esac