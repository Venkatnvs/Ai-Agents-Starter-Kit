import asyncio
import os
import json
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import MemorySaver
from dotenv import load_dotenv

load_dotenv()

memory = MemorySaver()

system_prompt = """
You are an intelligent, resourceful, and efficient AI assistant with access to a comprehensive set of tools.
And always prefer not to ask questions to the user unless necessary.
Your primary goal is to provide accurate, up-to-date, and helpful responses while maintaining a friendly and professional tone. 
Follow these guidelines:
1. Tool Usage Priority:
   - Always use tools for real-time data, calculations, and external actions
   - Only use internal knowledge for general facts that don't require current data
   - When in doubt, prefer using tools over assumptions
2. Response Format:
   - Keep responses concise (100-200 words)
   - Present information in a clear, structured manner
   - Include relevant context and sources when using tools
USE playwright tool for web browsing and doing actions on the web
Always try to use playwright tool for web browsing search or anything related to the web.
"""

def read_config():
    with open("config.json", "r") as f:
        return json.load(f)

async def main():
    config = read_config()
    mcp_servers = config.get("mcpServers", {})
    
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.0-flash",
        temperature=0,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )
    
    tools = []
    
    async with AsyncExitStack() as stack:
        for server_name, server_info in mcp_servers.items():
            server_params = StdioServerParameters(
                command=server_info["command"],
                args=server_info["args"],
                env=server_info.get("env", {})
            )
            
            try:
                read, write = await stack.enter_async_context(stdio_client(server_params))
                session = await stack.enter_async_context(ClientSession(read, write))
                await session.initialize()
                server_tools = await load_mcp_tools(session)
                tools.extend(server_tools)
                print(f"Loaded {len(server_tools)} tools from {server_name}")
            except Exception as e:
                print(f"Failed to connect to {server_name}: {e}")
        
        if not tools:
            print("No tools loaded. Exiting.")
            return
            
        agent = create_react_agent(llm, tools, prompt=system_prompt, checkpointer=memory)
        print("\nSimple MCP Assistant Ready!")
        print("Ask me about weather or time! Type 'quit' to exit.\n")
        
        while True:
            query = input("You: ").strip()
            if query.lower() == "quit":
                print("Goodbye!")
                break
            if not query:
                continue
                
            try:
                response = await agent.ainvoke({"messages": query},{"configurable": {"thread_id": "1"}, "recursion_limit": 50})
                print(f"Assistant: {response['messages'][-1].content}\n")
            except Exception as e:
                print(f"Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())