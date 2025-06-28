# RAG (Retrieval-Augmented Generation) Module

This module is responsible for providing the core infrastructure for advanced context retrieval. It integrates vector search with knowledge graph traversal to find the most relevant information to augment prompts for Large Language Models (LLMs).

## Modules

- **/data**: Contains data models and structures for search results and context.
- **/vector**: Provides abstractions and implementations for vector databases (e.g., ChromaDB, Pinecone).
- **/graph**: Provides abstractions and implementations for graph databases (e.g., Neo4j).
- **/search**: Contains the hybrid search logic that combines vector and graph search, and the specialized `RAGAgent`.

## High-Level TODOs

- [ ] Define core data structures in `rag/data`.
- [ ] Implement abstract base classes for `VectorStore` and `GraphDatabase`.
- [ ] Create initial implementations for ChromaDB and Neo4j.
- [ ] Develop the `RAGAgent` with hybrid search logic.
- [ ] Add comprehensive tests for each component.
