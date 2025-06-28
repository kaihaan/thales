# src/thales/rag/vector/dummy.py

from typing import List, Optional
from thales.rag.data.models import SearchResult
from thales.rag.vector.base import VectorStore

class DummyVectorStore(VectorStore):
    """A dummy vector store for testing purposes."""

    async def similarity_search(
        self,
        query: str,
        k: int = 10,
        tags: Optional[List[str]] = None
    ) -> List[SearchResult]:
        """Returns a fixed list of dummy search results, printing any tags received."""
        print(f"DummyVectorStore: Searching for '{query}' with k={k} and tags={tags}")
        return [
            SearchResult(
                node_id=f"vec_node_{i}",
                content=f"Dummy content for vector search result {i}",
                score=1.0 - (i * 0.1),
                metadata={"source": "dummy_vector_store"}
            ) for i in range(k)
        ]
