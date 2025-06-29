# src/thales/rag/data/models.py

from dataclasses import dataclass, field
from typing import List, Mapping, Optional, Union, TypeAlias

# IDs
ID = str
IDs = List[ID]

# Tags (same as Metadata)
# example: {"genre": "technology", "year": 2025}
Metadata = Mapping[str, Optional[Union[str, int, float, bool]]]
# example [{"genre": "technology", "year": 2025}, {"genre": "fiction", "year": 1962}]
Metadatas = List[Metadata]

# Documents
Document = str
Documents = List[Document]

# Distances
Distance = float
Distances = List[Distance]

@dataclass
class SearchResult:
    """Represents a single item returned from a search query."""
    ids: List[IDs]
    documents: List[Documents] | None
    metadatas: List[Metadatas] | None
    distances: List[Distances] | None

@dataclass
class Context:
    """Represents a piece of contextual information, enriched with graph relationships."""
    source_node: SearchResult
    combined_relevance: float
    related_nodes: List[SearchResult] = field(default_factory=list)


"""
Chromadb data models

class QueryResult(TypedDict):
    ids: List[IDs]
    embeddings: Optional[
        Union[
            List[Embeddings],
            List[PyEmbeddings],
            List[NDArray[Union[np.int32, np.float32]]],
        ]
    ]
    documents: Optional[List[List[Document]]]
    uris: Optional[List[List[URI]]]
    data: Optional[List[Loadable]]
    metadatas: Optional[List[List[Metadata]]]
    distances: Optional[List[List[float]]]
    included: Include



# Embeddings
PyEmbedding = PyVector
PyEmbeddings = List[PyEmbedding]
Embedding = Vector
Embeddings = List[Embedding]

Space = Literal["cosine", "l2", "ip"]

CollectionMetadata = Dict[str, Any]
UpdateCollectionMetadata = UpdateMetadata

# Documents
Document = str
Documents = List[Document]

LiteralValue = Union[str, int, float, bool]
LogicalOperator = Union[Literal["$and"], Literal["$or"]]
WhereOperator = Union[
    Literal["$gt"],
    Literal["$gte"],
    Literal["$lt"],
    Literal["$lte"],
    Literal["$ne"],
    Literal["$eq"],
]
InclusionExclusionOperator = Union[Literal["$in"], Literal["$nin"]]
OperatorExpression = Union[
    Dict[Union[WhereOperator, LogicalOperator], LiteralValue],
    Dict[InclusionExclusionOperator, List[LiteralValue]],
]

Where = Dict[
    Union[str, LogicalOperator], Union[LiteralValue, OperatorExpression, List["Where"]]
]

    """
