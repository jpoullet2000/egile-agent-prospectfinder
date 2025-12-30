# Quick Reference - Egile Agent ProspectFinder

## Installation
```bash
pip install -e .
```

## Start MCP Server
```bash
cd ../egile-mcp-prospectfinder
python -m egile_mcp_prospectfinder.server --transport sse --port 8000
```

## Basic Usage

### Auto-Discovery
```python
from egile_agent_core import Agent
from egile_agent_core.plugins import discover_plugins

plugins = discover_plugins()
agent = Agent(name="Agent", model="gpt-4", plugins=plugins)
await agent.start()
```

### Manual Setup
```python
from egile_agent_prospectfinder import ProspectFinderPlugin

plugin = ProspectFinderPlugin(mcp_host="localhost", mcp_port=8000)
# Use with agent or directly
```

### Search for Prospects
```python
results = await plugin.find_prospects(
    sector="Marketing",
    country="Belgium", 
    limit=10
)
```

## API Reference

### ProspectFinderPlugin

**Properties:**
- `name` → "prospectfinder"
- `version` → "0.1.0"
- `description` → Plugin description

**Methods:**
- `find_prospects(sector, country="Belgium", limit=10)` → Search results
- `list_available_tools()` → List MCP tools
- `cleanup()` → Close connections

**Lifecycle Hooks:**
- `on_agent_start(agent)` → Initialize MCP client
- `on_message_received(message)` → Process messages

### MCPClient

**Constructor:**
```python
MCPClient(transport="sse", host="localhost", port=8000, timeout=30.0)
```

**Methods:**
- `connect()` → Establish connection to MCP server
- `call_tool(tool_name, arguments)` → Call any MCP tool
- `find_prospects(sector, country, limit)` → Search prospects
- `list_tools()` → List available tools
- `close()` → Close client

**Note:** Uses Agno's `MCPClient` internally for robust MCP communication.

## Configuration

```python
plugin = ProspectFinderPlugin(
    mcp_host="localhost",     # MCP server host
    mcp_port=8000,            # MCP server port  
    mcp_transport="sse",      # Transport mode
    timeout=30.0              # Request timeout (seconds)
)
```

## Testing

```bash
# Run integration test
python test_plugin_integration.py

# Run unit tests
pytest tests/

# Run example
python example.py
```

## Common Issues

**Plugin not discovered:**
```bash
pip uninstall egile-agent-prospectfinder
pip install -e .
```

**Connection refused:**
- Check MCP server is running
- Verify host:port match configuration

**Import errors:**
```bash
pip install egile-agent-core agno
```

## File Structure

```
src/egile_agent_prospectfinder/
  ├── __init__.py          # Exports
  ├── plugin.py            # Main plugin
  └── mcp_client.py        # MCP client
```

## Entry Point

Registered in `pyproject.toml`:
```toml
[project.entry-points."egile_agent_core.plugins"]
prospectfinder = "egile_agent_prospectfinder:ProspectFinderPlugin"
```

## Example Workflow

1. Start MCP server
2. Create plugin instance
3. Register with agent
4. Agent can now find prospects automatically

## Links

- [Full README](README.md)
- [Installation Guide](INSTALL.md)  
- [Package Structure](PACKAGE_STRUCTURE.md)
- [Example Code](example.py)
