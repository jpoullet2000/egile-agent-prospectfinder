# Egile Agent ProspectFinder

A complete AI agent system for finding business prospects. Includes:
- 🤖 **ProspectFinder Agent** - AI agent with prospect search capabilities
- 🔌 **Plugin Architecture** - Seamlessly integrates with Egile Agent Core
- 🌐 **MCP Integration** - Uses Agno's robust MCP client
- 💬 **Chat Interface** - Ready-to-use web UI via Agent UI
- 📦 **One-Command Install** - Get started in minutes

## ⚡ Quick Start (2 Commands!)

### 1. Install Everything
```bash
# Windows
.\install.bat

# macOS/Linux
chmod +x install.sh && ./install.sh
```

### 2. Run the System

**Terminal 1:**
```bash
prospectfinder
```

**Terminal 2:**
```bash
cd ../agent-ui
pnpm dev
```

**Then open:** http://localhost:3000 and start chatting!

👉 **See [QUICKSTART.md](QUICKSTART.md) for detailed instructions**

---

## Features

- 🔍 **Prospect Search**: Search for businesses in specific sectors and countries
- 🤖 **Complete Agent System**: Includes MCP server + AgentOS + Web UI
- 💬 **Natural Language**: Chat with the agent using plain English
- 🔌 **Plugin Architecture**: Extends Egile Agent Core
- 🌐 **MCP Integration**: Uses Agno's robust MCP client
- 📦 **One-Command Setup**: Install and run with simple commands
- 🎨 **Beautiful UI**: Modern chat interface via Agent UI
- 📊 **Structured Results**: Returns formatted prospect information
- 🔧 **Flexible Deployment**: Run all-in-one or individual services

---

## Installation Options

### Option 1: One-Command Install (Recommended)

Installs egile-agent-core + egile-mcp-prospectfinder + this package:

```bash
# Windows
.\install.bat

# macOS/Linux  
./install.sh
```

### Option 2: Manual Install

```bash
pip install egile-agent-core
pip install egile-mcp-prospectfinder
pip install -e ".[all]"
```

### Option 3: From PyPI (when published)

```bash
pip install egile-agent-prospectfinder[all]
```

---

## Running the System

### Easiest Way: All-in-One

```bash
prospectfinder
```

This starts:
- MCP server on http://localhost:8001
- AgentOS on http://localhost:8000

Then in another terminal:
```bash
cd ../agent-ui && pnpm dev
```

### Individual Services

```bash
# MCP server only
prospectfinder-mcp

# AgentOS only  
prospectfinder-agent

# Agent UI
cd ../agent-ui && pnpm dev
```

### Using Python Directly

```bash
# All services
python -m egile_agent_prospectfinder

# Individual services
python -m egile_agent_prospectfinder.run_mcp
python -m egile_agent_prospectfinder.run_agent
```

---

## What You Get

After installation, you have a complete AI agent system:

| Component | What it does | Port |
|-----------|--------------|------|
| **MCP Server** | Searches for prospects using Google/Brave/DuckDuckGo | 8001 |
| **AgentOS** | AI agent with chat capabilities | 8000 |
| **Agent UI** | Beautiful web chat interface | 3000 |

**Chat with the agent:**
- "Find marketing companies in Belgium"
- "Search for construction businesses in France"  
- "Show me healthcare providers in Germany"

---

## Advanced Usage

