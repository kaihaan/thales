# src/thales/rag/tests/test_chroma_vector_store.py

import asyncio
import pytest
import shutil
import os
import gc
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Generator

from thales.rag.vector.chroma_impl import ChromaVectorStore

DB_PATH = "./test_chroma_db"

@asynccontextmanager
async def chroma_store_context() -> AsyncGenerator[ChromaVectorStore, None]:
    """A context manager to create and cleanup a ChromaVectorStore instance."""
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)
    
    store = ChromaVectorStore(path=DB_PATH, collection_name="test_collection")
    
    docs = [
        "The sky is blue.",
        "The grass is green.",
        "The sun is bright.",
        "The moon is white."
    ]
    metadatas = [
        {"tags": ["nature", "day"]},
        {"tags": ["nature", "color"]},
        {"tags": ["nature", "day", "hot"]},
        {"tags": ["space", "night"]}
    ]
    await store.add_documents(docs, metadatas)
    
    try:
        yield store
    finally:
        store.client.delete_collection(name="test_collection")
        store.client.reset()
        del store
        gc.collect()

        delays = [0.5, 1, 2, 4, 8]
        for delay in delays:
            try:
                if os.path.exists(DB_PATH):
                    shutil.rmtree(DB_PATH)
                break
            except PermissionError:
                await asyncio.sleep(delay)
        else:
            raise RuntimeError("Failed to delete DB_PATH after retries due to file lock.")

@pytest.mark.asyncio
async def test_similarity_search() -> None:
    """Tests basic similarity search."""
    async with chroma_store_context() as chroma_store:
        results = await chroma_store.similarity_search("celestial body", k=1)
        assert len(results) == 1
        assert "moon" in results[0].content.lower()

@pytest.mark.asyncio
async def test_similarity_search_with_tag_filter() -> None:
    """Tests similarity search with a tag filter."""
    async with chroma_store_context() as chroma_store:
        results = await chroma_store.similarity_search("natural phenomena", k=2, tags=["day"])
        assert len(results) == 2
        for result in results:
            assert result.metadata.get("tag_day") is True

@pytest.mark.asyncio
async def test_similarity_search_with_multiple_tags() -> None:
    """Tests similarity search with multiple tags."""
    async with chroma_store_context() as chroma_store:
        results = await chroma_store.similarity_search("hot thing", k=1, tags=["day", "hot"])
        assert len(results) == 1
        assert "sun" in results[0].content.lower()

@pytest.mark.asyncio
async def test_similarity_search_no_results() -> None:
    """Tests a search that should return no results."""
    async with chroma_store_context() as chroma_store:
        results = await chroma_store.similarity_search("nonexistent", k=1, tags=["nonexistent_tag"])
        assert len(results) == 0
