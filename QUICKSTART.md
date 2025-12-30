# 🚀 QuickStart Guide

Get the ProspectFinder Agent running in **2 simple steps**!

## The Easiest Way (Recommended)

### Step 1: Install Everything

**Windows:**
```batch
.\install.bat
```

**macOS/Linux:**
```bash
chmod +x install.sh
./install.sh
```

This single command installs:
- ✅ egile-agent-core (Agent framework)
- ✅ egile-mcp-prospectfinder (MCP server for prospect search)
- ✅ egile-agent-prospectfinder (This plugin with AgentOS integration)

### Step 2: Start the System

**Terminal 1 - Start Backend:**
```bash
prospectfinder
```

This starts both:
- MCP Server on http://localhost:8001
- AgentOS on http://localhost:8000

**Terminal 2 - Start UI:**
```bash
cd ../agent-ui
pnpm dev
```

### Step 3: Use It!

1. Open http://localhost:3000 in your browser
2. Connect to `http://localhost:8000`
3. Select the "prospectfinder" agent
4. Start asking for prospects!

**Example prompts:**
- "Find marketing companies in Belgium"
- "Search for construction businesses in France"
- "Show me 5 healthcare companies in Germany"

---

## Alternative: Individual Commands

If you prefer to run services separately:

### Install (once)
```bash
pip install -e ".[all]"
```

### Run MCP Server (Terminal 1)
```bash
prospectfinder-mcp
```

### Run AgentOS (Terminal 2)
```bash
prospectfinder-agent
```

### Run Agent UI (Terminal 3)
```bash
cd ../agent-ui
pnpm dev
```

---

## Even Easier: Python Module

You can also use Python directly:

```bash
# Run everything
python -m egile_agent_prospectfinder

# Run MCP only
python -m egile_agent_prospectfinder.run_mcp

# Run Agent only
python -m egile_agent_prospectfinder.run_agent
```

---

## Configuration (Optional)

Create a `.env` file for search API keys (optional - uses DuckDuckGo by default):

```env
# Google Custom Search (optional)
GOOGLE_API_KEY=your_key
GOOGLE_CSE_ID=your_cse_id

# Brave Search (optional)
BRAVE_API_KEY=your_key

# OpenAI or XAI for the agent (required)
OPENAI_API_KEY=your_key
# OR
XAI_API_KEY=your_key
```

---

## Troubleshooting

**Port already in use?**
```bash
# Kill existing process on Windows
taskkill /F /IM python.exe

# Kill existing process on macOS/Linux
lsof -ti:8000 | xargs kill -9
lsof -ti:8001 | xargs kill -9
```

**MCP server connection failed?**
- Make sure MCP server started successfully
- Check logs in Terminal 1
- Verify port 8001 is accessible

**Agent UI can't connect?**
- Ensure AgentOS is running on port 8000
- Try connecting to `http://localhost:8000` in the Agent UI
- Check browser console for errors

---

## What's Running?

After setup, you have:

| Service | Port | URL |
|---------|------|-----|
| MCP Server | 8001 | http://localhost:8001 |
| AgentOS API | 8000 | http://localhost:8000 |
| Agent UI | 3000 | http://localhost:3000 |

---

## Next Steps

- Read the [Full README](README.md) for detailed documentation
- Check [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) for more examples
- Customize the agent in [run_server.py](src/egile_agent_prospectfinder/run_server.py)

---

## Summary: The 2-Command Setup

```bash
# 1. Install (once)
./install.sh  # or install.bat on Windows

# 2. Run backend
prospectfinder

# 3. Run UI (in another terminal)
cd ../agent-ui && pnpm dev
```

🎉 **That's it!** Open http://localhost:3000 and start finding prospects!
