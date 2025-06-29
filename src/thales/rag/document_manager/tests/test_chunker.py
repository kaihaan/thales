"""
Test script for the Chunker component.
Tests document chunking strategies.
"""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from thales.rag.document_manager.ingestion.chunker import (
    DocumentChunker, SlidingWindowChunker, SemanticChunker, DocumentChunk
)


def test_sliding_window_chunker() -> None:
    """Test the sliding window chunking strategy."""
    print(f"\n{'='*60}")
    print("Testing SlidingWindowChunker")
    print(f"{'='*60}\n")
    
    # Create test text
    test_text = """The quick brown fox jumps over the lazy dog. This is a test sentence that should be long enough to demonstrate chunking. 
We need multiple sentences to show how the chunker handles text boundaries. 
Here's another paragraph with more content. The chunker should split this text into overlapping chunks of approximately the specified size.
Let's add even more text to ensure we have enough content for multiple chunks. This will help us see how the overlap works between chunks.
Final paragraph here. We want to see how the chunker handles the end of the document."""
    
    # Test with different chunk sizes
    chunk_sizes = [(100, 20), (200, 50)]
    
    for chunk_size, overlap in chunk_sizes:
        print(f"\nChunk size: {chunk_size}, Overlap: {overlap}")
        print("-" * 40)
        
        chunker = SlidingWindowChunker(chunk_size=chunk_size, overlap=overlap)
        chunks = chunker.chunk(test_text, {"source": "test"})
        
        print(f"Text length: {len(test_text)}")
        print(f"Number of chunks: {len(chunks)}")
        
        for i, chunk in enumerate(chunks[:3]):  # Show first 3 chunks
            print(f"\nChunk {i + 1}:")
            print(f"  Length: {len(chunk.text)}")
            print(f"  Start: {chunk.start_char}, End: {chunk.end_char}")
            print(f"  Text: '{chunk.text[:50]}...'" if len(chunk.text) > 50 else f"  Text: '{chunk.text}'")
            print(f"  Metadata: {chunk.metadata}")
        
        if len(chunks) > 3:
            print(f"\n... and {len(chunks) - 3} more chunks")


def test_semantic_chunker() -> None:
    """Test the semantic chunking strategy."""
    print(f"\n{'='*60}")
    print("Testing SemanticChunker")
    print(f"{'='*60}\n")
    
    # Create test text with clear paragraph boundaries
    test_text = """This is the first paragraph. It contains some information about a topic. We want to keep this together as one chunk if possible.

This is the second paragraph. It's a bit longer and discusses a different aspect of the topic. The semantic chunker should recognize the paragraph boundary and potentially split here.

Here's a third paragraph that's quite short.

The fourth paragraph is much longer. It contains detailed information that goes on for quite a while. In fact, this paragraph is so long that it might need to be split into multiple chunks even though it's a single semantic unit. We're adding more and more text to demonstrate this behavior. The chunker needs to handle cases where a single paragraph exceeds the maximum chunk size. This is important for documents that have very long paragraphs or sections without clear breaks.

Final paragraph for testing."""
    
    chunker = SemanticChunker(max_chunk_size=200, min_chunk_size=50)
    chunks = chunker.chunk(test_text, {"source": "test"})
    
    print(f"Text length: {len(test_text)}")
    print(f"Number of chunks: {len(chunks)}")
    
    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i + 1}:")
        print(f"  Length: {len(chunk.text)}")
        print(f"  Text preview: '{chunk.text[:80]}...'" if len(chunk.text) > 80 else f"  Text: '{chunk.text}'")


def test_document_chunker() -> None:
    """Test the main DocumentChunker with strategy selection."""
    print(f"\n{'='*60}")
    print("Testing DocumentChunker (Main Interface)")
    print(f"{'='*60}\n")
    
    test_text = "This is a test document. " * 50  # Create a longer text
    
    chunker = DocumentChunker(default_chunk_size=150, overlap=30)
    
    # Test auto-selection based on format
    formats = [
        {"format": "txt"},
        {"format": "pdf"},
        {"format": "unknown"}
    ]
    
    for metadata in formats:
        print(f"\nFormat: {metadata['format']}")
        chunks = chunker.chunk_document(test_text, metadata)
        print(f"  Strategy used: {'semantic' if metadata['format'] == 'pdf' else 'default'}")
        print(f"  Number of chunks: {len(chunks)}")
        print(f"  First chunk length: {len(chunks[0].text) if chunks else 0}")
    
    # Test explicit strategy selection
    print("\n\nExplicit strategy selection:")
    chunks_sliding = chunker.chunk_document(test_text, {}, strategy="default")
    chunks_semantic = chunker.chunk_document(test_text, {}, strategy="semantic")
    
