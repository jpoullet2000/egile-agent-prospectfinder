"""MCP client for connecting to egile-mcp-prospectfinder server."""

from __future__ import annotations

import logging
from typing import Any, Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp.client.sse import sse_client

logger = logging.getLogger(__name__)


class MCPClient:
    """
    MCP client for communicating with the ProspectFinder MCP server.
    
    Supports both stdio (recommended) and SSE transports.
    """

    def __init__(
        self,
        transport: str = "stdio",
        host: str = "localhost",
        port: int = 8000,
        command: Optional[str] = None,
        timeout: float = 30.0,
    ):
        """
        Initialize the MCP client.

        Args:
            transport: Transport mode - "stdio" (recommended) or "sse"
            host: Server host (for SSE transport)
            port: Server port (for SSE transport)
            command: Command to start MCP server (for stdio transport)
            timeout: Request timeout in seconds
        """
        self.transport = transport
        self.host = host
        self.port = port
        self.command = command
        self.timeout = timeout
        self.base_url = f"http://{host}:{port}/sse"  # For SSE
        self._session: Optional[ClientSession] = None
        self._exit_stack: Optional[AsyncExitStack] = None

    async def __aenter__(self) -> MCPClient:
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.close()

    async def connect(self) -> None:
        """Establish connection to the MCP server."""
        if self._session is not None:
            return  # Already connected
            
        self._exit_stack = AsyncExitStack()
        
        if self.transport == "stdio":
            # Use stdio transport - spawn server as subprocess
            if not self.command:
                raise ValueError("command is required for stdio transport")
            
            logger.info(f"Starting MCP server via stdio: {self.command}")
            
            # Parse command into list
            import shlex
            command_list = shlex.split(self.command)
            
            server_params = StdioServerParameters(
                command=command_list[0],
                args=command_list[1:],
                env=None
            )
            
            stdio_transport = await self._exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            
            self._session = await self._exit_stack.enter_async_context(
                ClientSession(stdio_transport[0], stdio_transport[1])
            )
            
            await self._session.initialize()
            logger.info("MCP client connected via stdio and initialized")
            
        elif self.transport == "sse":
            # Use SSE transport - connect to existing server
            logger.info(f"Connecting to MCP server at {self.base_url}")
            
            sse_transport = await self._exit_stack.enter_async_context(
                sse_client(self.base_url)
            )
            
            self._session = await self._exit_stack.enter_async_context(
                ClientSession(sse_transport[0], sse_transport[1])
            )
            
            await self._session.initialize()
            logger.info("MCP client connected via SSE and initialized")
        else:
            raise ValueError(f"Unsupported transport: {self.transport}")

    async def close(self) -> None:
        """Close the MCP client connection."""
        if self._exit_stack is not None:
            await self._exit_stack.aclose()
            self._exit_stack = None
            self._session = None
            logger.info("MCP client connection closed")

    async def call_tool(
        self, tool_name: str, arguments: Optional[dict[str, Any]] = None
    ) -> str:
        """
        Call a tool on the MCP server using the MCP SDK with timeout protection.

        Args:
            tool_name: Name of the tool to call
            arguments: Tool arguments as a dictionary

        Returns:
            The tool response as a string
        """
        if not self._session:
            raise RuntimeError("MCP client not connected. Call connect() first.")
        
        arguments = arguments or {}
        logger.info(f"🔌 MCP CLIENT: Calling tool '{tool_name}' with arguments: {arguments}")
        
        try:
            import asyncio
            
            # Add aggressive timeout to prevent hanging
            result = await asyncio.wait_for(
                self._session.call_tool(tool_name, arguments=arguments),
                timeout=self.timeout
            )
            
            # Extract text content from result
            if hasattr(result, 'content') and result.content:
                # result.content is a list of TextContent or ImageContent objects
                text_parts = []
                for content_item in result.content:
                    if hasattr(content_item, 'text'):
                        text_parts.append(content_item.text)
                result_text = '\n'.join(text_parts)
            else:
                result_text = str(result)
            
            logger.info(f"🔌 MCP CLIENT: Tool completed, {len(result_text)} chars returned")
            return result_text
            
        except asyncio.TimeoutError:
            error_msg = f"Tool '{tool_name}' timed out after {self.timeout}s"
            logger.error(f"🔌 MCP CLIENT: {error_msg}")
            raise TimeoutError(error_msg)
        except Exception as e:
            logger.error(f"🔌 MCP CLIENT: Tool '{tool_name}' failed: {type(e).__name__}: {e}")
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
        if self._session is None:
            await self.connect()
            
        if self._session is None:
            raise RuntimeError("Failed to initialize MCP session")
            
        try:
            result = await self._session.list_tools()
            # Convert MCP tool definitions to dict format
            return [
                {
                    "name": tool.name,
                    "description": tool.description or "",
                    "inputSchema": tool.inputSchema if hasattr(tool, 'inputSchema') else {}
                }
                for tool in result.tools
            ] if hasattr(result, 'tools') else []
        except Exception as e:
            logger.error(f"Error listing MCP tools: {e}")
            return []
