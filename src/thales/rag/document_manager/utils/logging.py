"""
Logging utilities for document manager.

Provides structured logging with file and console output.
"""

import logging
from pathlib import Path
from typing import Optional
from datetime import datetime
import json


class DocumentManagerLogger:
    """
    Custom logger for document manager operations.
    
    Features:
    - Structured logging
    - File and console output
    - JSON format for parsing
    - Log rotation
    """
    
    def __init__(self, 
                 name: str = "document_manager",
                 log_dir: str = "./logs",
                 console_level: str = "INFO",
                 file_level: str = "DEBUG"):
        """
        Initialize logger.
        
        Args:
            name: Logger name
            log_dir: Directory for log files
            console_level: Console logging level
            file_level: File logging level
            
        TODO:
        - Add log rotation
        - Support for remote logging
        - Structured log parsing
        """
        self.name = name
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        
        # Create logger
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        self.logger.handlers = []
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(getattr(logging, console_level))
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler
        log_file = self.log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(getattr(logging, file_level))
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        self.logger.addHandler(file_handler)
        
        # JSON file handler for structured logs
        json_file = self.log_dir / f"{name}_{datetime.now().strftime('%Y%m%d')}.json"
        self.json_handler = logging.FileHandler(json_file)
        self.json_handler.setLevel(logging.DEBUG)
        self.json_handler.setFormatter(JsonFormatter())
        self.logger.addHandler(self.json_handler)
    
    def log_document_processed(self, 
                             document_path: str,
                             collection: str,
                             chunks: int,
                             duration: float,
                             success: bool = True,
                             error: Optional[str] = None):
        """
        Log document processing event.
        
        Args:
            document_path: Path to document
            collection: Collection name
            chunks: Number of chunks created
            duration: Processing duration in seconds
            success: Whether processing succeeded
            error: Error message if failed
        """
        event = {
            'event': 'document_processed',
            'document_path': document_path,
            'collection': collection,
            'chunks': chunks,
            'duration': duration,
            'success': success,
            'error': error,
            'timestamp': datetime.now().isoformat()
        }
        
        if success:
            self.logger.info(f"Processed {document_path} ({chunks} chunks in {duration:.2f}s)")
        else:
            self.logger.error(f"Failed to process {document_path}: {error}")
        
        # Log structured data
        self.logger.debug(json.dumps(event))
    
    def log_batch_complete(self,
                          batch_size: int,
                          duration: float,
                          success_count: int,
                          failed_count: int):
        """
        Log batch processing completion.
        
        Args:
            batch_size: Number of documents in batch
            duration: Total duration
            success_count: Successful documents
            failed_count: Failed documents
        """
        event = {
            'event': 'batch_complete',
            'batch_size': batch_size,
            'duration': duration,
            'success_count': success_count,
            'failed_count': failed_count,
            'timestamp': datetime.now().isoformat()
        }
        
        self.logger.info(
            f"Batch complete: {success_count}/{batch_size} successful "
            f"({failed_count} failed) in {duration:.2f}s"
        )
        self.logger.debug(json.dumps(event))
    
    def log_collection_created(self, 
                             collection_name: str,
                             source_path: str):
        """
        Log collection creation.
        
        Args:
            collection_name: Name of created collection
            source_path: Source directory path
        """
        event = {
            'event': 'collection_created',
            'collection_name': collection_name,
            'source_path': source_path,
            'timestamp': datetime.now().isoformat()
        }
        
        self.logger.info(f"Created collection '{collection_name}' from {source_path}")
        self.logger.debug(json.dumps(event))
    
    def log_error(self, 
                 error_type: str,
                 message: str,
                 details: Optional[dict] = None):
        """
        Log an error with structured details.
        
        Args:
            error_type: Type of error
            message: Error message
            details: Additional error details
        """
        event = {
            'event': 'error',
            'error_type': error_type,
            'message': message,
            'details': details or {},
            'timestamp': datetime.now().isoformat()
        }
        
        self.logger.error(f"{error_type}: {message}")
        self.logger.debug(json.dumps(event))
    
    def get_logger(self) -> logging.Logger:
        """Get the underlying logger instance."""
        return self.logger


class JsonFormatter(logging.Formatter):
    """
    Custom formatter that outputs JSON.
    
    Useful for log parsing and analysis.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Add exception info if present
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        # Add extra fields
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'created', 'filename', 
                          'funcName', 'levelname', 'levelno', 'lineno', 
                          'module', 'msecs', 'message', 'pathname', 'process',
                          'processName', 'relativeCreated', 'thread', 
                          'threadName', 'exc_info', 'exc_text', 'stack_info']:
                log_data[key] = value
        
        return json.dumps(log_data)


def get_logger(name: Optional[str] = None) -> DocumentManagerLogger:
    """
    Get or create a logger instance.
    
    Args:
        name: Logger name (defaults to 'document_manager')
        
    Returns:
        DocumentManagerLogger instance
    """
    return DocumentManagerLogger(name or "document_manager")


# Global logger instance
logger = get_logger()
