# Installation and Setup Guide

## Prerequisites

1. **Python 3.10+** installed
2. **egile-agent-core** package installed
3. **egile-mcp-prospectfinder** MCP server set up and running

## Step-by-Step Installation

### 1. Install egile-agent-core (if not already installed)

```bash
cd ../egile-agent-core
pip install -e .
```

### 2. Install egile-mcp-prospectfinder (if not already installed)

```bash
cd ../egile-mcp-prospectfinder
pip install -e .
```

### 3. Install egile-agent-prospectfinder

```bash
cd ../egile-agent-prospectfinder
pip install -e .
```

For development:
```bash
pip install -e ".[dev]"
```

### 4. Start the MCP Server

In a separate terminal:

```bash
cd ../egile-mcp-prospectfinder
python -m egile_mcp_prospectfinder.server --transport sse --port 8000
```

You should see output like:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 5. Verify Installation

Test that the plugin is discoverable:

```python
from egile_agent_core.plugins import discover_plugins

plugins = discover_plugins()
print([p.name for p in plugins])
# Should include 'prospectfinder'
```

### 6. Run the Example

```bash
python example.py
```

## Configuration

### Environment Variables

The MCP server (egile-mcp-prospectfinder) uses these environment variables:

- `GOOGLE_API_KEY`: Google Custom Search API key (optional)
- `GOOGLE_CSE_ID`: Google Custom Search Engine ID (optional)
- `BRAVE_API_KEY`: Brave Search API key (optional)

Create a `.env` file in the `egile-mcp-prospectfinder` directory:

```bash
GOOGLE_API_KEY=your_google_api_key
GOOGLE_CSE_ID=your_cse_id
BRAVE_API_KEY=your_brave_api_key
```

### Plugin Configuration

Configure the plugin when creating it:

```python
from egile_agent_prospectfinder import ProspectFinderPlugin

plugin = ProspectFinderPlugin(
    mcp_host="localhost",  # MCP server host
    mcp_port=8000,         # MCP server port
    timeout=30.0           # Request timeout in seconds
)
```

## Testing

Run the test suite:

```bash
# Install dev dependencies if not already installed
pip install -e ".[dev]"

# Run tests
pytest tests/

# Run with coverage
pytest --cov=egile_agent_prospectfinder tests/
```

## Troubleshooting

### Plugin Not Found

If `discover_plugins()` doesn't find the plugin:

1. Reinstall in editable mode:
   ```bash
   pip uninstall egile-agent-prospectfinder
   pip install -e .
   ```

2. Check entry points are registered:
   ```bash
   pip show egile-agent-prospectfinder
   ```

### Connection Errors

If you get "Connection refused" errors:

1. Ensure the MCP server is running:
   ```bash
   python -m egile_mcp_prospectfinder.server --transport sse --port 8000
   ```

2. Check the port matches your plugin configuration

3. Try accessing the server directly:
   ```bash
   curl http://localhost:8000
   ```

### Import Errors

If you get import errors:

1. Ensure all dependencies are installed:
   ```bash
   pip install egile-agent-core mcp httpx
   ```

2. Check your Python version:
   ```bash
   python --version  # Should be 3.10+
   ```

## Next Steps

1. Read the [README.md](README.md) for usage examples
2. Check the [example.py](example.py) for code samples
3. Review the [egile-agent-core documentation](../egile-agent-core/README.md)
4. Explore the [egile-mcp-prospectfinder documentation](../egile-mcp-prospectfinder/README.md)
