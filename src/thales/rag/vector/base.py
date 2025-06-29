# src/thales/rag/vector/base.py

from abc import ABC, abstractmethod
from thales.rag.data import SearchResult, Metadata, Metadatas, Documents

class VectorStore(ABC):
    """Abstract base class for vector database operations."""

    @abstractmethod
    def add_documents_sync(self, documents: Documents, metadatas: Metadatas | None) -> None:
        """
        Syncronous adds docs to vectorStore collection.
        """

        pass

    @abstractmethod
    def similarity_search_sync(
        self,
        query: str,
        k: int = 10,
        metadata: Metadata | None = None
    ) -> SearchResult:
        """
        Performs Syncronous similarity search against the vector store.
        
        Args:
            query: The text to search for.
            k: The number of results to return.
            tags: An optional list of tags to filter the search.
            
        Returns:
            A list of ranked search results.
        """
        pass
