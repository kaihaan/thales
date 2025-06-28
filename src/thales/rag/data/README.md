# Data Module

This module contains the dataclasses and data models for the RAG system. These structures ensure type-safe and consistent data transfer between the different components (vector stores, graph databases, and search agents).

## Core Data Structures

- `SearchResult`: A standardized format for results from any search source (vector, graph, etc.).
- `Context`: An enriched data structure representing a final piece of context, combining a source node with its related graph information.

## High-Level TODOs

- [ ] Define and implement the `SearchResult` dataclass.
- [ ] Define and implement the `Context` dataclass.
- [ ] Add validation logic to the dataclasses if necessary.
