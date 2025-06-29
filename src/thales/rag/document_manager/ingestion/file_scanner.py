"""
File system scanner for document discovery.

Scans directories to find documents for ingestion.
"""

from pathlib import Path
from typing import List, Set, Iterator, Optional
from dataclasses import dataclass
import os


@dataclass
class DocumentFile:
    """Represents a document file to be processed."""
    path: Path
    relative_path: str
    collection_name: str
    size: int
    modified_time: float


class FileScanner:
    """
    Scans file system for documents to ingest.
    
    Features:
    - Discovers documents by file extension
    - Groups by top-level folder for collections
    - Filters hidden files and system files
    - Tracks file metadata
    """
    
    DEFAULT_EXTENSIONS = {
        '.pdf', '.txt', '.doc', '.docx', '.rtf', '.md', '.html',
        '.csv', '.xlsx', '.xls', '.ppt', '.pptx', '.epub'
    }
    
    def __init__(self, 
                 base_path: Path,
                 extensions: Optional[Set[str]] = None,
                 skip_hidden: bool = True):
        """
        Initialize scanner.
        
        Args:
            base_path: Root directory to scan
            extensions: File extensions to include (with dots)
            skip_hidden: Whether to skip hidden files/folders
            
        TODO:
        - Add pattern-based exclusions
        - Support for .gitignore style rules
        """
        self.base_path = Path(base_path).resolve()
        self.extensions = extensions or self.DEFAULT_EXTENSIONS
        self.skip_hidden = skip_hidden
    
    def scan(self) -> Iterator[DocumentFile]:
        """
        Scan for documents.
        
        Yields DocumentFile objects for each discovered document.
        
        TODO:
        - Add progress callback
        - Handle permission errors
        - Skip symlinks optionally
        """
        for root, dirs, files in os.walk(self.base_path):
            root_path = Path(root)
            
            # Skip hidden directories
            if self.skip_hidden:
                dirs[:] = [d for d in dirs if not d.startswith('.')]
            
            # Determine collection name from top-level folder
            try:
                relative = root_path.relative_to(self.base_path)
                parts = relative.parts
                collection_name = f"KnowledgeBase_{parts[0]}" if parts else "KnowledgeBase_Root"
            except ValueError:
                continue
            
            for file in files:
                if self.skip_hidden and file.startswith('.'):
                    continue
                
                file_path = root_path / file
                if file_path.suffix.lower() in self.extensions:
                    yield self._create_document_file(file_path, collection_name)
    
    def _create_document_file(self, path: Path, collection_name: str) -> DocumentFile:
        """Create DocumentFile object with metadata."""
        stat = path.stat()
        relative = path.relative_to(self.base_path)
        
        return DocumentFile(
            path=path,
            relative_path=str(relative),
            collection_name=collection_name,
            size=stat.st_size,
            modified_time=stat.st_mtime
        )
    
    def count_documents(self) -> dict[str, int]:
        """
        Count documents by collection.
        
        Returns dict mapping collection names to document counts.
        
        TODO:
        - Add size statistics
        - Cache results
        """
        counts = {}
        for doc in self.scan():
            counts[doc.collection_name] = counts.get(doc.collection_name, 0) + 1
        return counts
    
    def get_collections(self) -> List[str]:
        """Get list of collection names that would be created."""
        collections = set()
        
        # Only scan top-level directories
        for item in self.base_path.iterdir():
            if item.is_dir() and not (self.skip_hidden and item.name.startswith('.')):
                collections.add(f"KnowledgeBase_{item.name}")
        
        return sorted(collections)
