#!/bin/bash
# Start all ProspectFinder services

echo "========================================"
echo "Starting ProspectFinder Agent System"
echo "========================================"
echo
echo "This will start:"
echo "  - MCP Server (port 8001)"
echo "  - AgentOS Server (port 8000)"
echo
echo "After this starts, run in another terminal:"
echo "  cd ../agent-ui"
echo "  pnpm dev"
echo
echo "Then open: http://localhost:3000"
echo "========================================"
echo

python -m egile_agent_prospectfinder
