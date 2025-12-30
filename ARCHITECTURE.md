# System Architecture

## Overview

```
┌──────────────────────────────────────────────────────────────┐
│                         User's Browser                         │
│                     http://localhost:3000                      │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │ HTTP/SSE
                           │
┌──────────────────────────▼───────────────────────────────────┐
│                      Agent UI (Next.js)                        │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  - Chat Interface                                     │    │
│  │  - Session Management                                 │    │
│  │  - Real-time Streaming                                │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │ POST /v1/agents/prospectfinder/sessions
                           │ SSE streaming responses
                           │
┌──────────────────────────▼───────────────────────────────────┐
│              AgentOS Server (FastAPI/Uvicorn)                 │
│                  http://localhost:8000                         │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  ProspectFinder Agent                                 │    │
│  │  ┌────────────────────────────────────────────┐      │    │
│  │  │  - Instructions & System Prompt            │      │    │
│  │  │  - LLM (GPT-4/Grok)                       │      │    │
│  │  │  - Plugin: ProspectFinderPlugin           │      │    │
│  │  └────────────────────────────────────────────┘      │    │
│  └──────────────────────────────────────────────────────┘    │
└──────────────────────────┬───────────────────────────────────┘
                           │
                           │ MCP Protocol (SSE)
                           │ call_tool("find_prospects", {...})
                           │
┌──────────────────────────▼───────────────────────────────────┐
│              MCP Server (FastMCP/Uvicorn)                     │
│                  http://localhost:8001                         │
│  ┌──────────────────────────────────────────────────────┐    │
│  │  ProspectFinder Tools                                 │    │
│  │  ┌────────────────────────────────────────────┐      │    │
│  │  │  @mcp.tool()                               │      │    │
│  │  │  def find_prospects(sector, country, ...): │      │    │
│  │  │      - SearchService                       │      │    │
│  │  │      - Google Custom Search API            │      │    │
│  │  │      - Brave Search API                    │      │    │
│  │  │      - DuckDuckGo Search                   │      │    │
│  │  │      - Fallback to mock data               │      │    │
│  │  └────────────────────────────────────────────┘      │    │
│  └──────────────────────────────────────────────────────┘    │
└────────────────────────────────────────────────────────────┘
```

## Component Details

### 1. Agent UI (Port 3000)
- **Technology:** Next.js, React, TailwindCSS
- **Location:** `../agent-ui`
- **Start:** `cd ../agent-ui && pnpm dev`
- **Features:**
  - Modern chat interface
  - Session management
  - Real-time streaming
  - Multi-agent support

### 2. AgentOS Server (Port 8000)
- **Technology:** FastAPI, Agno, Uvicorn
- **Location:** `src/egile_agent_prospectfinder/run_server.py`
- **Start:** `prospectfinder` or `prospectfinder-agent`
- **Features:**
  - RESTful API endpoints
  - SSE streaming support
  - Agent lifecycle management
  - Plugin integration
  - Auto session creation

### 3. MCP Server (Port 8001)
- **Technology:** FastMCP, Uvicorn
- **Location:** `egile-mcp-prospectfinder`
- **Start:** `prospectfinder` or `prospectfinder-mcp`
- **Features:**
  - MCP protocol implementation
  - Multiple search providers
  - Tool registration
  - Error handling & fallbacks

### 4. ProspectFinder Plugin
- **Technology:** Python, Agno MCP Client
- **Location:** `src/egile_agent_prospectfinder/plugin.py`
- **Features:**
  - Plugin lifecycle hooks
  - MCP client wrapper
  - Agent integration
  - Auto-discovery via entry points

## Data Flow

### User Query → Response

```
1. User types: "Find marketing companies in Belgium"
   └─> Agent UI sends POST to /v1/agents/prospectfinder/sessions

2. AgentOS receives message
   └─> Creates/retrieves session
   └─> Passes to ProspectFinder Agent

3. Agent (LLM) decides to use find_prospects tool
   └─> ProspectFinderPlugin.find_prospects() called

4. Plugin sends MCP request to server
   └─> MCPClient.call_tool("find_prospects", {
         sector: "Marketing",
         country: "Belgium",
         limit: 10
       })

5. MCP Server executes tool
   └─> SearchService tries providers in order:
       1. Google Custom Search (if API key)
       2. Brave Search (if API key)
       3. DuckDuckGo
       4. Mock data (fallback)

6. Results flow back:
   MCP Server → Plugin → Agent → AgentOS → UI

7. User sees formatted results in chat
```

## Communication Protocols

### Agent UI ↔ AgentOS
- **Protocol:** HTTP + SSE (Server-Sent Events)
- **Format:** JSON
- **Streaming:** Yes (real-time response chunks)

### AgentOS ↔ MCP Server (via Plugin)
- **Protocol:** MCP over SSE
- **Format:** JSON-RPC 2.0
- **Client:** Agno's MCPClient
- **Transport:** HTTP

## Deployment Options

### Option 1: All-in-One (Development)
```bash
# Single command starts MCP + AgentOS
prospectfinder

# Separate terminal for UI
cd ../agent-ui && pnpm dev
```

### Option 2: Separate Services (Production)
```bash
# Terminal 1 - MCP Server
prospectfinder-mcp

# Terminal 2 - AgentOS
prospectfinder-agent

# Terminal 3 - UI
cd ../agent-ui && pnpm dev
```

### Option 3: Docker (Future)
```yaml
services:
  mcp-server:
    image: prospectfinder-mcp
    ports: ["8001:8001"]
  
  agentos:
    image: prospectfinder-agent
    ports: ["8000:8000"]
    depends_on: [mcp-server]
  
  ui:
    image: prospectfinder-ui
    ports: ["3000:3000"]
    depends_on: [agentos]
```

## Environment Variables

### AgentOS (.env)
```env
# Required
OPENAI_API_KEY=sk-...
# OR
XAI_API_KEY=xai-...

# Optional
MCP_HOST=localhost
MCP_PORT=8001
AGENTOS_PORT=8000
```

### MCP Server (.env in egile-mcp-prospectfinder)
```env
# Optional - uses DuckDuckGo by default
GOOGLE_API_KEY=...
GOOGLE_CSE_ID=...
BRAVE_API_KEY=...
```

## Security Considerations

### Production Deployment
1. **CORS:** Configure allowed origins
2. **API Keys:** Use secrets manager
3. **Rate Limiting:** Add rate limits to endpoints
4. **HTTPS:** Use reverse proxy (nginx, Caddy)
5. **Authentication:** Add auth to AgentOS endpoints

### Example nginx config
```nginx
server {
    listen 443 ssl;
    server_name prospectfinder.example.com;
    
    location / {
        proxy_pass http://localhost:3000;  # UI
    }
    
    location /api/ {
        proxy_pass http://localhost:8000;  # AgentOS
    }
}
```

## Scaling

### Horizontal Scaling
- **MCP Server:** Stateless, easy to replicate
- **AgentOS:** Sessions in DB, can scale with load balancer
- **UI:** Static files, CDN-ready

### Vertical Scaling
- Increase uvicorn workers
- Use Redis for session storage
- Cache search results

## Monitoring

### Health Checks
```bash
# MCP Server
curl http://localhost:8001/health

# AgentOS
curl http://localhost:8000/health

# UI
curl http://localhost:3000
```

### Logs
- AgentOS: stdout/stderr (capture with systemd)
- MCP Server: stdout/stderr
- UI: Next.js logs

## Troubleshooting

See [QUICKSTART.md](QUICKSTART.md#troubleshooting) for common issues.
