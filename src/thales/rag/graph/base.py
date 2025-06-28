# src/thales/rag/graph/base.py

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from thales.rag.data.models import SearchResult

class GraphDatabase(ABC):
    """Abstract base class for graph database operations."""

    @abstractmethod
    async def get_connected_nodes(
        self,
        node_ids: List[str],
        depth: int = 1,
        tags: Optional[List[str]] = None
    ) -> List[SearchResult]:
        """
        Retrieves nodes connected to a given set of starting nodes.
        
        Args:
            node_ids: The IDs of the starting nodes.
            depth: The traversal depth.
            tags: An optional list of tags to filter the connected nodes.
            
        Returns:
            A list of connected nodes.
        """
        pass

    @abstractmethod
    async def query(self, cypher_query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Executes a raw Cypher query against the graph.
        """
        pass
