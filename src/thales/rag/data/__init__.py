# src/thales/rag/data/__init__.py

"""
Data Models for the RAG Module

This package defines the data structures used for search results,
context objects, and other data flowing through the RAG system.
"""

from .models import ID, IDs, Metadata, Metadatas, Document, Documents, SearchResult, Context

__all__ = ['ID', 'IDs', 'Metadata', 'Metadatas', 'Document', 'Documents', 'SearchResult', 'Context']
