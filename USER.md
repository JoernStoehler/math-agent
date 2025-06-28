# Math Agent System - Quick Start Guide

## 🚀 Starting the System

### Step 1: Install Requirements
```bash
pip install flask requests
```

### Step 2: Start the Web Server
```bash
python server.py
```
You should see:
```
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5001
```

### Step 3: Open Your Browser
Go to: **http://localhost:5001**

That's it! The system is now running.

---

## 📝 How to Submit a Math Problem

1. **Click "Submit New Job"** on the dashboard
2. **Fill out the form:**
   - **Exercise**: Pick a math problem (e.g., `simple_addition.tex`)
   - **Model**: Choose AI model (default: `claude-sonnet-4`)
   - **Max Turns**: Leave at 100 (usually plenty)
   - **Prompt**: Select `v2` or `v3` (these are instruction sets for the AI)
3. **Click "Submit Job"**
4. **Return to dashboard** - your job will appear in the list

---

## 📊 Understanding the Dashboard

The dashboard auto-refreshes every 5 seconds showing:

- **Job ID**: Unique identifier for each job
- **Status colors**:
  - ⚪ Gray = Scheduled (waiting to start)
  - 🟡 Yellow = Running (AI is working)
  - 🟢 Green = Completed (solution ready!)
  - 🔴 Red = Failed (something went wrong)
- **Files**: Click links to view:
  - `log` - What the AI is doing
  - `solution` - The final answer (when ready)

---

## 🔍 Viewing Results

Once a job shows green (completed):
1. Click the **"solution"** link in the Files column
2. This downloads/shows the PDF with the AI's solution

To see what the AI did:
1. Click the **"log"** link to see the AI's work process

---

## ⚠️ Common Issues

### "Maximum concurrent jobs (5) reached"
- Too many jobs running at once
- Wait a few minutes for jobs to finish
- Check the dashboard for job status

### Job stays yellow (running) for too long
- Some complex problems take 5-10 minutes
- Check the log file to see if AI is still working
- If stuck for >15 minutes, restart the server

### Can't connect to localhost:5001
- Make sure `python server.py` is still running
- Check no other program is using port 5001
- Try `http://127.0.0.1:5001` instead

---

## 🌐 Public Access (Optional)

### Making it accessible from anywhere using Cloudflare:

1. **Install cloudflared** (one-time):
   ```bash
   # For Linux/Codespaces:
   wget https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
   sudo dpkg -i cloudflared-linux-amd64.deb
   
   # For Mac:
   brew install cloudflared
   ```

2. **Run the tunnel**:
   ```bash
   # Quick test (gives you a random URL):
   cloudflared tunnel --url http://localhost:5001 --protocol http2
   ```
   
   You'll see something like:
   ```
   Your quick tunnel has been created! Visit it at:
   https://random-name-here.trycloudflare.com
   ```

3. **For custom domain (joernstoehler.com)**:
   ```bash
   # First login to Cloudflare:
   cloudflared tunnel login
   
   # Create a named tunnel:
   cloudflared tunnel create math-agent
   
   # Route to your domain (creates DNS record):
   cloudflared tunnel route dns math-agent math-agent.joernstoehler.com
   
   # Run the tunnel:
   cloudflared tunnel run --url http://localhost:5001 --protocol http2 math-agent
   ```
   
   Your app will be available at: **https://math-agent.joernstoehler.com**
   
   **Or simply run:** `./start-cloudflare.sh` (handles all the setup automatically)

**Note**: The `--protocol http2` flag is important to avoid QUIC timeout issues.

---

## 💡 Pro Tips

1. **Start simple**: Try `simple_addition.tex` first to test the system
2. **Watch the logs**: Click log files to see the AI's reasoning
3. **Prompt versions**: 
   - `v2` = Standard instructions
   - `v3` = More detailed instructions
   - `v4` = Latest version (if available)
4. **Browser bookmark**: Save http://localhost:5001 for quick access

---

## 🛑 Stopping the System

To stop the server:
1. Go to the terminal running `python server.py`
2. Press `Ctrl+C`

---

## 📁 Where Are My Files?

- **Exercises**: `exercises/` folder (the math problems)
- **Results**: `jobs/*/workspace/solution.pdf` (the AI's answers)
- **Logs**: `jobs/*/log.jsonl` (what the AI did)

---

## Need Help?

1. Check if the server is running: `ps aux | grep server.py`
2. Look at server logs in the terminal
3. Try refreshing the browser (F5)
4. Restart the server: Ctrl+C then `python server.py` again