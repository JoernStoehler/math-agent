"""Tests for the job executor"""
import json
from unittest.mock import Mock, AsyncMock, patch
import pytest

from math_agent.services.job_executor import JobExecutor
from math_agent.core.models import JobStatusEnum


class TestJobExecutor:
    """Test the JobExecutor class"""
    
    def test_build_command_claude(self, tmp_path):
        """Test command building for Claude models"""
        executor = JobExecutor(tmp_path / "test_job")
        
        # Test basic Claude command
        cmd = executor._build_command("claude-opus-4")
        assert cmd == [
            "claude",
            "--print", "@prompt.md",
            "--verbose",
            "--output-format", "stream-json",
            "--model", "claude-opus-4"
        ]
        
        # Test with disallowed tools
        cmd = executor._build_command("claude-sonnet-4", "WebSearch,Bash")
        assert cmd == [
            "claude",
            "--print", "@prompt.md",
            "--verbose",
            "--output-format", "stream-json",
            "--model", "claude-sonnet-4",
            "--disallowedTools", "WebSearch,Bash"
        ]
    
    def test_build_command_gemini(self, tmp_path):
        """Test command building for Gemini models"""
        executor = JobExecutor(tmp_path / "test_job")
        
        # Test basic Gemini command
        cmd = executor._build_command("gemini-2.5-pro")
        assert cmd == [
            "gemini",
            "--print", "@prompt.md",
            "--verbose",
            "--output-format", "stream-json",
            "--model", "gemini-2.5-pro"
        ]
        
        # Test with disallowed tools
        cmd = executor._build_command("gemini-2.5-flash", "WebFetch")
        assert cmd == [
            "gemini",
            "--print", "@prompt.md",
            "--verbose",
            "--output-format", "stream-json",
            "--model", "gemini-2.5-flash",
            "--disallowedTools", "WebFetch"
        ]
    
    @pytest.mark.asyncio
    async def test_load_status(self, tmp_path):
        """Test loading job status from file"""
        job_dir = tmp_path / "test_job"
        job_dir.mkdir()
        
        # Create status file
        status_data = {
            "status": JobStatusEnum.SETUP.value,
            "model": "claude-opus-4",
            "disallowedTools": "WebSearch"
        }
        status_file = job_dir / "status.json"
        status_file.write_text(json.dumps(status_data))
        
        executor = JobExecutor(job_dir)
        loaded_status = await executor._load_status()
        
        assert loaded_status == status_data
    
    @pytest.mark.asyncio
    async def test_load_status_error_handling(self, tmp_path):
        """Test status loading with missing/corrupt file"""
        job_dir = tmp_path / "test_job"
        job_dir.mkdir()
        
        executor = JobExecutor(job_dir)
        
        # Missing file should return error status
        status = await executor._load_status()
        assert status["status"] == JobStatusEnum.ERROR
        assert "Failed to load status" in status["error"]
    
    @pytest.mark.asyncio
    async def test_update_status(self, tmp_path):
        """Test status update functionality"""
        job_dir = tmp_path / "test_job"
        job_dir.mkdir()
        
        # Create initial status
        initial_status = {"status": JobStatusEnum.SETUP.value, "model": "claude-opus-4"}
        status_file = job_dir / "status.json"
        status_file.write_text(json.dumps(initial_status))
        
        executor = JobExecutor(job_dir)
        
        # Update status
        await executor._update_status(JobStatusEnum.RUNNING, startedAt="2024-01-01T00:00:00Z")
        
        # Verify update
        with open(status_file) as f:
            updated = json.load(f)
        
        assert updated["status"] == JobStatusEnum.RUNNING.value
        assert updated["startedAt"] == "2024-01-01T00:00:00Z"
        assert updated["model"] == "claude-opus-4"  # Original field preserved
    
    @pytest.mark.asyncio
    async def test_stream_output(self, tmp_path):
        """Test log streaming from process output"""
        job_dir = tmp_path / "test_job"
        job_dir.mkdir()
        
        executor = JobExecutor(job_dir)
        
        # Mock process with stdout
        mock_process = Mock()
        mock_stdout = AsyncMock()
        
        # Simulate JSON output lines
        output_lines = [
            b'{"type": "message", "content": "Starting analysis..."}\n',
            b'{"type": "message", "content": "Working on problem..."}\n',
            b''  # EOF
        ]
        mock_stdout.readline.side_effect = output_lines
        mock_process.stdout = mock_stdout
        
        executor.process = mock_process
        
        # Stream output
        await executor._stream_output()
        
        # Verify log file created with correct content
        log_file = job_dir / "log.jsonl"
        assert log_file.exists()
        
        lines = log_file.read_text().strip().split('\n')
        assert len(lines) == 2
        
        log1 = json.loads(lines[0])
        assert log1["type"] == "message"
        assert log1["content"] == "Starting analysis..."
        
        log2 = json.loads(lines[1])
        assert log2["type"] == "message"
        assert log2["content"] == "Working on problem..."
    
    @pytest.mark.asyncio
    async def test_stream_output_handles_invalid_json(self, tmp_path):
        """Test log streaming handles non-JSON output"""
        job_dir = tmp_path / "test_job"
        job_dir.mkdir()
        
        executor = JobExecutor(job_dir)
        
        # Mock process with invalid JSON output
        mock_process = Mock()
        mock_stdout = AsyncMock()
        
        output_lines = [
            b'This is not JSON\n',
            b'{"valid": "json"}\n',
            b''  # EOF
        ]
        mock_stdout.readline.side_effect = output_lines
        mock_process.stdout = mock_stdout
        
        executor.process = mock_process
        
        # Stream output
        await executor._stream_output()
        
        # Verify both lines logged appropriately
        log_file = job_dir / "log.jsonl"
        lines = log_file.read_text().strip().split('\n')
        assert len(lines) == 2
        
        # First line should be wrapped as system message
        log1 = json.loads(lines[0])
        assert log1["type"] == "system"
        assert log1["content"] == "This is not JSON"
        
        # Second line should be parsed normally
        log2 = json.loads(lines[1])
        assert log2["valid"] == "json"
    
    @pytest.mark.asyncio
    async def test_execute_success_flow(self, tmp_path):
        """Test successful job execution flow"""
        job_dir = tmp_path / "test_job"
        job_dir.mkdir()
        workspace_dir = job_dir / "workspace"
        workspace_dir.mkdir()
        
        # Create initial status
        status_file = job_dir / "status.json"
        status_file.write_text(json.dumps({
            "status": "setup",
            "model": "claude-opus-4"
        }))
        
        executor = JobExecutor(job_dir)
        
        # Mock subprocess execution
        with patch('asyncio.create_subprocess_exec') as mock_create_subprocess:
            # Create mock process
            mock_process = AsyncMock()
            mock_process.wait.return_value = 0  # Success
            mock_process.stdout = AsyncMock()
            mock_process.stdout.readline.return_value = b''  # EOF immediately
            
            mock_create_subprocess.return_value = mock_process
            
            # Execute
            await executor.execute()
            
            # Verify command was built correctly
            mock_create_subprocess.assert_called_once()
            cmd = mock_create_subprocess.call_args[0]
            assert cmd[0] == "claude"
            assert "--model" in cmd
            assert "claude-opus-4" in cmd
            
            # Verify status updated to completed
            final_status = json.loads(status_file.read_text())
            assert final_status["status"] == "completed"
            assert "completedAt" in final_status
    
    @pytest.mark.asyncio  
    async def test_execute_error_flow(self, tmp_path):
        """Test job execution error handling"""
        job_dir = tmp_path / "test_job"
        job_dir.mkdir()
        workspace_dir = job_dir / "workspace"
        workspace_dir.mkdir()
        
        # Create initial status
        status_file = job_dir / "status.json"
        status_file.write_text(json.dumps({
            "status": "setup",
            "model": "claude-opus-4"
        }))
        
        executor = JobExecutor(job_dir)
        
        # Mock subprocess execution with error
        with patch('asyncio.create_subprocess_exec') as mock_create_subprocess:
            # Create mock process that fails
            mock_process = AsyncMock()
            mock_process.wait.return_value = 1  # Error code
            mock_process.stdout = AsyncMock()
            mock_process.stdout.readline.return_value = b''  # EOF
            
            mock_create_subprocess.return_value = mock_process
            
            # Execute
            await executor.execute()
            
            # Verify status updated to error
            final_status = json.loads(status_file.read_text())
            assert final_status["status"] == "error"
            assert "Process exited with code 1" in final_status["error"]
            assert "completedAt" in final_status
    
    @pytest.mark.asyncio
    async def test_cancel_running_job(self, tmp_path):
        """Test job cancellation"""
        job_dir = tmp_path / "test_job"
        job_dir.mkdir()
        
        executor = JobExecutor(job_dir)
        
        # Mock running process
        mock_process = Mock()
        mock_process.returncode = None  # Still running
        mock_process.terminate = Mock()
        mock_process.wait = AsyncMock()
        
        executor.process = mock_process
        
        # Cancel
        await executor.cancel()
        
        # Verify process was terminated
        mock_process.terminate.assert_called_once()
        mock_process.wait.assert_called_once()