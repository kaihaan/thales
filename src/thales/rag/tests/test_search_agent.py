import pytest
from typing import List, Optional, Dict, Any

from thales.rag.search.agent import RAGAgent
from thales.rag.data.models import SearchResult, Context
from thales.rag.graph.dummy import DummyGraphDatabase
from thales.rag.vector.base import VectorStore
from thales.agents.base.ontology.ontology import AgentOntology
from thales.agents.base.ontology.identity import AgentIdentity, AgentType


class FakeVectorStore(VectorStore):
    """Stub vector store returning a fixed SearchResult."""
    def add_documents_sync(self, documents: List[str], metadatas: List[Dict[str, Any]] | None) -> None:
        pass

    def similarity_search_sync(
        self,
        query: str,
        k: int = 10,
        metadata: Optional[Dict[str, Any]] = None
    ) -> SearchResult:
        # Two dummy items
        ids = [["id1", "id2"]]
        docs = [["doc for id1", "doc for id2"]]
        metas = [[{"original_node": "id1"}, {"original_node": "id2"}]]
        dists = [[0.5, 0.8]]
        return SearchResult(ids=ids, documents=docs, metadatas=metas, distances=dists)


@pytest.mark.asyncio
async def test_retrieve_context_basic():
    """Test that RAGAgent retrieves and ranks context correctly."""
    # Setup fake vector store and dummy graph DB
    vector_store = FakeVectorStore()
    graph_db = DummyGraphDatabase()
    ontology = AgentOntology(identity=AgentIdentity(agent_id="aid", name="agent", agent_type=AgentType.RAG))
    agent = RAGAgent(vector_store=vector_store, graph_db=graph_db, ontology=ontology)

    # Execute retrieval
    contexts: List[Context] = await agent.retrieve_context("any query", k=2, depth=1)

    # Verify number of context items matches number of vector items
    assert isinstance(contexts, list)
    assert len(contexts) == 1

    ctx = contexts[0]
    # Source node should be a SearchResult with nested single lists
    assert isinstance(ctx.source_node, SearchResult)
    assert ctx.source_node.ids == [["id1", "id2"]]
    # combined_relevance comes from distance value
    assert ctx.combined_relevance == 0.5 or ctx.combined_relevance == 0.8

    # Related nodes should come from DummyGraphDatabase and include correct metadata
    assert all(isinstance(n, SearchResult) for n in ctx.related_nodes)
    # Make sure metadata original_node matches one of the ids
    origs = [n.metadatas[0][0].get("original_node") for n in ctx.related_nodes]
    assert set(origs).issubset({"id1", "id2"})
