# src/thales/rag/vector/chroma_impl.py

import chromadb
from chromadb.config import Settings, DEFAULT_TENANT, DEFAULT_DATABASE
from chromadb.utils import embedding_functions
from chromadb.types import Metadata
from typing import List, Dict, Any
import uuid

from thales.rag.vector.base import VectorStore
from thales.rag.data.models import SearchResult


class ChromaVectorStore(VectorStore):
    """A vector store implementation using ChromaDB."""

    def __init__(
        self,
        path: str = "./chroma_db",
        collection_name: str = "thales_rag_collection",
        embedding_model_name: str = "all-MiniLM-L6-v2"
    ):
        self.client = chromadb.PersistentClient(
            path=path,
            settings=Settings(allow_reset=True),
            tenant=DEFAULT_TENANT,
            database=DEFAULT_DATABASE
        )
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model_name
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function, # type: ignore
            metadata={"use": "testing", "year": "2025", "subject": "nonsense"}
        )

    def add_documents_sync(self, documents: List[str], metadatas: List[Metadata] | None) -> None:
        """Adds documents to the collection, converting list of tags to separate boolean fields."""
        ids = [str(uuid.uuid4()) for _ in documents]
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )

    def similarity_search_sync(
        self,
        query: str,
        k: int = 10,
        metadata: Metadata | None = None
    ) -> SearchResult:
        """Performs a similarity search against the vector store.  Default AND for tags for now """
        where_clause: Dict[str, Any] | None = None
        if metadata:
            if len(metadata)>1:
                where_clause = {
                    "$and": [{f"{key}": f"{value}"} for key, value in metadata.items()]
                }
            else:
                key, value = next(iter(metadata.items()))
                where_clause = {
                    f"{key}": f"{value}"
                }

        # chromadb search
        cq = self.collection.query(
            query_texts=[query],
            n_results=k,
            where=where_clause,
            include=["documents", "distances", "metadatas"]
        )

        print(f"Found {cq}")

        # convert to expected thales SearchResult
        results = SearchResult(ids = cq["ids"], documents=cq["documents"], metadatas=cq["metadatas"], distances=cq["distances"])


        return results
