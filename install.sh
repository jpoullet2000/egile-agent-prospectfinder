#!/bin/bash
# ProspectFinder Agent - One Command Installation
# This installs everything needed to run the ProspectFinder agent

set -e  # Exit on error

echo "========================================"
echo "ProspectFinder Agent - Installation"
echo "========================================"
echo

echo "Installing egile-agent-core..."
cd ../egile-agent-core
pip install -e .

echo
echo "Installing egile-mcp-prospectfinder..."
cd ../egile-mcp-prospectfinder
pip install -e .

echo
echo "Installing egile-agent-prospectfinder..."
cd ../egile-agent-prospectfinder
pip install -e ".[all]"

echo
echo "========================================"
echo "Installation Complete!"
echo "========================================"
echo
echo "To run the system:"
echo "  1. In one terminal:  prospectfinder"
echo "  2. In another terminal: cd ../agent-ui && pnpm dev"
echo
echo "Or run services separately:"
echo "  - MCP only:   prospectfinder-mcp"
echo "  - Agent only: prospectfinder-agent"
echo "  - UI:         cd ../agent-ui && pnpm dev"
echo
echo "Then open: http://localhost:3000"
echo "========================================"
