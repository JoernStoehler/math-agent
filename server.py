#!/usr/bin/env python3
"""
Math Agent Benchmarking System Web Dashboard
A minimal Flask-based web server for running and monitoring math agent benchmarks.
"""

from flask import Flask, request, render_template_string, redirect, url_for, send_file, Response
import subprocess
import os
import json
import glob
import shutil
from datetime import datetime
import requests
from pathlib import Path
import mimetypes

app = Flask(__name__)

# Configuration
JOBS_DIR = "jobs"
EXERCISES_DIR = "exercises"
PROMPTS_DIR = "prompts"
FILE_SERVER_URL = "http://localhost:8001"
MAX_CONCURRENT_JOBS = 5

# HTML Templates
DASHBOARD_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Math Agent Benchmark Dashboard</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1, h2 {
            color: #333;
        }
        a {
            color: #0066cc;
            text-decoration: none;
        }
        a:hover {
            text-decoration: underline;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            background: white;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin-top: 20px;
        }
        th, td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        th {
            background-color: #f8f9fa;
            font-weight: 600;
            color: #555;
        }
        tr:hover {
            background-color: #f8f9fa;
        }
        .status-completed { background-color: #d4edda; }
        .status-running { background-color: #fff3cd; }
        .status-failed { background-color: #f8d7da; }
        .status-scheduled { background-color: #e2e3e5; }
        
        /* Model Pills */
        .model-pill {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 14px;
            font-weight: 500;
            color: white;
        }
        .model-claude-sonnet-4 {
            background-color: #FF6B6B;
        }
        .model-claude-opus-4 {
            background-color: #4ECDC4;
        }
        .model-claude-haiku-3 {
            background-color: #95E1D3;
        }
        .model-default {
            background-color: #748FFC;
        }
        
        /* File Links */
        .file-link {
            display: inline-flex;
            align-items: center;
            padding: 6px 12px;
            margin: 0 4px;
            background-color: #f0f0f0;
            border-radius: 6px;
            text-decoration: none;
            transition: all 0.2s ease;
            font-size: 14px;
            font-weight: 500;
            color: #333;
        }
        .file-link:hover {
            background-color: #e0e0e0;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            text-decoration: none;
        }
        .file-link svg {
            margin-right: 6px;
            width: 16px;
            height: 16px;
        }
        .file-link.log-link {
            background-color: #e3f2fd;
            color: #1976d2;
        }
        .file-link.log-link:hover {
            background-color: #bbdefb;
        }
        .file-link.pdf-link {
            background-color: #ffebee;
            color: #c62828;
        }
        .file-link.pdf-link:hover {
            background-color: #ffcdd2;
        }
        .navigation {
            margin-bottom: 20px;
            padding: 15px;
            background: white;
            border-radius: 5px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .navigation a {
            display: inline-block;
            margin-right: 20px;
            padding: 8px 16px;
            background-color: #0066cc;
            color: white;
            border-radius: 5px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        .navigation a:hover {
            background-color: #0052a3;
            text-decoration: none;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .filter-container {
            margin-bottom: 20px;
            padding: 15px;
            background: white;
            border-radius: 5px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }
        .filter-input {
            width: 300px;
            padding: 8px 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }
        .filter-input:focus {
            outline: none;
            border-color: #0066cc;
            box-shadow: 0 0 0 2px rgba(0,102,204,0.2);
        }
        th.sortable {
            cursor: pointer;
            user-select: none;
            position: relative;
            padding-right: 25px;
        }
        th.sortable:hover {
            background-color: #f0f0f0;
        }
        th.sortable::after {
            content: '↕';
            position: absolute;
            right: 8px;
            color: #999;
            font-size: 12px;
        }
        th.sortable.asc::after {
            content: '↑';
            color: #333;
        }
        th.sortable.desc::after {
            content: '↓';
            color: #333;
        }
    </style>
    <meta http-equiv="refresh" content="30">
    <script>
        let currentSort = { column: null, direction: 'asc' };
        
        function sortTable(column) {
            const table = document.getElementById('jobsTable');
            const tbody = table.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            
            // Toggle sort direction
            if (currentSort.column === column) {
                currentSort.direction = currentSort.direction === 'asc' ? 'desc' : 'asc';
            } else {
                currentSort.column = column;
                currentSort.direction = 'asc';
            }
            
            // Update header classes
            document.querySelectorAll('th.sortable').forEach(th => {
                th.classList.remove('asc', 'desc');
            });
            const th = document.querySelector(`th[data-column="${column}"]`);
            th.classList.add(currentSort.direction);
            
            // Sort rows
            rows.sort((a, b) => {
                let aVal = a.querySelector(`td:nth-child(${getColumnIndex(column)})`).textContent.trim();
                let bVal = b.querySelector(`td:nth-child(${getColumnIndex(column)})`).textContent.trim();
                
                // Handle timestamp sorting
                if (column === 'job_id') {
                    // Extract timestamp from job_id
                    aVal = aVal.split('.').pop() || aVal;
                    bVal = bVal.split('.').pop() || bVal;
                }
                
                if (aVal < bVal) return currentSort.direction === 'asc' ? -1 : 1;
                if (aVal > bVal) return currentSort.direction === 'asc' ? 1 : -1;
                return 0;
            });
            
            // Re-append sorted rows
            rows.forEach(row => tbody.appendChild(row));
        }
        
        function getColumnIndex(column) {
            const columns = ['job_id', 'exercise', 'model', 'prompt', 'status', 'files'];
            return columns.indexOf(column) + 1;
        }
        
        function filterTable() {
            const input = document.getElementById('filterInput');
            const filter = input.value.toLowerCase();
            const table = document.getElementById('jobsTable');
            const rows = table.querySelectorAll('tbody tr');
            
            rows.forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        }
        
        // Disable auto-refresh when user is interacting
        document.addEventListener('DOMContentLoaded', function() {
            const metaRefresh = document.querySelector('meta[http-equiv="refresh"]');
            const filterInput = document.getElementById('filterInput');
            
            filterInput.addEventListener('focus', () => {
                metaRefresh.setAttribute('content', '');
            });
            
            filterInput.addEventListener('blur', () => {
                metaRefresh.setAttribute('content', '30');
            });
        });
    </script>
</head>
<body>
    <h1>Math Agent Benchmark Dashboard</h1>
    <div class="navigation">
        <a href="/submit">Submit New Job</a>
        <a href="/files/">Browse Files</a>
    </div>
    
    <div class="filter-container">
        <input type="text" id="filterInput" class="filter-input" placeholder="Filter jobs..." onkeyup="filterTable()">
    </div>
    
    <h2>Jobs ({{ jobs|length }})</h2>
    <table id="jobsTable">
        <thead>
            <tr>
                <th class="sortable" data-column="job_id" onclick="sortTable('job_id')">Job ID</th>
                <th class="sortable" data-column="exercise" onclick="sortTable('exercise')">Exercise</th>
                <th class="sortable" data-column="model" onclick="sortTable('model')">Model</th>
                <th class="sortable" data-column="prompt" onclick="sortTable('prompt')">Prompt</th>
                <th class="sortable" data-column="status" onclick="sortTable('status')">Status</th>
                <th>Files</th>
            </tr>
        </thead>
        <tbody>
            {% for job in jobs %}
            <tr class="status-{{ job.status }}">
                <td>{{ job.job_id }}</td>
                <td><a href="/files/exercises/{{ job.exercise }}">{{ job.exercise }}</a></td>
                <td>
                    <span class="model-pill model-{{ job.model|replace('.', '-') }}">
                        {{ job.model }}
                    </span>
                </td>
                <td><a href="/files/prompts/{{ job.prompt }}/prompt.md">{{ job.prompt }}</a></td>
                <td>{{ job.status }}</td>
                <td>
                    <a href="/logs/{{ job.job_id }}" class="file-link log-link">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M14 2H6c-1.1 0-2 .9-2 2v16c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V8l-6-6zM6 20V4h7v5h5v11H6z"/>
                            <path d="M8 15h8v2H8zm0-4h8v2H8z"/>
                        </svg>
                        log
                    </a>
                    {% if job.has_solution %}
                    <a href="/files/jobs/{{ job.job_id }}/workspace/solution.pdf" class="file-link pdf-link">
                        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">
                            <path d="M20 2H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-8.5 7.5c0 .83-.67 1.5-1.5 1.5H9v2H7.5V7H10c.83 0 1.5.67 1.5 1.5v1zm5 2c0 .83-.67 1.5-1.5 1.5h-2.5V7H15c.83 0 1.5.67 1.5 1.5v3zm4-3H19v1h1.5V11H19v2h-1.5V7h3v1.5zM9 9.5h1v-1H9v1zM4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6zm10 5.5h1v-3h-1v3z"/>
                        </svg>
                        solution
                    </a>
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </tbody>
    </table>
</body>
</html>
"""

SUBMIT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Submit New Job - Math Agent Benchmark</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
        }
        .form-container {
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            max-width: 600px;
            margin: 20px auto;
        }
        label {
            display: block;
            margin-bottom: 5px;
            font-weight: 600;
            color: #555;
        }
        select, input[type="number"], input[type="text"], textarea {
            width: 100%;
            padding: 8px 12px;
            margin-bottom: 20px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 16px;
        }
        textarea {
            resize: vertical;
            min-height: 150px;
        }
        button {
            background-color: #0066cc;
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0052a3;
        }
        .error {
            background-color: #f8d7da;
            color: #721c24;
            padding: 12px;
            border-radius: 4px;
            margin-bottom: 20px;
        }
        .back-link {
            margin-bottom: 20px;
            display: inline-block;
            padding: 8px 16px;
            background-color: #6c757d;
            color: white;
            border-radius: 5px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        .back-link:hover {
            background-color: #5a6268;
            text-decoration: none;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        #prompt_preview {
            background-color: #f8f9fa;
            font-family: monospace;
            font-size: 14px;
        }
    </style>
    <script>
        function togglePromptInput() {
            const promptType = document.querySelector('[name="prompt_type"]').value;
            document.getElementById('existing_prompt').style.display = 
                promptType === 'existing' ? 'block' : 'none';
            document.getElementById('new_prompt').style.display = 
                promptType === 'new' ? 'block' : 'none';
        }
        
        function updatePromptPreview() {
            const select = document.querySelector('[name="existing_prompt"]');
            const preview = document.getElementById('prompt_preview');
            if (select.value) {
                fetch('/get_prompt_content?prompt=' + select.value)
                    .then(response => response.text())
                    .then(text => preview.value = text);
            }
        }
        
        function updateExercisePreview() {
            const select = document.querySelector('[name="exercise"]');
            const preview = document.getElementById('exercise_preview');
            if (select.value) {
                fetch('/get_exercise_content?exercise=' + encodeURIComponent(select.value))
                    .then(response => response.text())
                    .then(text => preview.value = text);
            }
        }
        
        window.onload = function() {
            updatePromptPreview();
            updateExercisePreview();
        }
    </script>
</head>
<body>
    <h1>Submit New Job</h1>
    <a href="/" class="back-link">← Back to Dashboard</a>
    
    <div class="form-container">
        {% if error %}
        <div class="error">{{ error }}</div>
        {% endif %}
        
        <form method="post" action="/submit">
            <label>Exercise:</label>
            <select name="exercise" onchange="updateExercisePreview()" required>
                {% for exercise in exercises %}
                <option value="{{ exercise }}">{{ exercise }}</option>
                {% endfor %}
            </select>
            <label>Exercise Preview:</label>
            <textarea readonly id="exercise_preview" style="min-height: 150px; font-family: monospace;"></textarea>

            <label>Model:</label>
            <select name="model" required>
                <option value="claude-sonnet-4" selected>claude-sonnet-4</option>
                <option value="claude-opus-4">claude-opus-4</option>
                <option value="claude-haiku-3">claude-haiku-3</option>
            </select>

            <label>Max Turns:</label>
            <input type="number" name="max_turns" value="100" min="1" max="200">

            <label>
                <input type="checkbox" name="test_run" value="1" style="width: auto; margin-right: 8px;">
                Test Run (use claude-dummy for faster debugging)
            </label>

            <label>Prompt:</label>
            <select name="prompt_type" onchange="togglePromptInput()" required>
                <option value="existing">Use Existing Prompt</option>
                <option value="new">Create New Prompt</option>
            </select>

            <div id="existing_prompt">
                <label>Select Prompt:</label>
                <select name="existing_prompt" onchange="updatePromptPreview()">
                    {% for prompt in prompts %}
                    <option value="{{ prompt }}">{{ prompt }}</option>
                    {% endfor %}
                </select>
                <label>Prompt Preview:</label>
                <textarea readonly id="prompt_preview"></textarea>
            </div>

            <div id="new_prompt" style="display:none">
                <label>Prompt Name:</label>
                <input type="text" name="new_prompt_name" placeholder="e.g., v5">
                <label>Prompt Content:</label>
                <textarea name="new_prompt_content" placeholder="Enter prompt content..."></textarea>
            </div>

            <button type="submit">Submit Job</button>
        </form>
    </div>
</body>
</html>
"""

LOG_VIEWER_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Log Viewer - {{ job_id }} - Math Agent Benchmark</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            margin: 0;
            padding: 20px;
            background-color: #f5f5f5;
        }
        h1 {
            color: #333;
            margin-bottom: 10px;
        }
        .job-info {
            color: #666;
            margin-bottom: 20px;
            font-size: 14px;
        }
        .log-container {
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            max-width: 1200px;
            margin: 0 auto;
            max-height: 80vh;
            overflow-y: auto;
            padding: 20px;
        }
        .log-entry {
            margin-bottom: 15px;
            padding: 10px;
            border-radius: 4px;
        }
        .log-entry.system {
            background-color: #f8f9fa;
            color: #6c757d;
            font-family: monospace;
            font-size: 13px;
            padding: 5px 10px;
            margin-bottom: 5px;
        }
        .log-entry.message {
            background-color: #e3f2fd;
            border-left: 4px solid #2196f3;
        }
        .log-entry.tool-use {
            background-color: #f3e5f5;
            border-left: 4px solid #9c27b0;
        }
        .entry-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 5px;
            font-size: 12px;
            color: #666;
        }
        .entry-type {
            font-weight: bold;
            text-transform: uppercase;
        }
        .entry-duration {
            color: #28a745;
            font-family: monospace;
        }
        .entry-content {
            color: #333;
            line-height: 1.5;
        }
        .tool-name {
            font-weight: bold;
            color: #9c27b0;
        }
        .back-link {
            display: inline-block;
            margin-bottom: 20px;
            padding: 8px 16px;
            background-color: #6c757d;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        .back-link:hover {
            background-color: #5a6268;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .download-link {
            display: inline-block;
            margin-left: 10px;
            padding: 8px 16px;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            font-weight: 500;
            transition: all 0.2s ease;
        }
        .download-link:hover {
            background-color: #0056b3;
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
    </style>
</head>
<body>
    <a href="/" class="back-link">← Back to Dashboard</a>
    <a href="/files/jobs/{{ job_id }}/log.jsonl" class="download-link">Download Raw Log</a>
    
    <h1>Log Viewer: {{ job_info.exercise }}.{{ job_info.model }}.{{ job_info.prompt }}</h1>
    <div class="job-info">
        Job ID: {{ job_id }}<br>
        Timestamp: {{ job_info.timestamp }}
    </div>
    
    <div class="log-container">
        {% for entry in entries %}
            {% if entry.type == 'log' %}
                <div class="log-entry system">{{ entry.content }}</div>
            {% elif entry.type == 'json' %}
                {% if entry.data.type == 'message' %}
                    <div class="log-entry message">
                        <div class="entry-header">
                            <span class="entry-type">{{ entry.data.role }}</span>
                            {% if entry.duration %}
                                <span class="entry-duration">+{{ "%.2f"|format(entry.duration) }}s</span>
                            {% endif %}
                        </div>
                        <div class="entry-content">{{ entry.data.content }}</div>
                    </div>
                {% elif entry.data.type == 'tool_use' %}
                    <div class="log-entry tool-use">
                        <div class="entry-header">
                            <span class="entry-type">Tool Use</span>
                            {% if entry.duration %}
                                <span class="entry-duration">+{{ "%.2f"|format(entry.duration) }}s</span>
                            {% endif %}
                        </div>
                        <div class="entry-content">
                            <span class="tool-name">{{ entry.data.tool }}</span>: {{ entry.data.content }}
                        </div>
                    </div>
                {% endif %}
            {% endif %}
        {% endfor %}
    </div>
</body>
</html>
"""

def get_exercises():
    """Get list of exercise files from the exercises directory."""
    exercises = []
    if os.path.exists(EXERCISES_DIR):
        for file in os.listdir(EXERCISES_DIR):
            if file.endswith('.tex'):
                exercises.append(file)
    return sorted(exercises)

def get_prompts():
    """Get list of available prompts from the prompts directory."""
    prompts = []
    if os.path.exists(PROMPTS_DIR):
        for file in os.listdir(PROMPTS_DIR):
            if file.endswith('.md'):
                prompts.append(file.replace('.md', ''))
    return sorted(prompts)

def scan_jobs():
    """Scan the jobs directory and return job information."""
    jobs = []
    if not os.path.exists(JOBS_DIR):
        return jobs
    
    for job_dir in os.listdir(JOBS_DIR):
        job_path = os.path.join(JOBS_DIR, job_dir)
        if os.path.isdir(job_path):
            job_info = parse_job_id(job_dir)
            
            # Read status
            status_file = os.path.join(job_path, 'status.json')
            if os.path.exists(status_file):
                try:
                    with open(status_file, 'r') as f:
                        content = f.read()
                        if content.strip():  # Check if file is not empty
                            status_data = json.loads(content)
                            job_info['status'] = status_data.get('status', 'unknown')
                        else:
                            job_info['status'] = 'unknown'
                except (json.JSONDecodeError, IOError):
                    job_info['status'] = 'unknown'
            else:
                job_info['status'] = 'unknown'
            
            # Check for solution
            solution_path = os.path.join(job_path, 'workspace', 'solution.pdf')
            job_info['has_solution'] = os.path.exists(solution_path)
            
            jobs.append(job_info)
    
    # Sort by timestamp (newest first)
    jobs.sort(key=lambda x: x['job_id'], reverse=True)
    return jobs

def parse_job_id(job_id):
    """Parse job ID to extract components."""
    parts = job_id.split('.')
    if len(parts) >= 4:
        return {
            'job_id': job_id,
            'exercise': parts[0],
            'model': parts[1],
            'prompt': parts[2],
            'timestamp': parts[3]
        }
    else:
        # Handle legacy format or malformed IDs
        return {
            'job_id': job_id,
            'exercise': 'unknown',
            'model': 'unknown',
            'prompt': 'unknown',
            'timestamp': 'unknown'
        }

def get_running_job_count():
    """Count currently running math-agent.sh processes."""
    try:
        result = subprocess.run(
            ['bash', '-c', 'ps aux | grep "math-agent\\.sh" | grep -v grep | wc -l'],
            capture_output=True,
            text=True
        )
        return int(result.stdout.strip())
    except:
        return 0

def create_job(form_data):
    """Create a new job from form submission."""
    # Extract form data
    exercise = form_data.get('exercise')
    model = form_data.get('model')
    max_turns = form_data.get('max_turns', '100')
    prompt_type = form_data.get('prompt_type')
    test_run = form_data.get('test_run') == '1'
    
    # Validation
    if not exercise or not model:
        return {'success': False, 'error': 'Exercise and model are required'}
    
    # Check concurrent job limit
    running_jobs = get_running_job_count()
    if running_jobs >= MAX_CONCURRENT_JOBS:
        return {'success': False, 'error': f'Maximum concurrent jobs ({MAX_CONCURRENT_JOBS}) reached. Currently running: {running_jobs}'}
    
    # Handle prompt selection/creation
    if prompt_type == 'existing':
        prompt_name = form_data.get('existing_prompt')
        if not prompt_name:
            return {'success': False, 'error': 'Please select an existing prompt'}
    else:
        prompt_name = form_data.get('new_prompt_name')
        prompt_content = form_data.get('new_prompt_content')
        if not prompt_name or not prompt_content:
            return {'success': False, 'error': 'Prompt name and content are required'}
        
        # Create new prompt file
        new_prompt_file = os.path.join(PROMPTS_DIR, f'{prompt_name}.md')
        if os.path.exists(new_prompt_file):
            return {'success': False, 'error': f'Prompt {prompt_name} already exists'}
        
        with open(new_prompt_file, 'w') as f:
            f.write(prompt_content)
    
    # Generate job ID
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    job_id = f"{exercise.replace('.tex', '')}.{model}.{prompt_name}.{timestamp}"
    
    # Create job directory structure
    job_dir = os.path.join(JOBS_DIR, job_id)
    workspace_dir = os.path.join(job_dir, 'workspace')
    
    try:
        os.makedirs(workspace_dir, exist_ok=True)
        
        # Copy exercise file
        exercise_src = os.path.join(EXERCISES_DIR, exercise)
        exercise_dst = os.path.join(workspace_dir, 'exercise.tex')
        if os.path.exists(exercise_src):
            shutil.copy2(exercise_src, exercise_dst)
        else:
            return {'success': False, 'error': f'Exercise file {exercise} not found'}
        
        # Copy prompt file
        prompt_src = os.path.join(PROMPTS_DIR, f'{prompt_name}.md')
        prompt_dst = os.path.join(workspace_dir, 'prompt.md')
        if os.path.exists(prompt_src):
            shutil.copy2(prompt_src, prompt_dst)
        else:
            return {'success': False, 'error': f'Prompt file {prompt_name}.md not found'}
        
        # Note: agent.sh no longer needed in prompts directory
        
        # Write initial status
        status_data = {'status': 'scheduled', 'created': timestamp}
        with open(os.path.join(job_dir, 'status.json'), 'w') as f:
            json.dump(status_data, f)
        
        # Update status to running
        status_data['status'] = 'running'
        with open(os.path.join(job_dir, 'status.json'), 'w') as f:
            json.dump(status_data, f)
        
        # Spawn agent process using math-agent.sh
        log_file = os.path.join(job_dir, 'log.jsonl')
        math_agent_path = os.path.join('scripts', 'math-agent.sh')
        
        if not os.path.exists(math_agent_path):
            return {'success': False, 'error': 'math-agent.sh script not found'}
        
        # Prepare command with all necessary arguments
        cmd = [
            'bash', math_agent_path,
            '--job-dir', job_dir,
            '--exercise', os.path.join(EXERCISES_DIR, exercise),
            '--prompt', os.path.join(PROMPTS_DIR, f'{prompt_name}.md'),
            '--model', model,
            '--max-turns', str(max_turns)
        ]
        
        # Add test-run flag if enabled
        if test_run:
            cmd.append('--test-run')
        
        # Start the process
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            env={**os.environ}
        )
        
        # No need to update status - math-agent.sh handles that
        
        return {'success': True, 'job_id': job_id}
        
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.route('/')
def dashboard():
    """Display the main dashboard with all jobs."""
    jobs = scan_jobs()
    return render_template_string(DASHBOARD_HTML, jobs=jobs)

@app.route('/submit', methods=['GET', 'POST'])
def submit_job():
    """Handle job submission form and processing."""
    if request.method == 'POST':
        result = create_job(request.form)
        if result['success']:
            return redirect(url_for('dashboard'))
        else:
            exercises = get_exercises()
            prompts = get_prompts()
            return render_template_string(SUBMIT_HTML, 
                                        error=result['error'],
                                        exercises=exercises,
                                        prompts=prompts)
    
    # GET request - show form
    exercises = get_exercises()
    prompts = get_prompts()
    return render_template_string(SUBMIT_HTML, 
                                exercises=exercises,
                                prompts=prompts)

@app.route('/get_prompt_content')
def get_prompt_content():
    """AJAX endpoint to get prompt content for preview."""
    prompt = request.args.get('prompt')
    if prompt:
        prompt_file = os.path.join(PROMPTS_DIR, f'{prompt}.md')
        if os.path.exists(prompt_file):
            with open(prompt_file, 'r') as f:
                return f.read()
    return "Prompt not found"

@app.route('/get_exercise_content')
def get_exercise_content():
    """AJAX endpoint to get exercise content for preview."""
    exercise = request.args.get('exercise')
    if exercise:
        exercise_file = os.path.join(EXERCISES_DIR, exercise)
        if os.path.exists(exercise_file):
            with open(exercise_file, 'r') as f:
                return f.read()
    return "Exercise not found"

@app.route('/files/')
@app.route('/files/<path:filename>')
def serve_files(filename=''):
    """Proxy requests to the file server or serve files directly."""
    # Option 1: Proxy to file server
    try:
        response = requests.get(f"{FILE_SERVER_URL}/{filename}")
        return Response(
            response.content,
            status=response.status_code,
            headers=dict(response.headers)
        )
    except:
        # Option 2: Serve directly if file server is not running
        if filename == '':
            # Generate directory listing
            return generate_directory_listing('.')
        
        file_path = os.path.join(os.getcwd(), filename)
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                return generate_directory_listing(filename)
            else:
                mime_type = mimetypes.guess_type(file_path)[0]
                return send_file(file_path, mimetype=mime_type)
        
        return "File not found", 404

def generate_directory_listing(path):
    """Generate a simple HTML directory listing."""
    full_path = os.path.join(os.getcwd(), path)
    items = []
    
    if os.path.exists(full_path) and os.path.isdir(full_path):
        for item in sorted(os.listdir(full_path)):
            item_path = os.path.join(path, item) if path != '.' else item
            items.append(f'<li><a href="/files/{item_path}">{item}</a></li>')
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Directory: {path}</title>
        <style>
            body {{ font-family: monospace; margin: 20px; }}
            ul {{ list-style: none; }}
            li {{ margin: 5px 0; }}
        </style>
    </head>
    <body>
        <h1>Directory: {path}</h1>
        <ul>
            {''.join(items)}
        </ul>
    </body>
    </html>
    """
    return html

@app.route('/logs/<job_id>')
def view_log(job_id):
    """Display a job's log in a user-friendly format."""
    log_file = os.path.join(JOBS_DIR, job_id, 'log.jsonl')
    if not os.path.exists(log_file):
        return "Log file not found", 404
    
    # Parse the log file
    entries = parse_log_file(log_file)
    
    # Get job info
    job_info = parse_job_id(job_id)
    
    return render_template_string(LOG_VIEWER_HTML, 
                                job_id=job_id,
                                job_info=job_info,
                                entries=entries)

def parse_log_file(log_file):
    """Parse a JSONL log file and calculate durations."""
    entries = []
    last_timestamp = None
    
    with open(log_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            # Try to parse as JSON
            try:
                data = json.loads(line)
                if 'timestamp' in data:
                    timestamp = datetime.fromisoformat(data['timestamp'].replace('Z', '+00:00'))
                    
                    # Calculate duration since last timestamp
                    duration = None
                    if last_timestamp and data.get('type') in ['message', 'tool_use']:
                        duration = (timestamp - last_timestamp).total_seconds()
                    
                    entries.append({
                        'type': 'json',
                        'data': data,
                        'duration': duration,
                        'timestamp': timestamp
                    })
                    
                    if data.get('type') in ['message', 'tool_use']:
                        last_timestamp = timestamp
            except json.JSONDecodeError:
                # Regular log line
                entries.append({
                    'type': 'log',
                    'content': line
                })
    
    return entries

if __name__ == '__main__':
    # Ensure directories exist
    os.makedirs(JOBS_DIR, exist_ok=True)
    
    # Run the Flask app
    app.run(host='0.0.0.0', port=5001, debug=True)