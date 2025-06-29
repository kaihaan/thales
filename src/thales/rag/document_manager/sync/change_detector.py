"""
Change detection for documents.

Detects new, modified, and deleted documents.
"""

from pathlib import Path
from typing import List, Dict, Set, Optional, Any
from dataclasses import dataclass

from ..ingestion.file_scanner import FileScanner, DocumentFile
from ..storage.document_tracker import DocumentTracker


@dataclass
class DocumentChanges:
    """Container for document changes."""
    new: List[DocumentFile]
    modified: List[DocumentFile]
    deleted: List[Path]
    
    @property
    def total_changes(self) -> int:
        """Total number of changes."""
        return len(self.new) + len(self.modified) + len(self.deleted)
    
    def has_changes(self) -> bool:
        """Check if there are any changes."""
        return self.total_changes > 0


class ChangeDetector:
    """
    Detects changes in document library.
    
    Features:
    - Compare current state with tracked documents
    - Identify new, modified, and deleted files
    - Filter by collection
    - Support for force re-processing
    """
    
    def __init__(self, 
                 scanner: FileScanner,
                 tracker: DocumentTracker):
        """
        Initialize change detector.
        
        Args:
            scanner: File scanner instance
            tracker: Document tracker instance
        """
        self.scanner = scanner
        self.tracker = tracker
    
    def detect_changes(self, 
                      force: bool = False,
                      collection_filter: Optional[str] = None) -> DocumentChanges:
        """
        Detect document changes.
        
        Args:
            force: Force all documents as "new" for re-processing
            collection_filter: Only check specific collection
            
        Returns:
            DocumentChanges object
            
        TODO:
        - Add progress callback
        - Support for moved files
        - Parallel scanning
        """
        if force:
            # All documents are "new"
            all_docs = list(self.scanner.scan())
            if collection_filter:
                all_docs = [d for d in all_docs 
                           if d.collection_name == collection_filter]
            return DocumentChanges(new=all_docs, modified=[], deleted=[])
        
        # Scan current files
        current_files = {}
        current_docs = []
        
        for doc in self.scanner.scan():
            if collection_filter and doc.collection_name != collection_filter:
                continue
            
            current_files[str(doc.path)] = doc
            current_docs.append(doc)
        
        # Get changes from tracker
        file_paths = [Path(p) for p in current_files.keys()]
        changes_dict = self.tracker.find_changed_documents(
            self.scanner.base_path, 
            file_paths
        )
        
        # Convert to DocumentFile objects
        new_docs = []
        for path in changes_dict['new']:
            if str(path) in current_files:
                new_docs.append(current_files[str(path)])
        
        modified_docs = []
        for path in changes_dict['modified']:
            if str(path) in current_files:
                modified_docs.append(current_files[str(path)])
        
        # Deleted files are just paths
        deleted_paths = changes_dict['deleted']
        
        return DocumentChanges(
            new=new_docs,
            modified=modified_docs,
            deleted=deleted_paths
        )
    
    def get_failed_documents(self, 
                           collection: Optional[str] = None) -> List[DocumentFile]:
        """
        Get documents that previously failed processing.
        
        Args:
            collection: Filter by collection
            
        Returns:
            List of DocumentFile objects for retry
            
        TODO:
        - Add retry limit checking
        - Filter by error type
        """
        failed_records = self.tracker.get_failed_documents(collection)
        failed_docs = []
        
        for record in failed_records:
            path = Path(record['file_path'])
            if path.exists():
                # Re-scan to get current metadata
                for doc in self.scanner.scan():
                    if doc.path == path:
                        failed_docs.append(doc)
                        break
        
        return failed_docs
    
    def estimate_processing_time(self, changes: DocumentChanges) -> Dict[str, Any]:
        """
        Estimate time to process changes.
        
        TODO:
        - Use historical processing times
        - Factor in document types
        - Consider system load
        """
        total_size = 0
        doc_count = changes.total_changes
        
        for doc in changes.new + changes.modified:
            total_size += doc.size
        
        # Simple estimation (1MB per second)
        estimated_seconds = total_size / (1024 * 1024)
        
        return {
            'document_count': doc_count,
            'total_size_mb': total_size / (1024 * 1024),
            'estimated_seconds': estimated_seconds,
            'estimated_minutes': estimated_seconds / 60
        }
    
    def get_change_summary(self, changes: DocumentChanges) -> str:
        """
        Get human-readable summary of changes.
        
        Returns formatted string summary.
        """
        lines = []
        lines.append("Document Changes Summary")
        lines.append("=" * 40)
        
        if changes.new:
            lines.append(f"New documents: {len(changes.new)}")
            for doc in changes.new[:5]:  # Show first 5
                lines.append(f"  + {doc.relative_path}")
            if len(changes.new) > 5:
                lines.append(f"  ... and {len(changes.new) - 5} more")
        
        if changes.modified:
            lines.append(f"\nModified documents: {len(changes.modified)}")
            for doc in changes.modified[:5]:
                lines.append(f"  * {doc.relative_path}")
            if len(changes.modified) > 5:
                lines.append(f"  ... and {len(changes.modified) - 5} more")
        
        if changes.deleted:
            lines.append(f"\nDeleted documents: {len(changes.deleted)}")
            for path in changes.deleted[:5]:
                lines.append(f"  - {path}")
            if len(changes.deleted) > 5:
                lines.append(f"  ... and {len(changes.deleted) - 5} more")
        
        if not changes.has_changes():
            lines.append("No changes detected.")
        
        return "\n".join(lines)
