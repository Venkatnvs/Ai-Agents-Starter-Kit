# Simple MCP Agent

A minimal MCP (Model Context Protocol) based AI assistant — perfect for learning how AI tools can be modular and externalized.

## What is MCP?

MCP lets AI models talk to external tools as separate processes ("servers"). This app connects to:

- Date Tool (Python)
- Weather Tool (Python)
- Playwright MCP (via `npx @playwright/mcp`)

## Prerequisites

- Python 3.10+
- Node.js 18+ (required for the Playwright MCP server)
- A Google Generative AI API key
- An OpenWeatherMap API key

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` in this folder:
```
GOOGLE_API_KEY=your_google_api_key
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
```

3. Review `config.json`

`config.json` defines the MCP servers started via stdio:

```json
{
  "mcpServers": {
    "date_tool": { "command": "python", "args": ["servers/date_tool/server.py"] },
    "weather": {
      "command": "python",
      "args": ["servers/weather/server.py"],
      "env": { "OPENWEATHERMAP_API_KEY": "${{OPENWEATHERMAP_API_KEY}}" }
    },
    "playwright": { "command": "npx", "args": ["@playwright/mcp@latest"] }
  }
}
```

Environment variables like `OPENWEATHERMAP_API_KEY` are pulled from your `.env` at runtime.

## Run

```bash
python main.py
```

You should see logs like `Loaded X tools from ...`. Type `quit` to exit.

## Examples

- "What's the weather in Bengaluru?"
- "What day is it today?"
- "Open `https://example.com` and tell me the title" (uses Playwright MCP)

## Notes and Troubleshooting

- Ensure Node 18+ is installed so `npx @playwright/mcp` can run
- The Playwright MCP may download packages on first run — allow it internet access
- If weather fails, confirm `OPENWEATHERMAP_API_KEY` is set in `.env`
- If no tools load, check `config.json` paths and your Python/Node versions

## Why MCP vs Regular Tools?

- **Regular Tools**: functions live inside your app
- **MCP**: tools are separate processes you can swap in/out without changing app code
- **Benefits**: modularity, isolation, language/runtime flexibility
