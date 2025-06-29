"""
Document chunking strategies.

Splits documents into chunks for vector embedding.
"""

from typing import List, Dict, Any, Optional, Protocol
from dataclasses import dataclass
from abc import ABC, abstractmethod
import re


@dataclass
class DocumentChunk:
    """Represents a chunk of a document."""
    text: str
    metadata: Dict[str, Any]
    chunk_index: int
    start_char: int
    end_char: int


class ChunkingStrategy(ABC):
    """Base class for chunking strategies."""
    
    @abstractmethod
    def chunk(self, text: str, metadata: Dict[str, Any]) -> List[DocumentChunk]:
        """Split text into chunks."""
        pass


class SlidingWindowChunker(ChunkingStrategy):
    """
    Simple sliding window chunker.
    
    Splits text into overlapping chunks of fixed size.
    """
    
    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        """
        Initialize chunker.
        
        Args:
            chunk_size: Target size of each chunk in characters
            overlap: Number of overlapping characters between chunks
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
    
    def chunk(self, text: str, metadata: Dict[str, Any]) -> List[DocumentChunk]:
        """
        Split text into overlapping chunks.
        
        TODO:
        - Consider word boundaries
        - Handle very short texts
        - Add sentence boundary detection
        """
        chunks = []
        start = 0
        chunk_index = 0
        
        while start < len(text):
            end = start + self.chunk_size
            
            # Try to break at word boundary
            if end < len(text):
                # Look for last space before end
                space_pos = text.rfind(' ', start, end)
                if space_pos > start:
                    end = space_pos
            
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(DocumentChunk(
                    text=chunk_text,
                    metadata={
                        **metadata,
                        "chunk_index": chunk_index,
                        "total_chunks": None,  # Will be set later
                    },
                    chunk_index=chunk_index,
                    start_char=start,
                    end_char=end
                ))
                chunk_index += 1
            
            start = end - self.overlap
        
        # Update total chunks count
        for chunk in chunks:
            chunk.metadata["total_chunks"] = len(chunks)
        
        return chunks


class SemanticChunker(ChunkingStrategy):
    """
    Semantic-aware chunking.
    
    Splits text based on semantic boundaries like paragraphs, sections.
    """
    
    def __init__(self, max_chunk_size: int = 1000, min_chunk_size: int = 100):
        """
        Initialize semantic chunker.
        
        Args:
            max_chunk_size: Maximum size of a chunk
            min_chunk_size: Minimum size of a chunk
            
        TODO:
        - Add section detection
        - Support markdown headers
        - Handle lists and tables
        """
        self.max_chunk_size = max_chunk_size
        self.min_chunk_size = min_chunk_size
    
    def chunk(self, text: str, metadata: Dict[str, Any]) -> List[DocumentChunk]:
        """
        Split text on semantic boundaries.
        
        TODO:
        - Implement paragraph detection
        - Merge small paragraphs
        - Split large paragraphs
        """
        # Simple paragraph-based splitting for now
        paragraphs = re.split(r'\n\s*\n', text)
        
        chunks = []
        current_chunk = []
        current_size = 0
        chunk_index = 0
        start_char = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            
            para_size = len(para)
            
            # If paragraph is too large, split it
            if para_size > self.max_chunk_size:
                # Save current chunk if any
                if current_chunk:
                    chunk_text = '\n\n'.join(current_chunk)
                    chunks.append(self._create_chunk(
                        chunk_text, metadata, chunk_index, start_char
                    ))
                    chunk_index += 1
                    start_char += len(chunk_text) + 2
                    current_chunk = []
                    current_size = 0
                
                # Split large paragraph
                # TODO: Implement sentence-based splitting
                chunks.append(self._create_chunk(
                    para, metadata, chunk_index, start_char
                ))
                chunk_index += 1
                start_char += para_size + 2
            
            # If adding paragraph exceeds max size, start new chunk
            elif current_size + para_size > self.max_chunk_size:
                if current_chunk:
                    chunk_text = '\n\n'.join(current_chunk)
                    chunks.append(self._create_chunk(
                        chunk_text, metadata, chunk_index, start_char
                    ))
                    chunk_index += 1
                    start_char += len(chunk_text) + 2
                
                current_chunk = [para]
                current_size = para_size
            
            # Add to current chunk
            else:
                current_chunk.append(para)
                current_size += para_size
        
        # Don't forget last chunk
        if current_chunk:
            chunk_text = '\n\n'.join(current_chunk)
            chunks.append(self._create_chunk(
                chunk_text, metadata, chunk_index, start_char
            ))
        
        # Update total chunks
        for chunk in chunks:
            chunk.metadata["total_chunks"] = len(chunks)
        
        return chunks
    
    def _create_chunk(self, text: str, metadata: Dict[str, Any], 
                     index: int, start: int) -> DocumentChunk:
        """Create a document chunk."""
        return DocumentChunk(
            text=text,
            metadata={
                **metadata,
                "chunk_index": index,
            },
            chunk_index=index,
            start_char=start,
            end_char=start + len(text)
        )


class DocumentChunker:
    """
    Main chunker that selects strategy based on document type.
    
    TODO:
    - Add markdown chunker
    - Add code file chunker
    - Add table-aware chunker
    """
    
    def __init__(self, default_chunk_size: int = 1000, overlap: int = 200):
        """Initialize with default settings."""
        self.strategies = {
            'default': SlidingWindowChunker(default_chunk_size, overlap),
            'semantic': SemanticChunker(default_chunk_size),
            'pdf': SemanticChunker(default_chunk_size),
            'markdown': SemanticChunker(default_chunk_size),  # TODO: Specialized
        }
    
    def chunk_document(self, text: str, metadata: Dict[str, Any], 
                      strategy: Optional[str] = None) -> List[DocumentChunk]:
        """
        Chunk a document using appropriate strategy.
        
        Args:
            text: Document text
            metadata: Document metadata
            strategy: Strategy name or None for auto-selection
            
        Returns:
            List of document chunks
        """
        if not strategy:
            # Auto-select based on format
            format = metadata.get('format', 'default')
            strategy = format if format in self.strategies else 'default'
        
        chunker = self.strategies.get(strategy or 'default', self.strategies['default'])
        return chunker.chunk(text, metadata)
