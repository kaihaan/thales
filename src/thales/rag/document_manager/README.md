# RAG Document Manager

A CLI-based document ingestion system for creating and managing ChromaDB collections from document libraries.

## Features

- **Multi-format Support**: PDF, DOC/DOCX, TXT, RTF, MD, HTML, CSV/Excel, PPT/PPTX, EPUB
- **Automatic Collection Creation**: One collection per top-level folder
- **Incremental Updates**: Only process new or modified documents
- **Metadata Extraction**: File system metadata, folder hierarchy, and custom metadata
- **Progress Tracking**: Visual progress bars and detailed logging
- **ChromaDB Compatible**: Collections can be used with any ChromaDB client

## Installation

The document manager is installed as part of the Thales package:

```bash
pip install -e .
```

## Usage

### Initial Ingestion

Ingest all documents from a directory:

```bash
thales-rag ingest --path "d:\Knowledge Base"
```

With custom configuration:

```bash
thales-rag ingest --path "d:\Knowledge Base" --config config.yaml
```

Dry run to preview what will be processed:

```bash
thales-rag ingest --path "d:\Knowledge Base" --dry-run
```

### Update Collections

Process only new or modified documents:

```bash
thales-rag update --path "d:\Knowledge Base"
```

Force re-processing of all documents:

```bash
thales-rag update --path "d:\Knowledge Base" --force
```

### Collection Management

List all collections:

```bash
thales-rag collections list
```

Get detailed information about a collection:

```bash
thales-rag collections info KnowledgeBase_Research
```

Delete a collection:

```bash
thales-rag collections delete KnowledgeBase_Research
```

View collection statistics:

```bash
thales-rag collections stats
```

### Document Management

List documents in a collection:

```bash
thales-rag documents list --collection KnowledgeBase_Research
```

Filter by file type:

```bash
thales-rag documents list --collection KnowledgeBase_Research --filter "*.pdf"
```

Re-index a specific document:

```bash
thales-rag documents reindex "Research/paper.pdf"
```

View processing errors:

```bash
thales-rag documents errors
```

### Monitoring

Check processing status:

```bash
thales-rag status
```

Watch status in real-time:

```bash
thales-rag status --watch
```

View processing queue:

```bash
thales-rag queue list
```

Clear the queue:

```bash
thales-rag queue clear
```

View logs:

```bash
thales-rag logs --tail 50
```

Follow logs in real-time:

```bash
thales-rag logs --follow
```

## Configuration

Create a `config.yaml` file to customize behavior:

```yaml
document_manager:
  base_path: "d:\\Knowledge Base"
  
  chunking:
    default_chunk_size: 1000
    overlap: 200
    strategies:
      pdf: "semantic"
      txt: "sliding_window"
      
  processing:
    batch_size: 10
    parallel_workers: 4
    skip_hidden_files: true
    file_extensions:
      - pdf
      - txt
      - doc
      - docx
      - rtf
      - md
      - html
      
  storage:
    chroma_path: "./rag_collections"
    tracker_db: "./document_tracker.db"
```

## Using the Collections

The created collections are standard ChromaDB collections that can be accessed by any client:

```python
import chromadb

# Connect to the collections
client = chromadb.PersistentClient(path="./rag_collections")
collection = client.get_collection("KnowledgeBase_Research")

# Query the collection
results = collection.query(
    query_texts=["machine learning"],
    n_results=5
)

# Use with Thales RAG system
from thales.rag.vector.chroma_impl import ChromaVectorStore

store = ChromaVectorStore(
    path="./rag_collections",
    collection_name="KnowledgeBase_Research"
)
```

## Metadata Structure

Each document chunk includes the following metadata:

- `document_path`: Full path to the source document
- `relative_path`: Path relative to the base directory
- `collection`: Collection name
- `folder_hierarchy`: Full folder path (e.g., "Research/ML/Papers")
- `folder_1`, `folder_2`, etc.: Individual folder levels as tags
- `file_type`: Document format (pdf, docx, etc.)
- `created_date`: File creation date
- `modified_date`: File modification date
- `chunk_index`: Index of this chunk
- `total_chunks`: Total chunks for this document

## Custom Metadata

Add custom metadata by creating `.metadata.json` files in document folders:

```json
{
  "default": {
    "project": "ML Research",
    "year": 2024
  },
  "specific_file.pdf": {
    "author": "John Doe",
    "tags": ["neural networks", "deep learning"]
  }
}
```

## Architecture

The document manager consists of several modules:

- **CLI**: Command-line interface and configuration
- **Ingestion**: File scanning, parsing, chunking, and metadata extraction
- **Storage**: ChromaDB collection management and document tracking
- **Sync**: Change detection and update queue management
- **Utils**: Progress tracking and logging

## TODO

- Implement actual document parsers (currently placeholders)
- Add OCR support for scanned PDFs
- Implement entity extraction and language detection
- Add support for more document formats
- Implement parallel processing
- Add backup/restore functionality
- Create web UI for monitoring
