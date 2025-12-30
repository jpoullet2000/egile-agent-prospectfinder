"""Example: Using ProspectFinder plugin with an agent."""

import asyncio
from egile_agent_core import Agent
from egile_agent_prospectfinder import ProspectFinderPlugin


async def main():
    """Example of using the ProspectFinder plugin."""
    
    # Create the plugin
    plugin = ProspectFinderPlugin(
        mcp_host="localhost",
        mcp_port=8000
    )
    
    # Create an agent with the plugin
    agent = Agent(
        name="BusinessDevelopmentAgent",
        model="gpt-4",
        plugins=[plugin],
        system_prompt=(
            "You are a business development assistant. "
            "Help users find potential clients and business prospects."
        )
    )
    
    # Start the agent (this initializes all plugins)
    await agent.start()
    
    # Example 1: Direct plugin usage
    print("=" * 60)
    print("Example 1: Direct Plugin Usage")
    print("=" * 60)
    
    results = await plugin.find_prospects(
        sector="Marketing",
        country="Belgium",
        limit=5
    )
    print(results)
    
    # Example 2: Through agent chat
    print("\n" + "=" * 60)
    print("Example 2: Through Agent Chat")
    print("=" * 60)
    
    # Process a message (the agent will use the plugin if needed)
    response = await agent.process(
        "Find me 3 construction companies in France"
    )
    print(response)
    
    # Clean up
    await plugin.cleanup()
    print("\n✅ Example completed successfully!")


if __name__ == "__main__":
    # Note: Make sure the MCP server is running:
    # python -m egile_mcp_prospectfinder.server --transport sse --port 8000
    
    asyncio.run(main())
