# src/thales/rag/tests/test_chroma_vector_store.py

import pytest
import shutil
import os
from typing import Generator, Any

from thales.rag.vector.chroma_impl import ChromaVectorStore
from thales.rag.data import Metadatas

DB_PATH = "./test_chroma_db"

docs = [
    "The sky is blue.",
    "The grass is green.",
    "The sun is bright.",
    "The moon is white."
]
tags: Metadatas = [
    {"subject": "sky", "adjective": "blue", "daypart": "day", "temp": "hot"},
    {"subject": "grass", "adjective": "green", "daypart": "all", "temp": "cold"},
    {"subject": "sun",  "adjective": "bright", "daypart": "day", "temp": "hot"},
    {"subject": "moon", "adjective": "white", "daypart": "night", "temp": "cold"}
]


@pytest.fixture(scope="module")
def chroma_store() -> Generator[ChromaVectorStore, Any, Any]:
    """A context manager to create and cleanup a ChromaVectorStore instance."""

    # for test/debug purposes clearup
    if os.path.exists(DB_PATH):
        print("Deleting chroma store")
        shutil.rmtree(DB_PATH)
    
    print(f"Creating chroma store at {DB_PATH}")
    store = ChromaVectorStore(path=DB_PATH, collection_name="test_collection")
    
    yield store

    print("Closing and deleting ChromaDB store")
    store.client.reset()


def test_add_docs(chroma_store: ChromaVectorStore) -> None:
    """Tests adding docs to the store."""

    chroma_store.add_documents_sync(docs, tags)

    #count docs
    assert chroma_store.collection.count() == 4
    


def test_similarity_search(chroma_store: ChromaVectorStore) -> None:
    """Tests basic similarity search."""
    chroma_store.add_documents_sync(docs, tags)
    results = chroma_store.similarity_search_sync("celestial body", k=1)
    assert results.documents
    if results.documents:
        assert len(results.ids[0]) == 1
        assert any("moon" in s.casefold() for row in results.documents for s in row)


def test_similarity_search_with_tag_filter(chroma_store: ChromaVectorStore) -> None:
    """Tests similarity search with a tag filter."""
    chroma_store.add_documents_sync(docs, tags)
    results = chroma_store.similarity_search_sync("natural phenomena", k=2, metadata={"daypart": "day"})
    assert len(results.ids[0]) == 2



def test_similarity_search_with_multiple_tags(chroma_store: ChromaVectorStore) -> None:
    """Tests similarity search with multiple tags."""
    chroma_store.add_documents_sync(docs, tags)
    results = chroma_store.similarity_search_sync("hot thing", k=1, metadata={"daypart": "day", "temp": "hot"})
    assert results.documents
    if results.documents:
        assert len(results.ids[0]) == 1
        assert any("sun" in s.casefold() for row in results.documents for s in row)


def test_similarity_search_no_results(chroma_store: ChromaVectorStore) -> None:
    """Tests a search that should return no results."""
    chroma_store.add_documents_sync(docs, tags)
    results = chroma_store.similarity_search_sync("nonexistent", k=1, metadata={"nonexistent_tag": "Nonexistand"})
    assert len(results.ids[0]) == 0
