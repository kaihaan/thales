"""
Collection management commands for the RAG document manager.

Provides commands to list, delete, and inspect ChromaDB collections.
"""

import click
from typing import Optional
from pathlib import Path
from tabulate import tabulate

from ...storage.collection_manager import CollectionManager


@click.group()
def collections() -> None:
    """Manage document collections."""
    pass


@collections.command()
@click.option('--path', default='./rag_collections', help='ChromaDB storage path')
@click.option('--format', 'output_format', default='table', 
              type=click.Choice(['table', 'json', 'simple']),
              help='Output format')
def list(path: str, output_format: str) -> None:
    """List all collections with metadata and document counts."""
    try:
        manager = CollectionManager(chroma_path=path)
        collections_info = manager.list_collections()
        
        if not collections_info:
            click.echo("No collections found.")
            return
        
        if output_format == 'json':
            import json
            click.echo(json.dumps(collections_info, indent=2, default=str))
        elif output_format == 'simple':
            for coll in collections_info:
                click.echo(f"{coll['name']} ({coll['count']} documents)")
        else:  # table format
            headers = ['Name', 'Documents', 'Embedding Model', 'Created By']
            rows = []
            
            for coll in collections_info:
                metadata = coll.get('metadata', {})
                rows.append([
                    coll['name'],
                    coll['count'],
                    metadata.get('embedding_model', 'unknown'),
                    metadata.get('created_by', 'unknown')
                ])
            
            click.echo(tabulate(rows, headers=headers, tablefmt='grid'))
            
    except Exception as e:
        click.echo(f"Error listing collections: {e}", err=True)
        raise click.Abort()


@collections.command()
@click.argument('name')
@click.option('--path', default='./rag_collections', help='ChromaDB storage path')
@click.option('--yes', '-y', is_flag=True, help='Skip confirmation prompt')
def delete(name: str, path: str, yes: bool) -> None:
    """Delete a collection by name."""
    try:
        manager = CollectionManager(chroma_path=path)
        
        # Check if collection exists
        collection = manager.get_collection(name)
        if not collection:
            click.echo(f"Collection '{name}' not found.", err=True)
            raise click.Abort()
        
        # Get collection info for confirmation
        stats = manager.get_collection_stats(name)
        doc_count = stats.get('document_count', 0)
        
        # Confirmation prompt
        if not yes:
            if not click.confirm(
                f"Delete collection '{name}' with {doc_count} documents?"
            ):
                click.echo("Deletion cancelled.")
                return
        
        # Delete the collection
        success = manager.delete_collection(name)
        
        if success:
            click.echo(f"Collection '{name}' deleted successfully.")
        else:
            click.echo(f"Failed to delete collection '{name}'.", err=True)
            raise click.Abort()
            
    except Exception as e:
        click.echo(f"Error deleting collection: {e}", err=True)
        raise click.Abort()


@collections.command()
@click.argument('name')
@click.option('--path', default='./rag_collections', help='ChromaDB storage path')
@click.option('--format', 'output_format', default='table',
              type=click.Choice(['table', 'json']),
              help='Output format')
def stats(name: str, path: str, output_format: str) -> None:
    """Show detailed statistics for a collection."""
    try:
        manager = CollectionManager(chroma_path=path)
        
        # Check if collection exists
        collection = manager.get_collection(name)
        if not collection:
            click.echo(f"Collection '{name}' not found.", err=True)
            raise click.Abort()
        
        # Get detailed stats
        stats_info = manager.get_collection_stats(name)
        
        if output_format == 'json':
            import json
            click.echo(json.dumps(stats_info, indent=2, default=str))
        else:  # table format
            click.echo(f"\nCollection: {name}")
            click.echo("=" * (len(name) + 12))
            
            # Basic info
            click.echo(f"Document Count: {stats_info.get('document_count', 0)}")
            
            # Metadata
            metadata = stats_info.get('metadata', {})
            if metadata:
                click.echo("\nMetadata:")
                for key, value in metadata.items():
                    click.echo(f"  {key}: {value}")
            
            # TODO: Add more detailed statistics when available
            # - Storage size
            # - Date ranges
            # - Field analysis
            
    except Exception as e:
        click.echo(f"Error getting collection stats: {e}", err=True)
        raise click.Abort()


@collections.command()
@click.option('--path', default='./rag_collections', help='ChromaDB storage path')
@click.option('--output', '-o', help='Output file path')
def manifest(path: str, output: Optional[str]) -> None:
    """Export a manifest of all collections."""
    try:
        manager = CollectionManager(chroma_path=path)
        manifest_data = manager.export_collection_manifest()
        
        import json
        manifest_json = json.dumps(manifest_data, indent=2, default=str)
        
        if output:
            output_path = Path(output)
            output_path.write_text(manifest_json)
            click.echo(f"Manifest exported to {output_path}")
        else:
            click.echo(manifest_json)
            
    except Exception as e:
        click.echo(f"Error exporting manifest: {e}", err=True)
        raise click.Abort()


@collections.command()
@click.argument('name')
@click.option('--path', default='./rag_collections', help='ChromaDB storage path')
@click.option('--limit', default=10, help='Number of sample documents to show')
def inspect(name: str, path: str, limit: int) -> None:
    """Inspect a collection's contents."""
    try:
        manager = CollectionManager(chroma_path=path)
        
        # Check if collection exists
        collection = manager.get_collection(name)
        if not collection:
            click.echo(f"Collection '{name}' not found.", err=True)
            raise click.Abort()
        
        # Get sample documents
        # Note: This is a basic implementation
        # ChromaDB doesn't have a direct "sample" method, so we'd need to implement this
        click.echo(f"Collection: {name}")
        click.echo(f"Total documents: {collection.count()}")
        
        # TODO: Implement document sampling and display
        # This would require additional methods in CollectionManager
        click.echo("\nDocument sampling not yet implemented.")
        click.echo("Use 'thales-rag collections stats' for basic information.")
        
    except Exception as e:
        click.echo(f"Error inspecting collection: {e}", err=True)
        raise click.Abort()
