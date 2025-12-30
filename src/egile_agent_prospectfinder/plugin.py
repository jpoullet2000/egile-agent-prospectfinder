"""ProspectFinder plugin for Egile Agent Core."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any, Optional

from egile_agent_core.plugins import Plugin

from .mcp_client import MCPClient

if TYPE_CHECKING:
    from egile_agent_core.agent import Agent

logger = logging.getLogger(__name__)


class ProspectFinderPlugin(Plugin):
    """
    Plugin that provides prospect finding capabilities via the MCP server.
    
    This plugin integrates with the egile-mcp-prospectfinder MCP server to enable
    AI agents to search for business prospects in specific sectors and countries.
    
    Example:
        ```python
        from egile_agent_core import Agent
        from egile_agent_prospectfinder import ProspectFinderPlugin
        
        # Create and register the plugin
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
        
        # The agent can now search for prospects
        response = await agent.process("Find marketing companies in Belgium")
        ```
    """

    def __init__(
        self,
        mcp_host: str = "localhost",
        mcp_port: int = 8000,
        mcp_transport: str = "sse",
        timeout: float = 30.0,
    ):
        """
        Initialize the ProspectFinder plugin.

        Args:
            mcp_host: Host where the MCP server is running
            mcp_port: Port where the MCP server is running
            mcp_transport: Transport mode ("sse" or "stdio")
            timeout: Request timeout in seconds
        """
        self.mcp_host = mcp_host
        self.mcp_port = mcp_port
        self.mcp_transport = mcp_transport
        self.timeout = timeout
        self._client: Optional[MCPClient] = None
        self._agent: Optional[Agent] = None

    @property
    def name(self) -> str:
        """Plugin name for registration."""
        return "prospectfinder"

    @property
    def description(self) -> str:
        """Plugin description."""
        return (
            "Provides business prospect finding capabilities via MCP server. "
            "Can search for companies in specific sectors and countries."
        )

    @property
    def version(self) -> str:
        """Plugin version."""
        return "0.1.0"

    async def on_agent_start(self, agent: Agent) -> None:
        """
        Called when the agent starts.
        
        Initializes the MCP client connection.

        Args:
            agent: The Agent instance that is starting
        """
        self._agent = agent
        try:
            self._client = MCPClient(
                transport=self.mcp_transport,
                host=self.mcp_host,
                port=self.mcp_port,
                timeout=self.timeout,
            )
            # Connect to the MCP server
            await self._client.connect()
            logger.info(
                f"ProspectFinder plugin connected to MCP server at "
                f"{self.mcp_host}:{self.mcp_port}"
            )
        except Exception as e:
            logger.error(f"Failed to connect to MCP server: {e}")
            raise

    async def find_prospects(
        self, sector: str, country: str = "Belgium", limit: int = 10
    ) -> str:
        """
        Search for business prospects.

        Args:
            sector: Business sector to search for (e.g., "Marketing", "Construction")
            country: Country to search in (default: "Belgium")
            limit: Maximum number of results (default: 10)

        Returns:
            Formatted string with search results

        Raises:
            RuntimeError: If MCP client is not initialized
        """
        if not self._client:
            raise RuntimeError(
                "MCP client not initialized. Ensure the plugin is properly started."
            )

        logger.info(
            f"Searching for prospects: sector={sector}, country={country}, limit={limit}"
        )
        
        try:
            results = await self._client.find_prospects(sector, country, limit)
            logger.info(f"Successfully retrieved prospects for {sector} in {country}")
            return results
        except Exception as e:
            logger.error(f"Error finding prospects: {e}")
            raise

    async def on_message_received(self, message: str, **kwargs: Any) -> str:
        """
        Process incoming messages to detect prospect search requests.
        
        This hook can be used to automatically detect when the user is asking
        for prospect information and enrich the message context.

        Args:
            message: The original user message
            **kwargs: Additional context

        Returns:
            The processed message (potentially enriched)
        """
        # Keywords that might indicate a prospect search request
        prospect_keywords = [
            "find prospects",
            "search for companies",
            "businesses in",
            "companies in",
            "find businesses",
            "prospect",
            "leads",
        ]

        message_lower = message.lower()
        if any(keyword in message_lower for keyword in prospect_keywords):
            logger.info("Detected potential prospect search request")
            # Could add context or metadata here
            
        return message

    async def list_available_tools(self) -> list[dict[str, Any]]:
        """
        List all available tools from the MCP server.

        Returns:
            List of tool definitions from the MCP server
        """
        if not self._client:
            raise RuntimeError("MCP client not initialized")
            
        return await self._client.list_tools()

    async def cleanup(self) -> None:
        """Clean up resources and close connections."""
        if self._client:
            await self._client.close()
            logger.info("ProspectFinder plugin disconnected from MCP server")

    def get_tool_functions(self) -> dict[str, Any]:
        """
        Get the tool functions that can be called by the agent.
        
        Returns:
            Dictionary mapping function names to their implementations
        """
        return {
            "find_prospects": self.find_prospects,
            "list_available_tools": self.list_available_tools,
        }
