# math_server.py
from mcp.server.fastmcp import FastMCP
import time
import signal
import sys

# Handle SIGINT (Ctrl+C) gracefully
def signal_handler(sig, frame):
    print("Shutting down server gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

mcp = FastMCP(
    name="Maths",
    host="127.0.0.1",
    port=5000,
    # Add this to make the server more resilient
    timeout=30  # Increase timeout to 30 seconds
)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a: int, b: int) -> int:
    """Multiply two numbers"""
    return a * b
    
if __name__ == "__main__":
    try:
        print("Starting MCP server 'Math' on 127.0.0.1:5000")
        mcp.run(transport="sse")
    except Exception as e:
        print(f"Error: {e}")
        # Sleep before exiting to give time for error logs
        time.sleep(5)
