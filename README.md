# Math Agent Benchmarking System

A web-based system for automated mathematical problem solving using AI models (Claude and Gemini). Submit LaTeX exercises and get AI-generated solutions with full PDF compilation.

## 🚀 Quick Start

### Prerequisites
- Docker with Dev Containers support (VS Code recommended)
- Or: Python 3.8+, LaTeX, and AI CLI tools

### Using Dev Container (Recommended)

1. **Open in VS Code with Dev Containers**:
   ```bash
   code .
   ```
   Then click "Reopen in Container" when prompted.

2. **Start the web server**:
   ```bash
   python src/server.py
   ```

3. **Open browser**: http://localhost:5001

### Manual Setup

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   # Also need: pdflatex, claude CLI, gemini CLI
   ```

2. **Copy environment template**:
   ```bash
   cp .env.example .env
   # Edit .env with your API keys if needed
   ```

3. **Run server**:
   ```bash
   python src/server.py
   ```

## 📝 How to Use

### Submitting a Math Problem

1. Click **"Submit New Job"** on the dashboard
2. Fill out the form:
   - **Exercise**: Select a .tex file (e.g., `simple_addition.tex`)
   - **Model**: Choose AI model:
     - `claude-sonnet-4` (default, balanced)
     - `claude-opus-4` (most capable)
     - `gemini-2.5-pro` (Google's best)
     - `gemini-2.5-flash` (fast)
   - **Max Turns**: Leave at 100
   - **Prompt**: Select version (v6 is latest)
3. Click **"Submit Job"**
4. Return to dashboard to monitor progress

### Understanding Job Status

Dashboard auto-refreshes every 30 seconds:
- ⚪ **Gray** = Scheduled (queued)
- 🟡 **Yellow** = Running (AI working)
- 🟢 **Green** = Completed (solution ready)
- 🔴 **Red** = Failed (check logs)

### Viewing Results

When job is complete:
- Click **"solution"** for the PDF answer
- Click **"log"** to see AI's work process

## 🌟 Features

### Web Dashboard
- Real-time job monitoring
- Queue management (max 5 concurrent jobs)
- Color-coded status visualization
- Direct file access to all outputs
- Process monitoring page

### Batch Processing
- Submit multiple exercises
- Automatic queueing system
- Fire-and-forget execution
- Concurrent job limiting

### AI Models
- Multiple Claude versions
- Gemini integration
- Configurable max conversation turns
- Custom prompt engineering

### Output Management
- Automatic LaTeX compilation
- PDF generation
- Full execution logs
- Organized job directories

## 📁 Project Structure

```
math-agent/
├── .devcontainer/          # Dev container configuration
│   ├── devcontainer.json   # VS Code settings
│   ├── docker-compose.yml  # Multi-container setup
│   └── Dockerfile          # Custom image with LaTeX
├── exercises/              # Math problems (.tex files)
├── prompts/                # AI instruction sets
│   ├── v6.md              # Latest prompt version
│   └── ...                # Other versions
├── jobs/                   # Output directory
│   └── {job_id}/
│       ├── status.json     # Job status
│       ├── log.jsonl       # Execution log
│       └── workspace/
│           ├── exercise.tex    # Input
│           ├── solution.tex    # AI output
│           └── solution.pdf    # Final PDF
├── src/                    # Source code
│   ├── server.py           # Web dashboard
│   ├── math-agent-simple.sh # CLI runner
│   └── start-cloudflare.sh # Tunnel script
└── README.md               # This file
```

## 🌐 Public Access (Optional)

Make your instance accessible via Cloudflare Tunnel:

```bash
# Quick public URL:
./src/start-cloudflare.sh

# Or manual setup:
cloudflared tunnel --url http://localhost:5001
```

## 🛠️ Advanced Usage

### Command Line Processing

Process single exercise without web UI:
```bash
./src/math-agent-simple.sh \
  -j jobs/test \
  -e exercises/example.tex \
  -p prompts/v6.md \
  -m claude-sonnet-4
```

### Custom Prompts

1. Create new prompt file in `prompts/`
2. Use existing prompt as template
3. Test on sample exercises
4. Select in web UI or use with CLI

### API Endpoints

- `GET /` - Main dashboard
- `GET /submit` - Job submission form
- `POST /submit` - Create new job
- `GET /processes` - Process monitor
- `GET /logs/{job_id}` - View job logs

## ⚠️ Troubleshooting

### Job stuck in "running"
- Complex problems may take 10-15 minutes
- Check `/processes` page for active processes
- View logs to see if AI is still working

### "Maximum concurrent jobs reached"
- System limits to 5 simultaneous jobs
- Wait for current jobs to complete
- Jobs automatically queue when limit reached

### LaTeX compilation errors
- Check exercise file is valid LaTeX
- Verify all required packages in Dockerfile
- Look for encoding issues in logs

### Connection issues
- Ensure server is running on port 5001
- Check Docker container is healthy
- Verify no firewall blocking

## 🔧 Configuration

### Environment Variables
See `.env.example`:
- `HONEYCOMB_API_KEY` - Telemetry (optional)
- `CLAUDE_API_KEY` - If not using CLI auth
- `GEMINI_API_KEY` - If not using CLI auth

### Server Settings
In `src/server.py`:
- `MAX_CONCURRENT_JOBS = 5` - Job limit
- `port=5001` - Web server port

## 📊 Performance Notes

- Efficient for <100 total jobs
- No database needed at this scale
- Directory-based job tracking
- Automatic cleanup not implemented

## 🔒 Security

- No authentication (trusted environment)
- Read-only file access via web
- Process isolation per job
- No remote code execution

## 💡 Tips

1. Start with `simple_addition.tex` to test
2. Monitor first few jobs closely
3. Check logs if solutions seem wrong
4. Use v6 prompt for best results
5. Gemini models are good alternatives

## 🛑 Stopping the System

To stop server:
1. Find terminal running `python src/server.py`
2. Press `Ctrl+C`

To stop Cloudflare tunnel:
1. Find terminal running cloudflared
2. Press `Ctrl+C`

## 📄 License

Academic research project for mathematical AI benchmarking.