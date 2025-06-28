from pathlib import Path
import os

# Just simple constants
PROJECT_ROOT = Path(__file__).parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data"
JOBS_DIR = PROJECT_ROOT / "jobs"
STATIC_DIR = PROJECT_ROOT / "static"
EXERCISES_DIR = DATA_DIR / "exercises"
PROMPTS_DIR = DATA_DIR / "prompts"

# Ensure directories exist
JOBS_DIR.mkdir(exist_ok=True)
DATA_DIR.mkdir(exist_ok=True)
PROMPTS_DIR.mkdir(exist_ok=True)

# Job Manager Configuration
JOB_SCAN_INTERVAL = int(os.getenv("JOB_SCAN_INTERVAL", "5"))  # seconds
MAX_CONCURRENT_JOBS = int(os.getenv("MAX_CONCURRENT_JOBS", "2"))

# LaTeX Configuration
PDFLATEX_COMMAND = os.getenv("PDFLATEX_COMMAND", "pdflatex")
PDFLATEX_ARGS = ["-interaction=nonstopmode"]
PDFLATEX_RUNS = int(os.getenv("PDFLATEX_RUNS", "2"))  # Run twice for references

# Model to CLI tool mapping
MODEL_CLI_MAPPING = {
    "claude-opus-4": "claude",
    "claude-sonnet-4": "claude",
    "gemini-2.5-pro": "gemini",
    "gemini-2.5-flash": "gemini",
}
DEFAULT_CLI_TOOL = "gemini"  # Fallback for unknown models