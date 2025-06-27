"""
This package defines the structures and interfaces for an agent's knowledge base,
including conversation history, persistent storage, and dynamic tool integration.
"""
from thales.agents.base.ontology.knowledge.knowledge import Knowledge, Message, MessageRole, Session
from thales.agents.base.ontology.knowledge.tools import KnowledgeTool
from thales.agents.base.ontology.knowledge.mcp_client_interface import McpKnowledgeClient

__all__ = [
    "Knowledge",
    "Message",
    "MessageRole",
    "Session",
    "KnowledgeTool",
    "McpKnowledgeClient",
]
