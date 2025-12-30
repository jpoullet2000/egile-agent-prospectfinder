"""Tests for the ProspectFinder plugin."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from egile_agent_prospectfinder import ProspectFinderPlugin, MCPClient


class TestMCPClient:
    """Tests for the MCP client."""

    @pytest.mark.asyncio
    async def test_client_initialization(self):
        """Test client initialization."""
        client = MCPClient(host="localhost", port=8000)
        assert client.host == "localhost"
        assert client.port == 8000

    @pytest.mark.asyncio
    async def test_find_prospects(self):
        """Test finding prospects through the client."""
        with patch("egile_agent_prospectfinder.mcp_client.AgnoMCPClient") as mock_client_class:
            # Setup mock client
            mock_agno_client = AsyncMock()
            mock_agno_client.call_tool.return_value = [{"text": "Test prospect results"}]
            mock_client_class.return_value = mock_agno_client
            
            client = MCPClient(host="localhost", port=8000)
            await client.connect()
            
            result = await client.find_prospects(
                sector="Marketing",
                country="Belgium",
                limit=10
            )
            
            assert "Test prospect results" in result
            mock_agno_client.call_tool.assert_called_once()


class TestProspectFinderPlugin:
    """Tests for the ProspectFinder plugin."""

    def test_plugin_properties(self):
        """Test plugin properties."""
        plugin = ProspectFinderPlugin()
        assert plugin.name == "prospectfinder"
        assert plugin.version == "0.1.0"
        assert "prospect" in plugin.description.lower()

    @pytest.mark.asyncio
    async def test_plugin_initialization(self):
        """Test plugin initialization with agent."""
        from egile_agent_core import Agent
        
        plugin = ProspectFinderPlugin(
            mcp_host="localhost",
            mcp_port=8000
        )
        
        # Create a minimal agent for testing
        agent = Agent(name="test", model="gpt-4")
        
        with patch.object(plugin, "_client") as mock_client:
            await plugin.on_agent_start(agent)
            assert plugin._agent == agent

    @pytest.mark.asyncio
    async def test_find_prospects(self):
        """Test finding prospects through the plugin."""
        plugin = ProspectFinderPlugin()
        
        # Mock the MCP client
        mock_client = AsyncMock()
        mock_client.find_prospects.return_value = "Test results"
        plugin._client = mock_client
        
        result = await plugin.find_prospects(
            sector="Marketing",
            country="Belgium",
            limit=5
        )
        
        assert result == "Test results"
        mock_client.find_prospects.assert_called_once_with(
            "Marketing", "Belgium", 5
        )

    @pytest.mark.asyncio
    async def test_message_processing(self):
        """Test message processing hook."""
        plugin = ProspectFinderPlugin()
        
        # Should return the message unchanged
        message = "Find marketing companies in Belgium"
        result = await plugin.on_message_received(message)
        assert result == message

    def test_get_tool_functions(self):
        """Test getting tool functions."""
        plugin = ProspectFinderPlugin()
        tools = plugin.get_tool_functions()
        
        assert "find_prospects" in tools
        assert "list_available_tools" in tools
        assert callable(tools["find_prospects"])
