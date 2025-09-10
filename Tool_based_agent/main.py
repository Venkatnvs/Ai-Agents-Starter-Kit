import os
from dotenv import load_dotenv
from custom_mcp import CustomMCP
from tools import WeatherTool, DateTool
import google.generativeai as genai

load_dotenv()

tools = [
    WeatherTool(api_key=os.getenv("OPENWEATHERMAP_API_KEY")),
    DateTool()
]

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash-lite")

assistant = CustomMCP(model=model, tools=tools)

def main():
    print("🤖 Simple AI Assistant")
    print("Ask me about weather or time!")
    print("Type 'exit' to quit.\n")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Goodbye")
            break
        if not user_input.strip():
            continue
            
        response = assistant.chat(user_input)
        print(f"Assistant: {response}\n")

if __name__ == "__main__":
    main()