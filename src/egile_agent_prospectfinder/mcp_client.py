"""MCP client for connecting to egile-mcp-prospectfinder server."""

from __future__ import annotations

import logging
from typing import Any, Optional

import httpx

logger = logging.getLogger(__name__)


class MCPClient:
    """
    Simple HTTP client for communicating with the ProspectFinder MCP server.
    
    Supports SSE (HTTP) transport to call MCP tools.
    """

    def __init__(
        self,
        transport: str = "sse",
        host: str = "localhost",
        port: int = 8000,
        timeout: float = 30.0,
    ):
        """
        Initialize the MCP client.

        Args:
            transport: Transport mode - "sse" (HTTP) only
            host: Server host
            port: Server port
            timeout: Request timeout in seconds
        """
        self.transport = transport
        self.host = host
        self.port = port
        self.timeout = timeout
        self.base_url = f"http://{host}:{port}"
        self._client: Optional[httpx.AsyncClient] = None

    async def __aenter__(self) -> MCPClient:
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()

    async def connect(self) -> None:
        """Establish connection to the MCP server."""
        if self._client is not None:
            return  # Already connected
            
        if self.transport == "sse":
            logger.info(f"Connecting to MCP server at {self.base_url}")
            self._client = httpx.AsyncClient(timeout=self.timeout)
        else:
            raise ValueError(f"Unsupported transport: {self.transport}")

    async def close(self) -> None:
        """Close the client connection."""
        if self._client is not None:
            await self._client.aclose()
            self._client = None
            logger.info("MCP client connection closed")

    async def call_tool(
        self, tool_name: str, arguments: Optional[dict[str, Any]] = None
    ) -> str:
        """
        Call a tool on the MCP server via HTTP.

        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments as a dictionary

        Returns:
            The tool response as a string

        Raises:
            RuntimeError: If client is not connected
            httpx.HTTPError: If the HTTP request fails
        """
        if self._client is None:
            await self.connect()
        
        if self._client is None:
            raise RuntimeError("Failed to connect to MCP server")

        try:
            logger.info(f"Calling MCP tool '{tool_name}' with arguments: {arguments}")
            
            # Use FastMCP's HTTP endpoint
            # FastMCP exposes tools at /call_tool endpoint
            response = await self._client.post(
                f"{self.base_url}/call_tool",
                json={
                    "tool_name": tool_name,
                    "arguments": arguments or {}
                }
            )
            response.raise_for_status()
            
            result = response.json()
            logger.info(f"Successfully called tool '{tool_name}'")
            
            # FastMCP returns the tool result
            if isinstance(result, str):
                return result
            elif isinstance(result, dict) and "result" in result:
                return str(result["result"])
            
            return str(result)

        except httpx.HTTPError as e:
            logger.error(f"HTTP error calling MCP tool '{tool_name}': {e}")
            raise
        except Exception as e:
            logger.error(f"Error calling MCP tool '{tool_name}': {e}")
            raise

    async def find_prospects(
        self, sector: str, country: str = "Belgium", limit: int = 10
    ) -> str:
        """
        Search for business prospects using the MCP server.

        Args:
            sector: Business sector to search for
            country: Country to search in
            limit: Maximum number of results

        Returns:
            Formatted search results as a string
        """
        arguments = {
            "sector": sector,
            "country": country,
            "limit": limit,
        }
        
        return await self.call_tool("find_prospects", arguments)

    async def list_tools(self) -> list[dict[str, Any]]:
        """
        List available tools on the MCP server.

        Returns:
            List of tool definitions
        """
        if self._client is None:
            await self.connect()
            
        if self._client is None:
            raise RuntimeError("Failed to connect to MCP server")
            
        try:
            response = await self._client.get(f"{self.base_url}/tools")
            response.raise_for_status()
            result = response.json()
            return result if isinstance(result, list) else []
        except Exception as e:
            logger.error(f"Error listing MCP tools: {e}")
            return []
