# Simple AI Agent (Tool-based)

A minimal AI assistant with built-in weather and date tools — great for learning.

## Prerequisites

- Python 3.10+
- A Google Generative AI API key
- An OpenWeatherMap API key

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your API keys:
```
GEMINI_API_KEY=your_gemini_api_key
OPENWEATHERMAP_API_KEY=your_openweathermap_api_key
```

## Run

```bash
python main.py
```

You should see prompts like "Ask me about weather or time!". Type `exit` to quit.

## Examples

- "What's the weather in Paris?"
- "What's the date?"

## How it works

- `main.py`: CLI app that wires the model and tools
- `custom_mcp.py`: lightweight wrapper that routes model tool-calls to Python functions
- `tools.py`: implements `WeatherTool` and `DateTool`

The model (`gemini-2.5-flash-lite`) is configured in `main.py`.

## Troubleshooting

- Make sure your `.env` contains valid keys
- If weather calls fail, verify `OPENWEATHERMAP_API_KEY` and your internet connection
- Use Python 3.10+ and a clean virtual environment if you see dependency issues
