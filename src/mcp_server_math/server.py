from typing import Annotated
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    ErrorData,
    GetPromptResult,
    Prompt,
    PromptArgument,
    PromptMessage,
    TextContent,
    Tool,
    INVALID_PARAMS,
    INTERNAL_ERROR,
)
from pydantic import BaseModel, Field

class MathOperation(BaseModel):
    """Parameters for math operations."""
    a: Annotated[int, Field(description="First number")]
    b: Annotated[int, Field(description="Second number")]

async def serve() -> None:
    """Run the math MCP server."""
    server = Server("math-mcp")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="add",
                description="Adds two numbers.",
                inputSchema=MathOperation.model_json_schema(),
            ),
            Tool(
                name="multiply",
                description="Multiplies two numbers.",
                inputSchema=MathOperation.model_json_schema(),
            ),
        ]
        
    @server.list_prompts()
    async def list_prompts() -> list[Prompt]:
        return [
            Prompt(
                name="math",
                description="providing the math operation like add, multiply",
                arguments=[
                    PromptArgument(
                        name="a", description="first number", required=True
                    ),
                    PromptArgument(
                        name="b", description="second number", required=True
                    )
                ],
            )
        ]
        
    @server.call_tool()
    async def call_tool(name, arguments: dict) -> list[TextContent]:
        try:
            args = MathOperation(**arguments)
        except ValueError as e:
            raise ErrorData(code=INVALID_PARAMS, message=str(e))

        if name == "add":
            result = args.a + args.b
        elif name == "multiply":
            result = args.a * args.b
        else:
            raise ErrorData(code=INVALID_PARAMS, message="Unknown operation")

        return [TextContent(type="text", text=f"Result: {result}")]

    options = server.create_initialization_options()
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, options, raise_exceptions=True)

