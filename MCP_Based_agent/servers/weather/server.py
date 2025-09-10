import os
import requests
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Weather Tool")

@mcp.tool()
def get_weather(city: str = "Bengaluru"):
    """Get weather for any city"""
    API_KEY = os.getenv("OPENWEATHERMAP_API_KEY")
    if not API_KEY:
        return {"error": "Weather API key is required"}
        
    try:
        response = requests.get("https://api.openweathermap.org/data/2.5/weather", params={
            "q": city,
            "appid": API_KEY,
            "units": "metric"
        })
        response.raise_for_status()
        data = response.json()
        
        return {
            "city": data.get("name"),
            "temperature": f"{data.get('main', {}).get('temp', 0):.1f}°C",
            "weather": data.get("weather", [{}])[0].get("description", "Unknown")
        }
    except Exception as e:
        return {"error": f"Weather error: {e}"}

if __name__ == "__main__":
    mcp.run(transport='stdio')