"""
MCP Server Manager - manages list of known MCP Servers & tools for Local MCP Clients
- list_configured_servers(self) -> dict[str, MCPServerConfig]
- get_server(self, name: str) -> MCPServerConfig
- add_server(self, config: MCPServerConfig) -> bool

NOTE: tool discovery strategy
Allo curated colelctions of tools to be defined.
Agents can then be set up with tools = None | default-set | curated-set | [set of named-tools]
TODO Add get_known_tools
TODO Add get_tool_sets, create_tool_set, delete_tool_set
 

"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from mcp.types import ListToolsResult

@dataclass
class MCPServerConfig:
    """dataclass holding MCP Server configuration settings"""

    name: str
    command: str
    args: List[str]
    env: Optional[Dict[str, str]] = None
    description: str = ""


class MCPServerManager:
    """class to manage registry of MCP Server configuration settings"""

    def __init__(self) -> None:
        self.servers = {
            "filesystem": MCPServerConfig(
                name="filesystem",
                command="npx",
                args=[
                    "-y",
                    "@modelcontextprotocol/server-filesystem",
                    "D:/dev/Coursera/Agents/thales",
                ],
                description="Official filesystem server with secure file operations",
            ),
            "local-math": MCPServerConfig(
                name="local-math",
                command="python",
                args=["D:\\dev\\Coursera\\Agents\\thales\\src\\thales\\mcp\\server\\math_server.py"],
                description="Local math operations server",
            ),
            "context-db": MCPServerConfig(
                name="context-db",
                command="python",
                args=["D:\\dev\\Coursera\\Agents\\thales\\src\\thales\\mcp\\server\\context_db_server.py"],
                description="Server for storing and retrieving agent context components.",
            ),
        }

    def get_server(self, name: str) -> MCPServerConfig:
        if name not in self.servers:
            raise ValueError(
                f"Unknown server: {name}. Available servers: {list(self.servers.keys())}"
            )
        return self.servers[name]

    def list_configured_servers(self) -> dict[str, MCPServerConfig]:
        return self.servers.copy()

    def add_server(self, config: MCPServerConfig) -> bool:
        if config.name in self.servers:
            raise ValueError(f"Server name already exists: {config.name}.")
        self.servers[config.name] = config
        return True
    
    # TODO implement
    def get_tool_set(self, tool_set: str) -> ListToolsResult | None:
        tools: ListToolsResult | None = None
        return tools
