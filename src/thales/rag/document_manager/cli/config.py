"""
Configuration management for document manager.

Handles loading and validation of configuration files.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional
import yaml


@dataclass
class ChunkingConfig:
    """Configuration for document chunking."""
    default_chunk_size: int = 1000
    overlap: int = 200
    strategies: Dict[str, str] = field(default_factory=dict)


@dataclass
class ProcessingConfig:
    """Configuration for document processing."""
    batch_size: int = 10
    parallel_workers: int = 4
    skip_hidden_files: bool = True
    file_extensions: List[str] = field(default_factory=lambda: [
        "pdf", "txt", "doc", "docx", "rtf", "md", "html"
    ])


@dataclass
class StorageConfig:
    """Configuration for storage locations."""
    chroma_path: str = "./rag_collections"
    tracker_db: str = "./document_tracker.db"


@dataclass
class DocumentManagerConfig:
    """Main configuration for document manager."""
    base_path: str
    chunking: ChunkingConfig = field(default_factory=ChunkingConfig)
    processing: ProcessingConfig = field(default_factory=ProcessingConfig)
    storage: StorageConfig = field(default_factory=StorageConfig)


def load_config(config_path: Optional[Path] = None) -> DocumentManagerConfig:
    """
    Load configuration from YAML file or use defaults.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        DocumentManagerConfig instance
        
    TODO:
    - Implement YAML loading
    - Add validation
    - Support environment variable overrides
    """
    if config_path and config_path.exists():
        # TODO: Load from YAML
        pass
    
    # Return default config for now
    return DocumentManagerConfig(base_path=".")


def save_config(config: DocumentManagerConfig, path: Path) -> None:
    """
    Save configuration to YAML file.
    
    TODO: Implement YAML serialization
    """
    pass