For detailed examples and advanced usage, see:
- 📖 [QUICKSTART.md](QUICKSTART.md) - Get started in 2 commands
- 💡 [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - Chat examples and code samples  
- 🔧 [API Reference](#api-reference) - Programmatic usage
- 🔌 [Plugin Development](src/egile_agent_prospectfinder/plugin.py) - Customize the plugin

### Prerequisites

- Python 3.10 or higher
- [egile-agent-core](https://github.com/yourusername/egile-agent-core) installed
- [egile-mcp-prospectfinder](https://github.com/yourusername/egile-mcp-prospectfinder) server running

### Install from PyPI

```bash
pip install egile-agent-prospectfinder
```

### Install from Source

```bash
git clone https://github.com/yourusername/egile-agent-prospectfinder.git
cd egile-agent-prospectfinder
pip install -e .
```

### Development Installation

```bash
pip install -e ".[dev]"
```

## Quick Start

### 1. Start the MCP Server

First, ensure the ProspectFinder MCP server is running:

```bash
cd egile-mcp-prospectfinder
python -m egile_mcp_prospectfinder.server --transport sse --port 8000
```

### 2. Use the Plugin with Egile Agent Core

#### Automatic Discovery

The plugin is automatically discovered via entry points when installed:

```python
from egile_agent_core import Agent
from egile_agent_core.plugins import discover_plugins

# Discover and register all installed plugins
plugins = discover_plugins()

# Create agent with auto-discovered plugins
agent = Agent(
    name="ProspectAgent",
    model="gpt-4",
    plugins=plugins
)

# Use the agent
response = await agent.process("Find marketing companies in Belgium")
```

#### Manual Registration

You can also manually register the plugin:

```python
from egile_agent_core import Agent
from egile_agent_prospectfinder import ProspectFinderPlugin

# Create the plugin
plugin = ProspectFinderPlugin(
    mcp_host="localhost",
    mcp_port=8000
)

# Create agent with the plugin
agent = Agent(
    name="ProspectAgent",
    model="gpt-4",
    plugins=[plugin]
)

# Initialize the agent (this starts the plugin)
await agent.start()

# Use the plugin directly
results = await plugin.find_prospects(
    sector="Marketing",
    country="Belgium",
    limit=10
)
print(results)
```

### 3. Direct Usage Without Agent

You can also use the plugin's functionality directly:

```python
from egile_agent_prospectfinder import ProspectFinderPlugin

# Create and initialize the plugin
plugin = ProspectFinderPlugin(
    mcp_host="localhost",
    mcp_port=8000
)

# Note: You need to manually initialize the client### Programmatic Usage (Without Chat UI)

```python
from egile_agent_prospectfinder import ProspectFinderPlugin
from egile_agent_core import Agent

# Create plugin
plugin = ProspectFinderPlugin(
    mcp_host="localhost",
    mcp_port=8001  # Note: MCP runs on 8001 when using prospectfinder command
)

# Initialize with a dummy agent
agent = Agent(name="dummy", model="gpt-4")
await plugin.on_agent_start(agent)

# Search for prospects
results = await plugin.find_prospects(
    sector="Construction",
    country="France",
    limit=5
)
print(results)

# Clean up
await plugin.cleanup()
```

---

## Configuration

### Environment Variables (Optional)

### Environment Variables (Optional)

Create a `.env` file in the project root:

```env
# Required: AI Model API Key
OPENAI_API_KEY=your_openai_key
# OR
XAI_API_KEY=your_xai_key

# Optional: Search API Keys (uses DuckDuckGo by default)
GOOGLE_API_KEY=your_google_key
GOOGLE_CSE_ID=your_cse_id
BRAVE_API_KEY=your_brave_key

# Optional: Custom Ports
MCP_PORT=8001
AGENTOS_PORT=8000
```

### Plugin Options

- `mcp_host` (str): Host where the MCP server is running (default: "localhost")
- `mcp_port` (int): Port where the MCP server is running (default: 8000)
- `mcp_transport` (str): Transport mode, currently only "sse" is supported (default: "sse")
- `timeout` (float): Request timeout in seconds (default: 30.0)

### Example with Custom Configuration

```python
plugin = ProspectFinderPlugin(
    mcp_host="192.168.1.100",
    mcp_port=9000,
    timeout=60.0
)
```

## API Reference

### ProspectFinderPlugin

The main plugin class that integrates with Egile Agent Core.

#### Methods

- `find_prospects(sector: str, country: str = "Belgium", limit: int = 10) -> str`
  - Search for business prospects in a specific sector and country
  - Returns formatted results as a string

- `list_available_tools() -> list[dict[str, Any]]`
  - List all available tools from the MCP server
  - Returns a list of tool definitions

- `cleanup() -> None`
  - Clean up resources and close MCP client connection

### MCPClient

Low-level client for communicating with the MCP server using Agno's MCP client.

#### Methods

- `connect() -> None`
  - Establish connection to the MCP server
  
- `call_tool(tool_name: str, arguments: dict[str, Any] | None = None) -> str`
  - Call any tool on the MCP server
  - Returns the tool's response as a string

- `find_prospects(sector: str, country: str = "Belgium", limit: int = 10) -> str`
  - Convenience method for the find_prospects tool

- `list_tools() -> list[dict[str, Any]]`
  - List available tools on the MCP server

## Examples

### Example 1: Integration with Chat Agent

```python
from egile_agent_core import Agent
from egile_agent_prospectfinder import ProspectFinderPlugin

# Create plugin
plugin = ProspectFinderPlugin()

# Create agent
agent = Agent(
    name="BusinessDevelopmentAgent",
    model="gpt-4",
    plugins=[plugin],
    system_prompt="You are a business development assistant. Help users find potential clients."
)

# Start the agent
await agent.start()

# Chat with the agent
response = await agent.process("I need to find construction companies in Germany")
print(response)
```

### Example 2: Batch Processing

```python
from egile_agent_prospectfinder import ProspectFinderPlugin

plugin = ProspectFinderPlugin()

# Initialize
from egile_agent_core import Agent
agent = Agent(name="batch", model="gpt-4")
await plugin.on_agent_start(agent)

# Search multiple sectors
sectors = ["Marketing", "Construction", "Healthcare"]
country = "Belgium"

for sector in sectors:
    results = await plugin.find_prospects(sector, country, limit=5)
    print(f"\n{'='*50}")
    print(f"Results for {sector} in {country}")
    print('='*50)
    print(results)

await plugin.cleanup()
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black src/
ruff check src/
```

### Type Checking

```bash
mypy src/
```

## Architecture

This plugin follows the Egile Agent Core plugin architecture:

1. **Plugin Interface**: ImplAgno's `MCPClient` for robust MCP server communicationins`
2. **Lifecycle Hooks**: Uses `on_agent_start()` for initialization and connection setup
3. **Entry Points**: Registered via `pyproject.toml` for automatic discovery
4. **MCP Integration**: Uses an async MCP client to communicate with the server via SSE

## Troubleshooting

### MCP Server Connection Failed

If you see connection errors:

1. Ensure the MCP server is running:
   ```bash
   python -m egile_mcp_prospectfinder.server --transport sse --port 8000
   ```

2. Check that the host and port match your configuration

3. Verify firewall settings allow connections on the specified port

### Plugin Not Discovered

If automatic discovery doesn't work:

1. Ensure the package is properly installed:
   ```bash
   pip install -e .
   ```

2. Check that entry points are registered:
   ```bash
   pip show egile-agent-prospectfinder
   ```

3. Try manual registration instead of automatic discovery

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details

## Links

- 📖 [QUICKSTART.md](QUICKSTART.md) - Get started in 2 commands
- 💡 [USAGE_EXAMPLES.md](USAGE_EXAMPLES.md) - Chat examples and code samples
- 📦 [COMPLETE_SETUP.md](COMPLETE_SETUP.md) - Full setup documentation
- 🔧 [INSTALL.md](INSTALL.md) - Detailed installation guide
- [Egile Agent Core](https://github.com/yourusername/egile-agent-core)
- [Egile MCP ProspectFinder](https://github.com/yourusername/egile-mcp-prospectfinder)
- [Model Context Protocol](https://github.com/modelcontextprotocol/specification)
