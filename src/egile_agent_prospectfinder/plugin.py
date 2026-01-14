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
        mcp_transport: str = "stdio",
        mcp_command: Optional[str] = None,
        timeout: float = 30.0,
        use_mcp: bool = False,
    ):
        """
        Initialize the ProspectFinder plugin.

        Args:
            mcp_host: Host where the MCP server is running (for SSE transport)
            mcp_port: Port where the MCP server is running (for SSE transport)
            mcp_transport: Transport mode - "stdio" (recommended) or "sse"
            mcp_command: Command to start MCP server (for stdio transport)
            timeout: Request timeout in seconds
            use_mcp: If True, use MCP client; if False, use direct search_service (default: False for Windows compatibility)
        """
        self.mcp_host = mcp_host
        self.mcp_port = mcp_port
        self.mcp_transport = mcp_transport
        self.mcp_command = mcp_command or "python -m egile_mcp_prospectfinder.server"
        self.timeout = timeout
        self.use_mcp = use_mcp
        self._client: Optional[MCPClient] = None
        self._search_service = None
        self._agent: Optional[Agent] = None

    @property
    def name(self) -> str:
        """Plugin name for registration."""
        return "prospectfinder"

    @property
    def description(self) -> str:
        """Plugin description."""
        return (
            "Provides business prospect finding capabilities via direct search service. "
            "Can search for companies in specific sectors and countries."
        )

    @property
    def version(self) -> str:
        """Plugin version."""
        return "0.1.0"

    @property
    def mcp_server_module(self) -> str:
        """MCP server module path."""
        return "egile_mcp_prospectfinder.server"

    async def on_agent_start(self, agent: Agent) -> None:
        """
        Called when the agent starts.
        
        Connects to the MCP server or initializes direct search service.

        Args:
            agent: The Agent instance that is starting
        """
        self._agent = agent
        
        if self.use_mcp:
            # Use MCP client (external compatibility mode)
            try:
                self._client = MCPClient(
                    transport=self.mcp_transport,
                    host=self.mcp_host,
                    port=self.mcp_port,
                    command=self.mcp_command,
                    timeout=self.timeout,
                )
                await self._client.connect()
                logger.info(f"ProspectFinder plugin connected to MCP server via {self.mcp_transport}")
            except Exception as e:
                logger.error(f"Failed to connect to MCP server: {e}")
                raise
        else:
            # Use direct mode (faster, more reliable)
            from egile_mcp_prospectfinder.search_service import SearchService
            self._search_service = SearchService()
            logger.info("ProspectFinder plugin initialized in direct mode (using search_service)")

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
            RuntimeError: If plugin is not initialized
        """
        logger.info(
            f"Searching for prospects: sector={sector}, country={country}, limit={limit}"
        )
        
        try:
            if self.use_mcp:
                # Use MCP client
                if not self._client:
                    raise RuntimeError("MCP client not initialized. Call on_agent_start first.")
                result = await self._client.find_prospects(
                    sector=sector, country=country, limit=limit
                )
            else:
                # Use direct search service
                if not self._search_service:
                    raise RuntimeError("Search service not initialized. Call on_agent_start first.")
                
                # Call search_service directly (synchronous)
                results = self._search_service.search_prospects(sector, country, limit)
                
                # Return compact structured data that the LLM will format
                if not results:
                    result = f"No prospects found for {sector} in {country}."
                else:
                    # Compact format - just title, URL, and key details
                    result = f"Found {len(results)} {sector} prospects in {country}:\n\n"
                    for i, res in enumerate(results, 1):
                        result += f"{i}. {res['title']} - {res['link']}\n"
            
            logger.info(f"Search completed: {len(result)} characters")
            return result
        except Exception as e:
            error_msg = f"Failed to search for prospects: {str(e)}"
            logger.error(error_msg)
            raise RuntimeError(error_msg)

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
    
    def get_tools(self) -> list[dict[str, Any]]:
        """
        Get OpenAI-compatible tool definitions for function calling.
        
        Returns:
            List of tool definitions in OpenAI function calling format
        """
        return [
            {
                "type": "function",
                "function": {
                    "name": "find_prospects",
                    "description": "Search for business prospects in a specific sector and country. Returns detailed information about companies including names, descriptions, and contact details.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "sector": {
                                "type": "string",
                                "description": "The business sector to search for (e.g., 'Marketing', 'Construction', 'Technology', 'Healthcare', 'Finance', 'fintech')",
                            },
                            "country": {
                                "type": "string",
                                "description": "The country to search in (e.g., 'Belgium', 'France', 'Netherlands')",
                                "default": "Belgium",
                            },
                            "limit": {
                                "type": "integer",
                                "description": "Maximum number of results to return (default: 10, max: 50)",
                                "default": 10,
                            },
                        },
                        "required": ["sector"],
                    },
                },
            }
        ]    
    async def execute_task_direct(self, task: str) -> str:
        """
        Execute task using direct tool calling, bypassing the agent framework.
        
        This is a workaround for framework limitations with async tool results.
        Directly invokes search service to generate a complete prospects report.
        
        Args:
            task: Task description containing search parameters
            
        Returns:
            Complete prospects report as markdown string
        """
        logger.info("Executing prospect search using direct tool calling...")
        
        import re
        from datetime import datetime
        
        report_parts = []
        report_parts.append("# Business Prospects Report\n")
        report_parts.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        
        try:
            # Parse task to extract search parameters
            country = "Belgium"  # Default
            
            # Try to find country in task
            country_match = re.search(r'country:\s*([A-Za-z\s]+)', task, re.IGNORECASE)
            if country_match:
                country = country_match.group(1).strip()
            elif "Belgium" in task or "belgian" in task.lower():
                country = "Belgium"
            
            # Try to find sectors
            sectors = []
            if "financial" in task.lower() or "finance" in task.lower():
                sectors.extend(["financial services", "banking", "fintech", "insurance"])
            if "marketing" in task.lower():
                sectors.append("marketing")
            if "technology" in task.lower() or "tech" in task.lower():
                sectors.append("technology")
            
            # If no specific sectors found, extract from task
            sector_match = re.search(r'sector:\s*([^.\n]+)', task, re.IGNORECASE)
            if sector_match:
                sector_text = sector_match.group(1).strip()
                sectors.extend([s.strip() for s in sector_text.split(',')])
            
            # Default to finance if nothing found
            if not sectors:
                sectors = ["finance"]
            
            report_parts.append(f"## Search Parameters\n")
            report_parts.append(f"- **Country**: {country}\n")
            report_parts.append(f"- **Sectors**: {', '.join(sectors)}\n\n")
            
            # Search for prospects in each sector
            for sector in sectors[:4]:  # Limit to 4 searches to avoid rate limits
                try:
                    logger.info(f"Searching for prospects in {sector} sector in {country}...")
                    result = await self.find_prospects(sector=sector, country=country, limit=5)
                    
                    report_parts.append(f"## {sector.title()} Sector\n\n")
                    report_parts.append(result)
                    report_parts.append("\n\n")
                    
                except Exception as e:
                    logger.warning(f"Failed to search {sector}: {e}")
                    report_parts.append(f"## {sector.title()} Sector\n\n")
                    report_parts.append(f"*Search failed: {str(e)}*\n\n")
            
            # Add engagement recommendations
            report_parts.append("## Engagement Recommendations\n\n")
            report_parts.append("Based on the prospects found:\n\n")
            report_parts.append("1. **Prioritize financial services and fintech companies** - They are more likely to need AI/tech solutions\n")
            report_parts.append("2. **Focus on mid-sized companies** - They have budget but are still agile enough to adopt new technologies\n")
            report_parts.append("3. **Highlight automation and efficiency gains** - Key value propositions for financial sector\n")
            report_parts.append("4. **Research company websites** - Visit the links to understand their current tech stack and pain points\n")
            report_parts.append("5. **LinkedIn outreach** - Connect with decision makers in IT, Operations, or Digital Transformation roles\n\n")
            
            # Add next steps
            report_parts.append("## Next Steps\n\n")
            report_parts.append("1. Review and prioritize the prospects based on company size and industry alignment\n")
            report_parts.append("2. Research each company's recent news and technology initiatives\n")
            report_parts.append("3. Identify key decision makers via LinkedIn\n")
            report_parts.append("4. Prepare personalized outreach messages highlighting relevant use cases\n")
            report_parts.append("5. Schedule follow-up research for additional sectors if needed\n")
            
            final_report = "".join(report_parts)
            logger.info(f"Direct prospectfinder execution completed, report length: {len(final_report)} characters")
            return final_report
            
        except Exception as e:
            logger.error(f"Direct prospectfinder execution failed: {e}", exc_info=True)
            raise RuntimeError(f"Direct prospectfinder execution failed: {e}")