"""
mcp client

Usage:
    - connect(self, server_name: str) -> None
    - disconnect(self, server_name: str) -> None
    - list_servers(self) -> Dict[str, MCPServerConfig]
    - list_tools(self, server_name: str | None = None) -> ListToolsResult | None
    - execute_tool(self, server_name: str, tool_name: str, args: Dict[str, Any]) -> CallToolResult
    - interactive_mode(self) -> None

    NOTE: tool selection strategy
    TODO Need to explore a basic use-case of allowing teh agent to use a given tool from the MCP Server first
    TODO MCPServerManager allows creation of tool sets
    TODO MCP Client should allow caller to choose a tool-set, or define a list of named tools, or a default set
    TODO Also offer an LLM tool to choose from all known tools on basis of Agent Purpose
    TODO Also offer LLM too to find best-fit tool from all known tools, given query (if no suitable tool already found)
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
from thales.utils import get_logger

load_dotenv()
logger = get_logger(__name__)

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

    def __init__(self) -> None:
        self.sessions: Dict[str, ClientSession] = {}
        self.exit_stack = AsyncExitStack()
        #self.anthropic = Anthropic()
        self.server_manager = MCPServerManager()
        self.active_servers: Dict[str, MCPServerConfig] = {}

        # for debugging
        current_dir = os.getcwd()
        logger.debug("Enhanced MCP Client Initialised")
        logger.debug(f"Current directory {current_dir}")

    async def connect(self, server_name: str) -> None:
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
            toolcall = await session.list_tools()
            tools = toolcall.tools
            logger.debug(f"Connected to {server_name}")
            logger.debug(f"Available tools {[tool.name for tool in tools]}")

            # list resources
            try:
                rescall = await session.list_resources()
                if rescall.resources:
                    logger.debug(
                        f"Available resource {[res.name for res in rescall.resources]}"
                    )
            except:
                pass  # not all servers have resources

        except Exception as e:
            logger.debug(f"❌ Failed to connect to server {server_name}")
            raise

    async def disconnect(self, server_name: str) -> None:
        """Disconnect from specified MCP server"""
        if server_name not in self.sessions:
            logger.debug(f"Not connected to {server_name}")
            return

        del self.sessions[server_name]
        del self.active_servers[server_name]
        logger.debug(f"Disconnected from {server_name}")


    async def list_servers(self) -> Dict[str, MCPServerConfig]:
        """List all connected servers"""
        for name, config in self.active_servers.items():
            logger.debug(f"\n🔗 {name}: {config.description}")

        return self.active_servers

    
    async def list_tools(self, server_name: str | None = None) -> ListToolsResult | None:
        """List all connected servers and their tools"""
        if not self.sessions:
            logger.debug("No active server sessions")
            return None

        found = ListToolsResult(tools=[])

        for session_name, session in self.sessions.items():

            if server_name and session_name != server_name:
                print(f"Searching for tools for x1 server: {server_name}")
                continue

            config = self.active_servers[session_name]
            print(f"\n🔗 {session_name}: {config.description}")

            try:
                res = await session.list_tools()
                found.tools.extend(res.tools)

            except Exception as e:
                logger.debug(f"❌ Error listing tools: {e}")

        for tool in found.tools:
            print(f"🔧 {tool.name}: {tool.description}")
        
        return found if found.tools else None

    # TODO impliment
    def get_tool_set(self, tool_set: str) -> ListToolsResult | None:
        tools = self.server_manager.get_tool_set(tool_set)
        return tools


    async def execute_tool(
        self, server_name: str, tool_name: str, args: dict[str, Any],
    ) -> CallToolResult:
        """Execute a tool on a specific server"""

        #TODO re-write this to call tool by name, without needing server name
        if server_name not in self.sessions:
            logger.debug(
                f"Error - Can't execute tool because not connected to {server_name}"
            )
            raise ValueError(f"Not connected to {server_name}")

        #
        
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
                            await self.connect(command[1])

                    case "disconnect":
                        if len(command) > 1:
                            await self.disconnect(command[1])
                
                    case "servers":
                        for name, config in self.server_manager.list_configured_servers().items():
                            status = "🟢 Connected" if name in self.sessions else "⚪ Available"
                            print(f"  {status} {name}: {config.description}")

                    case "connected":
                        await self.list_servers()

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
                            await self.list_tools(command[1])
                        else:
                            await self.list_tools()

                    case "help":
                        print(instructions)

            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"Error: {e}")

    async def cleanup(self) -> None:
        """Clean up all connections"""
        await self.exit_stack.aclose()

async def main() -> None:
    if len(sys.argv) > 1:
        # direct server connection mode
        server_name = sys.argv[1]
        client = EnhancedMCPClient()
        try:
            await client.connect(server_name)
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
