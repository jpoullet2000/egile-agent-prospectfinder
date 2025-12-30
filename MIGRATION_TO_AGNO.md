# Migration to Agno MCP Client

## Overview

The plugin has been updated to use **Agno's built-in MCP client** instead of a custom implementation. This provides:

✅ **Better reliability** - Agno's MCP client is well-tested and production-ready  
✅ **Less code to maintain** - No custom HTTP/JSON-RPC handling  
✅ **Better integration** - Seamless integration with egile-agent-core's Agno foundation  
✅ **Future-proof** - Agno handles MCP protocol updates automatically

## What Changed

### Dependencies

**Before:**
```toml
dependencies = [
    "egile-agent-core>=0.1.0",
    "mcp>=1.0.0",
    "httpx>=0.27.0",
]
```

**After:**
```toml
dependencies = [
    "egile-agent-core>=0.1.0",
    "agno>=2.3.0",
]
```

### MCP Client Implementation

**Before:** Custom HTTP client with manual JSON-RPC handling  
**After:** Wrapper around `agno.tools.mcp.MCPClient`

### Key Benefits

1. **Simplified code**: ~170 lines → ~160 lines (cleaner, more focused)
2. **Better error handling**: Agno handles retries and connection management
3. **Protocol compliance**: Agno ensures MCP spec compliance
4. **Consistency**: Same MCP client used across all Agno-based agents

## API Compatibility

The public API remains **100% compatible**. No changes needed to your code:

```python
from egile_agent_prospectfinder import ProspectFinderPlugin

# Still works exactly the same
plugin = ProspectFinderPlugin(mcp_host="localhost", mcp_port=8000)
results = await plugin.find_prospects("Marketing", "Belgium", 10)
```

## Migration Steps

If you already have the package installed:

```bash
# 1. Reinstall with updated dependencies
pip uninstall egile-agent-prospectfinder
pip install -e .

# 2. Verify it works
python test_plugin_integration.py
```

## Technical Details

### Connection Management

**Before:**
```python
self.client = httpx.AsyncClient(timeout=timeout)
```

**After:**
```python
self._client = AgnoMCPClient(server_url=server_url)
await self._client.connect()  # Explicit connection
```

### Tool Calling

**Before:** Manual JSON-RPC payload construction and HTTP POST
**After:** Direct method call on Agno client

```python
# Agno handles the protocol
result = await self._client.call_tool(
    tool_name=tool_name,
    arguments=arguments or {}
)
```

## No Breaking Changes

All existing code continues to work:
- ✅ Plugin discovery
- ✅ Agent integration
- ✅ Direct plugin usage
- ✅ All methods and properties
- ✅ Error handling
- ✅ Async context managers

## Why This Matters

1. **Leverages existing dependencies**: egile-agent-core already uses Agno
2. **Reduces attack surface**: Less custom networking code
3. **Better support**: Agno's MCP client is actively maintained
4. **Future features**: Get new MCP features automatically via Agno updates

## Questions?

- Check the updated [README.md](README.md)
- Run the integration tests: `python test_plugin_integration.py`
- Review the [mcp_client.py](src/egile_agent_prospectfinder/mcp_client.py) source
