"""
mcp client
"""

import asyncio
import sys
import os

from typing import Optional, Dict, Any
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
# from anthropic import Anthropic
from dotenv import load_dotenv

from thales.mcp.server.mcp_config import MCPConfigManager, MCPServerConfig
from thales.utils.logger.logger import logger

load_dotenv()


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
        self.config_manager = MCPConfigManager()
        self.active_servers: Dict[str, MCPServerConfig] = {}

        # for debugging
        current_dir = os.getcwd()
        logger.debug("Enhanced MCP Client Initialised")
        logger.debug(f"Current directory {current_dir}")

    async def connect(self, server_name: str):
        """Connect to an MCP Server

        Args:
            server_name: named server in MCP Server Config
        """
        if server_name in self.sessions:
            logger.debug(f"Already connected to {server_name}")
            return

        config = self.config_manager.get_server(server_name)
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

    async def disconnect(self, server_name: str):
        """Disconnect from specified MCP server"""
        if server_name not in self.sessions:
            logger.debug(f"Not connected to {server_name}")
            return

        del self.sessions[server_name]
        del self.active_servers[server_name]
        logger.debug(f"Disconnected from {server_name}")

    async def list_servers(self):
        """list all connected servers and their tools"""
        if not self.sessions:
            logger.debug("No active server sessions")
            return

        for server_name, session in self.sessions:
            config = self.active_servers[server_name]
            logger.debug(f"\n🔗 {server_name}: {config.description}")

            try:
                res = await session.list_tools()
                tools = res.tools
                for tool in tools:
                    logger.debug(f"🔧 {tool.name}: {tool.description}")
            except Exception as e:
                logger.debug(f"❌ Error listing tools: {e}")

    async def execute_tool(
        self, server_name: str, tool_name: str, args: Dict[str, Any]
    ):
        """Execute a tool on a specific server"""
        if server_name not in self.sessions:
            logger.debug(
                f"Error - Can't execute tool because not connected to {server_name}"
            )
            raise ValueError(f"Not connected to {server_name}")

        session = self.sessions[server_name]
        try:
            result = await session.call_tool(tool_name, args)
            return result
        except Exception as e:
            logger.debug(f"Error executing tool {tool_name} on server {server_name} : {e}")
            raise

    async def interactive_mode(self):
        """Interactive mode for testing servers"""
        print("\n🚀 Enhanced MCP Client - Interactive Mode")
        print("Commands:")
        print("  connect <server_name>  - Connect to a server")
        print("  disconnect <server_name> - Disconnect from a server")
        print("  list                   - List connected servers")
        print("  servers               - Show available servers")
        print("  tool <server> <tool> <args> - Execute a tool")
        print("  quit                  - Exit")

        while True:
            try:
                command = input("\n> ").strip().split()
                if not command:
                    continue

                cmd = command[0].lower()

                if cmd == "quit":
                    break
                elif cmd == "connect" and len(command) > 1:
                    await self.connect_to_server(command[1])
                elif cmd == "disconnect" and len(command) > 1:
                    await self.disconnect_server(command[1])
                elif cmd == "list":
                    await self.list_connected_servers()
                elif cmd == "servers":
                    print("\nAvailable servers:")
                    for name, config in self.config_manager.list_servers().items():
                        status = "🟢 Connected" if name in self.sessions else "⚪ Available"
                        print(f"  {status} {name}: {config.description}")
                elif cmd == "tool" and len(command) >= 3:
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
                    
                    result = await self.execute_tool(server_name, tool_name, args)
                    print(f"Result: {result}")
                else:
                    print("Unknown command or missing arguments")

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
            await client.connect(server_name=server_name)
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

if __name__ == "main":
    asyncio.run(main())

