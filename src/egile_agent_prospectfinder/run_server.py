"""ProspectFinder Agent - Complete setup with AgentOS integration.

This example creates a ProspectFinder agent that integrates with:
- egile-agent-core (AgentOS server)
- egile-mcp-prospectfinder (MCP server for prospect search)
- agent-ui (Web interface)

To use:
1. Install: pip install -e .[all]
2. Configure: Set API keys in .env (optional, uses DuckDuckGo by default)
3. Run: python -m egile_agent_prospectfinder.run_all

Or run services individually:
- MCP Server: python -m egile_agent_prospectfinder.run_mcp
- Agent Server: python -m egile_agent_prospectfinder.run_agent  
- Agent UI: cd ../agent-ui && pnpm dev
"""

import asyncio
import logging
import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv
import uvicorn

from egile_agent_core.models import OpenAI, XAI
from egile_agent_core.server import create_agent_os
from egile_agent_prospectfinder import ProspectFinderPlugin

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


def create_prospectfinder_agent_os():
    """Create AgentOS with ProspectFinder plugin."""
    
    # Create the ProspectFinder plugin
    plugin = ProspectFinderPlugin(
        mcp_host=os.getenv("MCP_HOST", "localhost"),
        mcp_port=int(os.getenv("MCP_PORT", "8001")),  # MCP on 8001, AgentOS on 8000
    )
    
    # Configure agent with the plugin
    agents_config = [
        {
            "name": "prospectfinder",
            "model": XAI(model="grok-4-1-fast-reasoning") if os.getenv("XAI_API_KEY") else OpenAI(model="gpt-4o-mini"),
            "description": "AI agent that finds business prospects in specific sectors and countries.",
            "instructions": [
                "You are a business development assistant specialized in finding prospects.",
                "You have access to a prospect finder tool that can search for companies.",
                "When users ask about companies, businesses, or prospects, use the find_prospects tool.",
                "Provide clear, actionable information about potential business prospects.",
                "Always specify the sector and country when searching.",
            ],
            "plugins": [plugin],
            "markdown": True,
        },
    ]
    
    # Create AgentOS with correct parameter name
    agent_os = create_agent_os(
        agents_config=agents_config,
        os_id="prospectfinder-os",
        description="ProspectFinder AgentOS - Find business prospects with AI",
    )
    
    return agent_os


async def start_mcp_server():
    """Start the MCP server in a subprocess."""
    logger.info("Starting MCP server on port 8001...")
    
    # Find egile-mcp-prospectfinder
    mcp_module = "egile_mcp_prospectfinder.server"
    
    process = subprocess.Popen(
        [sys.executable, "-m", mcp_module, "--transport", "sse", "--port", "8001"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Wait a bit for server to start
    await asyncio.sleep(2)
    
    if process.poll() is not None:
        stderr = process.stderr.read() if process.stderr else ""
        logger.error(f"MCP server failed to start: {stderr}")
        return None
    
    logger.info("✅ MCP server started successfully")
    return process


def start_agent_ui():
    """Instructions to start Agent UI."""
    ui_path = Path(__file__).parent.parent.parent / "agent-ui"
    
    logger.info("\n" + "="*60)
    logger.info("To start the Agent UI, run in a separate terminal:")
    logger.info("="*60)
    if ui_path.exists():
        logger.info(f"cd {ui_path}")
        logger.info("pnpm dev")
    else:
        logger.info("cd /path/to/agent-ui")
        logger.info("pnpm dev")
    logger.info("\nThen open: http://localhost:3000")
    logger.info("Connect to: http://localhost:8000")
    logger.info("="*60 + "\n")


def run_all():
    """Run all services (MCP server + AgentOS)."""
    logger.info("🚀 Starting ProspectFinder Agent System...")
    logger.info("="*60)
    
    # Start MCP server
    mcp_process = None
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        mcp_process = loop.run_until_complete(start_mcp_server())
        
        if mcp_process is None:
            logger.error("Failed to start MCP server. Exiting.")
            return
        
        # Show UI instructions
        start_agent_ui()
        
        # Create and run AgentOS
        logger.info("Starting AgentOS on port 8000...")
        agent_os = create_prospectfinder_agent_os()
        app = agent_os.get_app()
        
        logger.info("✅ AgentOS started successfully")
        logger.info("\n" + "="*60)
        logger.info("System Ready!")
        logger.info("="*60)
        logger.info("MCP Server:   http://localhost:8001")
        logger.info("AgentOS API:  http://localhost:8000")
        logger.info("Agent UI:     http://localhost:3000 (start separately)")
        logger.info("="*60 + "\n")
        
        # Run uvicorn
        uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
        
    except KeyboardInterrupt:
        logger.info("\n🛑 Shutting down...")
    finally:
        if mcp_process:
            mcp_process.terminate()
            mcp_process.wait()
            logger.info("✅ MCP server stopped")


def run_agent_only():
    """Run only the AgentOS server (assumes MCP is running separately)."""
    logger.info("🚀 Starting AgentOS on port 8000...")
    logger.info("(Connecting to MCP server at localhost:8001)")
    
    agent_os = create_prospectfinder_agent_os()
    app = agent_os.get_app()
    
    logger.info("\n" + "="*60)
    logger.info("AgentOS Ready!")
    logger.info("="*60)
    logger.info("AgentOS API:  http://localhost:8000")
    logger.info("MCP Server:   http://localhost:8001 (must be running)")
    logger.info("Agent UI:     http://localhost:3000 (start separately)")
    logger.info("="*60 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")


def run_mcp_only():
    """Run only the MCP server."""
    from egile_mcp_prospectfinder import server
    
    logger.info("🚀 Starting MCP server on port 8001...")
    
    # Run the MCP server
    server.mcp.run(transport="sse", port=8001, host="0.0.0.0")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="ProspectFinder Agent System")
    parser.add_argument(
        "--mode",
        choices=["all", "agent", "mcp"],
        default="all",
        help="What to run: 'all' (MCP+AgentOS), 'agent' (AgentOS only), 'mcp' (MCP only)"
    )
    
    args = parser.parse_args()
    
    if args.mode == "all":
        run_all()
    elif args.mode == "agent":
        run_agent_only()
    elif args.mode == "mcp":
        run_mcp_only()
