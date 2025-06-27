"""
Job execution logic for the math agent system.

This module handles the actual execution of math problem-solving jobs,
including running the AI agent, managing output, and compiling LaTeX.
"""

import asyncio
import json
import logging
import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from ..utils import atomic_write_json

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
            await self._update_status("running", startedAt=datetime.utcnow().isoformat() + "Z")
            
            # Load job configuration
            status = self._load_status()
            model = status.get("model", "claude-opus-4")
            disallowed_tools = status.get("disallowedTools", "")
            
            # Build command
            cmd = [
                "claude" if model.startswith("claude") else "gemini",
                "--print", "@prompt.md",
                "--verbose",
                "--output-format", "stream-json",
                "--model", model
            ]
            
            if disallowed_tools:
                cmd.extend(["--disallowedTools", disallowed_tools])
            
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
                    "status": "completed",
                    "completedAt": datetime.utcnow().isoformat() + "Z",
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
                    "error",
                    completedAt=datetime.utcnow().isoformat() + "Z",
                    error=f"Process exited with code {return_code}"
                )
                
        except asyncio.CancelledError:
            # Job was cancelled
            if self.process:
                self.process.terminate()
                await self.process.wait()
            await self._update_status(
                "cancelled",
                completedAt=datetime.utcnow().isoformat() + "Z"
            )
            raise
            
        except Exception as e:
            logger.exception("Job execution failed")
            await self._update_status(
                "error",
                completedAt=datetime.utcnow().isoformat() + "Z",
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
                with open(self.log_file, 'a') as f:
                    f.write(json.dumps(entry) + '\n')
            except json.JSONDecodeError:
                # Write raw line as system message
                entry = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "type": "system",
                    "content": line.decode('utf-8').strip()
                }
                with open(self.log_file, 'a') as f:
                    f.write(json.dumps(entry) + '\n')
                    
    async def _compile_pdf(self) -> bool:
        """Compile solution.tex to PDF"""
        try:
            # Run pdflatex
            result = await asyncio.create_subprocess_exec(
                "pdflatex",
                "-interaction=nonstopmode",
                "solution.tex",
                cwd=str(self.workspace_dir),
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await result.communicate()
            
            if result.returncode == 0:
                # Run again for references
                result2 = await asyncio.create_subprocess_exec(
                    "pdflatex",
                    "-interaction=nonstopmode",
                    "solution.tex",
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
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "type": "error",
                    "content": f"LaTeX compilation failed: {error_msg[:500]}"
                }
                with open(self.log_file, 'a') as f:
                    f.write(json.dumps(entry) + '\n')
                return False
                
        except Exception as e:
            logger.exception("PDF compilation failed")
            return False
            
    def _load_status(self) -> Dict[str, Any]:
        """Load current job status"""
        with open(self.status_file, 'r') as f:
            return json.load(f)
            
    async def _update_status(self, status: Optional[str] = None, **kwargs):
        """Update job status"""
        current = self._load_status()
        
        if status:
            current["status"] = status
            
        current.update(kwargs)
        
        atomic_write_json(self.status_file, current)