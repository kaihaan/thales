# src/thales/rag/graph/dummy.py

from typing import List, Dict, Any, Optional
from thales.rag.data.models import SearchResult
from thales.rag.graph.base import GraphDatabase

class DummyGraphDatabase(GraphDatabase):
    """A dummy graph database for testing purposes."""

    async def get_connected_nodes(
        self,
        node_ids: List[str],
        depth: int = 1,
        tags: Optional[List[str]] = None
    ) -> List[SearchResult]:
        """Returns a fixed list of dummy connected nodes, printing any tags received."""
        print(f"DummyGraphDatabase: Getting connected nodes for {node_ids} at depth {depth} with tags={tags}")
        results = []
        for i, node_id in enumerate(node_ids):
            results.append(
                SearchResult(
                    node_id=f"graph_node_for_{node_id}",
                    content=f"Dummy content for node connected to {node_id}",
                    score=0.9,
                    metadata={"source": "dummy_graph_db", "original_node": node_id}
                )
            )
        return results

    async def query(self, cypher_query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Returns a dummy result for a cypher query."""
        print(f"DummyGraphDatabase: Executing query '{cypher_query}' with params {params}")
        return [{"result": "dummy_query_result"}]
