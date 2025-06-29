"""
Test script for the DocumentParser component.
Tests document parsing functionality with real files.
"""

import sys
from pathlib import Path
from pprint import pprint

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from thales.rag.document_manager.ingestion.document_parser import DocumentParser, ParsedDocument


def test_document_parser() -> None:
    """Test the document parser with various file types."""
    print(f"\n{'='*60}")
    print("Testing DocumentParser")
    print(f"{'='*60}\n")
    
    # Create parser
    parser = DocumentParser()
    
    # Test files from the Knowledge Base
    test_files = [
        # Text file
        ("D:/Knowledge Base/index.html", "HTML file"),
        # PDF file
        ("D:/Knowledge Base/Bahai/Abdul-Baha/tablet-auguste-forel.pdf", "Small PDF"),
        # If we find a .txt file
        ("D:/Knowledge Base/test.txt", "Text file (if exists)"),
    ]
    
    for file_path, description in test_files:
        path = Path(file_path)
        if not path.exists():
            print(f"\n{description} not found at: {file_path}")
            continue
            
        print(f"\n{'='*40}")
        print(f"Testing: {description}")
        print(f"File: {path.name}")
        print(f"Size: {path.stat().st_size:,} bytes")
        print(f"{'='*40}")
        
        # Parse the document
        result = parser.parse(path)
        
        print(f"\nParsing Result:")
        print(f"  Success: {result.error is None}")
        if result.error:
            print(f"  Error: {result.error}")
        else:
            print(f"  Text length: {len(result.text)} characters")
            print(f"  Text preview: {result.text[:200]}...")
            print(f"  Metadata: {result.metadata}")
            if result.page_count:
                print(f"  Page count: {result.page_count}")
    
    # Test unsupported file type
    print(f"\n{'='*40}")
    print("Testing unsupported file type")
    print(f"{'='*40}")
    
    fake_path = Path("test.xyz")
    result = parser.parse(fake_path)
    print(f"  Error (expected): {result.error}")
    
    # Show supported formats
    print(f"\n{'='*40}")
    print("Supported formats:")
    print(f"{'='*40}")
    for ext, handler in parser.parsers.items():
        print(f"  {ext} -> {handler.__name__}")


def test_specific_parser() -> None:
    """Test a specific parser implementation."""
    print(f"\n{'='*60}")
    print("Testing Text Parser Implementation")
    print(f"{'='*60}\n")
    
    # Create a test text file
    test_content = """This is a test document.
It has multiple lines.
And some special characters: é, ñ, ü

This is a second paragraph.
"""
    
    test_path = Path("test_document.txt")
    test_path.write_text(test_content, encoding='utf-8')
    
    try:
        parser = DocumentParser()
        result = parser.parse(test_path)
        
        print(f"Original content length: {len(test_content)}")
        print(f"Parsed content length: {len(result.text)}")
        print(f"Content matches: {result.text == test_content}")
        print(f"Metadata: {result.metadata}")
        
        # Test with different encoding
        test_path.write_text(test_content, encoding='latin-1')
        result2 = parser.parse(test_path)
        print(f"\nLatin-1 encoding test:")
        print(f"  Success: {result2.error is None}")
        print(f"  Encoding detected: {result2.metadata.get('encoding')}")
        
    finally:
        # Clean up
        if test_path.exists():
            test_path.unlink()
            print("\nTest file cleaned up.")


def main() -> None:
    """Main function to run all tests."""
    test_document_parser()
    test_specific_parser()
    
    print(f"\n{'='*60}")
    print("NOTES:")
    print("- Currently all parsers return placeholder text")
    print("- Real implementations would need:")
    print("  - PyPDF2 or pdfplumber for PDFs")
    print("  - python-docx for DOCX files")
    print("  - BeautifulSoup for HTML")
    print("  - etc.")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    main()
