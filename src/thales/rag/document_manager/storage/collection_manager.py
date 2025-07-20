"""
ChromaDB collection management.

Handles creation, management, and access to ChromaDB collections.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction
from chromadb.api.types import EmbeddingFunction 
import uuid

from ...vector.chroma_impl import ChromaVectorStore

class CollectionManager:
    """
    Manages ChromaDB collections for document storage.
    
    Features:
    - Create collections per top-level folder
    - Consistent naming convention
    - Collection metadata tracking
    - Batch document insertion
    """
    
    def __init__(self, 
                 chroma_path: str = "./rag_collections",
                 embedding_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize collection manager.
        
        Args:
            chroma_path: Path to ChromaDB storage
            embedding_model: Name of sentence transformer model
            
        TODO:
        - Support multiple embedding models
        - Add collection versioning
        - Implement backup/restore
        """
        self.chroma_path = Path(chroma_path)
        self.embedding_model = embedding_model
        
        # Initialize ChromaDB client
        self.client = chromadb.PersistentClient(
            path=str(self.chroma_path),
            settings=Settings(allow_reset=True)
        )
        
        # Create embedding function
        self.embedding_function: SentenceTransformerEmbeddingFunction = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model
        )
    
    def create_collection(self, name: str, metadata: Optional[Dict[str, Any]] = None) -> Any:
        """
        Create or get a collection.
        
        Args:
            name: Collection name
            metadata: Collection metadata
            
        Returns:
            ChromaDB collection object
            
        TODO:
        - Validate collection name
        - Handle existing collections
        - Set collection-specific settings
        """
        collection_metadata = metadata or {}
        collection_metadata.update({
            "embedding_model": self.embedding_model,
            "created_by": "document_manager"
        })
        
        return self.client.get_or_create_collection(
            name=name,
            embedding_function=self.embedding_function,  # type: ignore[arg-type]
            metadata=collection_metadata
        )
    
    def list_collections(self) -> List[Dict[str, Any]]:
        """
        List all collections with metadata.
        
        Returns:
            List of collection info dictionaries
            
        TODO:
        - Add document counts
        - Include size information
        - Sort by date/name
        """
        collections = []
        
        for coll in self.client.list_collections():
            info = {
                "name": coll.name,
                "metadata": coll.metadata,
                "count": coll.count()
            }
            collections.append(info)
        
        return collections
    
    def get_collection(self, name: str) -> Optional[Any]:
        """
        Get a collection by name.
        
        Returns None if collection doesn't exist.
        """
        try:
            return self.client.get_collection(
                name=name,
                embedding_function=self.embedding_function  # type: ignore[arg-type]
            )
        except ValueError:
            return None
    
    def delete_collection(self, name: str) -> bool:
        """
        Delete a collection.
        
        Args:
            name: Collection name
            
        Returns:
            True if deleted, False if not found
            
        TODO:
        - Add safety checks
        - Backup before deletion
        - Update tracker
        """
        try:
            self.client.delete_collection(name)
            return True
        except ValueError:
            return False
    
    def add_documents(self,
                     collection_name: str,
                     documents: List[str],
                     metadatas: List[Dict[str, Any]],
                     ids: Optional[List[str]] = None) -> int:
        """
        Add documents to a collection.
        
        Args:
            collection_name: Target collection
            documents: List of document texts
            metadatas: List of metadata dicts
            ids: Optional document IDs
            
        Returns:
            Number of documents added
            
        TODO:
        - Batch processing for large sets
        - Duplicate detection
        - Error handling per document
        """
        collection = self.get_collection(collection_name)
        if not collection:
            collection = self.create_collection(collection_name)
        
        # Generate IDs if not provided
        if not ids:
            ids = [str(uuid.uuid4()) for _ in documents]
        
        # Add in batches to avoid memory issues
        batch_size = 100
        added = 0
        
        for i in range(0, len(documents), batch_size):
            batch_docs = documents[i:i + batch_size]
            batch_meta = metadatas[i:i + batch_size]
            batch_ids = ids[i:i + batch_size]
            
            collection.add(
                documents=batch_docs,
                metadatas=batch_meta,
                ids=batch_ids
            )
            added += len(batch_docs)
        
        return added
    
    def update_document(self,
                       collection_name: str,
                       document_id: str,
                       document: str,
                       metadata: Dict[str, Any]) -> bool:
        """
        Update a document in a collection.
        
        TODO:
        - Implement update logic
        - Handle missing documents
        - Update chunk references
        """
        collection = self.get_collection(collection_name)
        if not collection:
            return False
        
        try:
            collection.update(
                ids=[document_id],
                documents=[document],
                metadatas=[metadata]
            )
            return True
        except Exception:
            return False
    
    def get_collection_stats(self, name: str) -> Dict[str, Any]:
        """
        Get detailed statistics for a collection.
        
        TODO:
        - Add size calculations
        - Metadata field analysis
        - Date range information
        """
        collection = self.get_collection(name)
        if not collection:
            return {}
        
        return {
            "name": name,
            "document_count": collection.count(),
            "metadata": collection.metadata,
            # TODO: Add more stats
        }
    
    def create_vector_store(self, collection_name: str) -> ChromaVectorStore:
        """
        Create a vector store interface for a collection.
        
        This allows using the collection with the existing RAG system.
        """
        return ChromaVectorStore(
            path=str(self.chroma_path),
            collection_name=collection_name,
            embedding_model_name=self.embedding_model
        )
    
    def export_collection_manifest(self) -> Dict[str, Any]:
        """
        Export manifest of all collections.
        
        Useful for external tools to understand the structure.
        
        TODO:
        - Include schema information
        - Add usage examples
        - Export to file
        """
        manifest: dict[str, Any] = {
            "chroma_path": str(self.chroma_path),
            "embedding_model": self.embedding_model,
            "collections": {}
        }
        
        for coll_info in self.list_collections():
            name = coll_info["name"]
            manifest["collections"][name] = {
                "document_count": coll_info["count"],
                "metadata": coll_info["metadata"]
            }
        
        return manifest
