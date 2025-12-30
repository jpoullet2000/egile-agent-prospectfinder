# Package Structure

The egile-agent-prospectfinder package has been successfully created with the following structure:

```
egile-agent-prospectfinder/
├── .gitignore                      # Git ignore patterns
├── LICENSE                         # MIT License
├── README.md                       # Comprehensive documentation
├── INSTALL.md                      # Installation and setup guide
├── pyproject.toml                  # Package configuration with entry points
├── example.py                      # Usage examples
├── test_plugin_integration.py      # Integration test script
├── src/
│   └── egile_agent_prospectfinder/
│       ├── __init__.py             # Package initialization
│       ├── plugin.py               # Main ProspectFinderPlugin class
│       └── mcp_client.py           # MCP client for server communication
└── tests/
    ├── __init__.py
    └── test_plugin.py              # Unit tests
```

## Key Components

### 1. Plugin Class (`plugin.py`)
- Extends `egile_agent_core.plugins.Plugin`
- Implements lifecycle hooks (`on_agent_start`, `on_message_received`)
- Provides `find_prospects()` method for searching
- Auto-cleanup on agent shutdown

### 2. MCP Client (`mcp_client.py`)
- Async HTTP client for MCP server communication
- Supports SSE (Server-Sent Events) transport
- Handles JSON-RPC protocol
- Error handling and logging

### 3. Package Configuration (`pyproject.toml`)
- Entry point registration: `egile_agent_core.plugins`
- Dependencies: egile-agent-core, mcp, httpx
- Development dependencies: pytest, black, ruff, mypy

### 4. Documentation
- **README.md**: Full documentation with API reference and examples
- **INSTALL.md**: Step-by-step installation guide
- **example.py**: Working code examples
- **test_plugin_integration.py**: Verification script

## Installation

```bash
cd egile-agent-prospectfinder
pip install -e .
```

## Quick Test

1. Start the MCP server:
   ```bash
   cd ../egile-mcp-prospectfinder
   python -m egile_mcp_prospectfinder.server --transport sse --port 8000
   ```

2. Run the integration test:
   ```bash
   python test_plugin_integration.py
   ```

3. Try the example:
   ```bash
   python example.py
   ```

## Usage

### Automatic Discovery
```python
from egile_agent_core import Agent
from egile_agent_core.plugins import discover_plugins

plugins = discover_plugins()
agent = Agent(name="MyAgent", model="gpt-4", plugins=plugins)
```

### Manual Registration
```python
from egile_agent_core import Agent
from egile_agent_prospectfinder import ProspectFinderPlugin

plugin = ProspectFinderPlugin(mcp_host="localhost", mcp_port=8000)
agent = Agent(name="MyAgent", model="gpt-4", plugins=[plugin])

await agent.start()
results = await plugin.find_prospects("Marketing", "Belgium", 10)
```

## Features

✅ Plugin auto-discovery via entry points
✅ Async MCP client with SSE transport
✅ Lifecycle management (initialization, cleanup)
✅ Comprehensive error handling and logging
✅ Type hints and documentation
✅ Unit tests and integration tests
✅ Example code and documentation

## Next Steps

1. Install the package in development mode
2. Start the MCP server
3. Run the integration test to verify everything works
4. Try the examples
5. Build your own agents using the plugin!
