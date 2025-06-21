"""
mcp client

Usage:
    - connect_to_server(self, server_name: str) -> None
    - disconnect_server(self, server_name: str) -> None
    - list_connected_servers(self) -> None
    - list_connected_tools(self) -> ListToolsResult | None
    - execute_tool(self, server_name: str, tool_name: str, args: Dict[str, Any]) -> CallToolResult
    - interactive_mode(self) -> None

"""

import asyncio
import sys
import os

from typing import Optional, Dict, Any
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
# import mcp.types as types
from mcp.types import ListToolsResult, CallToolResult, Tool
from mcp.client.stdio import stdio_client
# from anthropic import Anthropic
from dotenv import load_dotenv

from thales.mcp.server import MCPServerManager, MCPServerConfig
from thales.utils.logger import logger

load_dotenv()


"""
class ListToolsResult(PaginatedResult):
    tools: list[Tool]


class Tool(BaseModel):
    name: str
    description: str | None = None
    inputSchema: dict[str, Any]
    annotations: ToolAnnotations | None = None

e.g.    {
  name: "execute_command",
  description: "Run a shell command",
  inputSchema: {
    type: "object",
    properties: {
      command: { type: "string" },
      args: { type: "array", items: { type: "string" } }
    }
  }
}
    
    """

class EnhancedMCPClient:
    """
    - connects MCP servers in config (runs as NPX or local *.py)
    - TODO add http/streamed servers when I find one I want to use
    - search/finds tools
    - executes tools
    """

    def __init__(self):
        self.sessions: Dict[str, ClientSession] = {}
        self.exit_stack = AsyncExitStack()
        #self.anthropic = Anthropic()
        self.server_manager = MCPServerManager()
        self.active_servers: Dict[str, MCPServerConfig] = {}

        # for debugging
        current_dir = os.getcwd()
        logger.debug("Enhanced MCP Client Initialised")
        logger.debug(f"Current directory {current_dir}")

    async def connect_to_server(self, server_name: str) -> None:
        """Connect to an MCP Server

        Args:
            server_name: named server in MCP Server Config
        """
        if server_name in self.sessions:
            logger.debug(f"Already connected to {server_name}")
            return

        config = self.server_manager.get_server(server_name)
        logger.debug(f"Connecting to {config.name}: {config.description}")

        server_params = StdioServerParameters(
            command=config.command, args=config.args, env=config.env
        )

        try:
            stdio_transport = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            stdio, write = stdio_transport
            session = await self.exit_stack.enter_async_context(
                ClientSession(stdio, write)
            )

            await session.initialize()
            self.sessions[server_name] = session
            self.active_servers[server_name] = config

            # list tools
            response = await session.list_tools()
            tools = response.tools
            logger.debug(f"Connected to {server_name}")
            logger.debug(f"Available tools {[tool.name for tool in tools]}")

            # list resources
            try:
                response = await session.list_resources()
                if response.resources:
                    logger.debug(
                        f"Available resource {[res.name for res in response.resources]}"
                    )
            except:
                pass  # not all servers have resources

        except Exception as e:
            logger.debug(f"❌ Failed to connect to server {server_name}")
            raise

    async def disconnect_server(self, server_name: str) -> None:
        """Disconnect from specified MCP server"""
        if server_name not in self.sessions:
            logger.debug(f"Not connected to {server_name}")
            return

        del self.sessions[server_name]
        del self.active_servers[server_name]
        logger.debug(f"Disconnected from {server_name}")


    async def list_connected_servers(self) -> Dict[str, MCPServerConfig]:
        """list all connected servers"""
        for name, config in self.active_servers.items():
            logger.debug(f"\n🔗 {name}: {config.description}")

        return self.active_servers

    
    async def list_connected_tools(self, requested_server_name: str | None = None) -> ListToolsResult | None:
        """list all connected servers and their tools"""
        if not self.sessions:
            logger.debug("No active server sessions")
            return

        found = ListToolsResult(tools=[])

        for server_name, session in self.sessions.items():

            if  requested_server_name and server_name != requested_server_name:
                print(f"Searching for tools for x1 server: {requested_server_name}")
                continue

            config = self.active_servers[server_name]
            print(f"\n🔗 {server_name}: {config.description}")

            try:
                res = await session.list_tools()
                found.tools.extend(res.tools)

            except Exception as e:
                logger.debug(f"❌ Error listing tools: {e}")

        for tool in found.tools:
            print(f"🔧 {tool.name}: {tool.description}")
        
        return found if found.tools else None

    async def execute_tool(
        self, server_name: str, tool_name: str, args: dict[str, Any],
    ) -> CallToolResult:
        """Execute a tool on a specific server"""
        if server_name not in self.sessions:
            logger.debug(
                f"Error - Can't execute tool because not connected to {server_name}"
            )
            raise ValueError(f"Not connected to {server_name}")

        session = self.sessions[server_name]
        try:
            print(f"Calling {tool_name} on server {server_name}")
            print(f"With args: {args}")
            result = await session.call_tool(tool_name, args)
            return result
        except Exception as e:
            logger.debug(f"Error executing tool {tool_name} on server {server_name} : {e}")
            raise

    async def interactive_mode(self) -> None:
        """Interactive mode for testing servers"""

        instructions = """🚀 Enhanced MCP Client - Interactive Mode
Commands:
- servers                            - Show available servers
- connect <server_name>              - Connect to a server
- disconnect <server_name>           - Disconnect from a server
- tools <server_name>                - List tools
- execute <server> <tool> <arg=val>  - Execute a tool
- help                               - Show this list
- quit                               - Exit"""

        print(instructions)

        while True:
            try:
                command = input("\n> ").strip().split()
                if not command:
                    continue

                match command[0].lower():
                    case "quit":
                        break

                    case "connect":
                        if len(command) > 1:
                            await self.connect_to_server(command[1])

                    case "disconnect":
                        if len(command) > 1:
                            await self.disconnect_server(command[1])
                
                    case "servers":
                        for name, config in self.server_manager.list_configured_servers().items():
                            status = "🟢 Connected" if name in self.sessions else "⚪ Available"
                            print(f"  {status} {name}: {config.description}")

                    case "execute":
                        if len(command) >= 3:  # <server> <tool> <args>
                            server_name = command[1]
                            tool_name = command[2]
                            # Simple args parsing - in real implementation, you'd want JSON
                            args = {}
                            if len(command) > 3:
                                # Basic key=value parsing
                                for arg in command[3:]:
                                    if "=" in arg:
                                        key, value = arg.split("=", 1)
                                        args[key] = value
                            
                            meta, content, isError = await self.execute_tool(server_name, tool_name, args)
                            print(content[1][0].text)
                            # for msg in content:
                            #     print(f"Result: {msg}")
                        else:
                            print("Must be in form: execute <server> <tool> <args>")

                    case "tools":
                        if len(command) == 2:
                            await self.list_connected_tools(command[1])
                        else:
                            await self.list_connected_tools()

                    case "help":
                        print(instructions)

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")

    async def cleanup(self):
        """Clean up all connections"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) > 1:
        # direct server connection mode
        server_name = sys.argv[1]
        client = EnhancedMCPClient()
        try:
            await client.connect_to_server(server_name=server_name)
            await client.interactive_mode()
        finally:
            await client.cleanup()
    else:
        # interactive
        client = EnhancedMCPClient()
        try:
            await client.interactive_mode()
        finally:
            await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
