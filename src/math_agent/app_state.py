"""Simple app state module to hold shared instances"""
from math_agent.services.job_manager import JobManager
from math_agent.config import JOBS_DIR

# Initialize job manager - it will be started when first job is submitted
job_manager = JobManager(JOBS_DIR)