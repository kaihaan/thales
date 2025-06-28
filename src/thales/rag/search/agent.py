# src/thales/rag/search/agent.py

from typing import Any, List, Optional
import asyncio

from thales.agents.base.base import BaseAgent, TaskResult
from thales.agents.base.ontology import AgentOntology, Task
from thales.rag.data.models import Context, SearchResult
from thales.rag.vector.base import VectorStore
from thales.rag.graph.base import GraphDatabase

class RAGAgent(BaseAgent):
    """A specialized agent for retrieving context from a knowledge graph."""

    def __init__(
        self,
        vector_store: VectorStore,
        graph_db: GraphDatabase,
        ontology: AgentOntology,
        **kwargs: Any
    ):
        """
        Initializes the RAGAgent.
        
        Args:
            vector_store: An instance of a VectorStore implementation.
            graph_db: An instance of a GraphDatabase implementation.
            ontology: The agent's ontology.
            **kwargs: Arguments passed to the BaseAgent.
        """
        super().__init__(ontology=ontology, **kwargs)
        self.vector_store = vector_store
        self.graph_db = graph_db

    async def retrieve_context(
        self,
        query: str,
        k: int = 5,
        depth: int = 1,
        tags: Optional[List[str]] = None
    ) -> List[Context]:
        """
        The primary method for this agent. It retrieves and ranks context.
        """
        print(f"RAGAgent: Retrieving context for query: '{query}' with tags: {tags}")
        initial_results = await self.vector_store.similarity_search(query, k=k, tags=tags)
        
        node_ids = [res.node_id for res in initial_results]
        connected_nodes = await self.graph_db.get_connected_nodes(node_ids, depth=depth, tags=tags)
        
        final_context = self._rank_and_combine(initial_results, connected_nodes)
        
        print(f"RAGAgent: Found {len(final_context)} context items.")
        return final_context

    def _rank_and_combine(self, vector_results: List[SearchResult], graph_results: List[SearchResult]) -> List[Context]:
        """
        Dummy ranking logic. Creates a context object for each initial vector result.
        """
        contexts = []
        for vec_res in vector_results:
            related = [gr for gr in graph_results if gr.metadata.get("original_node") == vec_res.node_id]
            ctx = Context(
                source_node=vec_res,
                related_nodes=related,
                combined_relevance=vec_res.score
            )
            contexts.append(ctx)
        return contexts

    async def execute_task(self, task: Task) -> TaskResult:
        """
        Overrides the BaseAgent's execute_task to handle retrieval tasks.
        """
        print(f"RAGAgent executing task: {task.action}")
        if task.action == "retrieve_context":
            query = task.description
            if query:
                context = await self.retrieve_context(query)
                return TaskResult(task_id=task.task_id, success=True, result=context, tool_used="RAGAgent/retrieve_context")
            else:
                return TaskResult(task_id=task.task_id, success=False, result=None, error="No query provided in task description")

        return await super().execute_task(task)
