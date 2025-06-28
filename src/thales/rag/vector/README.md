# Vector Module

This module provides the necessary abstractions for interacting with vector databases. It defines a common `VectorStore` interface to ensure that different vector database backends can be used interchangeably for semantic similarity search.

## Core Components

- `VectorStore` (in `base.py`): An abstract base class defining the standard method for similarity search (`similarity_search`).
- `ChromaVectorStore` (in `chroma_impl.py`): A concrete implementation of the `VectorStore` interface for ChromaDB.

## High-Level TODOs

- [ ] Define the `VectorStore` abstract base class in a `base.py` file.
- [ ] Implement the `ChromaVectorStore` class.
- [ ] Add embedding model configuration.
- [ ] Create tests to validate the ChromaDB implementation.
