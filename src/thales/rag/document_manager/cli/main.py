"""
Main CLI entry point for the document manager.

Usage:
    thales-rag ingest --path <path> [--config <config>]
    thales-rag update --path <path> [--force]
    thales-rag collections list
    thales-rag status
"""

import click
from pathlib import Path
from typing import Optional


@click.group()
@click.version_option(version="0.1.0")
def cli():
    """RAG Document Manager - Ingest and manage document collections."""
    pass


# Import commands after cli is defined to avoid circular imports
from .commands import ingest, collections, documents, status

# Register command groups
cli.add_command(ingest.ingest)
cli.add_command(ingest.update)
cli.add_command(collections.collections)
cli.add_command(documents.documents)
cli.add_command(status.status)
cli.add_command(status.queue)
cli.add_command(status.logs)


def main():
    """Main entry point for the CLI."""
    cli()


if __name__ == "__main__":
    main()
