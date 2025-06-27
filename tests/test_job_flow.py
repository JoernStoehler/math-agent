"""
Integration tests for full job lifecycle.
"""
import asyncio
import json
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock

import pytest
from freezegun import freeze_time

from src.backend.job import JobExecutor
from src.backend.job_manager import JobManager
from src.backend.server import app
from tests.utils import (
    create_job_status,
    write_job_files,
    read_job_status,
    read_job_log,
    create_sample_exercise,
    create_sample_solution,
    create_log_entry
)


class TestJobLifecycle:
    """Test complete job lifecycle from creation to completion."""
    
    @pytest.mark.asyncio
    async def test_full_job_success_flow(self, temp_data_dir):
        """Test successful job from creation to completion."""
        jobs_dir = temp_data_dir / "jobs"
        
        # Setup exercise
        exercises_dir = temp_data_dir / "exercises"
        course_dir = exercises_dir / "test_course"
        course_dir.mkdir(parents=True)
        (course_dir / "problem.tex").write_text(create_sample_exercise())
        
        # Create job manager
        manager = JobManager(jobs_dir, max_concurrent_jobs=1)
        
        # Mock subprocess for Claude
        mock_process = AsyncMock()
        mock_process.returncode = 0
        mock_process.wait = AsyncMock(return_value=0)
        
        # Simulate Claude output
        outputs = [
            b'{"type": "message", "content": "Analyzing the problem..."}\n',
            b'{"type": "message", "content": "I need to prove that 1 + 1 = 2"}\n',
            b'{"type": "tool_use", "name": "Write", "params": {"file_path": "solution.tex", "content": "' + 
            create_sample_solution().encode() + b'"}}\n',
            b'{"type": "message", "content": "Solution written to solution.tex"}\n',
            b''  # EOF
        ]
        mock_process.stdout.readline = AsyncMock(side_effect=outputs)
        
        with patch('asyncio.create_subprocess_exec', return_value=mock_process):
            # Start manager
            await manager.start()
            
            # Create job directory manually (normally done by API)
            job_name = "test-job"
            job_dir = jobs_dir / job_name
            job_dir.mkdir(parents=True)
            workspace = job_dir / "workspace"
            workspace.mkdir()
            
            # Setup job files
            (workspace / "prompt.md").write_text("Solve the math problem")
            (workspace / "problem.tex").write_text(create_sample_exercise())
            
            # Create initial status
            status = {
                "status": "setup",
                "createdAt": "2024-01-01T00:00:00Z",
                "model": "claude-opus-4",
                "exercise": "test_course/problem",
                "disallowedTools": ""
            }
            (job_dir / "status.json").write_text(json.dumps(status))
            (job_dir / "log.jsonl").touch()
            
            # Add job to queue
            await manager.submit_job(job_name)
            
            # Wait for job to complete
            await asyncio.sleep(0.2)
            
            # Verify final status
            final_status = read_job_status(job_dir)
            assert final_status["status"] == "completed"
            assert "startedAt" in final_status
            assert "completedAt" in final_status
            assert final_status["solutionTexCreated"] is True
            
            # Verify log entries
            log = read_job_log(job_dir)
            assert len(log) >= 3
            assert any(entry["type"] == "message" for entry in log)
            assert any(entry["type"] == "tool_use" for entry in log)
            
            await manager.stop()
    
    @pytest.mark.asyncio
    async def test_job_failure_flow(self, temp_data_dir):
        """Test job failure handling."""
        jobs_dir = temp_data_dir / "jobs"
        manager = JobManager(jobs_dir, max_concurrent_jobs=1)
        
        # Mock subprocess to fail
        mock_process = AsyncMock()
        mock_process.returncode = 1
        mock_process.wait = AsyncMock(return_value=1)
        mock_process.stdout.readline = AsyncMock(return_value=b'')
        
        with patch('asyncio.create_subprocess_exec', return_value=mock_process):
            await manager.start()
            
            # Create failing job
            job_name = "failing-job"
            job_dir = jobs_dir / job_name
            write_job_files(
                job_dir,
                status=create_job_status("setup"),
                workspace_files={"prompt.md": "Test"}
            )
            
            await manager.submit_job(job_name)
            await asyncio.sleep(0.1)
            
            # Verify error status
            status = read_job_status(job_dir)
            assert status["status"] == "error"
            assert "Process exited with code 1" in status["error"]
            
            await manager.stop()
    
    @pytest.mark.asyncio
    async def test_job_cancellation_flow(self, temp_data_dir):
        """Test job cancellation during execution."""
        jobs_dir = temp_data_dir / "jobs"
        manager = JobManager(jobs_dir, max_concurrent_jobs=1)
        
        # Mock long-running subprocess
        mock_process = AsyncMock()
        mock_process.returncode = None
        mock_process.terminate = MagicMock()
        mock_process.wait = AsyncMock()
        
        execution_started = asyncio.Event()
        
        async def slow_readline():
            execution_started.set()
            await asyncio.sleep(10)  # Simulate slow execution
            return b''
        
        mock_process.stdout.readline = slow_readline
        
        with patch('asyncio.create_subprocess_exec', return_value=mock_process):
            await manager.start()
            
            # Create job
            job_name = "cancel-job"
            job_dir = jobs_dir / job_name
            write_job_files(
                job_dir,
                status=create_job_status("setup"),
                workspace_files={"prompt.md": "Test"}
            )
            
            await manager.submit_job(job_name)
            
            # Wait for execution to start
            await execution_started.wait()
            
            # Cancel the job
            result = await manager.cancel_job(job_name)
            assert result is True
            
            # Wait a bit for cancellation to process
            await asyncio.sleep(0.1)
            
            # Verify process was terminated
            mock_process.terminate.assert_called()
            
            # Verify status
            status = read_job_status(job_dir)
            assert status["status"] == "cancelled"
            
            await manager.stop()
    
    @pytest.mark.asyncio
    async def test_pdf_compilation_flow(self, temp_data_dir):
        """Test automatic PDF compilation after solution.tex creation."""
        jobs_dir = temp_data_dir / "jobs"
        manager = JobManager(jobs_dir, max_concurrent_jobs=1)
        
        # Mock Claude process
        claude_process = AsyncMock()
        claude_process.returncode = 0
        claude_process.wait = AsyncMock(return_value=0)
        claude_process.stdout.readline = AsyncMock(return_value=b'')
        
        # Mock pdflatex process
        pdf_process = AsyncMock()
        pdf_process.returncode = 0
        pdf_process.communicate = AsyncMock(return_value=(b"Success", b""))
        
        exec_count = 0
        
        def mock_subprocess(*args, **kwargs):
            nonlocal exec_count
            exec_count += 1
            
            if args[0] == "claude":
                # Create solution.tex during execution
                job_dir = jobs_dir / "pdf-job"
                (job_dir / "workspace" / "solution.tex").write_text(create_sample_solution())
                return claude_process
            elif args[0] == "pdflatex":
                # Create PDF on second call
                if exec_count == 3:  # Second pdflatex call
                    job_dir = jobs_dir / "pdf-job"
                    (job_dir / "workspace" / "solution.pdf").touch()
                return pdf_process
            
            return claude_process
        
        with patch('asyncio.create_subprocess_exec', side_effect=mock_subprocess):
            await manager.start()
            
            # Create job
            job_name = "pdf-job"
            job_dir = jobs_dir / job_name
            write_job_files(
                job_dir,
                status=create_job_status("setup"),
                workspace_files={"prompt.md": "Test"}
            )
            
            await manager.submit_job(job_name)
            await asyncio.sleep(0.2)
            
            # Verify PDF was created
            status = read_job_status(job_dir)
            assert status["status"] == "completed"
            assert status["solutionTexCreated"] is True
            assert status["solutionPdfCreated"] is True
            assert (job_dir / "workspace" / "solution.pdf").exists()
            
            await manager.stop()
    
    @pytest.mark.asyncio
    async def test_concurrent_jobs_flow(self, temp_data_dir):
        """Test multiple jobs running concurrently."""
        jobs_dir = temp_data_dir / "jobs"
        manager = JobManager(jobs_dir, max_concurrent_jobs=3)
        
        # Track job execution
        executing_jobs = []
        completed_jobs = []
        
        async def mock_execute(self):
            job_name = self.job_dir.name
            executing_jobs.append(job_name)
            await asyncio.sleep(0.1)  # Simulate work
            completed_jobs.append(job_name)
        
        with patch.object(JobExecutor, 'execute', mock_execute):
            await manager.start()
            
            # Create and queue multiple jobs
            job_names = [f"job-{i}" for i in range(5)]
            for job_name in job_names:
                job_dir = jobs_dir / job_name
                write_job_files(
                    job_dir,
                    status=create_job_status("setup"),
                    workspace_files={"prompt.md": f"Test {job_name}"}
                )
                await manager.submit_job(job_name)
            
            # Wait for initial jobs to start
            await asyncio.sleep(0.05)
            
            # Should have 3 jobs running (max concurrent)
            assert len(manager.running_jobs) <= 3
            
            # Wait for all jobs to complete
            await asyncio.sleep(0.3)
            
            # All jobs should be completed
            assert len(completed_jobs) == 5
            assert set(completed_jobs) == set(job_names)
            assert len(manager.running_jobs) == 0
            
            await manager.stop()
    
    @pytest.mark.asyncio
    @freeze_time("2024-01-01T12:00:00Z")
    async def test_job_with_gemini_model(self, temp_data_dir):
        """Test job execution with Gemini model."""
        jobs_dir = temp_data_dir / "jobs"
        manager = JobManager(jobs_dir, max_concurrent_jobs=1)
        
        # Mock Gemini process
        mock_process = AsyncMock()
        mock_process.returncode = 0
        mock_process.wait = AsyncMock(return_value=0)
        mock_process.stdout.readline = AsyncMock(side_effect=[
            b'{"type": "message", "content": "Using Gemini to solve"}\n',
            b''
        ])
        
        with patch('asyncio.create_subprocess_exec', return_value=mock_process) as mock_exec:
            await manager.start()
            
            # Create Gemini job
            job_name = "gemini-job"
            job_dir = jobs_dir / job_name
            write_job_files(
                job_dir,
                status=create_job_status("setup", model="gemini-2.5-pro"),
                workspace_files={"prompt.md": "Test"}
            )
            
            await manager.submit_job(job_name)
            await asyncio.sleep(0.1)
            
            # Verify Gemini was called
            mock_exec.assert_called()
            args = mock_exec.call_args[0]
            assert args[0] == "gemini"
            assert "--model" in args
            assert "gemini-2.5-pro" in args
            
            await manager.stop()
    
    @pytest.mark.asyncio
    async def test_job_with_disallowed_tools(self, temp_data_dir):
        """Test job execution with disallowed tools."""
        jobs_dir = temp_data_dir / "jobs"
        manager = JobManager(jobs_dir, max_concurrent_jobs=1)
        
        mock_process = AsyncMock()
        mock_process.returncode = 0
        mock_process.wait = AsyncMock(return_value=0)
        mock_process.stdout.readline = AsyncMock(return_value=b'')
        
        with patch('asyncio.create_subprocess_exec', return_value=mock_process) as mock_exec:
            await manager.start()
            
            # Create job with disallowed tools
            job_name = "restricted-job"
            job_dir = jobs_dir / job_name
            write_job_files(
                job_dir,
                status=create_job_status("setup", disallowedTools="Bash(git:*),WebSearch"),
                workspace_files={"prompt.md": "Test"}
            )
            
            await manager.submit_job(job_name)
            await asyncio.sleep(0.1)
            
            # Verify disallowed tools were passed
            args = mock_exec.call_args[0]
            assert "--disallowedTools" in args
            assert "Bash(git:*),WebSearch" in args
            
            await manager.stop()
    
    @pytest.mark.asyncio
    async def test_job_recovery_after_crash(self, temp_data_dir):
        """Test job recovery after system restart."""
        jobs_dir = temp_data_dir / "jobs"
        
        # Create jobs in various states
        write_job_files(
            jobs_dir / "setup-job",
            status=create_job_status("setup")
        )
        write_job_files(
            jobs_dir / "running-job",
            status=create_job_status("running", startedAt="2024-01-01T00:01:00Z")
        )
        write_job_files(
            jobs_dir / "completed-job",
            status=create_job_status("completed", completedAt="2024-01-01T00:02:00Z")
        )
        
        # Start manager (simulating restart)
        manager = JobManager(jobs_dir, max_concurrent_jobs=2)
        
        # Track which jobs get executed
        executed_jobs = []
        
        async def track_execution(self):
            executed_jobs.append(self.job_dir.name)
        
        with patch.object(JobExecutor, 'execute', track_execution):
            await manager.start()
            
            # Wait for scan to process
            await asyncio.sleep(0.2)
            
            # Only setup job should be re-queued
            assert "setup-job" in executed_jobs
            assert "running-job" not in executed_jobs  # Left in running state
            assert "completed-job" not in executed_jobs
            
            await manager.stop()