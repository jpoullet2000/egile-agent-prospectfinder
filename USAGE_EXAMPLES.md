# Usage Examples

## Example 1: Find Marketing Companies

**User:** Find marketing companies in Belgium

**Agent Response:**
```
Found 10 prospects for Marketing in Belgium:

1. Digital Marketing Agency Brussels
   URL: https://example.com/marketing-agency
   Snippet: Leading digital marketing agency specializing in SEO, PPC, and social media...
   Potential Gen AI Use Cases: Content generation, Campaign optimization, Customer insights

2. Creative Solutions Marketing
   URL: https://example.com/creative-marketing
   Snippet: Full-service marketing firm helping B2B companies grow...
   Potential Gen AI Use Cases: Ad copy generation, Market analysis, Lead scoring
   
[... more results ...]
```

## Example 2: Construction Sector Search

**User:** I need 5 construction companies in France

**Agent Response:**
```
Found 5 prospects for Construction in France:

1. BTP Services France
   URL: https://example.com/btp-services
   Snippet: General contractor for residential and commercial projects...
   Potential Gen AI Use Cases: Project planning, Safety compliance, Documentation

[... more results ...]
```

## Example 3: Multi-Country Search

**User:** Compare healthcare companies in Belgium and Netherlands

**Agent Response:**
```
I'll search for healthcare companies in both countries.

**Belgium Healthcare:**
[search results for Belgium]

**Netherlands Healthcare:**
[search results for Netherlands]

Key differences:
- Belgium has more specialized clinics
- Netherlands focuses on digital health solutions
```

## Example 4: Specific Use Case

**User:** Find companies that could benefit from AI chatbots

**Agent Response:**
```
I'll search for customer service-heavy sectors. Let me check:
1. E-commerce companies
2. Financial services
3. Telecom providers

[Proceeds to search and list relevant companies]
```

## Example 5: Programmatic Usage

Instead of using the UI, you can use the agent programmatically:

```python
from egile_agent_core.models import OpenAI
from egile_agent_prospectfinder import ProspectFinderPlugin

# Create plugin
plugin = ProspectFinderPlugin()

# Direct API call
results = await plugin.find_prospects(
    sector="Healthcare",
    country="Germany",
    limit=10
)

print(results)
```

## Example 6: Integration with Custom Agent

```python
from egile_agent_core import Agent
from egile_agent_core.models import XAI
from egile_agent_prospectfinder import ProspectFinderPlugin

# Create custom agent with prospectfinder
plugin = ProspectFinderPlugin()

agent = Agent(
    name="sales-assistant",
    model=XAI(model="grok-beta"),
    instructions=[
        "You are a sales development representative.",
        "Help find qualified leads for our SaaS product.",
        "Focus on companies in tech-forward industries.",
    ],
    plugins=[plugin]
)

await agent.start()

# Now agent can find prospects automatically
response = await agent.process(
    "Find 10 SaaS companies in the Netherlands that might need our product"
)
```

## Example 7: Batch Processing

```python
sectors = ["Marketing", "Construction", "Healthcare", "Technology"]
country = "Belgium"

for sector in sectors:
    results = await plugin.find_prospects(sector, country, 5)
    
    # Save to database, send emails, generate reports, etc.
    save_to_crm(sector, results)
```

## Example 8: Custom Search Criteria

While the agent uses natural language, you can also be very specific:

**User:** Find B2B SaaS companies in Belgium with 10-50 employees that focus on marketing automation

**Agent:** I'll search for marketing technology companies in Belgium...

[The agent will use find_prospects with appropriate parameters and filter/interpret results]

## Example 9: Follow-up Questions

**User:** Find marketing companies in Belgium  
**Agent:** [Returns 10 companies]

**User:** Tell me more about the first one  
**Agent:** [Provides details about the first company]

**User:** Find similar companies in France  
**Agent:** [Searches for marketing companies in France]

## Example 10: Export Results

**User:** Find construction companies in Germany and export to CSV

**Agent:** [Searches and provides results]

*Note: CSV export would require additional implementation, but the agent can provide structured data that you can easily parse and export.*

## Chat Examples in Agent UI

### Natural Conversation

```
You: Hi! I'm looking for potential clients in the construction sector.
Agent: I'd be happy to help! Which country are you targeting?
You: Belgium
Agent: Great! How many prospects would you like?
You: Let's start with 10
Agent: [Searches and returns 10 construction companies in Belgium]
```

### Quick Request

```
You: marketing companies belgium
Agent: [Immediately searches and returns results]
```

### Refinement

```
You: Find marketing companies in Belgium
Agent: [Returns 10 results]
You: Show me only digital marketing agencies
Agent: [Filters or re-searches with more specific criteria]
```

## API Endpoints

When running AgentOS, you can also use HTTP API:

```bash
# Get agent info
curl http://localhost:8000/v1/agents

# Send message to agent
curl -X POST http://localhost:8000/v1/agents/prospectfinder/sessions \
  -H "Content-Type: application/json" \
  -d '{"message": "Find marketing companies in Belgium"}'
```

## Tips for Best Results

1. **Be specific about location**: "Belgium" works better than "EU"
2. **Use clear sector names**: "Marketing", "Construction", "Healthcare"
3. **Specify quantity**: "5 companies" or "top 10 prospects"
4. **Ask follow-up questions**: The agent maintains context
5. **Natural language works**: No need for exact syntax

## Advanced: Custom Instructions

You can customize the agent's behavior by modifying the instructions in [run_server.py](src/egile_agent_prospectfinder/run_server.py):

```python
"instructions": [
    "Focus on companies with 50+ employees",
    "Prioritize tech-savvy industries",
    "Highlight companies that mention AI or automation",
],
```
