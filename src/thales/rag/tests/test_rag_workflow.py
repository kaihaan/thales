# src/thales/rag/tests/test_rag_workflow.py

import asyncio
import pytest
import uuid
from typing import List

from thales.rag.vector.dummy import DummyVectorStore
from thales.rag.graph.dummy import DummyGraphDatabase
from thales.rag.search.agent import RAGAgent
from thales.rag.data.models import Context
from thales.agents.base.ontology import AgentOntology, AgentIdentity, AgentType

# Mark the entire module as async
pytestmark = pytest.mark.asyncio

async def test_rag_agent_workflow() -> None:
    """
    Tests the end-to-end workflow of the RAGAgent using dummy components.
    """
    # 1. Setup
    dummy_vector_store = DummyVectorStore()
    dummy_graph_db = DummyGraphDatabase()
    
    # Create a dummy ontology required by the BaseAgent constructor
    dummy_identity = AgentIdentity(
        agent_id=str(uuid.uuid4()),
        name="TestRAGAgent",
        agent_type=AgentType.RAG,
        description="A test agent for RAG workflows"
    )
    dummy_ontology = AgentOntology(identity=dummy_identity)

    rag_agent = RAGAgent(
        vector_store=dummy_vector_store,
        graph_db=dummy_graph_db,
        ontology=dummy_ontology
    )

    # 2. Execution
    query = "What is the main idea?"
    k = 3
    tags_filter = ["technical", "2025"]
    retrieved_context: List[Context] = await rag_agent.retrieve_context(
        query,
        k=k,
        tags=tags_filter
    )

    # 3. Assertion
    assert isinstance(retrieved_context, list)
    assert len(retrieved_context) == k
    
    for item in retrieved_context:
        assert isinstance(item, Context)
        assert item.source_node.node_id.startswith("vec_node_")
        assert len(item.related_nodes) == 1
        related_node = item.related_nodes[0]
        assert related_node.node_id == f"graph_node_for_{item.source_node.node_id}"
        print(f"Validated context for source: {item.source_node.node_id}")
