"""
Document tracking database.

Tracks processed documents to enable incremental updates.
"""

import sqlite3
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime
import json
import hashlib


class DocumentTracker:
    """
    Tracks document processing status and history.
    
    Features:
    - Track processed documents with hashes
    - Detect new/modified/deleted files
    - Store processing errors
    - Maintain processing history
    """
    
    def __init__(self, db_path: str = "./document_tracker.db"):
        """
        Initialize tracker database.
        
        Args:
            db_path: Path to SQLite database
            
        TODO:
        - Add database migrations
        - Implement backup/restore
        - Add indexing for performance
        """
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._init_database()
    
    def _init_database(self) -> None:
        """Initialize database schema."""
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            
            # Documents table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS documents (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    file_path TEXT UNIQUE NOT NULL,
                    collection_name TEXT NOT NULL,
                    file_hash TEXT NOT NULL,
                    file_size INTEGER NOT NULL,
                    modified_time REAL NOT NULL,
                    processed_time REAL NOT NULL,
                    status TEXT NOT NULL,
                    chunk_count INTEGER DEFAULT 0,
                    error_message TEXT,
                    metadata TEXT
                )
            """)
            
            # Processing history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS processing_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    document_id INTEGER NOT NULL,
                    action TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    details TEXT,
                    FOREIGN KEY (document_id) REFERENCES documents(id)
                )
            """)
            
            # Create indexes
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_documents_path 
                ON documents(file_path)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_documents_collection 
                ON documents(collection_name)
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_documents_status 
                ON documents(status)
            """)
            
            conn.commit()
    
    def track_document(self,
                      file_path: Path,
                      collection_name: str,
                      status: str = "processed",
                      chunk_count: int = 0,
                      error_message: Optional[str] = None,
                      metadata: Optional[Dict[str, Any]] = None) -> int:
        """
        Track a processed document.
        
        Args:
            file_path: Path to document
            collection_name: Collection it belongs to
            status: Processing status (processed, failed, pending)
            chunk_count: Number of chunks created
            error_message: Error if failed
            metadata: Additional metadata
            
        Returns:
            Document ID
            
        TODO:
        - Handle duplicate tracking
        - Add retry count
        """
        file_hash = self._calculate_file_hash(file_path)
        stat = file_path.stat()
        
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            
            # Insert or update document
            cursor.execute("""
                INSERT OR REPLACE INTO documents 
                (file_path, collection_name, file_hash, file_size, 
                 modified_time, processed_time, status, chunk_count, 
                 error_message, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                str(file_path),
                collection_name,
                file_hash,
                stat.st_size,
                stat.st_mtime,
                datetime.now().timestamp(),
                status,
                chunk_count,
                error_message,
                json.dumps(metadata) if metadata else None
            ))
            
            document_id = cursor.lastrowid
            
            # Add to history
            cursor.execute("""
                INSERT INTO processing_history 
                (document_id, action, timestamp, details)
                VALUES (?, ?, ?, ?)
            """, (
                document_id,
                "processed" if status == "processed" else "failed",
                datetime.now().timestamp(),
                json.dumps({"chunks": chunk_count, "error": error_message})
            ))
            
            conn.commit()
            
        return document_id or 0
    
    def get_document_status(self, file_path: Path) -> Optional[Dict[str, Any]]:
        """
        Get current status of a document.
        
        Returns None if not tracked.
        """
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM documents WHERE file_path = ?
            """, (str(file_path),))
            
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                return dict(zip(columns, row))
            
        return None
    
    def find_changed_documents(self, 
                             base_path: Path,
                             file_paths: List[Path]) -> Dict[str, List[Path]]:
        """
        Find new, modified, and deleted documents.
        
        Args:
            base_path: Base directory path
            file_paths: Current list of files
            
        Returns:
            Dict with 'new', 'modified', 'deleted' lists
            
        TODO:
        - Add file pattern filtering
        - Handle moved files
        """
        changes: dict[str, list[Any]] = {
            'new': [],
            'modified': [],
            'deleted': []
        }
        
        # Get all tracked documents
        tracked = {}
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT file_path, file_hash, modified_time 
                FROM documents 
                WHERE status != 'deleted'
            """)
            
            for path, file_hash, mod_time in cursor.fetchall():
                tracked[path] = (file_hash, mod_time)
        
        # Check current files
        current_paths = set()
        for file_path in file_paths:
            path_str = str(file_path)
            current_paths.add(path_str)
            
            if path_str not in tracked:
                changes['new'].append(file_path)
            else:
                # Check if modified
                stat = file_path.stat()
                if stat.st_mtime > tracked[path_str][1]:
                    # Verify with hash
                    new_hash = self._calculate_file_hash(file_path)
                    if new_hash != tracked[path_str][0]:
                        changes['modified'].append(file_path)
        
        # Find deleted files
        for tracked_path in tracked:
            if tracked_path not in current_paths:
                changes['deleted'].append(Path(tracked_path))
        
        return changes
    
    def _calculate_file_hash(self, file_path: Path) -> str:
        """
        Calculate hash of file contents.
        
        TODO:
        - Handle large files efficiently
        - Add progress callback
        """
        hasher = hashlib.sha256()
        
        with open(file_path, 'rb') as f:
            # Read in chunks for large files
            while chunk := f.read(8192):
                hasher.update(chunk)
        
        return hasher.hexdigest()
    
    def get_failed_documents(self, 
                           collection: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get documents that failed processing.
        
        Args:
            collection: Filter by collection name
            
        Returns:
            List of failed document records
        """
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            
            if collection:
                cursor.execute("""
                    SELECT * FROM documents 
                    WHERE status = 'failed' AND collection_name = ?
                    ORDER BY processed_time DESC
                """, (collection,))
            else:
                cursor.execute("""
                    SELECT * FROM documents 
                    WHERE status = 'failed'
                    ORDER BY processed_time DESC
                """)
            
            columns = [desc[0] for desc in cursor.description]
            return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get processing statistics.
        
        TODO:
        - Add time-based stats
        - Collection breakdown
        - Error analysis
        """
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            
            # Overall stats
            cursor.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'processed' THEN 1 ELSE 0 END) as processed,
                    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
                    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
                    SUM(chunk_count) as total_chunks
                FROM documents
            """)
            
            stats = cursor.fetchone()
            
            return {
                'total_documents': stats[0],
                'processed': stats[1],
                'failed': stats[2],
                'pending': stats[3],
                'total_chunks': stats[4] or 0
            }
    
    def mark_deleted(self, file_paths: List[Path]) -> int:
        """
        Mark documents as deleted.
        
        Returns number of documents marked.
        """
        with sqlite3.connect(str(self.db_path)) as conn:
            cursor = conn.cursor()
            
            count = 0
            for path in file_paths:
                cursor.execute("""
                    UPDATE documents 
                    SET status = 'deleted', processed_time = ?
                    WHERE file_path = ?
                """, (datetime.now().timestamp(), str(path)))
                
                count += cursor.rowcount
            
            conn.commit()
            
        return count
