"""
Tests for the JobExecutor class - the core job execution logic.
"""
import asyncio
import json
from pathlib import Path
from unittest.mock import AsyncMock, patch, MagicMock, call

import pytest
from freezegun import freeze_time

from src.backend.job import JobExecutor
from tests.utils import (
    create_job_status,
    create_log_entry,
    write_job_files,
    read_job_status,
    read_job_log,
    assert_status_valid,
    create_sample_solution
)


class TestJobExecutor:
    """Test JobExecutor functionality."""
    
    async def test_execute_claude_success(self, job_executor, temp_job_dir, mock_subprocess):
        """Test successful Claude job execution."""
        # Setup initial job status
        write_job_files(
            temp_job_dir,
            status=create_job_status(model="claude-opus-4"),
            workspace_files={"prompt.md": "Solve this problem"}
        )
        
        # Mock subprocess creation
        mock_subprocess.stdout.readline = AsyncMock(side_effect=[
            b'{"type": "message", "content": "Starting solution..."}\n',
            b'{"type": "tool_use", "name": "Write", "params": {"file_path": "solution.tex"}}\n',
            b'{"type": "message", "content": "Done"}\n',
            b''  # EOF
        ])
        
        with patch('asyncio.create_subprocess_exec', return_value=mock_subprocess):
            await job_executor.execute()
        
        # Verify status updates
        status = read_job_status(temp_job_dir)
        assert status["status"] == "completed"
        assert "startedAt" in status
        assert "completedAt" in status
        assert_status_valid(status)
        
        # Verify log entries
        log = read_job_log(temp_job_dir)
        assert len(log) == 3
        assert log[0]["type"] == "message"
        assert log[0]["content"] == "Starting solution..."
    
    async def test_execute_gemini_success(self, job_executor, temp_job_dir, mock_subprocess):
        """Test successful Gemini job execution."""
        # Setup initial job status
        write_job_files(
            temp_job_dir,
            status=create_job_status(model="gemini-2.5-pro"),
            workspace_files={"prompt.md": "Solve this problem"}
        )
        
        # Mock subprocess
        mock_subprocess.stdout.readline = AsyncMock(side_effect=[b''])
        
        with patch('asyncio.create_subprocess_exec', return_value=mock_subprocess) as mock_exec:
            await job_executor.execute()
            
            # Verify gemini command was used
            mock_exec.assert_called_once()
            args = mock_exec.call_args[0]
            assert args[0] == "gemini"
            assert "--model" in args
            assert "gemini-2.5-pro" in args
    
    async def test_execute_with_disallowed_tools(self, job_executor, temp_job_dir, mock_subprocess):
        """Test execution with disallowed tools parameter."""
        # Setup job with disallowed tools
        write_job_files(
            temp_job_dir,
            status=create_job_status(disallowedTools="Bash(git:*),WebSearch"),
            workspace_files={"prompt.md": "Solve this"}
        )
        
        mock_subprocess.stdout.readline = AsyncMock(return_value=b'')
        
        with patch('asyncio.create_subprocess_exec', return_value=mock_subprocess) as mock_exec:
            await job_executor.execute()
            
            # Verify disallowedTools was passed
            args = mock_exec.call_args[0]
            assert "--disallowedTools" in args
            assert "Bash(git:*),WebSearch" in args
    
    async def test_execute_process_failure(self, job_executor, temp_job_dir, mock_subprocess):
        """Test handling of process failure."""
        write_job_files(
            temp_job_dir,
            status=create_job_status(),
            workspace_files={"prompt.md": "Solve this"}
        )
        
        # Mock process failure
        mock_subprocess.wait = AsyncMock(return_value=1)
        mock_subprocess.stdout.readline = AsyncMock(return_value=b'')
        
        with patch('asyncio.create_subprocess_exec', return_value=mock_subprocess):
            await job_executor.execute()
        
        # Verify error status
        status = read_job_status(temp_job_dir)
        assert status["status"] == "error"
        assert status["error"] == "Process exited with code 1"
        assert "completedAt" in status
    
    async def test_execute_exception_handling(self, job_executor, temp_job_dir):
        """Test exception handling during execution."""
        write_job_files(
            temp_job_dir,
            status=create_job_status(),
            workspace_files={"prompt.md": "Solve this"}
        )
        
        # Mock subprocess creation to raise exception
        with patch('asyncio.create_subprocess_exec', side_effect=OSError("Command not found")):
            await job_executor.execute()
        
        # Verify error status
        status = read_job_status(temp_job_dir)
        assert status["status"] == "error"
        assert "Command not found" in status["error"]
    
    async def test_cancel_running_job(self, job_executor, temp_job_dir, mock_subprocess):
        """Test cancelling a running job."""
        write_job_files(
            temp_job_dir,
            status=create_job_status(),
            workspace_files={"prompt.md": "Solve this"}
        )
        
        # Mock long-running process
        mock_subprocess.stdout.readline = AsyncMock(side_effect=asyncio.CancelledError)
        mock_subprocess.terminate = MagicMock()
        
        with patch('asyncio.create_subprocess_exec', return_value=mock_subprocess):
            with pytest.raises(asyncio.CancelledError):
                await job_executor.execute()
        
        # Verify process was terminated
        mock_subprocess.terminate.assert_called_once()
        mock_subprocess.wait.assert_called()
        
        # Verify cancelled status
        status = read_job_status(temp_job_dir)
        assert status["status"] == "cancelled"
    
    async def test_cancel_no_process(self, job_executor):
        """Test cancelling when no process is running."""
        # Should not raise exception
        await job_executor.cancel()
    
    async def test_cancel_already_finished(self, job_executor, mock_subprocess):
        """Test cancelling an already finished process."""
        mock_subprocess.returncode = 0
        job_executor.process = mock_subprocess
        
        # Should not call terminate
        await job_executor.cancel()
        mock_subprocess.terminate.assert_not_called()
    
    async def test_stream_json_output(self, job_executor, temp_job_dir, mock_subprocess):
        """Test streaming JSON output to log file."""
        write_job_files(temp_job_dir, status=create_job_status())
        
        # Mock JSON output
        outputs = [
            b'{"type": "message", "content": "Hello"}\n',
            b'{"type": "tool_use", "name": "Test"}\n',
            b''  # EOF
        ]
        mock_subprocess.stdout.readline = AsyncMock(side_effect=outputs)
        job_executor.process = mock_subprocess
        
        await job_executor._stream_output()
        
        # Verify log entries
        log = read_job_log(temp_job_dir)
        assert len(log) == 2
        assert log[0]["type"] == "message"
        assert log[0]["content"] == "Hello"
        assert log[1]["type"] == "tool_use"
    
    async def test_stream_invalid_json(self, job_executor, temp_job_dir, mock_subprocess):
        """Test handling of invalid JSON in output stream."""
        write_job_files(temp_job_dir, status=create_job_status())
        
        # Mock invalid JSON
        outputs = [
            b'Invalid JSON\n',
            b'{"valid": "json"}\n',
            b''
        ]
        mock_subprocess.stdout.readline = AsyncMock(side_effect=outputs)
        job_executor.process = mock_subprocess
        
        await job_executor._stream_output()
        
        # Verify both entries were logged
        log = read_job_log(temp_job_dir)
        assert len(log) == 2
        assert log[0]["type"] == "system"
        assert "Invalid JSON" in log[0]["content"]
        assert log[1]["valid"] == "json"
    
    async def test_compile_pdf_success(self, job_executor, temp_job_dir):
        """Test successful PDF compilation."""
        # Create solution.tex
        (temp_job_dir / "workspace" / "solution.tex").write_text(create_sample_solution())
        
        # Mock pdflatex
        mock_result = AsyncMock()
        mock_result.returncode = 0
        mock_result.communicate = AsyncMock(return_value=(b"Success", b""))
        
        with patch('asyncio.create_subprocess_exec', return_value=mock_result) as mock_exec:
            # Create fake PDF file
            def create_pdf(*args, **kwargs):
                if "pdflatex" in args:
                    (temp_job_dir / "workspace" / "solution.pdf").touch()
                return mock_result
            
            mock_exec.side_effect = create_pdf
            
            result = await job_executor._compile_pdf()
            
        assert result is True
        # Verify pdflatex was called twice (for references)
        assert mock_exec.call_count == 2
    
    async def test_compile_pdf_failure(self, job_executor, temp_job_dir):
        """Test PDF compilation failure."""
        (temp_job_dir / "workspace" / "solution.tex").write_text("\\invalid{latex}")
        
        # Mock failed pdflatex
        mock_result = AsyncMock()
        mock_result.returncode = 1
        mock_result.communicate = AsyncMock(return_value=(b"", b"Error: Undefined control sequence"))
        
        with patch('asyncio.create_subprocess_exec', return_value=mock_result):
            result = await job_executor._compile_pdf()
        
        assert result is False
        
        # Verify error was logged
        log = read_job_log(temp_job_dir)
        assert any("LaTeX compilation failed" in entry.get("content", "") for entry in log)
    
    async def test_compile_pdf_exception(self, job_executor, temp_job_dir):
        """Test PDF compilation with exception."""
        with patch('asyncio.create_subprocess_exec', side_effect=FileNotFoundError("pdflatex not found")):
            result = await job_executor._compile_pdf()
        
        assert result is False
    
    @freeze_time("2024-01-01T12:00:00Z")
    async def test_solution_file_tracking(self, job_executor, temp_job_dir, mock_subprocess):
        """Test tracking of solution file creation."""
        write_job_files(
            temp_job_dir,
            status=create_job_status(),
            workspace_files={"prompt.md": "Solve this"}
        )
        
        # Create solution files during execution
        def create_solution_files(*args, **kwargs):
            (temp_job_dir / "workspace" / "solution.tex").write_text(create_sample_solution())
            (temp_job_dir / "workspace" / "solution.pdf").touch()
            return mock_subprocess
        
        mock_subprocess.stdout.readline = AsyncMock(return_value=b'')
        
        with patch('asyncio.create_subprocess_exec', side_effect=create_solution_files):
            await job_executor.execute()
        
        # Verify solution tracking
        status = read_job_status(temp_job_dir)
        assert status["solutionTexCreated"] is True
        assert status["solutionPdfCreated"] is True
    
    async def test_auto_pdf_compilation(self, job_executor, temp_job_dir, mock_subprocess):
        """Test automatic PDF compilation when tex exists but pdf doesn't."""
        write_job_files(
            temp_job_dir,
            status=create_job_status(),
            workspace_files={
                "prompt.md": "Solve this",
                "solution.tex": create_sample_solution()
            }
        )
        
        mock_subprocess.stdout.readline = AsyncMock(return_value=b'')
        
        # Mock PDF compilation
        pdf_mock = AsyncMock()
        pdf_mock.returncode = 0
        pdf_mock.communicate = AsyncMock(return_value=(b"", b""))
        
        exec_count = 0
        def mock_exec(*args, **kwargs):
            nonlocal exec_count
            exec_count += 1
            if args[0] == "pdflatex":
                # Create PDF on second pdflatex call
                if exec_count == 3:
                    (temp_job_dir / "workspace" / "solution.pdf").touch()
                return pdf_mock
            return mock_subprocess
        
        with patch('asyncio.create_subprocess_exec', side_effect=mock_exec):
            await job_executor.execute()
        
        # Verify PDF was created
        status = read_job_status(temp_job_dir)
        assert status["solutionPdfCreated"] is True
    
    async def test_command_construction(self, job_executor, temp_job_dir, mock_subprocess):
        """Test correct command construction for different configurations."""
        test_cases = [
            # (model, disallowed_tools, expected_cmd_start)
            ("claude-opus-4", "", ["claude"]),
            ("claude-sonnet-4", "Bash", ["claude"]),
            ("gemini-2.5-pro", "", ["gemini"]),
            ("gemini-2.5-flash", "WebSearch,Bash", ["gemini"]),
        ]
        
        mock_subprocess.stdout.readline = AsyncMock(return_value=b'')
        
        for model, tools, expected_start in test_cases:
            write_job_files(
                temp_job_dir,
                status=create_job_status(model=model, disallowedTools=tools),
                workspace_files={"prompt.md": "Test"}
            )
            
            with patch('asyncio.create_subprocess_exec', return_value=mock_subprocess) as mock_exec:
                await job_executor.execute()
                
                args = mock_exec.call_args[0]
                assert args[0] == expected_start[0]
                assert "--model" in args
                assert model in args
                
                if tools:
                    assert "--disallowedTools" in args
                    assert tools in args


@pytest.fixture
def mock_freezegun():
    """Provide freezegun for time mocking."""
    import freezegun
    return freezegun