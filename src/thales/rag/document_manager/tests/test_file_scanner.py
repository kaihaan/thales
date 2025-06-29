"""
Test script for the FileScanner component.
Tests the first functionality: discovering documents in a directory.
"""

import sys
from pathlib import Path
from pprint import pprint

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from thales.rag.document_manager.ingestion.file_scanner import FileScanner, DocumentFile


def test_file_scanner(base_path: str) -> None:
    """Test the file scanner with a given directory."""
    print(f"\n{'='*60}")
    print(f"Testing FileScanner with: {base_path}")
    print(f"{'='*60}\n")
    
    # Check if path exists
    path = Path(base_path)
    if not path.exists():
        print(f"ERROR: Path '{base_path}' does not exist!")
        print("\nPlease provide a valid path. Examples:")
        print("  - D:\\Knowledge Base")
        print("  - C:\\Documents")
        print("  - ./test_docs")
        return
    
    # Create scanner
    scanner = FileScanner(Path(base_path))
    
    # 1. Test: Get collections that would be created
    print("1. Collections that would be created:")
    print("-" * 40)
    collections = scanner.get_collections()
    if collections:
        for collection in collections:
            print(f"  - {collection}")
    else:
        print("  No collections found (no subdirectories)")
    
    # 2. Test: Count documents by collection
    print("\n2. Document count by collection:")
    print("-" * 40)
    doc_counts = scanner.count_documents()
    if doc_counts:
        for collection, count in doc_counts.items():
            print(f"  {collection}: {count} documents")
    else:
        print("  No documents found")
    
    # 3. Test: Scan and show first 10 documents
    print("\n3. First 10 documents found:")
    print("-" * 40)
    documents = list(scanner.scan())
    
    if documents:
        for i, doc in enumerate(documents[:10]):
            print(f"\nDocument {i+1}:")
            print(f"  Path: {doc.path}")
            print(f"  Relative: {doc.relative_path}")
            print(f"  Collection: {doc.collection_name}")
            print(f"  Size: {doc.size:,} bytes")
            print(f"  Extension: {doc.path.suffix}")
        
        if len(documents) > 10:
            print(f"\n... and {len(documents) - 10} more documents")
    else:
        print("  No documents found!")
    
    # 4. Test: File type distribution
    print("\n4. File type distribution:")
    print("-" * 40)
    file_types: dict[str, int] = {}
    for doc in documents:
        ext = doc.path.suffix.lower()
        file_types[ext] = file_types.get(ext, 0) + 1
    
    if file_types:
        for ext, count in sorted(file_types.items(), key=lambda x: x[1], reverse=True):
            print(f"  {ext}: {count} files")
    
    # 5. Test: Check for any issues
    print("\n5. Potential issues:")
    print("-" * 40)
    
    # Check for very large files
    large_files = [doc for doc in documents if doc.size > 10 * 1024 * 1024]  # > 10MB
    if large_files:
        print(f"  - Found {len(large_files)} large files (>10MB):")
        for doc in large_files[:3]:
            print(f"    - {doc.relative_path} ({doc.size / (1024*1024):.1f} MB)")
    
    # Check for unsupported extensions
    supported_exts = scanner.extensions
    unsupported = set()
    for doc in documents:
        if doc.path.suffix.lower() not in supported_exts:
            unsupported.add(doc.path.suffix.lower())
    
    if unsupported:
        print(f"  - Found files with extensions not in default list: {unsupported}")
    
    if not large_files and not unsupported:
        print("  - No issues found!")
    
    print(f"\n{'='*60}")
    print(f"Total documents found: {len(documents)}")
    print(f"Total collections: {len(collections)}")
    print(f"{'='*60}\n")


def main() -> None:
    """Main function to run the test."""
    # Default test path
    test_path = "D:\\Knowledge Base"
    
    # Allow command line override
    if len(sys.argv) > 1:
        test_path = sys.argv[1]
    
    # If the default doesn't exist, try some alternatives
    if not Path(test_path).exists():
        alternatives = [
            "D:/Knowledge Base",
            "C:/Knowledge Base",
            "./test_docs",
            ".",
        ]
        
        for alt in alternatives:
            if Path(alt).exists():
                test_path = alt
                print(f"Using alternative path: {test_path}")
                break
    
    # Run the test
    test_file_scanner(test_path)
    
    # Test with current directory if nothing else works
    if not Path(test_path).exists():
        print("\nTesting with current directory instead:")
        test_file_scanner(".")


if __name__ == "__main__":
    main()
