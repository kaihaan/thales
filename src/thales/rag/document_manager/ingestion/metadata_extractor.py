"""
Metadata extraction from documents and file system.

Extracts and enriches metadata for documents.
"""

from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime
import os


class MetadataExtractor:
    """
    Extracts metadata from documents and their file system context.
    
    Features:
    - File system metadata (dates, size, path)
    - Folder hierarchy as tags
    - Document-specific metadata
    - Custom metadata from .metadata.json files
    """
    
    def __init__(self, base_path: Path):
        """
        Initialize extractor.
        
        Args:
            base_path: Base path for relative path calculation
        """
        self.base_path = Path(base_path).resolve()
    
    def extract_metadata(self, 
                        file_path: Path,
                        parsed_metadata: Dict[str, Any],
                        collection_name: str) -> Dict[str, Any]:
        """
        Extract complete metadata for a document.
        
        Args:
            file_path: Path to document file
            parsed_metadata: Metadata from document parser
            collection_name: Name of the collection
            
        Returns:
            Combined metadata dictionary
            
        TODO:
        - Extract author from document properties
        - Add language detection
        - Extract keywords/entities
        """
        metadata = {}
        
        # File system metadata
        metadata.update(self._extract_file_metadata(file_path))
        
        # Folder hierarchy
        metadata.update(self._extract_folder_metadata(file_path))
        
        # Collection info
        metadata['collection'] = collection_name
        
        # Document parser metadata
        metadata.update(parsed_metadata)
        
        # Custom metadata from folder
        custom = self._load_custom_metadata(file_path)
        if custom:
            metadata.update(custom)
        
        # Clean and validate
        metadata = self._clean_metadata(metadata)
        
        return metadata
    
    def _extract_file_metadata(self, path: Path) -> Dict[str, Any]:
        """Extract metadata from file system."""
        stat = path.stat()
        
        return {
            'document_path': str(path),
            'relative_path': str(path.relative_to(self.base_path)),
            'filename': path.name,
            'file_extension': path.suffix.lower(),
            'file_size': stat.st_size,
            'created_date': datetime.fromtimestamp(stat.st_ctime).isoformat(),
            'modified_date': datetime.fromtimestamp(stat.st_mtime).isoformat(),
        }
    
    def _extract_folder_metadata(self, path: Path) -> Dict[str, Any]:
        """Extract folder hierarchy as metadata."""
        metadata = {}
        
        try:
            relative = path.relative_to(self.base_path)
            parts = list(relative.parts[:-1])  # Exclude filename
            
            # Full hierarchy
            if parts:
                metadata['folder_hierarchy'] = '/'.join(parts)
                
                # Individual folder levels as tags
                for i, folder in enumerate(parts):
                    metadata[f'folder_{i+1}'] = folder
                
                # Folder depth
                metadata['folder_depth'] = len(parts)
        except ValueError:
            pass
        
        return metadata
    
    def _load_custom_metadata(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Load custom metadata from .metadata.json files.
        
        Looks for metadata files in the same directory and parent directories.
        
        TODO:
        - Merge metadata from multiple levels
        - Support YAML format
        - Cache loaded metadata
        """
        import json
        
        # Check same directory
        metadata_file = file_path.parent / '.metadata.json'
        if metadata_file.exists():
            try:
                with open(metadata_file, 'r') as f:
                    data = json.load(f)
                    
                # Check if there's file-specific metadata
                filename = file_path.name
                if filename in data:
                    return data[filename]
                elif 'default' in data:
                    return data['default']
            except Exception:
                pass
        
        return None
    
    def _clean_metadata(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and validate metadata.
        
        Ensures metadata values are compatible with ChromaDB.
        
        TODO:
        - Validate data types
        - Truncate long strings
        - Remove null values
        """
        cleaned = {}
        
        for key, value in metadata.items():
            # Skip None values
            if value is None:
                continue
            
            # Convert to string if needed
            if isinstance(value, (int, float, bool)):
                cleaned[key] = value
            elif isinstance(value, datetime):
                cleaned[key] = value.isoformat()
            else:
                cleaned[key] = str(value)
        
        return cleaned
    
    def enrich_chunk_metadata(self,
                            chunk_metadata: Dict[str, Any],
                            chunk_index: int,
                            total_chunks: int) -> Dict[str, Any]:
        """
        Enrich metadata for a specific chunk.
        
        Args:
            chunk_metadata: Base document metadata
            chunk_index: Index of this chunk
            total_chunks: Total number of chunks
            
        Returns:
            Enriched chunk metadata
        """
        enriched = chunk_metadata.copy()
        
        # Chunk-specific metadata
        enriched.update({
            'chunk_index': chunk_index,
            'total_chunks': total_chunks,
            'chunk_id': f"{chunk_metadata.get('document_path', 'unknown')}#chunk{chunk_index}",
        })
        
        return enriched
    
    def extract_entity_metadata(self, text: str) -> Dict[str, Any]:
        """
        Extract entities and keywords from text.
        
        TODO:
        - Implement NER (Named Entity Recognition)
        - Extract key phrases
        - Detect language
        - Extract dates/numbers
        """
        metadata = {}
        
        # Placeholder for entity extraction
        # Would use spaCy or similar for real implementation
        
        # Simple keyword extraction (word frequency)
        words = text.lower().split()
        word_freq = {}
        for word in words:
            if len(word) > 5:  # Simple filter
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Top keywords
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        if top_words:
            metadata['keywords'] = [word for word, _ in top_words]
        
        return metadata
