"""Quick test script to verify the plugin works correctly."""

import asyncio
import sys


async def test_plugin():
    """Test the ProspectFinder plugin."""
    
    print("🔍 Testing Egile Agent ProspectFinder Plugin\n")
    
    # Test 1: Import the plugin
    print("Test 1: Importing plugin...")
    try:
        from egile_agent_prospectfinder import ProspectFinderPlugin, MCPClient
        print("✅ Plugin imported successfully\n")
    except ImportError as e:
        print(f"❌ Failed to import plugin: {e}")
        print("💡 Make sure to install the package: pip install -e .")
        return False
    
    # Test 2: Create plugin instance
    print("Test 2: Creating plugin instance...")
    try:
        plugin = ProspectFinderPlugin(
            mcp_host="localhost",
            mcp_port=8000
        )
        print(f"✅ Plugin created: {plugin.name} v{plugin.version}")
        print(f"   Description: {plugin.description}\n")
    except Exception as e:
        print(f"❌ Failed to create plugin: {e}")
        return False
    
    # Test 3: Check if MCP server is running
    print("Test 3: Checking MCP server connection...")
    try:
        # Try to create and connect the MCP client
        test_client = MCPClient(host="localhost", port=8000)
        await test_client.connect()
        await test_client.close()
        print("✅ MCP server is running and connectable\n")
    except Exception as e:
        print(f"⚠️  MCP server not reachable: {e}")
        print("💡 Start the server with:")
        print("   python -m egile_mcp_prospectfinder.server --transport sse --port 8000\n")
        return False
    
    # Test 4: Initialize the plugin
    print("Test 4: Initializing plugin with agent...")
    try:
        from egile_agent_core import Agent
        
        agent = Agent(
            name="TestAgent",
            model="gpt-4"
        )
        
        await plugin.on_agent_start(agent)
        print("✅ Plugin initialized successfully\n")
    except Exception as e:
        print(f"❌ Failed to initialize plugin: {e}")
        print("💡 Make sure egile-agent-core is installed")
        return False
    
    # Test 5: Search for prospects
    print("Test 5: Testing prospect search...")
    try:
        results = await plugin.find_prospects(
            sector="Marketing",
            country="Belgium",
            limit=3
        )
        
        print("✅ Prospect search successful!")
        print("\nResults preview:")
        print("-" * 60)
        # Print first 500 characters
        preview = results[:500] + "..." if len(results) > 500 else results
        print(preview)
        print("-" * 60)
        print()
    except Exception as e:
        print(f"❌ Prospect search failed: {e}")
        return False
    
    # Test 6: List available tools
    print("Test 6: Listing available tools...")
    try:
        tools = plugin.get_tool_functions()
        print(f"✅ Available tools: {', '.join(tools.keys())}\n")
    except Exception as e:
        print(f"❌ Failed to list tools: {e}")
        return False
    
    # Cleanup
    print("Cleaning up...")
    try:
        await plugin.cleanup()
        print("✅ Cleanup successful\n")
    except Exception as e:
        print(f"⚠️  Cleanup warning: {e}\n")
    
    return True


async def test_discovery():
    """Test plugin auto-discovery."""
    
    print("🔎 Testing Plugin Auto-Discovery\n")
    
    try:
        from egile_agent_core.plugins import discover_plugins
        
        print("Discovering installed plugins...")
        plugins = discover_plugins(register=False)
        
        plugin_names = [p.name for p in plugins]
        print(f"✅ Found {len(plugins)} plugin(s): {', '.join(plugin_names)}")
        
        if "prospectfinder" in plugin_names:
            print("✅ ProspectFinder plugin is discoverable!\n")
            return True
        else:
            print("⚠️  ProspectFinder plugin not found in discovered plugins")
            print("💡 Try reinstalling: pip install -e .\n")
            return False
            
    except Exception as e:
        print(f"❌ Discovery failed: {e}\n")
        return False


async def main():
    """Run all tests."""
    
    print("=" * 70)
    print("  EGILE AGENT PROSPECTFINDER - PLUGIN TEST SUITE")
    print("=" * 70)
    print()
    
    # Run discovery test
    discovery_ok = await test_discovery()
    
    print()
    print("=" * 70)
    print()
    
    # Run plugin test
    plugin_ok = await test_plugin()
    
    print()
    print("=" * 70)
    print("  TEST SUMMARY")
    print("=" * 70)
    
    if discovery_ok and plugin_ok:
        print("✅ All tests passed!")
        print("\n🎉 The plugin is ready to use!")
        print("\nNext steps:")
        print("  1. Check out example.py for usage examples")
        print("  2. Read README.md for detailed documentation")
        print("  3. Start building your prospect-finding agents!")
        return 0
    else:
        print("❌ Some tests failed")
        print("\n💡 Check the errors above and:")
        print("  1. Ensure all dependencies are installed")
        print("  2. Make sure the MCP server is running")
        print("  3. Verify the package is installed: pip install -e .")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
