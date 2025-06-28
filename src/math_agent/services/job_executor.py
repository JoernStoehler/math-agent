"""
Job execution logic for the math agent system.

This module handles the actual execution of math problem-solving jobs,
including running the AI agent, managing output, and compiling LaTeX.
"""

import asyncio
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional, Dict, Any

import aiofiles

from ..core.utils import atomic_write_json
from ..core.models import JobStatusEnum
from ..config import PDFLATEX_COMMAND, PDFLATEX_ARGS, PDFLATEX_RUNS, MODEL_CLI_MAPPING, DEFAULT_CLI_TOOL

logger = logging.getLogger(__name__)


class JobExecutor:
    """Executes math agent jobs"""
    
    def __init__(self, job_dir: Path):
        self.job_dir = job_dir
        self.workspace_dir = job_dir / "workspace"
        self.status_file = job_dir / "status.json"
        self.log_file = job_dir / "log.jsonl"
        self.process: Optional[asyncio.subprocess.Process] = None
        
    async def execute(self):
        """Execute the job"""
        try:
            # Update status to running
            await self._update_status(JobStatusEnum.RUNNING, startedAt=datetime.now(timezone.utc).isoformat() + "Z")
            
            # Load job configuration
            status = await self._load_status()
            model = status.get("model", "claude-opus-4")
            disallowed_tools = status.get("disallowedTools", "")
            
            # Build command
            cmd = self._build_command(model, disallowed_tools)
            
            # Execute in workspace directory
            self.process = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=str(self.workspace_dir),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            # Stream output to log
            await self._stream_output()
            
            # Wait for completion
            return_code = await self.process.wait()
            
            if return_code == 0:
                # Check for solution files
                solution_tex = self.workspace_dir / "solution.tex"
                solution_pdf = self.workspace_dir / "solution.pdf"
                
                updates = {
                    "status": JobStatusEnum.COMPLETED,
                    "completedAt": datetime.now(timezone.utc).isoformat() + "Z",
                    "solutionTexCreated": solution_tex.exists()
                }
                
                # Try to compile PDF if tex exists
                if solution_tex.exists() and not solution_pdf.exists():
                    pdf_created = await self._compile_pdf()
                    updates["solutionPdfCreated"] = pdf_created
                else:
                    updates["solutionPdfCreated"] = solution_pdf.exists()
                
                await self._update_status(**updates)
            else:
                await self._update_status(
                    JobStatusEnum.ERROR,
                    completedAt=datetime.now(timezone.utc).isoformat() + "Z",
                    error=f"Process exited with code {return_code}"
                )
                
        except asyncio.CancelledError:
            # Job was cancelled
            if self.process:
                self.process.terminate()
                await self.process.wait()
            await self._update_status(
                JobStatusEnum.CANCELLED,
                completedAt=datetime.now(timezone.utc).isoformat() + "Z"
            )
            raise
            
        except Exception as e:
            logger.exception("Job execution failed")
            await self._update_status(
                JobStatusEnum.ERROR,
                completedAt=datetime.now(timezone.utc).isoformat() + "Z",
                error=str(e)
            )
            
    async def cancel(self):
        """Cancel the running job"""
        if self.process and self.process.returncode is None:
            self.process.terminate()
            await self.process.wait()
            
    async def _stream_output(self):
        """Stream process output to log file"""
        if not self.process or not self.process.stdout:
            return
            
        while True:
            line = await self.process.stdout.readline()
            if not line:
                break
                
            # Parse JSON output
            try:
                entry = json.loads(line.decode('utf-8'))
                # Write to log
                async with aiofiles.open(self.log_file, 'a') as f:
                    await f.write(json.dumps(entry) + '\n')
            except json.JSONDecodeError:
                # Write raw line as system message
                entry = {
                    "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
                    "type": "system",
                    "content": line.decode('utf-8').strip()
                }
                async with aiofiles.open(self.log_file, 'a') as f:
                    await f.write(json.dumps(entry) + '\n')
                    
    async def _compile_pdf(self) -> bool:
        """Compile solution.tex to PDF"""
        try:
            # Run pdflatex
            cmd = [PDFLATEX_COMMAND] + PDFLATEX_ARGS + ["solution.tex"]
            result = await asyncio.create_subprocess_exec(
                *cmd,
                cwd=str(self.workspace_dir),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await result.communicate()
            
            if result.returncode == 0 and PDFLATEX_RUNS > 1:
                # Run again for references
                for _ in range(PDFLATEX_RUNS - 1):
                    result2 = await asyncio.create_subprocess_exec(
                        *cmd,
                    cwd=str(self.workspace_dir),
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE
                    )
                    await result2.wait()
                
                return (self.workspace_dir / "solution.pdf").exists()
            else:
                # Log compilation error
                error_msg = stderr.decode('utf-8') if stderr else stdout.decode('utf-8')
                entry = {
                    "timestamp": datetime.now(timezone.utc).isoformat() + "Z",
                    "type": "error",
                    "content": f"LaTeX compilation failed: {error_msg[:500]}"
                }
                async with aiofiles.open(self.log_file, 'a') as f:
                    await f.write(json.dumps(entry) + '\n')
                return False
                
        except Exception:
            logger.exception("PDF compilation failed")
            return False
            
    def _build_command(self, model: str, disallowed_tools: str = "") -> list[str]:
        """Build the command to execute the AI agent"""
        cli_tool = MODEL_CLI_MAPPING.get(model)
        if not cli_tool:
            logger.warning(f"Unknown model {model}, defaulting to {DEFAULT_CLI_TOOL} CLI")
            cli_tool = DEFAULT_CLI_TOOL
        
        cmd = [
            cli_tool,
            "--print", "@prompt.md",
            "--verbose",
            "--output-format", "stream-json",
            "--model", model
        ]
        
        if disallowed_tools:
            cmd.extend(["--disallowedTools", disallowed_tools])
            
        return cmd
    
    async def _load_status(self) -> Dict[str, Any]:
        """Load current job status"""
        try:
            async with aiofiles.open(self.status_file, 'r') as f:
                content = await f.read()
                return json.loads(content)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            logger.error(f"Failed to load job status: {e}")
            # Return minimal status if file is missing/corrupt
            return {"status": JobStatusEnum.ERROR, "error": f"Failed to load status: {e}"}
            
    async def _update_status(self, status: Optional[JobStatusEnum] = None, **kwargs):
        """Update job status"""
        current = await self._load_status()
        
        if status:
            current["status"] = status.value
            
        current.update(kwargs)
        
        atomic_write_json(self.status_file, current)