@echo off
REM ProspectFinder Agent - One Command Installation
REM This installs everything needed to run the ProspectFinder agent

echo ========================================
echo ProspectFinder Agent - Installation
echo ========================================
echo.

echo Installing egile-agent-core...
cd ..\egile-agent-core
pip install -e .
if errorlevel 1 (
    echo ERROR: Failed to install egile-agent-core
    exit /b 1
)

echo.
echo Installing egile-mcp-prospectfinder...
cd ..\egile-mcp-prospectfinder
pip install -e .
if errorlevel 1 (
    echo ERROR: Failed to install egile-mcp-prospectfinder
    exit /b 1
)

echo.
echo Installing egile-agent-prospectfinder...
cd ..\egile-agent-prospectfinder
pip install -e ".[all]"
if errorlevel 1 (
    echo ERROR: Failed to install egile-agent-prospectfinder
    exit /b 1
)

echo.
echo ========================================
echo Installation Complete!
echo ========================================
echo.
echo To run the system:
echo   1. In one terminal:  prospectfinder
echo   2. In another terminal: cd ..\agent-ui ^&^& pnpm dev
echo.
echo Or run services separately:
echo   - MCP only:   prospectfinder-mcp
echo   - Agent only: prospectfinder-agent
echo   - UI:         cd ..\agent-ui ^&^& pnpm dev
echo.
echo Then open: http://localhost:3000
echo ========================================
