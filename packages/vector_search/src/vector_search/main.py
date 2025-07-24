import asyncio

from fastmcp import Client

import vector_search.weather_server  # Import the server module


async def main():
    async with Client(vector_search.weather_server.mcp) as mcp_client:
        tools = await mcp_client.list_tools()
        print(tools)
        return tools


if __name__ == "__main__":
    result = asyncio.run(main())
