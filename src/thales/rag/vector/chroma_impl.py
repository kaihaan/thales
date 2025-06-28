# src/thales/rag/vector/chroma_impl.py

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from typing import List, Optional, Dict, Any, cast
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
            settings=Settings(allow_reset=True)
        )
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model_name
        )
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function # type: ignore
        )

    async def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]]) -> None:
        """Adds documents to the collection, converting list of tags to separate boolean fields."""
        processed_metadatas = []
        for meta in metadatas:
            new_meta: Dict[str, Any] = {}
            for k, v in meta.items():
                if k == 'tags' and isinstance(v, list):
                    for tag in v:
                        new_meta[f"tag_{tag}"] = True
                else:
                    new_meta[k] = v
            processed_metadatas.append(new_meta)

        ids = [str(uuid.uuid4()) for _ in documents]
        self.collection.add(
            documents=documents,
            metadatas=cast(List[Dict[str, str | int | float | bool]], processed_metadatas),
            ids=ids
        )

    async def similarity_search(
        self,
        query: str,
        k: int = 10,
        tags: Optional[List[str]] = None
    ) -> List[SearchResult]:
        """Performs a similarity search against the vector store."""
        where_clause: Optional[Dict[str, Any]] = None
        if tags:
            if len(tags) > 1:
                where_clause = {
                    "$and": [{f"tag_{tag}": {"$eq": True}} for tag in tags]
                }
            else:
                where_clause = {f"tag_{tags[0]}": {"$eq": True}}

        results = self.collection.query(
            query_texts=[query],
            n_results=k,
            where=where_clause
        )

        search_results = []
        if results and results['ids'] and results['documents'] and results['distances'] and results['metadatas']:
            ids = results['ids'][0]
            documents = results['documents'][0]
            distances = results['distances'][0]
            metadatas = results['metadatas'][0]

            for i in range(len(ids)):
                search_results.append(
                    SearchResult(
                        node_id=ids[i],
                        content=documents[i],
                        score=1.0 - distances[i],
                        metadata=cast(Dict[str, Any], metadatas[i])
                    )
                )
        return search_results
