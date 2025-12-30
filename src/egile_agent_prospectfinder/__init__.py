"""
Egile Agent ProspectFinder Plugin

A complete AI agent system for finding business prospects.
Includes MCP server integration, AgentOS, and web UI support.
"""

from .plugin import ProspectFinderPlugin
from .mcp_client import MCPClient
from .run_server import run_all, run_agent_only, run_mcp_only

__version__ = "0.1.0"

__all__ = [
    "ProspectFinderPlugin",
    "MCPClient",
    "run_all",
    "run_agent_only",
    "run_mcp_only",
]
