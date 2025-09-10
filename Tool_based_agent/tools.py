import requests
from datetime import datetime

class Tool:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

    def execute(self, params: dict) -> dict:
        raise NotImplementedError("Subclasses must implement execute method")

    def get_schema(self) -> dict:
        raise NotImplementedError("Subclasses must implement get_schema method")

class WeatherTool(Tool):
    def __init__(self, api_key: str):
        super().__init__("weather", "Get weather for any city")
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def execute(self, params: dict) -> dict:
        city = params.get("city", "Bengaluru")
        
        try:
            response = requests.get(self.base_url, params={
                "q": city,
                "appid": self.api_key,
                "units": "metric"
            })
            response.raise_for_status()
            data = response.json()
            
            return {
                "status": "success",
                "city": data.get("name"),
                "temperature": f"{data.get('main', {}).get('temp', 0):.1f}°C",
                "weather": data.get("weather", [{}])[0].get("description", "Unknown")
            }
        except Exception as e:
            return {"status": "error", "message": f"Weather error: {e}"}

    def get_schema(self) -> dict:
        return {
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name"}
                }
            }
        }

class DateTool(Tool):
    def __init__(self):
        super().__init__("date", "Get current date and time")

    def execute(self, params: dict) -> dict:
        now = datetime.now()
        return {
            "status": "success",
            "full_date": now.strftime("%A, %B %d, %Y"),
            "time": now.strftime("%I:%M %p"),
            "day": now.strftime("%A"),
            "year": now.strftime("%Y")
        }

    def get_schema(self) -> dict:
        return {
            "parameters": {
                "type": "object",
                "properties": {}
            }
        }
