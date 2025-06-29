"""
RAG Document Manager - Ingestion pipeline for document libraries.

This module provides a CLI-based document ingestion system that:
- Scans document libraries and creates ChromaDB collections
- Supports multiple document formats (PDF, DOC, TXT, etc.)
- Tracks changes and performs incremental updates
- Organizes collections by top-level folders
"""

__version__ = "0.1.0"
