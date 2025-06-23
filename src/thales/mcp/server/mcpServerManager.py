"""MCP Server Configuration Management"""

import os
from typing import Dict, List, Optional
from dataclasses import dataclass


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
            )
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
