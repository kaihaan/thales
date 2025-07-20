"""
Update queue for document processing.

Manages the queue of documents to be processed.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional, Iterator
from dataclasses import dataclass, field
from datetime import datetime
from queue import Queue, PriorityQueue
import threading

from ..ingestion.file_scanner import DocumentFile


@dataclass
class QueueItem:
    """Item in the processing queue."""
    document: DocumentFile
    priority: int = 0  # Lower number = higher priority
    retry_count: int = 0
    added_time: datetime = field(default_factory=datetime.now)
    error: Optional[str] = None
    
    def __lt__(self, other: "QueueItem") -> bool:
        """For priority queue comparison."""
        return self.priority < other.priority


class UpdateQueue:
    """
    Manages document processing queue.
    
    Features:
    - Priority-based processing
    - Batch retrieval
    - Failed document tracking
    - Thread-safe operations
    """
    
    def __init__(self, max_retries: int = 3):
        """
        Initialize update queue.
        
        Args:
            max_retries: Maximum retry attempts for failed documents
            
        TODO:
        - Persist queue to disk
        - Add queue size limits
        - Implement dead letter queue
        """
        self.queue: PriorityQueue[QueueItem] = PriorityQueue()
        self.processing: dict[str, QueueItem] = {}  # Track items being processed
        self.failed: list[QueueItem] = []  # Failed items
        self.completed: list[QueueItem] = []  # Completed items
        self.max_retries = max_retries
        self.lock = threading.Lock()
    
    def add_documents(self, 
                     documents: List[DocumentFile],
                     priority: int = 0) -> int:
        """
        Add documents to the queue.
        
        Args:
            documents: List of documents to add
            priority: Processing priority (0 = highest)
            
        Returns:
            Number of documents added
            
        TODO:
        - Check for duplicates
        - Validate documents
        """
        count = 0
        for doc in documents:
            item = QueueItem(document=doc, priority=priority)
            self.queue.put(item)
            count += 1
        
        return count
    
    def get_batch(self, batch_size: int = 10) -> List[QueueItem]:
        """
        Get a batch of documents to process.
        
        Args:
            batch_size: Maximum number of items to retrieve
            
        Returns:
            List of queue items
            
        TODO:
        - Group by collection for efficiency
        - Consider document size in batching
        """
        batch: list[QueueItem] = []
        
        with self.lock:
            while len(batch) < batch_size and not self.queue.empty():
                try:
                    item = self.queue.get_nowait()
                    batch.append(item)
                    # Track as processing
                    self.processing[str(item.document.path)] = item
                except:
                    break
        
        return batch
    
    def mark_completed(self, item: QueueItem) -> None:
        """
        Mark an item as successfully processed.
        
        Args:
            item: Completed queue item
        """
        with self.lock:
            path_str = str(item.document.path)
            if path_str in self.processing:
                del self.processing[path_str]
            self.completed.append(item)
    
    def mark_failed(self, item: QueueItem, error: str) -> bool:
        """
        Mark an item as failed.
        
        Args:
            item: Failed queue item
            error: Error message
            
        Returns:
            True if will be retried, False if exceeded retries
            
        TODO:
        - Implement exponential backoff
        - Track error patterns
        """
        with self.lock:
            path_str = str(item.document.path)
            if path_str in self.processing:
                del self.processing[path_str]
            
            item.error = error
            item.retry_count += 1
            
            if item.retry_count < self.max_retries:
                # Re-queue with lower priority
                item.priority = min(item.priority + 1, 10)
                self.queue.put(item)
                return True
            else:
                # Max retries exceeded
                self.failed.append(item)
                return False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get queue status.
        
        Returns:
            Status dictionary
        """
        with self.lock:
            return {
                'queued': self.queue.qsize(),
                'processing': len(self.processing),
                'completed': len(self.completed),
                'failed': len(self.failed),
                'total_processed': len(self.completed) + len(self.failed)
            }
    
    def get_failed_items(self) -> List[QueueItem]:
        """Get list of failed items."""
        with self.lock:
            return self.failed.copy()
    
    def clear(self) -> None:
        """Clear the queue."""
        with self.lock:
            # Clear queue
            while not self.queue.empty():
                try:
                    self.queue.get_nowait()
                except:
                    break
            
            self.processing.clear()
            self.failed.clear()
            self.completed.clear()
    
    def is_empty(self) -> bool:
        """Check if queue is empty."""
        return self.queue.empty() and len(self.processing) == 0
    
    def estimate_time_remaining(self) -> Dict[str, float]:
        """
        Estimate time to process remaining items.
        
        TODO:
        - Use actual processing times
        - Factor in document types
        """
        total_items = self.queue.qsize() + len(self.processing)
        
        # Simple estimate: 5 seconds per document
        seconds = total_items * 5
        
        return {
            'items_remaining': total_items,
            'estimated_seconds': seconds,
            'estimated_minutes': seconds / 60,
            'estimated_hours': seconds / 3600
        }
    
    def get_queue_items(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Peek at queue items without removing them.
        
        Args:
            limit: Maximum items to return
            
        Returns:
            List of item summaries
            
        TODO:
        - Implement proper queue peeking
        """
        items = []
        
        # For now, just show processing items
        with self.lock:
            for path, item in list(self.processing.items())[:limit]:
                items.append({
                    'path': item.document.relative_path,
                    'collection': item.document.collection_name,
                    'priority': item.priority,
                    'retry_count': item.retry_count,
                    'status': 'processing'
                })
        
        return items
