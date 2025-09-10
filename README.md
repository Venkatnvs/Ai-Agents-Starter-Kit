## AI Agents Workspace

This repository contains two minimal, student-friendly AI agents:

- Tool-based Agent: simple tools embedded directly in the app
- MCP-based Agent: tools run as separate MCP servers via the Model Context Protocol (MCP)

### Repository Structure

- `Tool_based_agent/`: self-contained assistant with weather and date tools
- `MCP_Based_agent/`: assistant that connects to external MCP tool servers (date, weather, Playwright)

### Prerequisites

- Python 3.10+
- Pip
- Node.js 18+ (only for the MCP agent to use the Playwright MCP server via `npx`)

## Demo

- Video

https://github.com/user-attachments/assets/12887c75-5b87-4dac-97b5-94dd47ac10e6



### Quick Start

- Tool-based Agent: see `Tool_based_agent/README.md`
- MCP-based Agent: see `MCP_Based_agent/README.md`

### Environment Variables

Create a `.env` file in each project folder as described in the corresponding README. Common variables:

- `GEMINI_API_KEY`: Google Generative AI API key (Tool-based agent)
- `GOOGLE_API_KEY`: Google Generative AI API key (MCP-based agent)
- `OPENWEATHERMAP_API_KEY`: OpenWeatherMap API key (both)

### Getting Help

If you run into issues, check the per-agent README troubleshooting sections first. Ensure your API keys are set and you are using compatible Python/Node versions.
