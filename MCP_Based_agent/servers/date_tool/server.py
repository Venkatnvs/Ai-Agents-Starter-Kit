from datetime import datetime
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Date Tool")

@mcp.tool()
def get_date():
    """Get current date and time"""
    now = datetime.now()
    return {
        "full_date": now.strftime("%A, %B %d, %Y"),
        "time": now.strftime("%I:%M %p"),
        "day": now.strftime("%A"),
        "year": now.strftime("%Y")
    }

if __name__ == "__main__":
    mcp.run(transport='stdio')