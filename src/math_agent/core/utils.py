"""
Utility functions for the math agent system.
"""
import json
import os
import tempfile
from pathlib import Path
from typing import Any


def atomic_write_json(file_path: Path, data: Any, indent: int = 2) -> None:
    """
    Write JSON data to a file atomically.
    
    This prevents file corruption if the process is interrupted during write.
    
    Args:
        file_path: Path to the file to write
        data: Data to serialize as JSON
        indent: JSON indentation level
    """
    # Write to temporary file in same directory (for same filesystem)
    temp_fd, temp_path = tempfile.mkstemp(
        dir=file_path.parent,
        prefix=f".{file_path.name}.",
        suffix=".tmp"
    )
    
    try:
        # Write data to temp file
        with os.fdopen(temp_fd, 'w') as f:
            json.dump(data, f, indent=indent)
            f.flush()
            os.fsync(f.fileno())
        
        # Atomically replace the original file
        os.replace(temp_path, file_path)
    except:
        # Clean up temp file on error
        try:
            os.unlink(temp_path)
        except:
            pass
        raise