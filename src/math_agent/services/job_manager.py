"""
Job queue management for the math agent system.

This module manages the job queue, handles concurrent execution,
and coordinates job lifecycle.
"""

import asyncio
import json
import logging
from pathlib import Path
from typing import Dict
from contextlib import suppress

from .job_executor import JobExecutor
from ..core.models import JobStatusEnum
from ..config import JOB_SCAN_INTERVAL, MAX_CONCURRENT_JOBS

logger = logging.getLogger(__name__)


class JobManager:
    """Manages job execution queue and lifecycle"""
    
    def __init__(self, jobs_dir: Path, max_concurrent_jobs: int = MAX_CONCURRENT_JOBS):
        self.jobs_dir = jobs_dir
        self.max_concurrent_jobs = max_concurrent_jobs
        self.running_jobs: Dict[str, asyncio.Task] = {}
        self.job_queue: asyncio.Queue = asyncio.Queue()
        self.executors: Dict[str, JobExecutor] = {}
        self._running = False
        self._workers = []
        
    async def start(self):
        """Start the job manager"""
        self._running = True
        
        # Start worker tasks
        for i in range(self.max_concurrent_jobs):
            worker = asyncio.create_task(self._worker(i))
            self._workers.append(worker)
            
        # Start job scanner
        asyncio.create_task(self._scan_for_jobs())
        
        logger.info(f"Job manager started with {self.max_concurrent_jobs} workers")
        
    async def stop(self):
        """Stop the job manager"""
        self._running = False
        
        # Cancel all running jobs
        for job_name, task in self.running_jobs.items():
            task.cancel()
            with suppress(asyncio.CancelledError):
                await task
                
        # Stop workers
        for worker in self._workers:
            worker.cancel()
            with suppress(asyncio.CancelledError):
                await worker
                
        logger.info("Job manager stopped")
        
    async def submit_job(self, job_name: str):
        """Submit a job for execution"""
        await self.job_queue.put(job_name)
        logger.info(f"Job {job_name} submitted to queue")
        
    async def cancel_job(self, job_name: str) -> bool:
        """Cancel a running job"""
        if job_name in self.running_jobs:
            task = self.running_jobs[job_name]
            task.cancel()
            
            # Wait for cancellation
            with suppress(asyncio.CancelledError):
                await task
                
            # Also cancel the executor
            if job_name in self.executors:
                await self.executors[job_name].cancel()
                
            logger.info(f"Job {job_name} cancelled")
            return True
        return False
        
    async def _worker(self, worker_id: int):
        """Worker task that processes jobs from the queue"""
        logger.info(f"Worker {worker_id} started")
        
        while self._running:
            try:
                # Get job from queue with timeout
                job_name = await asyncio.wait_for(
                    self.job_queue.get(),
                    timeout=1.0
                )
                
                logger.info(f"Worker {worker_id} processing job {job_name}")
                
                # Create executor
                job_dir = self.jobs_dir / job_name
                executor = JobExecutor(job_dir)
                self.executors[job_name] = executor
                
                # Create task
                task = asyncio.create_task(executor.execute())
                self.running_jobs[job_name] = task
                
                try:
                    # Wait for completion
                    await task
                    logger.info(f"Job {job_name} completed")
                except asyncio.CancelledError:
                    logger.info(f"Job {job_name} was cancelled")
                    raise
                except Exception as e:
                    logger.error(f"Job {job_name} failed: {e}")
                finally:
                    # Cleanup
                    self.running_jobs.pop(job_name, None)
                    self.executors.pop(job_name, None)
                    
            except asyncio.TimeoutError:
                # No jobs in queue, continue
                continue
            except asyncio.CancelledError:
                # Worker is being stopped
                break
            except Exception as e:
                logger.exception(f"Worker {worker_id} error: {e}")
                await asyncio.sleep(1)  # Prevent tight loop on errors
                
        logger.info(f"Worker {worker_id} stopped")
        
    async def _scan_for_jobs(self):
        """Periodically scan for jobs in setup state"""
        while self._running:
            try:
                # Check all job directories
                if self.jobs_dir.exists():
                    for job_dir in self.jobs_dir.iterdir():
                        if not job_dir.is_dir():
                            continue
                            
                        job_name = job_dir.name
                        
                        # Skip if already running
                        if job_name in self.running_jobs:
                            continue
                            
                        # Check status
                        status_file = job_dir / "status.json"
                        if status_file.exists():
                            try:
                                with open(status_file, 'r') as f:
                                    status = json.load(f)
                                    
                                if status.get("status") == JobStatusEnum.SETUP.value:
                                    # Submit for execution
                                    await self.submit_job(job_name)
                            except (FileNotFoundError, json.JSONDecodeError) as e:
                                logger.error(f"Failed to read status for {job_name}: {e}")
                                # Skip this job and continue with others
                                
            except Exception as e:
                logger.exception(f"Job scanner error: {e}")
                
            # Wait before next scan
            await asyncio.sleep(JOB_SCAN_INTERVAL)
            
    def get_queue_size(self) -> int:
        """Get number of jobs in queue"""
        return self.job_queue.qsize()
        
    def get_running_jobs(self) -> list:
        """Get list of currently running jobs"""
        return list(self.running_jobs.keys())