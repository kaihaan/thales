# src/thales/rag/data/models.py

from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class SearchResult:
    """Represents a single item returned from a search query."""
    node_id: str
    content: str
    score: float
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Context:
    """Represents a piece of contextual information, enriched with graph relationships."""
    source_node: SearchResult
    combined_relevance: float
    related_nodes: List[SearchResult] = field(default_factory=list)
