"""Describes a colelction of MCP Tools
   - Manually defined for now
   - Assumes tools available through MCP server (Server Name / Tool Name)
   - Part of Ontology 
"""

from dataclasses import dataclass
from mcp import Tool

@dataclass
class Toolkit:
    name: str
    description: str
    tools: list[Tool]
