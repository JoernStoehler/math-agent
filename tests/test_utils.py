"""
Tests for utility functions.
"""
import json
import tempfile
from pathlib import Path

import pytest

from src.utils import atomic_write_json


class TestAtomicWriteJson:
    """Test atomic JSON writing utility."""
    
    def test_atomic_write_creates_file(self):
        """Test atomic write creates a new file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.json"
            data = {"key": "value", "number": 42}
            
            atomic_write_json(file_path, data)
            
            assert file_path.exists()
            with open(file_path) as f:
                loaded = json.load(f)
            assert loaded == data
    
    def test_atomic_write_overwrites_existing(self):
        """Test atomic write overwrites existing file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.json"
            
            # Write initial data
            file_path.write_text('{"old": "data"}')
            
            # Overwrite with new data
            new_data = {"new": "data", "updated": True}
            atomic_write_json(file_path, new_data)
            
            with open(file_path) as f:
                loaded = json.load(f)
            assert loaded == new_data
    
    def test_atomic_write_preserves_permissions(self):
        """Test atomic write preserves file permissions."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.json"
            
            # Create file with specific permissions
            file_path.touch(mode=0o600)
            original_mode = file_path.stat().st_mode
            
            atomic_write_json(file_path, {"data": "test"})
            
            # Check permissions are preserved
            assert file_path.stat().st_mode == original_mode
    
    def test_atomic_write_handles_path_object(self):
        """Test atomic write handles Path objects."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.json"
            data = {"test": "path"}
            
            atomic_write_json(file_path, data)
            
            assert file_path.exists()
            assert json.loads(file_path.read_text()) == data
    
    def test_atomic_write_requires_parent_dirs(self):
        """Test atomic write requires parent directories to exist."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "nested" / "dir" / "test.json"
            data = {"nested": True}
            
            # Should fail without parent directory
            with pytest.raises(FileNotFoundError):
                atomic_write_json(file_path, data)