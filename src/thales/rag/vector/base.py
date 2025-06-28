# src/thales/rag/vector/base.py

from abc import ABC, abstractmethod
from typing import List, Optional
from thales.rag.data.models import SearchResult

class VectorStore(ABC):
    """Abstract base class for vector database operations."""

    @abstractmethod
    async def similarity_search(
        self,
        query: str,
        k: int = 10,
        tags: Optional[List[str]] = None
    ) -> List[SearchResult]:
        """
        Performs a similarity search against the vector store.
        
        Args:
            query: The text to search for.
            k: The number of results to return.
            tags: An optional list of tags to filter the search.
            
        Returns:
            A list of ranked search results.
        """
        pass
