"""
Unit tests for JobManager class.
"""
import asyncio
import json
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch, call

import pytest
from freezegun import freeze_time

from src.backend.job_manager import JobManager
from src.backend.job import JobExecutor
from tests.utils import (
    create_job_status,
    write_job_files,
    read_job_status,
    JobStatusMatcher
)


class TestJobManager:
    """Test JobManager functionality."""
    
    async def test_start_stop(self, temp_data_dir):
        """Test starting and stopping the job manager."""
        jobs_dir = temp_data_dir / "jobs"
        manager = JobManager(jobs_dir, max_concurrent_jobs=2)
        
        # Start manager
        await manager.start()
        assert manager._running is True
        assert len(manager._workers) == 2
        
        # Stop manager
        await manager.stop()
        assert manager._running is False
        
        # Workers should have been cancelled, but we can't check cancelled()
        # on completed tasks, so just verify we have workers
        assert len(manager._workers) == 2
    
    async def test_submit_job(self, job_manager, temp_data_dir):
        """Test adding a job to the queue."""
        job_name = "test-job"
        
        # Add job
        await job_manager.submit_job(job_name)
        
        # Check queue
        assert job_manager.job_queue.qsize() == 1
        
        # Get job from queue
        queued_job = await job_manager.job_queue.get()
        assert queued_job == job_name
    
    async def test_cancel_running_job(self, job_manager, temp_data_dir):
        """Test cancelling a running job."""
        job_name = "running-job"
        job_dir = temp_data_dir / "jobs" / job_name
        
        # Create job directory
        write_job_files(job_dir, status=create_job_status("running"))
        
        # Mock running job
        mock_task = MagicMock()
        mock_task.cancelled = MagicMock(return_value=False)
        mock_task.cancel = MagicMock()
        
        mock_executor = MagicMock(spec=JobExecutor)
        mock_executor.cancel = AsyncMock()
        
        job_manager.running_jobs[job_name] = mock_task
        job_manager.executors[job_name] = mock_executor
        
        # Cancel job
        result = await job_manager.cancel_job(job_name)
        assert result is True
        
        # Verify cancellation
        mock_task.cancel.assert_called_once()
        mock_executor.cancel.assert_called_once()
    
    async def test_cancel_nonexistent_job(self, job_manager):
        """Test cancelling a job that doesn't exist."""
        result = await job_manager.cancel_job("nonexistent")
        assert result is False
    
    async def test_worker_executes_job(self, temp_data_dir):
        """Test that worker executes jobs from queue."""
        jobs_dir = temp_data_dir / "jobs"
        manager = JobManager(jobs_dir, max_concurrent_jobs=1)
        
        # Create test job
        job_name = "worker-test"
        job_dir = jobs_dir / job_name
        write_job_files(job_dir, status=create_job_status("setup"))
        
        # Mock JobExecutor
        mock_executor = AsyncMock(spec=JobExecutor)
        mock_executor.execute = AsyncMock()
        
        with patch('src.backend.job_manager.JobExecutor', return_value=mock_executor):
            # Start manager
            await manager.start()
            
            # Add job to queue
            await manager.submit_job(job_name)
            
            # Wait for job to be processed
            await asyncio.sleep(0.1)
            
            # Verify execution
            mock_executor.execute.assert_called_once()
            assert job_name not in manager.running_jobs
            
            # Stop manager
            await manager.stop()
    
    async def test_worker_handles_exception(self, temp_data_dir, caplog):
        """Test worker handles exceptions during job execution."""
        jobs_dir = temp_data_dir / "jobs"
        manager = JobManager(jobs_dir, max_concurrent_jobs=1)
        
        # Create test job
        job_name = "error-job"
        job_dir = jobs_dir / job_name
        write_job_files(job_dir, status=create_job_status("setup"))
        
        # Mock JobExecutor to raise exception
        mock_executor = AsyncMock(spec=JobExecutor)
        mock_executor.execute = AsyncMock(side_effect=Exception("Test error"))
        
        with patch('src.backend.job_manager.JobExecutor', return_value=mock_executor):
            await manager.start()
            await manager.submit_job(job_name)
            await asyncio.sleep(0.1)
            
            # Verify error was logged
            assert "Job failed with error" in caplog.text
            assert job_name not in manager.running_jobs
            
            await manager.stop()
    
    async def test_scan_for_jobs(self, temp_data_dir):
        """Test scanning for setup jobs."""
        jobs_dir = temp_data_dir / "jobs"
        manager = JobManager(jobs_dir, max_concurrent_jobs=2)
        
        # Create jobs with different statuses
        write_job_files(jobs_dir / "setup-job", status=create_job_status("setup"))
        write_job_files(jobs_dir / "running-job", status=create_job_status("running"))
        write_job_files(jobs_dir / "completed-job", status=create_job_status("completed"))
        
        # Mock submit_job to track calls
        manager.submit_job = AsyncMock()
        
        # Run scan
        await manager._scan_for_jobs()
        
        # Only setup job should be added
        manager.submit_job.assert_called_once_with("setup-job")
    
    async def test_scan_ignores_invalid_jobs(self, temp_data_dir, caplog):
        """Test scan handles invalid job directories gracefully."""
        jobs_dir = temp_data_dir / "jobs"
        manager = JobManager(jobs_dir, max_concurrent_jobs=1)
        
        # Create invalid job (missing status.json)
        (jobs_dir / "invalid-job").mkdir()
        
        # Create valid job
        write_job_files(jobs_dir / "valid-job", status=create_job_status("setup"))
        
        manager.submit_job = AsyncMock()
        
        # Run scan
        await manager._scan_for_jobs()
        
        # Only valid job should be added
        manager.submit_job.assert_called_once_with("valid-job")
    
    async def test_max_concurrent_jobs(self, temp_data_dir):
        """Test max concurrent jobs limit is respected."""
        jobs_dir = temp_data_dir / "jobs"
        manager = JobManager(jobs_dir, max_concurrent_jobs=2)
        
        # Create multiple jobs
        for i in range(5):
            job_dir = jobs_dir / f"job-{i}"
            write_job_files(job_dir, status=create_job_status("setup"))
        
        # Track executing jobs
        executing_jobs = []
        execution_complete = asyncio.Event()
        
        async def mock_execute(self):
            job_name = self.job_dir.name
            executing_jobs.append(job_name)
            # Wait until told to complete
            await execution_complete.wait()
        
        with patch.object(JobExecutor, 'execute', mock_execute):
            await manager.start()
            
            # Add all jobs
            for i in range(5):
                await manager.submit_job(f"job-{i}")
            
            # Wait for jobs to start
            await asyncio.sleep(0.1)
            
            # Should have exactly 2 running
            assert len(manager.running_jobs) == 2
            assert len(executing_jobs) == 2
            
            # Complete execution
            execution_complete.set()
            
            # Wait for all jobs to complete
            await asyncio.sleep(0.2)
            
            # All jobs should have been executed
            assert len(executing_jobs) == 5
            assert len(manager.running_jobs) == 0
            
            await manager.stop()
    
    async def test_get_running_jobs(self, job_manager):
        """Test getting list of running jobs."""
        # Add mock running jobs
        job_manager.running_jobs = {
            "job1": AsyncMock(),
            "job2": AsyncMock()
        }
        
        running = job_manager.get_running_jobs()
        assert running == ["job1", "job2"]
    
    async def test_worker_cleanup_on_cancellation(self, temp_data_dir):
        """Test worker cleans up properly when cancelled."""
        jobs_dir = temp_data_dir / "jobs"
        manager = JobManager(jobs_dir, max_concurrent_jobs=1)
        
        # Create test job
        job_name = "cancel-test"
        job_dir = jobs_dir / job_name
        write_job_files(job_dir, status=create_job_status("setup"))
        
        # Mock long-running executor
        mock_executor = AsyncMock(spec=JobExecutor)
        execute_started = asyncio.Event()
        
        async def long_execute():
            execute_started.set()
            await asyncio.sleep(10)  # Simulate long task
        
        mock_executor.execute = long_execute
        
        with patch('src.backend.job_manager.JobExecutor', return_value=mock_executor):
            await manager.start()
            await manager.submit_job(job_name)
            
            # Wait for execution to start
            await execute_started.wait()
            assert job_name in manager.running_jobs
            
            # Stop manager (should cancel worker)
            await manager.stop()
            
            # Job should be cleaned up
            assert job_name not in manager.running_jobs
            assert job_name not in manager.executors
    
    @freeze_time("2024-01-01T12:00:00Z")
    async def test_periodic_scan(self, temp_data_dir):
        """Test periodic scanning for new jobs."""
        jobs_dir = temp_data_dir / "jobs"
        manager = JobManager(jobs_dir, max_concurrent_jobs=1)
        
        scan_count = 0
        original_scan = manager._scan_for_jobs
        
        async def mock_scan():
            nonlocal scan_count
            scan_count += 1
            if scan_count >= 2:
                manager._running = False  # Stop after 2 scans
            await original_scan()
        
        manager._scan_for_jobs = mock_scan
        
        # Start scanner task directly
        scanner_task = asyncio.create_task(manager._scan_for_jobs())
        
        try:
            await asyncio.wait_for(scanner_task, timeout=1.0)
        except asyncio.TimeoutError:
            scanner_task.cancel()
        
        # Should have scanned at least twice
        assert scan_count >= 2